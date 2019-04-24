import socket

from .BotStatus import BotStatus


class BotSocket:
    ip = "127.0.0.1"
    port = 19421

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def get_account_status(self, username):
        try:
            self.socket.sendall(('get status %s' % username).encode())
            data = self.socket.recv(1024).decode()
            if data == "RUNNING":
                return BotStatus.RUNNING
            if data == "STOPPED":
                return BotStatus.STOPPED
        except socket.error as e:
            # TODO: Inform the user that this failed.
            # TODO: This shouldn't be handled here though.
            print(str(e))
        return BotStatus.UNKNOWN

    def set_account_status(self, username, status):
        try:
            self.socket.sendall(('set status %s %s' % (username, status)).encode())
            return True
        except socket.error as e:
            return False
