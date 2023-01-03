from socket import *

serverName = '127.0.0.1' # server
print(serverName)
serverPort = 9541 # HTTP port number

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM) # client 소켓 생성 (TCP)

    clientSocket.connect((serverName, serverPort)) # (IP, port) 서버 연결
    print('server 접속')

    message = input('Request>> ')
    message = message.split()
    print(message)

    if message[0] == 'GET' or message[0] == 'HEAD' or message[0] == 'POST' or message[0] == 'PUT':
        header = " ".join(message)
    else:
        print("Invalid method")
        print("종료")
        break

    clientSocket.send(header.encode()) # sockt으로 header 보내기
    print('send message:', header)
    print('response 대기')

    response = clientSocket.recv(1024).decode() # server name, port에 접근할 필요 없음 -> socket 사용

    clientSocket.close()
    print('연결 해제')