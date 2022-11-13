import argparse
import os
import socket
import ssl
from request import ServerRequest

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
MAX_CONNECTIONS = 999
BUFF_SIZE = 1024


def init_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")
    return context


def execute_requests(req: ServerRequest):
    context = init_context()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((SERVER_HOST, req.port))
        server_socket.listen(MAX_CONNECTIONS)
        print(f'Listening on {SERVER_HOST}:{req.port}')
        ssl_connect = context.wrap_socket(server_socket, server_side=True)

        while True:
            conn, addr = ssl_connect.accept()
            handle_message(conn, addr)

    except ssl.CertificateError as e:
        print(f"CertificateError: {e}")
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        quit()


def handle_message(connection: ssl.SSLSocket, addr):
    message = connection.recv(BUFF_SIZE).decode('utf-8')
    print(f'{addr[0]}: "{message}"')
    connection.send(message.upper().encode())
    connection.close()


def setup_server_cmd_request() -> ServerRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 5000",
                        default=SERVER_PORT, type=int)
    parser.add_argument("-priv", "--privatekey", help="The private key file the server makes use of."
                                                      "Defaults to any file available in project folder",
                        default='key.pem')
    parser.add_argument("-pub", "--publickey", help="The public key file in which the program  uses."
                                                    "Defaults to any file available in project folder",
                        default='cert.pem')

    try:
        args = parser.parse_args()
        req = ServerRequest()
        req.port = args.port
        req.private_key = args.privatekey
        req.public_key = args.publickey

        if not os.path.isfile(req.private_key):
            raise FileExistsError("A private key File could not be found")

        if not os.path.isfile(req.public_key):
            raise FileExistsError("A certificate File could not be found")

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
