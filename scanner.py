import socket

DELAY = 5


def make_tcp_socket():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.settimeout(DELAY)
    return tcp_sock


def make_udp_socket():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.settimeout(DELAY)
    return udp_sock


def scan(host, port, output):
    tcp_sock = make_tcp_socket()
    udp_sock = make_udp_socket()
    host = socket.gethostbyname(host)
    try:
        tcp_sock.connect((host, port))
        output.append(f'TCP {port}')
    except:
        pass

    try:
        udp_sock.sendto(b'', (host, port))
        data, address = udp_sock.recv(1024)
        output.append(f'UDP {port}')
    except socket.timeout:
        pass
