import socket
from pynq import Overlay, allocate
import pynq.lib.dma
import numpy as np

# FPGA binary imports
ol = Overlay('./accel.bit')
ol.download()
dma0 = ol.axi_dma_0

# Server constants
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.2.99"
PORT = 12345
PACKET_SIZE = 4096
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Z2 constants
DIM = 256
DATA_TYPE = np.float32
in_buffer = allocate(shape=(DIM,), dtype=DATA_TYPE)
out_buffer = allocate(shape=(DIM,), dtype=DATA_TYPE)
C = np.zeros((DIM,), dtype=DATA_TYPE)

# Hardware calls
def silicon(A):
    np.copyto(in_buffer, A)
    np.copyto(out_buffer, C)
    dma0.sendchannel.transfer(in_buffer)
    dma0.recvchannel.transfer(out_buffer)
    dma0.sendchannel.wait()
    dma0.recvchannel.wait()

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    client_socket, addr = server_socket.accept()
    print(f'Connected to {addr}')

    # Receive the array from the client
    data = client_socket.recv(PACKET_SIZE)
    a = np.frombuffer(data, dtype=DATA_TYPE)
    
    # Execute FFT on array
    silicon(a)

    # Send the modified array back to the client
    client_socket.sendall(out_buffer.tobytes())

    # Clean up
    client_socket.close()