from socket import *

serverPort = 9541
serverSocket = socket(AF_INET, SOCK_STREAM) # TCP 방식의 socket 생성
serverSocket.bind(('', serverPort)) # (IP, port) tuple

serverSocket.listen(0) # port listening. 동시에 연결 가능한 socket 개수는 한개
print('The server is ready to receive') # 확인
print('accept 대기')

while True:
    connectionSocket, addr = serverSocket.accept() # 클라이언트 접속할 때까지 대기
    print('*****accept*****') # accpet가 되면 cennection setup

    while True:
        message = connectionSocket.recv(1024) #클라이언트 접속이 되면 데이터를 읽어들임.
        request = message.decode()
        print('request', request)

        request = request.split()
        print(request)

        connectionSocket.send(message) # socket 보내기
        print('send')
        connectionSocket.close() # 연결 종료
        print('close')