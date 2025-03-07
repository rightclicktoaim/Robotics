import socket
import threading

# SERVER_IP_ADDRESS = '144.75.132.28'
SERVER_IP_ADDRESS = 'localhost'
CONTROL_PORT_NUMBER = 8888
BUFFER_SIZE = 1024

# socket for control command exchange
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP_ADDRESS, CONTROL_PORT_NUMBER))
server_socket.listen()
print('Server is up and listening ....')

def messageOutHandler(client):
    while True:
        try:
            messageOut = input("Server>>>")
            client.send(messageOut.encode(('ascii')))

            if messageOut == 'EXIT':
                print("Connection Terminated")
                break

        except:
            client.close()
            break

def messageInHandler(client):
    while True:
        try:
            messageIn = client.recv(1024).decode('ascii')
            print("Client>>>" + messageIn)

            if messageIn == 'EXIT':
                print("Connection Terminated")
                client.close()
                break

        except:
            client.close()
            break

if __name__ == '__main__':
    
        client, address = server_socket.accept()
        print(f'Connected with {str(address)}')
        
        dispatcher_thread = threading.Thread(target=messageOutHandler, args=(client, ))
        receiver_thread = threading.Thread(target=messageInHandler, args=(client, ))
        dispatcher_thread.start()
        receiver_thread.start()
        