from scanner import Scanner
from argparse import *

parser = ArgumentParser(description='Port Scanner')
parser.add_argument('host', action='store', help='Host for scan')
parser.add_argument('-t', action='store_true', help='TCP port scan')
parser.add_argument('-u', action='store_true', help='UDP port scan')
parser.add_argument('-p', '--ports', action='store', nargs=2, type=int,
                    default=[1, 65535], help='Port scan range. Default 1- 65535')

if __name__ == "__main__":
    args = parser.parse_args()
    scanner = Scanner(args.host)
    scanner.scan(args)
    for output in scanner.output:
        print(output)
