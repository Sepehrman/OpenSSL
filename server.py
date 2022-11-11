import argparse
import os
import socket
import ssl

from request import ServerRequest

SERVER_HOST = socket.gethostbyname(socket.gethostname())

SERVER_PORT = 5000
MAX_INCOMING_CONNECTIONS = 999
DEFAULT_PATH = './server/downloads/'

def create_socket(req):
    try:
        # specify cntext
        # load certs
        # wrapped in context
        # ssl.OpenSSL

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) #trydefault context
        context.load_cert_chain('cert.pem', 'key.pem')  # Load certificates

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SERVER_HOST, req.port))
        s.listen(MAX_INCOMING_CONNECTIONS)
        # client_connect, client_addr = s.accept()

        s_socket = context.wrap_socket(s, server_side=True)
        # client_cert = clien

        print(f"[LOG] Listening as {SERVER_HOST}:{req.port}")
        accepting = True
        while accepting:
            conn, addr = s_socket.accept()
            s_socket.do_handshake()
            print(f"[LOG] {addr} has connnected.")
            received_message = conn.recv(1024).decode()
            print(f"message from client: {received_message}")
            conn.send(received_message.upper().encode())
        s_socket.close()
        s.close()
    except Exception as e:
        print(f"ERROR: {e}")

def init_server(req: ServerRequest):
    create_socket(req)

def setup_server_cmd_request() -> ServerRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=SERVER_PORT, type=int)
    # parser.add_argument("-pub", "--pubkey", help="The public key or file name",
    #                     required=True)
    # parser.add_argument("-priv", "--privkey", help="The public key or file name",
    #                     required=True)

    try:
        args = parser.parse_args()
        req = ServerRequest()
        req.port = args.port
        # req.public_key = args.pubkey
        # req.private_key = args.privkey

        # pub_key_exists = os.path.exists(req.public_key)

        # priv_key_exists = os.path.exists(req.private_key)
        # print(f"{req.private_key} is dir? {priv_key_exists}")

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def main():
    request = setup_server_cmd_request()
    init_server(request)


if __name__ == "__main__":
    main()
