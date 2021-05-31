import socket
from multiprocessing.pool import ThreadPool
from socket import *
from random import *

random_time = randint(2 ** 16, 2 ** 64 - 1).to_bytes(8, 'big')
udp_to_send = b'\x13' + b'\0' * 39 + random_time


class Scanner:
    def __init__(self, host):
        self.host = host
        self.output = []
        self._threads = ThreadPool()
        setdefaulttimeout(0.5)

    def scan(self, args):
        try:
            tasks = []
            for port in range(args.ports[0], args.ports[1] + 1):
                if args.t:
                    tcp_task = self._threads.apply_async(self._tcp_scan, args=(port, "TCP"))
                    tasks.append(tcp_task)
                if args.u:
                    udp_task = self._threads.apply_async(self._udp_scan, args=(port, "UDP"))
                    tasks.append(udp_task)
            for task in tasks:
                task.wait()
        finally:
            self._threads.terminate()
            self._threads.join()

    def _udp_scan(self, port: int, proto: str):
        with socket(AF_INET, SOCK_DGRAM) as sock:
            try:
                sock.sendto(b'', (self.host, port))
                sock.settimeout(3)
                data, address = sock.recvfrom(2048)
            except (timeout, OSError):
                pass
            except PermissionError:
                print(f'UDP port: {port} Permissom Error')
            else:
                print(f'{proto} {port} {Scanner.get_protocol(data, port, "udp")}')

    def _tcp_scan(self, port, proto: str):
        with socket(AF_INET, SOCK_STREAM) as sock:
            try:
                sock.connect((self.host, port))
                sock.send(b'')
                try:
                    data = sock.recv(1024)
                    print(f'TCP {port} {Scanner.get_protocol(data, port, "tcp")}')
                except timeout:
                    print(f'TCP {port}')
            except (ConnectionRefusedError, timeout):
                pass
            except PermissionError:
                print(f'{proto} port: {port} Permissom Error')

    @staticmethod
    def get_protocol(data: bytes, port: int, transport: str) -> str:
        if len(data) > 4 and b'HTTP' in data:
            return 'HTTP'
        if b'SMTP' in data or b'EHLO' in data:
            return 'SMTP'
        if b'POP3' in data or data.startswith(b'+OK') or data.startswith(b'+'):
            return 'POP3'
        if b'IMAP' in data:
            return 'IMAP'
        try:
            return getservbyport(port, transport).upper()
        except OSError:
            return ''
