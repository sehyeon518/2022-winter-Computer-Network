# 2022-winter-Computer-Network
2022학년도 겨울학기 컴퓨터네트워크 과제 \
Socket 통신을 활용한 HTTP server, client 프로그램
* [client](#clientpy) 코드 설명
* [server](#serverpy) 코드 설명
* [동작환경](#동작-환경)
    - [서버 대기](#서버-대기)
    - [연결 완료](#연결-완료)
    - [실행 전 파일 목록](#실행-전-파일-목록)
* [HTTP 명령어 결과](#http-명령어-결과) 
    - [GET](#get)
    - [POST](#post)
    - [HEAD](#head)
    - [PUT](#put)
    - [기타](#기타)
## client.py
server에 request 문자열을 보내고 response를 받아 출력한다.
<details>
<summary> 코드 설명 </summary>

server port 번호는 임의로 1230으로, server name은 local '127.0.0.1'로 설정한다. server port 번호는 server.py에서도 동일하게 설정한다.

TCP 기반 HTTP 구현을 위해서 연결과 해제를 반복하기 위해 while loop을 사용한다. 1회 반복 때마다 connect와 close를 수행한다. 모든 요청마다 '*' 기호와 'server 연결', 'close' 문자열을 사용하여 각 요청의 연결과 연결 종료를 구분한다. 사용자로부터 입력받은 request는 ['GET', 'test.html'] 같은 형태의 list로 분할하여 저장한다.

입력받은 request list의 0번 원소 즉 request method가 ‘GET’, ‘HEAD’, ‘POST’, ‘PUT’인 경우 요청할 data를 입력하였다면(하단 code line 1) http 버전, host 정보, accept, connection 정보 등을 포함하여 request message를 완성한다. -1을 입력받은 경우에는 server에 -1을 그대로 전달하고 즉시 connection을 종료하여 ‘close’를 출력한 뒤 반복을 마치는 것으로 설정하였다.

Request message는 request line, host, accept, connection, content 정보를 포함한다. Request line은 어떠한 method(GET, POST, HEAD, PUT)로 어떠한 방식(HTTP/1.0)으로 어떠한 파일을 요청하였는지 담는다.

Host는 요청하려는 server port 번호를 나타낸다. Accept는 client가 처리 가능한 미디어 타입의 종류를 나열한다. Accept-language는 client가 지원 가능한 언어를 나타낸다. 본 실행파일에서는 html 파일, 영어만으로 test하므로 accept는 표면적인 정보이다. Connection은 client와 server의 연결 방식을 나타낸다. 본 실행에서는 모든 request마다 연결과 종료를 반복하므로 HTTP/1.0 close이다. Content-type은 본문의 미디어 타입을 나타낸다.

Request message의 형태는 다음과 같다.

<span style="color:#808080">GET test.html / HTTP/1.0 \
HOST: 127.0.0.1 \
Accept: text/html \
Accept-Language: en-US \
Connection: keep-alive -> HTTP/1.1 본 파일에서는 close \
Content-Type: multipart/form-data; boundary=-1265974 </span>

정의되어 있는 method인 GET, HEAD, POST, PUT을 요청받은 경우에는 유효성을 판단하지 않고 request message를 만든다. 정의되어 있지 않은 method를 요청받은 경우에는 입력 message를 그대로 server로 보낸다. 요청의 유효성은 server에서 판단하여 ‘400 Bad Request’나 ‘404 Not Found’로 응답을 받는다.

완성된 request message(실행 파일의 변수 request)를 encode하여 socket 모듈 send 함수를 통해 전달한다.

server로부터 response를 받아 출력하고 연결을 종료한다.
</details>

## server.py
client로부터 받은 request를 출력하고 response를 보낸다.
<details>
<summary> 코드 설명 </summary>

Socket을 주고받기 위해서 socket의 모든 field를 import 한다. client로부터 요청받은 파일이 장치에 존재하는지 확인하기 위해 os를 import하고, header에 요청받은 시간인 Date를 기록하기 위해 time을 import한다.

Server port 번호는 임의의 숫자 1230으로 설정한다. SOCK_STREAM으로 TCP 방식의 socket을 생성한다. 동시에 연결 가능한 socket을 0으로 두어 자동으로 연결하도록 설정한다.

while loop을 통해 사용자가 직접 연결을 끊기 전까지 client와 server의 연결과 해제를 반복적으로 수행한다.

Client가 요청한 파일이 존재하는지 판단하기 위해 os를 사용한다. 실행 파일이 위치한 directory 내의 파일들을 files라는 list에 담는다. Header의 항목 중 ‘Date’에 요청한 시간을 구하기 위해 time을 사용한다. 현재 시간을 문자열로 변환하여 date 변수에 담는다.

Client 요청을 받을 때마다 파일 목록과 시간을 갱신해야하므로 files와 date 변수는 반복할 때마다 초기화한다. 예를 들어 POST new.html을 생성하면 바로 다음 요청에서 new.html에 대해 HEAD, GET 등의 요청을 하더라도 정상적으로 응답할 수 있다.

Date는 ‘01 Jan 2023 00:00:00 KST’ 형태이다.

Files는 [‘sample.txt’, ‘example.html’, ‘test.html’, ‘server.py’, ‘client.py’]와 같이 directory 내의 모든 파일을 인자로 두는 list 형태이다.

Client 접속을 대기한다. accept()가 수행되면 connection setup이 완료되고 message를 읽어 해독하고 출력한다. message는 공백을 기준으로 나누어 [‘GET’, ‘test.html’, ‘HTTP/1.0’, …]과 같은 list 형태로 request 변수에 담고 입력받은 method 즉 request 0번째 원소에 맞는 코드를 실행한다.

Response message는 HTTP version, status code, date, connection, content 정보를 담는다. Date는 요청을 받은 순간의 시간을 time method를 사용하여 구한다. Connection은 client와 마찬가지로 close이다. Content-Type은 client와 마찬가지로 본문의 미디어 타입을 나타낸다. Content-Length는 본문의 길이를 나타낸다. 본 실행파일에서는 GET, HEAD 요청을 정상적으로 받은 경우에만 body의 길이를 반환한다. Vary는 동일한 URL에서 사용자 agent에 따라 다른 응답을 내릴 때 필요한 것이므로 본 실행에서는 표면적인 정보이다.

Response message의 형태는 다음과 같다.

<span style="color:#808080">HTTP/1.0 200 OK \
Date: Wed, 10 Aug 2016 09:23:25 GMT \
Connection: close \
Content-Type: text/html; charset=iso-8859-1 \
Content-Length: 220 -> 선택사항 \
Vary: User-Agent, Accept-Encoding</span>

Response message는 response라는 변수에 string 형태로 담는다. 모든 요청마다 연결과 해제를 반복하므로 HTTP version은 1.0이다. 따라서 connection 정보는 ‘close’이다.

-1을 입력받은 경우 즉시 연결을 끊고 종료한다.

HEAD method를 통해 정상적인 파일을 요청받은 경우 response status는 ‘200 OK’이고 response message는 연결 형태, body의 길이 등을 포함하며 body 내용은 포함하지 않는다. Header의 content length 정보에 파일 길이를 출력하기 위해서 요청받은 파일을 읽기 모드로 열고 len() 함수를 사용한다.

존재하지 않은 파일을 요청받은 경우 ‘404 Not Found’ status code와 date, connection, content-type 정보를 반환한다.

GET method는 요청한 파일의 내용을 모두 가져온다. 존재하는 파일을 정상적으로 요청한 경우 ‘200 OK’, 응답이 불가능한 경우 ‘404 Not Found’를 반환한다.

‘200 OK’의 경우 header에 date, connection, content 정보를 포함한다. 또한 요청받은 파일을 읽기 모드로 열어 body를 반환한다. ‘404 Not Found’의 경우 header에 date, connection, content 정보를 포함한다.

POST method는 새로운 파일을 생성한다. 존재하지 않는 파일을 요청 받으므로 쓰기 모드로 파일을 열어 생성한다. 새로운 파일을 성공적으로 생성하면 ‘201 Created’, 이미 존재하는 파일을 요청한 경우에는 created가 아니므로 ‘200 OK’, 파일을 정상적으로 요청받지 않은 경우 ‘404 Not Found’를 반환한다.

PUT method를 입력받으면 존재하는 파일인지 확인하고 ‘200 OK’를 반환한다. PUT method는 file update를 수행하므로 존재하지 않는 파일을 요청받거나 요청이 정상적이지 않은 경우 ‘404 Not Found’를 반환한다.

‘200 OK’는 date, connection, content 정보와 body를 반환한다. Body는 요청받은 파일을 읽기모드로 open한 내용이다. ‘404 Not Found’는 date, connection, content type 정보를 포함하여 반환한다.

유효하지 않은 method는 client 측에서 그 유효성을 판단하지 않는다. 입력받은 request 그대로 server로 전달되기 때문에 유효성은 server에서 판단하여야 한다.

따라서 GET, HEAD, POST, PUT 이외에 실행이 불가능한 method를 요청받아 해석이 불가능한 경우 즉 request라는 이름의 list의 0번째 원소가 위의 method가 아닌 경우 모두 ‘400 Bad Request’를 반환한다.

‘400 Bad Request’는 요청한 시간 정보인 date만 header에 포함한다.

method 실행이 완료되면 response message를 암호화하여 socket 전송하고 연결을 종료한다.

‘close’ 문자열을 출력하여 다음 요청과 구분한다. Response message는 client 측에서 출력한다
</details>

## 동작 환경
1) 개발 언어 python 3.10.6

2) 실행 환경 Visual Studio Code 터미널

Local host에서 통신을 진행한다. client.py에서 설정한 server name은 ‘127.0.0.1’이며 사용한 port 번호는 ‘1230’이다.

다음 그림은 server가 client 접속을 기다리는 상태, 연결이 완료되어 request를 기다리는 상태이다.
### 서버 대기
![2서버대기](https://user-images.githubusercontent.com/84698896/211723538-029c58b2-7281-4ef6-894b-07f2efb275f3.png)
### 연결 완료
![3연결완료](https://user-images.githubusercontent.com/84698896/211723541-8171448a-f01f-45e4-8dfe-6d16e080d7c0.png)
모든 socket 통신은 문자열로만 이루어지며 HTTP header 형태를 따른다. 실제 header의 line 구분을 표현하기 위해서 ‘\r\n’ 문자를 사용한다.

프로그램의 정상적인 종료를 위해서 ‘-1’을 입력하는 경우를 따로 구현하였다. -1을 입력하면 즉시 모든 연결을 끊는다.

Request message는 server.py(우측 터미널) response message는 client.py(좌측 터미널)에서 출력된다.

모든 명령 실행 전 directory 내의 파일 목록이다.

### 실행 전 파일 목록
![1실행전파일목록](https://user-images.githubusercontent.com/84698896/211723534-e5521e06-3f96-4caf-a98f-6f01288f888b.png)

## HTTP 명령어 결과

### GET
200 OK, 404 Not Found
![GET](https://user-images.githubusercontent.com/84698896/212502739-657bfa41-36df-43ce-8120-de677794cd1f.png)
### POST
201 Created
![POST](https://user-images.githubusercontent.com/84698896/212502744-b862f579-26da-43c2-9e9c-733e4d696c99.png)

실행 후 파일 목록

![4실행후파일목록](https://user-images.githubusercontent.com/84698896/211723542-668485ca-8a77-47d9-b382-ed8217e69217.png)
### HEAD
200 OK, 404 Not Found
![HEAD](https://user-images.githubusercontent.com/84698896/212502741-be234a52-5aea-40ac-9183-e6228bda572c.png)
### PUT
200 Ok, 404 Not Found
![PUT](https://user-images.githubusercontent.com/84698896/212502745-17898490-6ac3-448f-a047-ead3c29e1d06.png)
### 기타
400 Bad Request
![NONE](https://user-images.githubusercontent.com/84698896/212502743-021d2de1-c055-4da2-b1c1-f5d43e28d01c.png)