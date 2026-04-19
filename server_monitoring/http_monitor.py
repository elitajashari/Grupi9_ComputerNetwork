from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging


class StatsHandler(BaseHTTPRequestHandler):
    stats_manager = None

    def do_GET(self):
        logging.info(f"HTTP request received: {self.path}")

        try:
            if self.path != "/stats":
                logging.warning(f"404 - Unknown HTTP endpoint requested: {self.path}")
                self._send_json(404, {"error": "Endpoint not found"})
                return

            if self.stats_manager is None:
                raise RuntimeError("Stats manager not initialized")

            response_data = self.stats_manager.get_stats()
            self._send_json(200, response_data)

            logging.info("Returned /stats successfully (200)")

        except Exception as e:
            logging.exception(f"HTTP server error: {e}")
            self._send_json(500, {"error": "Internal server error"})

    def _send_json(self, status_code, data):
        body = json.dumps(data, indent=4).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def start_http_monitor(stats_manager, host="127.0.0.1", port=8080):
    StatsHandler.stats_manager = stats_manager
    server = ThreadingHTTPServer((host, port), StatsHandler)

    logging.info(f"HTTP monitoring server running at http://{host}:{port}/stats")
    server.serve_forever()
