import base64
import pickle
import platform
import socket
import sys
from datetime import datetime

log_level = 2


def log_info(base, *args):
    if log_level > 2:
        return
    if args:
        sys.stdout.write((datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' [INFO] ' + base + '\n') % args)
    else:
        sys.stdout.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' [INFO] ' + base + '\n')


def log_error(base, *args):
    if log_level > 3:
        return
    if args:
        sys.stdout.write((datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' [ERROR] ' + base + '\n') % args)
    else:
        sys.stdout.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' [ERROR] ' + base + '\n')


def log_debug(base, *args):
    if log_level > 1:
        return
    if args:
        sys.stdout.write((datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' [DEBUG] ' + base + '\n') % args)
    else:
        sys.stdout.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' [DEBUG] ' + base + '\n')


def decode_command(command):
    return pickle.loads(base64.b64decode(command.encode('ascii')))


def encode_command(command):
    return base64.b64encode(pickle.dumps(command)).decode("ascii")


def date(raw):
    return datetime.strptime(raw, '%Y-%m-%dT%H:%M:%SZ')


def sys_info():
    return [platform.platform(),
            socket.gethostname(),
            [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]]


def read_file(file):
    with open(file, "rb") as f:
        return f.read()
