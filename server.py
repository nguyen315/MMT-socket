import socket
from threading import Thread


def handle_client(client):
    req = client.recv(1024).decode('utf-8')

    print(req)

    if len(req) == 0:
        csock.close()

    else:
        string_list = req.split('\r\n\r\n')  # Cắt request để xử lý

        first_line = string_list[0].split(' ')
        method = first_line[0]
        requesting_file = first_line[1]

        my_file = requesting_file

        # Xử lý các request tương ứng
        if method == 'GET':

            my_file = my_file.split("/")

            if my_file[1] == '':
                my_file = "index.html"
            elif my_file[1] == "image":
                my_file = my_file[1] + "/" + my_file[2]
            else:
                my_file = my_file[1]

            file = open(my_file, 'rb')
            response = file.read()
            file.close()

            header = 'HTTP/1.1 200 OK\n'

            if my_file.endswith(".jpg"):
                mimetype = 'image/jpg'
            elif my_file.endswith(".css"):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'

            header += 'Content-Type: ' + str(mimetype) + '\n\n'

        # method = POST
        else:

            data = string_list[1]

            uname, password = data.split('&')
            uname = uname.split('=')[1]
            password = password.split('=')[1]

            if uname == 'admin' and password == 'admin':
                header = '''HTTP/1.1 301 Moved Permanently\nLocation: /info.html\n\n'''
                response = "".encode('utf-8')

            else:

                my_file = '404.html'
                file = open(my_file, 'rb')
                response = file.read()
                file.close()

                header = 'HTTP/1.1 404 Not Found\n'

                mimetype = 'text/html'

                header += 'Content-Type: ' + str(mimetype) + '\n\n'

        final_response = header.encode('utf-8')
        final_response += response
        client.send(final_response)

        # print(final_response)

        client.close()


threads = []

host = ''
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)

print('Starting server on', host, port)

while True:
    csock, caddr = server.accept()

    newThread = Thread(target=handle_client, args=(csock,))

    newThread.start()
    newThread.join()
    threads.append(newThread)

