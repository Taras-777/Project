import threading


class Listener(threading.Thread):
    def __init__(self, port, callback, *args, **kwargs):
        super(Listener, self).__init__(target=self.listen, *args, **kwargs)
        self.port = port
        self.callback = callback
        self.is_killed = False

    def listen(self):
        while True and not self.is_killed:
            data = self.port.read(1)

            self.callback(data)