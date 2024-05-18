import socket
import sys
import threading

def read_socket_and_output(s):
    global bye_flag
    print("Enter 'bye' to quit chat")
    while True:
        if bye_flag:
            try:
                received_str = s.recv(1024).decode()
                print("\r>>> " + received_str + "\n<<<", end="", flush=True)
            except:
                print("Connection closed")
                break

            if received_str == "bye":
                bye_flag = 0
                break
        
    print("Remote user disconnected!!!")
    s.close()
    connect_to_peer()

def read_stdin_and_write_socket(s):
    global bye_flag
    while True:
        if bye_flag:
            send_str = input("<<< ")
            s.sendto(send_str.encode(), (broadcast_ip, port))
            if send_str == "bye":
                print("Chat termination signal sent!!!")
                bye_flag = 0
                s.close()
                connect_to_peer()

def broadcast_message():
    global bye_flag
    while True:
        if bye_flag:
            broadcast_str = input("Broadcast Message: ")
            s.sendto(broadcast_str.encode(), (broadcast_ip, port))
            if broadcast_str == "bye":
                bye_flag = 0
                s.close()
                connect_to_peer()

def connect_to_peer():
    global bye_flag
    bye_flag = 1
    ch = input("Connect[1] to peer or wait[2] for peer connection. Enter choice:")

    if ch == "1":
        host = input("Enter peer IP:")
        port = 54321
        s.connect((host, port))
        threading.Thread(target=read_socket_and_output, args=(s,)).start()
        threading.Thread(target=read_stdin_and_write_socket, args=(s,)).start()
        threading.Thread(target=broadcast_message).start()
        
    elif ch == "2":
        host = ''
        port = 54321
        s.bind((host, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.listen(2)
        print("Waiting for connection...")
        c, addr = s.accept()  # Establish connection with client.
        threading.Thread(target=read_socket_and_output, args=(c,)).start()
        threading.Thread(target=read_stdin_and_write_socket, args=(c,)).start()
        threading.Thread(target=broadcast_message).start()

    else:
        print("Incorrect choice")
        sys.exit()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

broadcast_ip = '<broadcast>'
port = 54321

connect_to_peer()
