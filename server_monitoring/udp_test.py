import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 🔥 shto timeout
sock.settimeout(3)

sock.sendto(b"/list", ("127.0.0.1", 9999))

try:
    data, _ = sock.recvfrom(4096)
    print(data.decode())
except socket.timeout:
    print("No response from server")
