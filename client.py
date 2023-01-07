# client.py
# server에 request를 보내고 response를 받아 출력한다

from socket import *

serverName = '127.0.0.1' # server
serverPort = 1230 # port number

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM) # SOCK_STREAM으로 TCP 방식의 client socket 생성
    clientSocket.connect((serverName, serverPort)) # (IP, port) 서버 연결
    print('********server 연결********')

    message = input('Request or exit(-1)>> ') # 사용자로부터 request 입력 받기
    message = message.split() # message = ['GET', 'test.html']

    # request 형태
    # GET test.html / HTTP/1.0
    # HOST: 127.0.0.1
    # User-Agent: Mozilla/5.0 (Macintosh; ...) ... Firefox/51.0
    # Accept: text/html, application/xhtml+xml,...,*/*;q=0.8
    # Accept-Language: en-US, en;q=0.5
    # Accept-Encoding: gzip, deflate
    # Connection: keep-alive -> HTTP/1.1
    # Upgrade-Insecure-Requests: 1
    # Content-Type: multipart/form-data; boundary=-1265974
    # Content-Length: 345
    if message[0] == '-1':
        request = message[0]
        clientSocket.send(request.encode())
        clientSocket.close()
        print('***********close***********')
        break
    if message[0] == 'GET' or message[0] == 'HEAD' or message[0] == 'POST' or message[0] == 'PUT':
        request = message[0] + ' '
        if len(message) > 1:
            request += ' '.join(message[1:])
        request += ' / HTTP/1.0\n' \
                 + 'HOST: ' + serverName + '\n' \
                 + 'Accept: text/html' \
                 + 'Accept-Language: en-us\n'  \
                 + 'Connection: close\n' \
                 + 'Content-Type: multipart/related'
    else:
        request = " ".join(message)

    clientSocket.send(request.encode()) # socket으로 request 보내기

    response = clientSocket.recv(1024).decode() # server name, port에 접근할 필요 없음 -> socket 사용
    print(response)
    clientSocket.close() # 연결 종료
    print('***********close***********')