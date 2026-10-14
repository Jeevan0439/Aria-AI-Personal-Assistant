# ◆ Aria — AI Personal Assistant

> A fully local, voice-activated AI personal assistant built from scratch using Python, Ollama, PyQt5, and Microsoft Edge TTS. Inspired by Jarvis from Iron Man.

---

## Demo

**Wake:** Press `Ctrl` three times  
**Sleep:** Press `Ctrl` three times again  
**Interrupt:** Press `Space` while Aria is speaking

---

## Features

### Voice & AI
- Wake word detection via triple Ctrl keypress
- Speech recognition using Google Speech API
- Natural voice responses via Microsoft Edge TTS (`en-US-AriaNeural`)
- Powered by Ollama running Mistral locally — 100% free, no API keys
- Persistent memory across sessions stored in JSON
- Full conversation context within each session

### System Control
- Open and close any application by voice
- Volume up / down / mute
- Screenshot — saves to Desktop automatically
- Shutdown / restart / sleep PC by voice
- Type text into any open application

### Smart Features
- Spotify control — search and play any song, next/previous track
- WhatsApp messaging — send messages hands-free
- Reminders — voice-set reminders with popup notifications and spoken alerts
- Live weather for Bengaluru
- Google search — opens results in browser
- Time and date queries

### UI
- Dark-mode PyQt5 window with animated pulsing orb
- Orb changes color: purple (idle), blue (listening), amber (thinking), violet (speaking)
- Live CPU, RAM, and clock in sidebar
- Full conversation chat log
- Cinematic HUD aesthetic

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Brain | Ollama + Mistral (local) |
| Voice Input | SpeechRecognition + PyAudio |
| Voice Output | Edge TTS + Pygame |
| GUI | PyQt5 |
| System Control | PyAutoGUI + ctypes |
| Wake Trigger | pynput (triple Ctrl) |
| Memory | JSON persistent storage |
| Notifications | Plyer |

---

## Setup

### Requirements
- Windows 10/11
- Python 3.11
- 8GB+ RAM (16GB recommended)
- Ollama installed

### Install Ollama
Download from [ollama.com](https://ollama.com) and pull the model:
```bash
ollama pull mistral
```

### Install Python dependencies
```bash
py -3.11 -m pip install edge-tts SpeechRecognition sounddevice numpy pyautogui psutil duckduckgo-search requests beautifulsoup4 pygame keyboard pyaudio plyer pynput pillow miniaudio PyQt5
```

### Run
Double-click `Start_Aria.bat` — Ollama starts automatically and Aria launches.

---

## Usage Examples

| Say this | Aria does this |
|----------|---------------|
| *(triple Ctrl)* | Wakes up |
| "Play Believer on Spotify" | Searches and plays on Spotify |
| "Send a WhatsApp to Darshan saying I'll be late" | Opens WhatsApp and sends message |
| "Remind me in 30 minutes to drink water" | Sets reminder with popup + voice alert |
| "Volume up" | Increases system volume |
| "Take a screenshot" | Saves screenshot to Desktop |
| "Open Chrome" | Launches Chrome |
| "What's the weather?" | Reads Bengaluru weather |
| "Remember that my exam is Monday" | Saves to persistent memory |
| "Shut down" | Shuts down PC in 5 seconds |

---

## Project Structure

```
Aria/
├── main.py              # Entry point, voice loop, command router
├── config.py            # Settings and constants
├── Start_Aria.bat       # One-click launcher
├── aria_core/
│   ├── brain.py         # Ollama AI integration
│   ├── voice.py         # Speech recognition and TTS
│   ├── gui.py           # PyQt5 dark UI with animated orb
│   ├── memory.py        # Persistent memory system
│   └── skills.py        # System control, Spotify, WhatsApp, reminders
└── memory/              # Auto-created — stores facts and conversation history
```

---

## Built By

**Jeevan** — AI/ML Engineering Student, RRCE Bengaluru  
Co-founder of Eventneve, Sketch2Spec and Jeedar Agency

---

## License

MIT License — free to use, modify and distribute.
