# 2022-winter-Computer-Network
## client.py
server에 request 문자열을 보내고 response를 받아 출력한다.
## server.py
client로부터 받은 request를 출력하고 response를 보낸다.
## 동작 환경
Local host에서 통신을 진행하였다. client.py에서 설정한 server name은 '127.0.0.1'이며 사용한 port 번호는 '1230'이다.

모든 socket 통신은 문자열로만 이루어지며 HTTP header 형태를 따른다. 실제 header의 line 구분을 표현하기 위해서 '\r\n' 문자를 사용하였다.

프로그램의 정상적인 종료를 위해서 '-1'을 입력하는 경우를 따로 구현하였다. -1을 입력하면 즉시 모든 연결을 끊는다.

### 실행 전 파일 목록
![1실행전파일목록](https://user-images.githubusercontent.com/84698896/211723534-e5521e06-3f96-4caf-a98f-6f01288f888b.png)

## HTTP 명령어 결과
### 서버 대기
![2서버대기](https://user-images.githubusercontent.com/84698896/211723538-029c58b2-7281-4ef6-894b-07f2efb275f3.png)
### 연결 완료
![3연결완료](https://user-images.githubusercontent.com/84698896/211723541-8171448a-f01f-45e4-8dfe-6d16e080d7c0.png)
### GET
200 OK, 404 Not Found
### POST
201 Created\
실행 후 파일 목록
![4실행후파일목록](https://user-images.githubusercontent.com/84698896/211723542-668485ca-8a77-47d9-b382-ed8217e69217.png)
### HEAD
200 OK, 404 Not Found
### PUT
200 Ok, 404 Not Found
### 기타
400 Bad Request