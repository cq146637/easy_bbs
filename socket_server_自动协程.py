import select
import socket
import queue
import time

class sock_server(object):
    def __init__(self):
        self.server = socket.socket()
        self.input = [self.server]
        self.input_name = ["server"]
        self.input_dict = {str(self.server): "0,1,1"}  # 字典绑定conn与name，第一个数字代表序号，未绑定0，未第一次输出1
        self.output = []
        self.msg_dict = {}
        self.say_hello = 0
        self.server.bind(("localhost",9000))
        self.server.listen()
    def read(self,readable):
        for r in readable:
            if r is self.server:
                conn, addr = self.server.accept()
                self.input.append(conn)
                self.input_dict[str(conn)] = str(len(self.input) - 1) + ",0,0"
                self.input_name.append("conn")
                self.msg_dict[conn] = queue.Queue()
            else:
                data = "break".encode("utf-8")
                try:
                    data = r.recv(1024)
                except ConnectionResetError:
                    self.exceptional(r)
                if data.decode() not in "break":
                    for name in self.input_dict:
                        if str(r) in name:
                            if self.input_dict[name][2] == "0":
                                index = self.input_dict[name][0]
                                self.input_name.insert(int(index), data.decode())
                                self.input_name.pop(int(index) + 1)
                                self.input_dict[name] = index + ",1,0"
                    self.msg_dict[r].put(data)
                    self.output.append(r)
    def write(self,writeable):
        for w in writeable:
            data = self.msg_dict[w].get()
            say_hello = 0
            for r in self.input:
                if r is not self.server:
                    index = self.input_dict[str(w)][0]
                    username = self.input_name[int(index)]
                    if self.input_dict[str(w)][4] in "0":
                        r.send((username + "/r/t/g/b/g/r/t/g/b/g" + "joined the chat room！！").encode("utf-8"))
                        say_hello += 1
                        if say_hello == len(self.input) - 1:
                            self.input_dict[str(w)] = str(index) + ",1,1"
                    else:
                        r.send((username + "/r/t/g/b/g/r/t/g/b/gis speaking : " + data.decode()).encode("utf-8"))
            self.output.remove(w)
    def exceptional(self,r):
        if r in self.output:
            self.output.remove(r)
            r.close()
        self.input.remove(r)
        break_num = int(self.input_dict[str(r)][0])
        self.input_name.pop(break_num)
        for num in self.input_dict:
            if int(self.input_dict[num][0]) > break_num:
                arg1 = int(self.input_dict[num][0]) - 1
                arg2 = self.input_dict[num][2]
                arg3 = self.input_dict[num][4]
                self.input_dict[num] = str(arg1) + arg2 + arg3
                print(self.input_dict)
        del self.msg_dict[r]
        del self.input_dict[str(r)]
    def select(self):
        while True:
            readable,writeable,exceptional = select.select(self.input,self.output,self.input)
            self.read(readable)
            self.write(writeable)

def main():
    server = sock_server()
    server.select()


if "__main__" == __name__:
    main()

