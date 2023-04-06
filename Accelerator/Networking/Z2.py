import socket
from pynq import Overlay, allocate
import pynq.lib.dma
import numpy as np

# FPGA binary imports
ol = Overlay('./accel.bit')
ol.download()
dma0 = ol.axi_dma_0
time_step_ip = ol.n_body_problem

# Server constants
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.2.99"
PORT = 12345
PACKET_SIZE = 4096
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Z2 constants
DIM = 1024
DATA_TYPE = np.float32
in_buffer = allocate(shape=(DIM,), dtype=DATA_TYPE)
out_buffer = allocate(shape=(DIM,), dtype=DATA_TYPE)
C = np.zeros((DIM,), dtype=DATA_TYPE)

# Physics variables
time_step = 0.0

# Hardware calls
def silicon(A):
    np.copyto(in_buffer, A)
    np.copyto(out_buffer, C)
    # ip write location found in: <vitis_solution_directory>/impl/misc/drivers/<solution_name>_v1_0/src/x<solution_name>_hw.h
    time_step_ip.write(0x10, DATA_TYPE(time_step))
    dma0.sendchannel.transfer(in_buffer)
    dma0.recvchannel.transfer(out_buffer)
    dma0.sendchannel.wait()
    dma0.recvchannel.wait()
    time_step += 0.01

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    client_socket, addr = server_socket.accept()
    print(f'Connected to {addr}')

    # Receive the array from the client
    data = client_socket.recv(PACKET_SIZE)
    A = np.frombuffer(data, dtype=DATA_TYPE)
    
    # Execute NBP on array
    silicon(A)

    # Send the modified array back to the client
    client_socket.sendall(out_buffer.tobytes())

    # Clean up
    client_socket.close()