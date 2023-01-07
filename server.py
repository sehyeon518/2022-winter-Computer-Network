# server.py
# client request를 받아 출력하고 response 보낸다

from socket import *
import os
import time

serverPort = 1230 # port number
serverSocket = socket(AF_INET, SOCK_STREAM) # SOCK_STREAM으로 TCP 방식의 socket 생성
serverSocket.bind(('', serverPort)) # (IP, port) tuple

serverSocket.listen(0) # port listen, 동시에 연결 가능한 socket 개수, 0이면 자동

while True:
    files = os.listdir(os.getcwd()) # 요청한 파일이 현재 dir에 있는지 판단하기 위함
    date = time.strftime('%d %b %Y %H:%M:%S %Z', time.localtime(time.time())) # header의 Date

    connectionSocket, addr = serverSocket.accept() # client 접속할 때까지 대기
    print('********client 연결********') # accpet가 되면 connection setup

    message = connectionSocket.recv(1024) # client 접속이 되면 message 읽기
    request = message.decode() # request message 해독
    print(request) # request message 출력
    request = request.split() # request = ['GET', 'test.html', 'HTTP/1.0', ...]

    # response 형태
    # HTTP/1.0 200 OK
    # Server: Apache
    # Content-Type: text/html; charset=iso-8859-1
    # Date: Wed, 10 Aug 2016 09:23:25 GMT
    # Keep-Alive: timeout=5, max=1000
    # Connection: Keep-Alive
    # Age: 3464
    # Date: Wed, 10 Aug 2016 09:46:25 GMT
    # X-Cache-Info: caching
    # Content-Length: 220 -> 선택사항
    response = 'HTTP/1.0 ' # HTTP 1.0: 모든 요청마다 연결과 해제 반복

    if request[0] == '-1':
        connectionSocket.send('-1'.encode())
        serverSocket.close()
        print('***********close***********')
        break
    # HEAD response 필요한 header 정보 #
    elif request[0] == 'HEAD':
        if request[1] in files: # 정상적으로 파일을 요청한 경우
            response += '200 OK\r\n'  \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Vary: User-Agent,Accept-Encoding\r\n' \
                      + 'Content-Type: text/html; charset=utf-8'
        else: # 존재하지 않는 파일을 요청한 경우
            response += '404 Not Found\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Content-Type: text/html; charset=utf-8'
    # GET response body #
    elif request[0] == 'GET':
        if request[1] in files: # 존재하는 파일을 정상적으로 요청
            f = open(request[1], 'r') # 파일을 읽기모드로 r에 담기
            r = f.read()
            f.close()
            response += '200 OK\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Vary: User-Agent,Accept-Encoding\r\n' \
                      + 'Content-Type: text/html; charset=utf-8\r\n\r\n' \
                      + r
        else:
            response += '404 Not Found\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Content-Type: text/html; charset=utf-8'
    # POST response #
    elif request[0] == 'POST':
        if request[1] not in files and '.' in request[1]: # 존재하지 않는 파일 create
            newfile = open(request[1], 'w')
            newfile.close()
            response += '201 Created ' + request[1] + '\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Vary: User-Agent,Accept-Encoding\r\n' \
                      + 'Content-Type: text/html; charset=utf-8\r\n\r\n'
        elif request[1] in files:
            f = open(request[1], 'r')
            r = f.read()
            f.close()
            response += '200 OK ' + request[1] + '\r\n' \
                      + 'Date: ' + date + '\r\n\r\n' \
                      + r
        else:
            response += '404 Not Found\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Content-Type: text/html; charset=utf-8'
    # PUT response #
    elif request[0] == 'PUT':
        if request[1] in files:
            f = open(request[1], 'r')
            r = f.read()
            f.close()
            response += '200 OK ' + request[1] + '\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Vary: User-Agent,Accept-Encoding\r\n' \
                      + 'Content-Type: text/html; charset=utf-8\r\n\r\n' \
                      + r
        else:
            response += '404 Not Found\r\n' \
                      + 'Date: ' + date + '\r\n' \
                      + 'Connection: close\r\n' \
                      + 'Content-Type: text/html; charset=utf-8'
    # Invalid method #
    else: # method 해석이 불가능한 경우
        response += '400 Bad Request\r\n' \
                  + 'Date: ' + date

    connectionSocket.send(response.encode()) # socket 보내기
    
    connectionSocket.close() # 연결 종료
    print('***********close***********')