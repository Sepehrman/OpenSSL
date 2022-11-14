# client.py
import argparse
# Example code used: https://github.com/arthurazs/python-tls
# --------------------------------------------------
import socket
import ssl
from request import ClientRequest

PORT = 5000
HOSTNAME = "www.bcit.ca"
DEFAULT_PORT = 5000
BUFF_SIZE = 1024


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


def init_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    try:
        context.load_verify_locations("cert.pem")
    except ssl.SSLError as e:
        print(f"SSLError : {e}")
        quit()
    return context


def execute_request(req: ClientRequest):
    context = init_context()

    client_socket = socket.socket()
    try:
        client_socket.settimeout(5)
        client_socket.connect((req.ip_address, req.port))

        ssl_context = context.wrap_socket(client_socket, server_hostname=HOSTNAME)
        client_cert = ssl_context.getpeercert()
        if not client_cert:
            raise Exception("Unable to retrieve server certificate")

        message = input()
        ssl_context.send(message.encode())
        capitalized_message = ssl_context.recv(BUFF_SIZE).decode()
        print(f'{capitalized_message}')
        ssl_context.close()
    except TimeoutError as e:
        print(f'TimeoutError: Failed to establish connection with {req.ip_address}:{req.port}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()
        quit()


def main():
    request = setup_client_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()
