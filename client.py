from socket import *

serverName = gethostname() # server
print(serverName)
serverPort = 80 # HTTP
clientSocket = socket(AF_INET, SOCK_STREAM) # client 소켓 생성

clientSocket.connect((serverName, serverPort)) # 
print('server 접속')

clientSocket.send('who is nerdy'.encode())
print('send message')
data = clientSocket.recv(1024) # server name, port에 접근할 필요 없음 -> socket 사용
print('From Server:', data.decode()) # write reply
clientSocket.close()
print('종료')