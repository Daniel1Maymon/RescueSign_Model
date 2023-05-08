import socket

BUFF_SIZE = 65536

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    host_name = socket.gethostname()
    host_ip = '0.0.0.0'
    port = 9999
    socket_address = (host_ip, port)

    message = b'control room'
    client_socket.sendto(message, socket_address)

except socket.error as e:
    print(f"Socket error occurred: {e}")
