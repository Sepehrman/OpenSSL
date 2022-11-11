import argparse
import socket
import ssl

from request import ClientRequest

DEFAULT_PORT = 5000
CLIENT_HOST = socket.gethostbyname(socket.gethostname())
# CLIENT_HOST = '192.168.1.239'


def setup_client_cmd_request() -> ClientRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--ip", help="The IP address the client sends the request for. "
                                           "Must be set to a valid IP Address", required=True)
    parser.add_argument("-p", "--port", help="The port in which the client runs on "
                                             "Defaults to 5001", required=False, default=DEFAULT_PORT, type=int)
    try:
        args = parser.parse_args()
        req = ClientRequest()

        req.ip_address = args.ip
        req.port = args.port

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()


def execute_request(req: ClientRequest):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # trydefault context
        context.load_verify_locations('cert.pem')  # Load certificates

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((req.ip_address, req.port))
        c_socket = context.wrap_socket(s, server_hostname=CLIENT_HOST)
        c_socket.connect((req.ip_address, req.port))
        message = input()
        c_socket.send(message.encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        c_socket.close()
        s.close()
    except Exception as e:
        print(f"CLIENT ERROR {e}")


def main():
    request = setup_client_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()
