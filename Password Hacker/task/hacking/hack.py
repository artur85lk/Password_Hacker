import sys
import socket
import itertools
import string



def main():
    args = sys.argv
    chars = string.ascii_lowercase + string.digits
    with socket.socket() as client_socket:
        client_socket.connect((args[1], int(args[2])))
        for length in range(1, 5):
            for i in itertools.product(chars, repeat=length):
                password = "".join(i)
                client_socket.send(password.encode())
                response = client_socket.recv(1024).decode()
                if response == "Connection success!":
                    return print(password)


if __name__ == "__main__":
    main()

