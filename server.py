import argparse
import socket
import ssl
from request import ServerRequest

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
MAX_CONNECTIONS = 999


def execute_requests(req: ServerRequest):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("cert.pem", "key.pem")

        server_socket.bind((SERVER_HOST, req.port))
        server_socket.listen(MAX_CONNECTIONS)
        print(f'Listening on {SERVER_HOST}:{req.port}')

        ssl_connect = context.wrap_socket(server_socket, server_side=True)

        # print(ssl_connect.getpeercert())
        # cert = ssl_connect.getpeercert()
        # cert = {'subject': ((('commonName', 'example.com'),),)}
        # ssl.match_hostname(cert, "www.bcit.ca")

        # ssl.match_hostname(cert, "example.org")
        # print(f'cert{cert}')
        conn, addr = ssl_connect.accept()
        print(conn)
        print(f'{addr} has connected.')
        message = conn.recv(1024).decode('utf-8')
        print(f'message from client {message}')
        conn.send(message.upper().encode())
        conn.close()
    except ssl.CertificateError as e:
        print(f"CertificateError: {e}")
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        quit()


def setup_server_cmd_request() -> ServerRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=SERVER_PORT, type=int)

    try:
        args = parser.parse_args()
        req = ServerRequest()
        req.port = args.port

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def main():
    request = setup_server_cmd_request()
    execute_requests(request)


if __name__ == "__main__":
    main()