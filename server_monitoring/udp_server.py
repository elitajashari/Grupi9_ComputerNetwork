import socket

from server_monitoring.validator import validate_message


def start_udp_server(stats_manager, host="127.0.0.1", port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"UDP server running on {host}:{port}")

    while True:
        data, client_address = server_socket.recvfrom(4096)

        is_valid, result = validate_message(data)

        if not is_valid:
            error_message = f"ERROR: {result}"
            server_socket.sendto(error_message.encode("utf-8"), client_address)
            continue

        message = result
        ip, client_port = client_address

        stats_manager.record_message(ip, client_port, message)

        success_message = f"OK: {message}"
        server_socket.sendto(success_message.encode("utf-8"), client_address)
