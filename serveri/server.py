import socket
import time
import os
import threading
import logging

from server_monitoring.stats_manager import stats_manager
from server_monitoring.http_monitor import start_http_monitor

logging.basicConfig(level=logging.INFO)

IP_ADDRESS = "0.0.0.0"
UDP_PORT = 9999
BUFFER_SIZE = 4096
MAX_CLIENTS = 10
TIMEOUT_LIMIT = 60
ADMIN_IPS = ["127.0.0.1", "10.180.23.44"]


def handle_command(command_str, addr):
    parts = command_str.split(maxsplit=1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    is_admin = addr[0] in ADMIN_IPS

    try:
        if cmd == "/list":
            files = os.listdir(".")
            return "\n".join(files)

        elif cmd == "/read":
            if not args:
                return "Error: Jepni emrin e file-it"
            with open(args, "r", encoding="utf-8") as f:
                return f.read()

        elif cmd == "/info":
            if not args:
                return "Error: Jepni emrin e file-it"
            info = os.stat(args)
            return f"Size: {info.st_size} bytes, Created: {time.ctime(info.st_ctime)}"

        if not is_admin:
            return "ACCESS DENIED: Ju nuk keni privilegje shkrimi."

        if cmd == "/delete":
            if not args:
                return "Error: Jepni emrin e file-it"
            os.remove(args)
            return f"File {args} u fshi."

        elif cmd == "/upload":
            return "Upload u pranua (Simulim)"

        return "Komanda e panjohur."

    except Exception as e:
        return f"Error: {str(e)}"


def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_ADDRESS, UDP_PORT))
    print(f"[*] UDP Server duke degjuar ne portin {UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        msg = data.decode("utf-8")
        logging.info(f"Received from {addr}: {msg}")

        active_clients = stats_manager.get_active_clients(timeout_seconds=TIMEOUT_LIMIT)
        client_key = f"{addr[0]}:{addr[1]}"

        if len(active_clients) >= MAX_CLIENTS and client_key not in active_clients:
            sock.sendto(b"Serveri i mbingarkuar", addr)
            continue

        stats_manager.record_message(addr[0], addr[1], msg)

        if addr[0] not in ADMIN_IPS:
            time.sleep(0.5)

        response = handle_command(msg, addr)
        sock.sendto(response.encode("utf-8"), addr)


if __name__ == "__main__":
    threading.Thread(
        target=start_http_monitor,
        args=(stats_manager, "127.0.0.1", 8080),
        daemon=True,
    ).start()

    udp_server()
