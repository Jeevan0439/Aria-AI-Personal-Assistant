import psutil, math
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QLabel, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QColor, QFont

class Signals(QObject):
    add_message = pyqtSignal(str, str)
    set_status  = pyqtSignal(str)

class PulseOrb(QWidget):
    def __init__(self):
        super().__init__()
        self.radius  = 40
        self.growing = True
        self.status  = "idle"
        self.angle   = 0
        self.setMinimumSize(120, 120)
        t = QTimer(self); t.timeout.connect(self._tick); t.start(35)

    def set_status(self, s):
        self.status = s
        self.update()

    def _tick(self):
        if self.status != "idle":
            self.radius += 1.2 if self.growing else -1.2
            if self.radius > 52: self.growing = False
            if self.radius < 32: self.growing = True
        else:
            self.radius = 38
        self.angle = (self.angle + 2) % 360
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cx = self.width() // 2
        cy = self.height() // 2

        colors = {
            "idle":      (124, 58, 237),
            "listening": (14, 165, 233),
            "thinking":  (245, 158, 11),
            "speaking":  (167, 139, 250),
        }
        r, g, b = colors.get(self.status, (124, 58, 237))

        # Outer glow
        p.setBrush(QColor(r, g, b, 40))
        p.setPen(Qt.NoPen)
        gr = int(self.radius + 18)
        p.drawEllipse(cx - gr, cy - gr, gr*2, gr*2)

        # Mid ring
        p.setBrush(QColor(r, g, b, 80))
        mr = int(self.radius + 8)
        p.drawEllipse(cx - mr, cy - mr, mr*2, mr*2)

        # Core
        p.setBrush(QColor(r, g, b))
        cr = int(self.radius)
        p.drawEllipse(cx - cr, cy - cr, cr*2, cr*2)

        # Center dot
        p.setBrush(QColor(255, 255, 255, 200))
        p.drawEllipse(cx - 6, cy - 6, 12, 12)

class AriaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Signals()
        self.signals.add_message.connect(self._add_msg)
        self.signals.set_status.connect(self._set_status)
        self._build()

    def _build(self):
        self.setWindowTitle("◆ ARIA — Personal AI Assistant")
        self.resize(1000, 620)
        self.setStyleSheet("background:#0a0e14; color:#cbd5e1;")

        root = QHBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Sidebar ──
        side = QFrame()
        side.setFixedWidth(230)
        side.setStyleSheet("background:#0d1420; border-right:1px solid #1e293b;")
        sv = QVBoxLayout(side)
        sv.setContentsMargins(16, 20, 16, 20)

        title = QLabel("◆  ARIA")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color:#a78bfa;")
        sv.addWidget(title)

        self.lbl_status = QLabel("● STANDBY")
        self.lbl_status.setStyleSheet("color:#475569; font-size:11px; font-weight:bold; margin-bottom:10px;")
        sv.addWidget(self.lbl_status)

        self.orb = PulseOrb()
        sv.addWidget(self.orb, alignment=Qt.AlignHCenter)

        sv.addSpacing(16)
        self.lbl_clock = QLabel()
        self.lbl_cpu   = QLabel()
        self.lbl_ram   = QLabel()
        for lbl in (self.lbl_clock, self.lbl_cpu, self.lbl_ram):
            lbl.setStyleSheet("color:#475569; font-size:12px; padding:3px 0;")
            sv.addWidget(lbl)

        sv.addStretch()
        sv.addWidget(QLabel("SPACE to interrupt", styleSheet="color:#1e293b; font-size:10px;"))

        # ── Chat area ──
        chat_frame = QFrame()
        chat_frame.setStyleSheet("background:#0a0e14;")
        cv = QVBoxLayout(chat_frame)
        cv.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Good " + self._greeting() + ", Jeevan.")
        header.setFont(QFont("Segoe UI", 13))
        header.setStyleSheet("color:#475569; margin-bottom:8px;")
        cv.addWidget(header)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
            QTextEdit {
                background:#0d1420;
                border:1px solid #1e293b;
                border-radius:12px;
                padding:16px;
                font-size:14px;
                color:#e2e8f0;
            }
        """)
        cv.addWidget(self.chat)

        root.addWidget(side)
        root.addWidget(chat_frame, 1)

        # Stats timer
        t = QTimer(self); t.timeout.connect(self._update_stats); t.start(1000)
        self._update_stats()

    def _greeting(self):
        h = datetime.now().hour
        if h < 12: return "morning"
        if h < 17: return "afternoon"
        return "evening"

    def _update_stats(self):
        self.lbl_clock.setText("⏰  " + datetime.now().strftime("%H:%M:%S"))
        self.lbl_cpu.setText(f"🔥  CPU  {psutil.cpu_percent()}%")
        self.lbl_ram.setText(f"💾  RAM  {psutil.virtual_memory().percent}%")

    def _add_msg(self, sender, text):
        color = "#a78bfa" if sender == "Aria" else "#34d399"
        self.chat.append(f'<b style="color:{color}">{sender}</b><br>{text}<br>')
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())

    def _set_status(self, status):
        labels = {
            "idle":      ("● STANDBY",  "#475569"),
            "listening": ("◉ LISTENING","#38bdf8"),
            "thinking":  ("◈ PROCESSING","#fbbf24"),
            "speaking":  ("▶ SPEAKING", "#c4b5fd"),
        }
        text, color = labels.get(status, ("● STANDBY","#475569"))
        self.lbl_status.setText(text)
        self.lbl_status.setStyleSheet(f"color:{color}; font-size:11px; font-weight:bold;")
        self.orb.set_status(status)

    # Thread-safe methods
    def add_message(self, sender, text):
        self.signals.add_message.emit(sender, text)

    def set_status(self, status):
        self.signals.set_status.emit(status)