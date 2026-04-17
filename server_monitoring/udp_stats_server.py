import socket
import logging

from server_monitoring.validator import validate_message


def start_udp_server(stats_manager, host="127.0.0.1", port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    logging.info(f"UDP server running on {host}:{port}")

    while True:
        try:
            data, client_address = server_socket.recvfrom(4096)
        except Exception as e:
            logging.error(f"UDP socket error: {e}")
            continue

        logging.info(f"Received from {client_address}: {data}")

        is_valid, result = validate_message(data)

        if not is_valid:
            logging.warning(f"Invalid message from {client_address}: {result}")
            error_message = f"ERROR: {result}"
            server_socket.sendto(error_message.encode("utf-8"), client_address)
            continue

        message = result
        ip, client_port = client_address

        stats_manager.record_message(ip, client_port, message)
        logging.info(f"Processed message from {client_address}: {message}")

        success_message = f"OK: {message}"
        server_socket.sendto(success_message.encode("utf-8"), client_address)
