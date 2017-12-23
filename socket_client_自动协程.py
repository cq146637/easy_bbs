import socket
import threading
import time

class sock_client(object):
    def __init__(self,name,HOST,PORT):
        self.name = name
        self.HOST = HOST  # The remote host
        self.PORT = PORT  # The same port as used by the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def request(self):
        self.s.connect((self.HOST, self.PORT))
        #self.s.setblocking(False)
        self.s.send(self.name.encode("utf-8"))
    def recives(self):
            while True:
                try:
                    time.sleep(0.5)
                    data = self.s.recv(1024).decode()
                    if data:
                        list = data.split("/r/t/g/b/g/r/t/g/b/g")
                        if list[0]!=self.name:
                            print("\033[42;1m[%s]%s\033[0m" % (list[0],list[1]))
                    else:continue
                except BlockingIOError as e :
                    pass
    def connection(self):
        while True:
            msg = input(">>:").strip()
            self.s.send(msg.encode("utf-8"))
            # data = s.recv(1024)
            # print (data)

def main():
    name = input("Please input your name:")
    client = sock_client(name, "localhost", 9000)
    client.request()
    th1 = threading.Thread(target=client.connection)
    th2 = threading.Thread(target=client.recives)
    # th1.setDaemon(True)
    # th2.setDaemon(True)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    client.s.close()


if __name__ == "__main__":
    main()