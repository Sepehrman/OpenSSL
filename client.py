# client.py
import argparse
# Example code used: https://github.com/arthurazs/python-tls
# --------------------------------------------------
import socket
import ssl
from request import ClientRequest

IP = "127.0.0.1"
PORT = 5000
HOSTNAME = "www.bcit.ca"
DEFAULT_PORT = 5000

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
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("cert.pem")

    client_socket = socket.socket()
    try:

        client_socket.connect((req.ip_address, req.port))

        ssl_context = context.wrap_socket(client_socket, server_hostname=HOSTNAME)
        client_cert = ssl_context.getpeercert()
        if not client_cert:
            raise Exception("Unable to retrieve server certificate")

        # print(f'cert {ssl.client_cert}')
        message = input()
        ssl_context.send(message.encode())

        capitalized_message = ssl_context.recv(1024).decode()
        print(f'{capitalized_message}')
        ssl_context.close()

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()


def main():
    request = setup_client_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()
