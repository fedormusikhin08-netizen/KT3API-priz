import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

users = {}
orders = {}
inventory = {"available": 17, "pending": 3, "sold": 1}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_GET(self):
        parts = self.path.strip("/").split("/")
        if parts[:3] == ["v2", "store", "inventory"]:
            return self._send(200, inventory)
        if len(parts) == 3 and parts[:2] == ["v2", "user"]:
            u = users.get(parts[2])
            return self._send(200, u) if u else self._send(
                404, {"code": 404, "type": "error", "message": "user not found"})
        if len(parts) == 4 and parts[:3] == ["v2", "store", "order"]:
            o = orders.get(parts[3])
            return self._send(200, o) if o else self._send(
                404, {"code": 404, "type": "error", "message": "order not found"})
        self._send(404, {"code": 404, "type": "error", "message": "not found"})

    def do_POST(self):
        parts = self.path.strip("/").split("/")
        data = self._body()
        if parts[:2] == ["v2", "user"]:
            users[data.get("username", "")] = data
            return self._send(200, {"code": 200, "type": "unknown",
                                    "message": str(data.get("id", ""))})
        if parts[:3] == ["v2", "store", "order"]:
            orders[str(data.get("id", ""))] = data
            return self._send(200, data)
        self._send(404, {"code": 404, "type": "error", "message": "not found"})

    def do_PUT(self):
        parts = self.path.strip("/").split("/")
        data = self._body()
        if len(parts) == 3 and parts[:2] == ["v2", "user"]:
            name = parts[2]
            if name not in users:
                return self._send(404, {"code": 404, "type": "error",
                                        "message": "user not found"})
            users[name] = data
            return self._send(200, {"code": 200, "type": "unknown",
                                    "message": name})
        self._send(404, {"code": 404, "type": "error", "message": "not found"})

    def do_DELETE(self):
        parts = self.path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["v2", "user"]:
            if users.pop(parts[2], None) is None:
                return self._send(404, {"code": 404, "type": "error",
                                        "message": "user not found"})
            return self._send(200, {"code": 200, "type": "unknown",
                                    "message": parts[2]})
        if len(parts) == 4 and parts[:3] == ["v2", "store", "order"]:
            if orders.pop(parts[3], None) is None:
                return self._send(404, {"code": 404, "type": "error",
                                        "message": "order not found"})
            return self._send(200, {"code": 200, "type": "unknown",
                                    "message": parts[3]})
        self._send(404, {"code": 404, "type": "error", "message": "not found"})


if __name__ == "__main__":
    print("mock petstore: http://127.0.0.1:8090/v2")
    ThreadingHTTPServer(("127.0.0.1", 8090), Handler).serve_forever()
