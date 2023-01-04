from socket import *

f = open('test.html', 'r')
r = f.read()

serverPort = 1230 # port number
serverSocket = socket(AF_INET, SOCK_STREAM) # SOCK_STREAM으로 TCP 방식의 socket 생성
serverSocket.bind(('', serverPort)) # (IP, port) tuple

serverSocket.listen(0) # port listen, 동시에 연결 가능한 socket 개수, 0이면 자동

while True:
    connectionSocket, addr = serverSocket.accept() # client 접속할 때까지 대기
    print('********client 연결********') # accpet가 되면 connection setup

    message = connectionSocket.recv(1024) # client 접속이 되면 message 읽기
    request = message.decode() # message 해독
    print(request)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    request = request.split()

    # response 형태
    # HTTP/1.0 200 OK
    # GET이면 파일 전체 읽어오기, HEAD이면 
    response = 'HTTP/1.0 '
    # HEAD
    if request[0] == 'HEAD':
        if request[1] !=  "/": # 요청한 데이터가 추가로 있으면
            response += '404 Not Found'
        else:
            response += '200 OK'
    # GET
    elif request[0] == 'GET':
        if request[1] == 'test.html':
            response += '200 OK\n' + r
        else:
            response += '404 Not Found'
    # POST
    elif request[0] == 'POST':
        if request[1] != 'test.html' and "." in request[1]:
            newfile = open(request[1], "w")
            newread = newfile.read()
            newfile.close()
            response += '200 OK\n' + newread
        else:
            response += '404 Not Found'
    else:
        response += '400 Bad Request' # method 해석 불가능한 경우

    connectionSocket.send(response.encode()) # socket 보내기
    print(response)
    
    connectionSocket.close() # 연결 종료
    print('***********close***********')