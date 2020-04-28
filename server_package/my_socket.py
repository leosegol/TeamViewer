from protocols.my_protocol import send as my_send
from protocols.my_protocol import receive as my_receive


class Socket:

    def __init__(self, client_send, client_recv):
        self.client_send = client_send
        self.client_recv = client_recv
        self.host = False
        self.partner = None
        self.started_hosting = False
        self.pin = -1
        self.viewer = False
        self.finished_session = False

    def send(self, data):
        if type(data) != bytes:
            data = data.encode()
        my_send(self.client_send, data)

    def recv(self):
        data = my_receive(self.client_recv)
        return data

    def stop_hosting(self):
        self.partner = None
        self.started_hosting = False
        self.pin = -1
        self.host = False

    def stop_viewing(self):
        self.partner = None
        self.viewer = False

    def become_host(self, password):
        if not self.viewer:
            self.pin = password
            self.host = True
        return self.host

    def start_hosting(self):
        if self.host and self.partner:
            self.started_hosting = True
        return self.started_hosting

    def exit(self):
        if self.partner:
            self.partner.viewer = False
            self.partner.partner = None
        self.client_recv.close()
        self.client_send.close()

    def connect(self, host_client, pin):
        if not self.host:
            if int(pin) == host_client.pin and pin != "-1":
                self.partner = host_client
                self.partner.partner = self
                self.viewer = True
                return True
        return False

    def can_start_session(self):
        return self.partner and self.partner.started_hosting or self.host

    def string(self):
        print(self.client_socket, self.partner, self.started_hosting, self.host, self.pin, self.viewer)
