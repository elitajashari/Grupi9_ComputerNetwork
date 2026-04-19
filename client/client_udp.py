import socket


# =========================
# CONFIG (MUST MATCH SERVER)
# =========================
HOST = "10.180.23.44"
PORT = 9999
BUFFER_SIZE = 4096
TIMEOUT = 3


# =========================
# UDP CLIENT CLASS
# =========================
class UDPClient:
    def __init__(self, host, port):
        self.server = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(TIMEOUT)

    def send(self, message: str):
        try:
            self.sock.sendto(message.encode("utf-8"), self.server)
            data, _ = self.sock.recvfrom(BUFFER_SIZE)
            return data.decode("utf-8")
        except socket.timeout:
            return "[TIMEOUT] No response from server"
        except ConnectionResetError:
            return "[ERROR] Server closed connection"
        except Exception as e:
            return f"[ERROR] {e}"

    def close(self):
        self.sock.close()


# =========================
# COMMAND PARSER (MATCH SERVER FORMAT)
# =========================
class CommandParser:
    def parse(self, cmd: str):

        cmd = cmd.strip()

        if not cmd:
            return None

        
        parts = cmd.split(maxsplit=1)
        base = parts[0]

        
        if base == "/list":
            return "/list"

   
        if base in ["/read", "/upload", "/download", "/delete", "/search", "/info"]:
            if len(parts) < 2 or not parts[1].strip():
                return None  
            return f"{base} {parts[1].strip()}"

  
        return None


# =========================
# MAIN LOOP
# =========================
def main():
    client = UDPClient(HOST, PORT)
    parser = CommandParser()

    print("=== UDP CLIENT STARTED ===")
    print(f"Connected to {HOST}:{PORT}\n")

    print("Commands:")
    print("/list")
    print("/read file.txt")
    print("/upload file.txt")
    print("/download file.txt")
    print("/delete file.txt")
    print("/search keyword")
    print("/info")
    print("type 'exit' to quit\n")

    while True:
        cmd = input(">>> ").strip()

        if cmd.lower() == "exit":
            break

        message = parser.parse(cmd)

        if message is None:
            print("[CLIENT ERROR] Invalid command format (must start with /)")
            continue

        response = client.send(message)
        print("[SERVER]:", response)

    client.close()


if __name__ == "__main__":
    main()