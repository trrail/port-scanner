import scanner
import threading


def scan_tcp(ports):
    ports_stat = []
    threads = []
    for i in range(ports):
        t = threading.Thread(target=scanner.scan, args=('149.112.112.112', i, ports_stat))
        threads.append(t)

    for i in range(ports):
        threads[i].start()

    for i in range(ports):
        threads[i].join()
    return ports_stat


if __name__ == "__main__":
    stat = scan_tcp(10000)
    for i in stat:
        print(i)
