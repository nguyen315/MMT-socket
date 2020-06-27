import socket
from threading import Thread
import os


def handle_client(client):
    req = client.recv(1024).decode('utf-8')
    
    if (len(req) == 0):
        csock.close()

        
    else:

        string_list = req.split('\r\n\r\n')     # Cắt request để xử lý

        firstLine = string_list[0].split(' ')
        method = firstLine[0]  
        requesting_file = firstLine[1]  


        myfile = requesting_file


        # Xử lý các request tương ứng

        if method == 'GET':
            if myfile == '/' or myfile == "/index.html":
                myfile = 'index.html'
            elif myfile == '/info.html':
                myfile = 'info.html'
            elif myfile == '/styles.css':
                myfile = 'styles.css'

            file = open(myfile, 'rb')
            response = file.read()
            file.close()

            header = 'HTTP/1.1 200 OK\n'

            if(myfile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(myfile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'

            header += 'Content-Type: '+str(mimetype)+'\n\n'

                
        # method = POST
        else :

            data = string_list[1]

            uname, password = data.split('&')
            uname = uname.split('=')[1]
            password = password.split('=')[1]

            if (uname == 'admin' and password == 'admin'):
                header = '''HTTP/1.1 301 Moved Permanently\nLocation: /info.html\n\n'''
                response = "".encode('utf-8')
            
            else:

                myfile = '404.html'
                file = open(myfile, 'rb')
                response = file.read()
                file.close()

                header = 'HTTP/1.1 404 Not Found\n'
               
                mimetype = 'text/html'

                header += 'Content-Type: ' + str(mimetype) + '\n\n'


        final_response = header.encode('utf-8')
        final_response += response
        client.send(final_response)
        #print(final_response)
        client.close()

threads = []

host = ''
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)

print('Starting server on', host, port)



while 1:
    
    

    csock, caddr = server.accept()

    newThread = Thread(target=handle_client, args=(csock,))

    newThread.start()
    threads.append(newThread)
    

    
for t in threads: 
    t.join()
    
