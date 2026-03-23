import socket
import threading
import json
from crypto_utils import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 5000


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))

        self.reader = self.sock.makefile('r')
        self.writer = self.sock.makefile('w')

    def send(self, data):
        self.writer.write(json.dumps(data) + '\n')
        self.writer.flush()

    def receive_loop(self):
        while True:
            try:
                msg = self.reader.readline()
                if not msg:
                    break

                data = json.loads(msg)

                if data['type'] == 'message':
                    try:
                        text = decrypt_message(data['payload'], self.password)
                        print(f"\n{data['from']}: {text}")
                    except:
                        print(f"\n{data['from']}: <cannot decrypt>")

                elif data['type'] == 'user_list':
                    print(f"\nUsers: {', '.join(data['users'])}")

                elif data['type'] == 'error':
                    print(f"\nError: {data['message']}")

            except:
                break

    def run(self):
        self.send({'type': 'register', 'username': self.username})

        response = json.loads(self.reader.readline())
        if response.get('type') != 'register_ok':
            print("Failed to connect")
            return

        threading.Thread(target=self.receive_loop, daemon=True).start()

        print("Commands:")
        print("/msg USER MESSAGE")
        print("/users")
        print("/quit")

        while True:
            cmd = input("> ")

            if cmd.startswith("/msg "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: /msg user message")
                    continue

                user = parts[1]
                message = parts[2]

                encrypted = encrypt_message(message, self.password)

                self.send({
                    'type': 'message',
                    'from': self.username,
                    'to': user,
                    'payload': encrypted
                })

            elif cmd == "/users":
                self.send({'type': 'list_users'})

            elif cmd == "/quit":
                self.send({'type': 'exit'})
                break

        self.sock.close()


def main():
    username = input("Username: ")
    password = input("Shared password: ")

    client = Client(username, password)
    client.run()


if __name__ == "__main__":
    main()