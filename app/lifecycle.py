"""CP4 — Graceful shutdown signal handling."""

from __future__ import annotations

import signal


class Lifecycle:
    """Giữ trạng thái vòng đời của process."""

    def __init__(self) -> None:
        self.shutting_down = False
        self._previous: dict = {}

    def request_shutdown(self, signum=None, frame=None) -> None:
        """Đánh dấu draining rồi nhường lại cho handler đã đăng ký trước."""
        self.shutting_down = True
        previous = self._previous.get(signum)
        if callable(previous):
            previous(signum, frame)

    def install(self) -> None:
        """Cài handler cho SIGTERM và SIGINT, đồng thời giữ handler cũ."""
        for sig in (signal.SIGTERM, signal.SIGINT):
            self._previous[sig] = signal.getsignal(sig)
            signal.signal(sig, self.request_shutdown)


lifecycle = Lifecycle()
