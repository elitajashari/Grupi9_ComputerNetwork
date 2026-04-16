from threading import RLock
from datetime import datetime, timedelta


class StatsManager:
    def __init__(self):
        self._lock = RLock()
        self._start_time = datetime.now()
        self._total_messages = 0
        self._recent_messages = []
        self._clients_last_seen = {}

    def record_message(self, ip: str, port: int, message: str):
        with self._lock:
            now = datetime.now()
            client_key = f"{ip}:{port}"

            self._total_messages += 1
            self._clients_last_seen[client_key] = now

            self._recent_messages.append(
                {
                    "client": client_key,
                    "message": message,
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

            if len(self._recent_messages) > 10:
                self._recent_messages.pop(0)

    def get_active_clients(self, timeout_seconds: int = 60):
        with self._lock:
            now = datetime.now()
            return [
                client
                for client, last_seen in self._clients_last_seen.items()
                if now - last_seen <= timedelta(seconds=timeout_seconds)
            ]

    def get_stats(self) -> dict:
        with self._lock:
            uptime_seconds = int((datetime.now() - self._start_time).total_seconds())
            active_clients = self.get_active_clients()

            return {
                "server_started_at": self._start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "uptime_seconds": uptime_seconds,
                "active_clients_count": len(active_clients),
                "active_clients": active_clients,
                "total_messages": self._total_messages,
                "recent_messages": list(self._recent_messages),
            }
