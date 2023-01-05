from socket import *

serverName = '127.0.0.1' # server
serverPort = 1230 # port number

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM) # SOCK_STREAM으로 TCP 방식의 client socket 생성
    clientSocket.connect((serverName, serverPort)) # (IP, port) 서버 연결
    print('********server 연결********')

    message = input('Request>> ') # 사용자로부터 request 입력 받기
    message = message.split()

    if message[0] == 'GET' or message[0] == 'HEAD' or message[0] == 'POST':
        request = message[0] + ' '
        if len(message) > 1:
            request += ' '.join(message[1:])
        request += ' / HTTP/1.0\n' \
                 + 'HOST: ' + serverName + '\n' \
                 + 'Accept-Language: en-us\n'
    else:
        request = " ".join(message)

    # request 형태
    # GET test.html * \ HTTP/1.0
    # HOST: 127.0.0.1
    clientSocket.send(request.encode()) # socket으로 request 보내기

    response = clientSocket.recv(1024).decode() # server name, port에 접근할 필요 없음 -> socket 사용
    print(response)
    clientSocket.close()
    print('***********close***********')