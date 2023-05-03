import socket
from pynq import Overlay, allocate
import pynq.lib.dma
import numpy as np

# FPGA binary imports
ol = Overlay('./accel.bit')
dma0 = ol.axi_dma_0

# ip write location found in: <vitis_solution_directory>/impl/misc/drivers/<solution_name>_v1_0/src/<solution_name>_hw.h
# > define XNBP_CONTROL_ADDR_TIME_STEP_DATA 0x10
ip = ol.nbp_0

# Server constants
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "192.168.2.99"
PORT = 5000
PACKET_SIZE = 4096
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Z2 constants
DIM = 1024
DATA_TYPE = np.float32
time_step = 0
in_buffer = allocate(shape=(DIM,), dtype=DATA_TYPE)
out_buffer = allocate(shape=(DIM,), dtype=DATA_TYPE)
C = np.zeros((DIM,), dtype=DATA_TYPE)

# Hardware calls
def silicon(a):
    ip.write(0x10, time_step)
    np.copyto(in_buffer, a)
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
            
    # Execute on array
    silicon(a)

    # Send the modified array back to the client
    client_socket.sendall(out_buffer.tobytes())

    # Clean up
    client_socket.close()