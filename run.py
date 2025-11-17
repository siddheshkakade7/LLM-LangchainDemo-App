# Entrypoint to run FastAPI server

import socket

import uvicorn

from app.config import Config


def find_available_port(host: str, start_port: int, max_tries: int = 20) -> int:
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found starting at {start_port}")


if __name__ == "__main__":
    host = Config.HOST
    display_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    port = find_available_port(host, Config.PORT)
    if port != Config.PORT:
        print(f"Port {Config.PORT} busy. Using {port} instead.")
    print(f"Server available at http://{display_host}:{port}")
    uvicorn.run("app.server:app", host=host, port=port)

