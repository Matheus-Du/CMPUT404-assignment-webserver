#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK",'utf-8'))
        
        requestType = self.data.decode().split()[0]
        
        if requestType == "GET":
            self.verifyGET()
        else:
            # since only allowed method is GET, return 405 for all other methods
            self.sendResponse(405)

    def verifyGET(self):
        # verify that the provided path is valid, returning 200 if it is and 404 if it is not
        path = self.getPath()

        if path is False:
            # if path is incorrect or not found, send 404
            self.sendResponse(404)
            return
        
        if path != "301":
            # if path is correct and not a redirect, send 200
            self.sendResponse(200, path)
            return
        
    def getPath(self):
        # get the path from the request and verify that the request can access it
        path = self.data.decode().split()[1]
        # TODO: verify that the path is valid
        print("Path is " + path)
        return path

    def sendResponse(self, responseType, path=None):
        # send the appropriate response to the client based on the response type
        # TODO: the following is just a placeholder, replace with actual responses
        print("Sending response of type " + str(responseType))
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
