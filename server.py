import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 5000

clients = {}
lock = threading.Lock()


def send_json(writer, data):
    writer.write(json.dumps(data) + '\n')
    writer.flush()


def broadcast_users():
    with lock:
        users = list(clients.keys())
        for _, writer in clients.values():
            send_json(writer, {'type': 'user_list', 'users': users})


def handle_client(conn, addr):
    reader = conn.makefile('r')
    writer = conn.makefile('w')
    username = None

    try:
        data = json.loads(reader.readline())

        if data['type'] != 'register':
            return

        username = data['username']

        with lock:
            if username in clients:
                send_json(writer, {'type': 'error', 'message': 'Username taken'})
                return
            clients[username] = (conn, writer)

        print(f"{username} connected")

        send_json(writer, {'type': 'register_ok'})
        broadcast_users()

        while True:
            msg = reader.readline()
            if not msg:
                break

            data = json.loads(msg)

            if data['type'] == 'message':
                to_user = data['to']

                with lock:
                    if to_user in clients:
                        _, w = clients[to_user]
                        send_json(w, {
                            'type': 'message',
                            'from': username,
                            'payload': data['payload']
                        })
                    else:
                        send_json(writer, {'type': 'error', 'message': 'User not found'})

            elif data['type'] == 'list_users':
                with lock:
                    send_json(writer, {'type': 'user_list', 'users': list(clients.keys())})

            elif data['type'] == 'exit':
                break

    except Exception as e:
        print("Error:", e)

    finally:
        if username:
            with lock:
                clients.pop(username, None)
            print(f"{username} disconnected")
            broadcast_users()

        conn.close()


def start():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start()