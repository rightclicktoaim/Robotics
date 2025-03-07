import socket
import threading

# SERVER_IP_ADDRESS = '145.75.132.28'
SERVER_IP_ADDRESS = 'localhost'
CONTROL_PORT_NUMBER = 8888
BUFFER_SIZE = 1024

chatLock = 0

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP_ADDRESS, CONTROL_PORT_NUMBER))
print(f'Connected to .... {SERVER_IP_ADDRESS}:{CONTROL_PORT_NUMBER}')

def messageOutHandler(client_socket):
    global chatLock
    while True:
        try:
            chatLock = 1
            messageOut = input("Client>>>")

            chatLock = 0
            client_socket.send(messageOut.encode('ascii'))

            if messageOut == 'EXIT':
                print("Connection Terminated")
                client_socket.close()
                break

        except:
            break

def messageInHandler(client_socket):
    while True:
        try:
            messageIn = client_socket.recv(1024).decode('ascii')

            if chatLock == 1:
                print("\x1b[2K")

            print("Server>>>" + messageIn )

            if messageIn == 'EXIT':
                print("Connection Terminated")
                client_socket.close()
                break

        except:
            break

if __name__ == '__main__':
    dispatcher_thread = threading.Thread(target=messageOutHandler, args=(client_socket, ))
    receiver_thread = threading.Thread(target=messageInHandler, args=(client_socket, ))
    dispatcher_thread.start()
    receiver_thread.start()
