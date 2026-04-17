from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging


class StatsHandler(BaseHTTPRequestHandler):
    stats_manager = None

    def do_GET(self):
        try:
            logging.info(f"HTTP request received: {self.path}")

            if self.path == "/stats":
                if not self.stats_manager:
                    raise Exception("Stats manager not initialized0")

                response_data = self.stats_manager.get_stats()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data, indent=4).encode("utf-8"))

                logging.info("Returned /stats successfully (200)")

            else:
                logging.warning(f"404 - Unknown HTTP endpoint requested: {self.path}")

                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": "Endpoint not found"}).encode("utf-8")
                )

        except Exception as e:
            logging.error(f"HTTP server error: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "Internal server error"}).encode("utf-8")
            )

    def log_message(self, format, *args):
        return


def start_http_monitor(stats_manager, host="127.0.0.1", port=8080):
    StatsHandler.stats_manager = stats_manager
    server = HTTPServer((host, port), StatsHandler)

    logging.info(f"HTTP monitoring server running at http://{host}:{port}/stats")

    server.serve_forever()
