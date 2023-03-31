import socket, datetime
import numpy as np

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Networking constants
host = '192.168.2.99'
port = 12345
PACKET_SIZE = 4096

# Connect to the server
client_socket.connect((host, port))

# Data constants
DATA_TYPE = np.float32
SIZE = 256

# Create an array to send operate on
a = np.zeros((SIZE, 4), dtype=DATA_TYPE)
for i in range(SIZE):
    a[i] = DATA_TYPE(10 * np.random.random_sample())

# Begin benchmark, and send the array to the server
times = datetime.datetime.now()
client_socket.sendall(a.tobytes())

# Receive the modified array from the server, and finish benchmark
data = client_socket.recv(4096)
a_modified = np.frombuffer(data, dtype=DATA_TYPE) #.reshape(-2, 4)
timee = datetime.datetime.now()

print("Time in microseconds: ", (timee - times).microseconds)

# Clean up
client_socket.close()