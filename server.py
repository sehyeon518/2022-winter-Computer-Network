from socket import *

serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM) # TCP 방식의 socket 생성
serverSocket.bind(('locslhost', serverPort)) # (IP, port) tuple

serverSocket.listen(0) # port listening. 동시에 연결 가능한 socket 개수는 한개
print('The server is ready to receive') # 확인

connectionSocket, addr = serverSocket.accept() # 클라이언트 접속할 때까지 대기
print('accept') # accpet가 되면 cennection setup

data = connectionSocket.recv(1024) #클라이언트 접속이 되면 데이터를 읽어들임.
print('print', data.decode())
connectionSocket.send(data) # socket 보내기
print('send')
connectionSocket.close() # 연결 종료
print('close')