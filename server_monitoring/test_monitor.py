import threading
import time

from server_monitoring.stats_manager import StatsManager
from server_monitoring.http_monitor import start_http_monitor
from server_monitoring.udp_server import start_udp_server


def main():
    stats_manager = StatsManager()

    http_thread = threading.Thread(
        target=start_http_monitor, args=(stats_manager, "127.0.0.1", 8080), daemon=True
    )
    http_thread.start()

    udp_thread = threading.Thread(
        target=start_udp_server, args=(stats_manager, "127.0.0.1", 9999), daemon=True
    )
    udp_thread.start()

    print("Servers started (HTTP + UDP)")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
