# 🧪 PROTOCOL AUTOPSY: GUI LESSONS LEARNED
[timedat: 2026-05-21 17:30:00]

## ❌ FAILED PROTOCOLS
- **CustomTkinter/ModernGL:** 
  - **Reason for Failure:** Excessive GPU overhead, high latency, missing library dependencies on 32-bit ARM/Termux.
  - **Lesson:** UI must be non-blocking, web-based (WebView), or pure TUI (ncurses-less).
- **Curses/TUI Blocking:**
  - **Reason for Failure:** Blocks the main thread, prevents background agent handoffs, poor resolution control.
  - **Lesson:** UI must be asynchronous; terminal output must be streaming, not buffered.

## 🏁 SUCCESSFUL PROTOCOLS
- **SQLite WAL + BLOBs:** High-speed random access; perfect for memory-constrained environments.
- **KQML/ACL Handoffs:** Formalized agent communication prevents race conditions.
- **WebView-based UI:** Allows for scalable, hardware-accelerated, and interactive interfaces without blocking the kernel core.

---
[Status: PROTOCOL DEFINITION]
