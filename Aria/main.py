import sys, threading, re, datetime, os
sys.path.insert(0, "F:\\Aria")

from PyQt5.QtWidgets import QApplication
from aria_core.gui    import AriaGUI
from aria_core.memory import Memory
from aria_core.brain  import Brain
from aria_core.voice  import Voice
from aria_core        import skills
from config           import WAKE_WORD, ASSISTANT_NAME, USER_NAME
from pynput           import keyboard as pynput_kb

# ── Triple Ctrl wake trigger ──────────────────────────────
import time
_ctrl_times  = []
_ctrl_event  = threading.Event()

def _on_key(key):
    try:
        if key in (pynput_kb.Key.ctrl_l, pynput_kb.Key.ctrl_r):
            now = time.time()
            _ctrl_times.append(now)
            recent = [t for t in _ctrl_times if now - t < 1.5]
            _ctrl_times.clear()
            _ctrl_times.extend(recent)
            if len(_ctrl_times) >= 3:
                _ctrl_times.clear()
                _ctrl_event.set()
    except: pass

# ── Command router ────────────────────────────────────────
def handle(cmd, brain, voice):
    # Power
    r = skills.pc_power(cmd)
    if r: return r

    # Volume
    if any(w in cmd for w in ["volume up","louder","turn up"]):   return skills.volume_up()
    if any(w in cmd for w in ["volume down","quieter","turn down"]): return skills.volume_down()
    if "mute" in cmd: return skills.mute()

    # Screenshot
    if "screenshot" in cmd: return skills.screenshot()

    # Spotify
    if "next" in cmd and ("song" in cmd or "track" in cmd): return skills.spotify_next()
    if ("previous" in cmd or "prev" in cmd) and ("song" in cmd or "track" in cmd): return skills.spotify_prev()
    if "pause" in cmd and ("music" in cmd or "song" in cmd or "spotify" in cmd): return skills.spotify_play_pause()

    if "play" in cmd and ("spotify" in cmd or "song" in cmd or "music" in cmd or "track" in cmd):
        patterns = [
            r"play (.+?) (?:on spotify|in spotify|song|music|track|please)",
            r"play (.+?) and",
            r"play (.+)$",
        ]
        song = ""
        for p in patterns:
            m = re.search(p, cmd)
            if m:
                candidate = m.group(1).strip()
                for w in ["the","a","some","me","please","spotify","open","and","in","on"]:
                    candidate = re.sub(r"\b" + w + r"\b", "", candidate)
                candidate = " ".join(candidate.split()).strip()
                if len(candidate) > 1:
                    song = candidate
                    break
        if song: return skills.spotify_search_play(song)
        else:    return skills.spotify_play_pause()

    # WhatsApp
    if any(w in cmd for w in ["whatsapp","send a message","message to","text"]):
        m = None
        for p in [r"send (?:a )?(?:whatsapp )?(?:message )?to (.+?) saying (.+)",
                  r"whatsapp (.+?) (?:saying|that) (.+)",
                  r"message (.+?) (?:saying|that) (.+)"]:
            m = re.search(p, cmd)
            if m: break
        if m: return skills.send_whatsapp(m.group(1).strip(), m.group(2).strip())
        return "Please say: send a WhatsApp to [name] saying [message]"

    # Time / Date / Weather
    if any(w in cmd for w in ["what time","the time"]):
        return f"It's {datetime.datetime.now().strftime('%I:%M %p')}."
    if any(w in cmd for w in ["what day","the date","today"]):
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d %Y')}."
    if any(w in cmd for w in ["weather","temperature"]):
        import requests as _r
        try: return _r.get("https://wttr.in/Bengaluru?format=%C+%t", timeout=5).text.strip()
        except: return "Can't reach weather service."

    # Reminders
    if any(w in cmd for w in ["remind me","set a reminder"]):
        ts, msg = skills.parse_reminder(cmd)
        if ts and msg: return skills.set_reminder(ts, msg)
        return "Please say: remind me in 10 minutes to [task]"

    # Memory
    if any(w in cmd for w in ["remember","don't forget","note that","keep in mind"]):
        fact = cmd
        for w in ["remember that","remember","don't forget","note that","keep in mind"]:
            fact = fact.replace(w,"").strip()
        brain.memory.remember_fact("note", fact)
        return "Got it, remembered."

    if any(w in cmd for w in ["what do you remember","do you remember","recall"]):
        facts = brain.memory.recall_facts()
        if facts: return "I know: " + ", ".join(f"{k}: {v}" for k,v in facts.items())
        return "Nothing saved yet."

    # Open / close apps
    if any(w in cmd for w in ["open ","launch ","start "]):
        r = skills.open_app(cmd)
        if r: return r
    if any(w in cmd for w in ["close ","quit ","kill "]):
        r = skills.close_app(cmd)
        if r: return r

    # Web search
    if any(w in cmd for w in ["search for","google","search"]):
        return skills.google_search(cmd)

    # Fallback to AI brain
    return brain.think(cmd)

# ── Main voice loop ───────────────────────────────────────
def voice_loop(gui, brain, voice):
    skills._speak_fn = voice.speak
    time.sleep(1.5)
    voice.speak(f"Aria online. Press Ctrl three times to wake me, Jeevan.")
    gui.set_status("idle")

    awake = False

    while True:
        _ctrl_event.clear()
        _ctrl_event.wait()   # wait for triple Ctrl

        if not awake:
            awake = True
            _ctrl_event.clear()
            voice.speak("Yeah?")
            gui.set_status("listening")
            silence = 0

            while awake:
                # Check ctrl before listening
                if _ctrl_event.is_set():
                    _ctrl_event.clear()
                    voice.speak("Going to sleep.")
                    gui.set_status("idle")
                    awake = False
                    break

                gui.set_status("listening")
                inp = voice.listen(timeout=7)

                # Check ctrl after listening
                if _ctrl_event.is_set():
                    _ctrl_event.clear()
                    voice.speak("Going to sleep.")
                    gui.set_status("idle")
                    awake = False
                    break

                if not inp:
                    silence += 1
                    if silence >= 2:
                        voice.speak("Going idle.")
                        gui.set_status("idle")
                        awake = False
                    break

                silence = 0
                gui.add_message(USER_NAME, inp)

                if any(w in inp.lower() for w in ["goodbye","bye","sleep","that's all","thanks"]):
                    voice.speak("Later, Jeevan.")
                    gui.set_status("idle")
                    awake = False
                    break

                gui.set_status("thinking")
                resp = handle(inp.lower(), brain, voice)
                gui.add_message(ASSISTANT_NAME, resp)
                gui.set_status("speaking")
                voice.speak(resp)
                gui.set_status("listening")
        else:
            # Already awake, Ctrl x3 = sleep
            voice.speak("Sleeping.")
            gui.set_status("idle")
            awake = False

# ── Entry point ───────────────────────────────────────────
def main():
    # Start keyboard listener
    listener = pynput_kb.Listener(on_press=_on_key)
    listener.daemon = True
    listener.start()

    app  = QApplication(sys.argv)
    gui  = AriaGUI()
    gui.show()

    mem   = Memory()
    brain = Brain(mem)
    voice = Voice()

    threading.Thread(target=voice_loop, args=(gui, brain, voice), daemon=True).start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()