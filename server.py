import socket
import os

host = '127.0.0.1'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(1)

print('Starting server on', host, port)

while 1:   

    csock, caddr = server.accept()
        
    req = csock.recv(1024).decode('utf-8')

    print(req)

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
            if myfile == '/':
                myfile = 'index.html'
            elif myfile == '/info.html':
                myfile = 'info.html'
            else:
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
               
                if(myfile.endswith(".css")):
                    mimetype = 'text/css'
                else:
                    mimetype = 'text/html'

                header += 'Content-Type: '+str(mimetype)+'\n\n'


        final_response = header.encode('utf-8')
        final_response += response
        csock.send(final_response)
        #print(final_response)
        csock.close()

