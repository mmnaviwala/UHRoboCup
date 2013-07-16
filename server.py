import SocketServer
import threading

#To start a theaded server run these lines in the robot that will be the server
#customServer = server.ThreadedTCPServer((ip, port), server.TCPRequestHandler)
#customServer.startTCPServerThread()
class TCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        curThread= threading.currentThread()
        #TODO code here!!!
        response = "sup you sent me something, here: "+data
        #send back processed data
        self.request.send(response)
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    def startTCPServerThread(self):
        serverThread = threading.Thread(target=self.serve_forever)
        serverThread.daemon = True
        serverThread.start()
