import socket

# Define the server (slave) address and port
slave_address = '127.0.0.1'
slave_port = 12345

# Create a socket object
slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the master
slave_socket.connect((slave_address, slave_port))
print(f"Connected to master at {slave_address}:{slave_port}")

# Receive the number from the master
received_data = slave_socket.recv(1024).decode()
number_received = int(received_data)
print(f"Received number from master: {number_received}")

# Close the connection
slave_socket.close()
