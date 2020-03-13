class Socket:

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.host = False
        self.partner = None
        self.started_hosting = False
        self.pin = -1
        self.viewer = False

    def send(self, data):
        if type(data) != bytes:
            data = data.encode()
        self.client_socket.send(data)

    def recv(self, size):
        data = self.client_socket.recv(size)
        return data

    def stop_hosting(self):
        self.partner = None
        self.started_hosting = False
        self.pin = -1
        self.host = False

    def become_host(self, password):
        if not self.viewer:
            self.pin = password
            self.host = True
        return self.host

    def start_hosting(self):
        if self.host and self.partner:
            self.started_hosting = True
        return self.start_hosting

    def exit(self):
        if self.partner:
            self.partner.viewer = False
            self.partner.partner = None
        self.client_socket.close()

    def connect(self, host_client, pin):
        if not self.host:
            if int(pin) == host_client.pin and pin != "-1":
                self.partner = host_client
                self.partner.partner = self
                self.viewer = True
                return "ok"
            return "not a matching password"
        return "You cant host and connect"

    def can_start_session(self):
        return self.started_hosting or self.viewer and self.partner and self.partner.viewer \
               or self.partner.started_hosting

    def string(self):
        print(self.client_socket, self.partner, self.started_hosting, self.host, self.pin, self.viewer)