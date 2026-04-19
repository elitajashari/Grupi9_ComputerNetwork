import socket
import threading
import time
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==========================================

IP_ADDRESS = "0.0.0.0"
UDP_PORT = 9999
HTTP_PORT = 8080
BUFFER_SIZE = 4096
MAX_CLIENTS = 10
TIMEOUT_LIMIT = 60  # sekonda
# Te Serveri (server.py)
ADMIN_IPS = ["127.0.0.1", "10.180.23.44"] 


 

stats = {
    "active_connections": {},  # {addr: last_seen}
    "total_messages": 0,
    "logs": []  # Ruajtja e mesazheve
}

lock = threading.Lock()

# ==========================================

def handle_command(command_str, addr):
    parts = command_str.split(maxsplit=1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    is_admin = addr[0] in ADMIN_IPS

    try:
        if cmd == "/list":
            files = os.listdir('.')
            return "\n".join(files)

        elif cmd == "/read":
            if not args: return "Error: Jepni emrin e file-it"
            with open(args, 'r') as f: return f.read()

        elif cmd == "/info":
            if not args: return "Error: Jepni emrin e file-it"
            info = os.stat(args)
            return f"Size: {info.st_size} bytes, Created: {time.ctime(info.st_ctime)}"

        # Komandat vetëm për ADMIN
        if not is_admin:
            return "ACCESS DENIED: Ju nuk keni privilegje shkrimi."

        if cmd == "/delete":
            os.remove(args)
            return f"File {args} u fshi."
        
        elif cmd == "/upload":
            # Thjeshtim: Në një rast real këtu do të pranoheshin bytes
            return "Upload u pranua (Simulim)"

        return "Komanda e panjohur."
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_ADDRESS, UDP_PORT))
    print(f"[*] UDP Server duke degjuar ne portin {UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        msg = data.decode("utf-8")

        with lock:
            # Kontrolli i pragut të lidhjeve
            if len(stats["active_connections"]) >= MAX_CLIENTS and addr not in stats["active_connections"]:
                sock.sendto(b"Serveri i mbingarkuar", addr)
                continue

            stats["active_connections"][addr] = time.time()
            stats["total_messages"] += 1
            stats["logs"].append({"ip": addr[0], "msg": msg, "time": time.time()})

      
        if addr[0] not in ADMIN_IPS:
            time.sleep(0.5) # Simulo vonesë për klientët e thjeshtë

        response = handle_command(msg, addr)
        sock.sendto(response.encode("utf-8"), addr)

# ==========================================

class StatsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Pastrojmë lidhjet e vjetra para se t'i shfaqim
            current_time = time.time()
            active_now = {str(k): v for k, v in stats["active_connections"].items() 
                          if current_time - v < TIMEOUT_LIMIT}
            
            output = {
                "active_users": len(active_now),
                "total_messages": stats["total_messages"],
                "connections": list(active_now.keys()),
                "recent_logs": stats["logs"][-10:]
            }
            self.wfile.write(json.dumps(output).encode())

def run_http():
    httpd = HTTPServer((IP_ADDRESS, HTTP_PORT), StatsHandler)
    print(f"[*] HTTP Monitor ne http://localhost:{HTTP_PORT}/stats")
    httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=udp_server, daemon=True).start()
    run_http()