import socket
import threading

PORT = 8888
SERVERS = [('localhost', 8000), ('localhost', 8001), ('localhost', 8002)]
MAX_FAILURES = 3
current_server_index = 0

def worker(conn, addr, request_data):
    redirect_request(conn, addr, request_data)
    conn.close()

def redirect_request(conn, addr, request_data):
    global current_server_index
    failures_in_a_row = 0
    while True:
        server_host, server_port = SERVERS[current_server_index]
        print(f'Redirecting request from {addr} to server {server_host}:{server_port}')
        try:
            current_server_index = (current_server_index + 1) % len(SERVERS)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
                server_sock.settimeout(10.0)
                server_sock.connect((server_host, server_port))
                print("Trying to send data:", request_data)
                server_sock.sendall(request_data)
                data = server_sock.recv(1024)
                conn.sendall(data)
            print(f'Success on {server_host}:{server_port}')
            failures_in_a_row = 0
            break
        except (Exception) as exc:
            failures_in_a_row += 1
            print(f'Server {server_host}:{server_port} is unavailable. Error: {exc}')
            current_server_index = (current_server_index) % len(SERVERS)
            if failures_in_a_row >= MAX_FAILURES:
                failures_in_a_row = 0
                print("All server connection attempts failed.")
                conn.sendall("Servers are unavailable. Try again later.".encode())
                conn.close()
                return

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', PORT))
        s.listen()
        print(f'Load balancer is listening on port {PORT}...')
        while True:
            conn, addr = s.accept()
            request_data = conn.recv(1024)
            print(f'Received request from {addr}')
            t = threading.Thread(target=worker, args=(conn, addr, request_data))
            t.start()

if __name__ == '__main__':
    start()