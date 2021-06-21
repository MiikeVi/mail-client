# mail-client
Mail client using sockets, SMTP and POP3 Protocols

## Run locally

~~~
pip install PyQt5

py main.py
~~~

## Use ui

Login window, need credentials:

![image](https://user-images.githubusercontent.com/59854430/122819340-5528ad80-d2a8-11eb-94cc-1bcaba087618.png)

Menu window:

![image](https://user-images.githubusercontent.com/59854430/122819388-65d92380-d2a8-11eb-98bd-7de4cc1f4204.png)

Send mail window:

- All fields are required
- It can be sent to multiple recipients, separating emails by ",".
  Example: test1@mail.com, test2@mail.com, test3@mail.com 

![image](https://user-images.githubusercontent.com/59854430/122819439-77bac680-d2a8-11eb-8cd9-0c8be15abc32.png)

Mailbox window:

- You need to enter the destination host 
- You can read or delete multiple emails by putting their respective ids separated by ",".
Example: 1, 4, 9 

![image](https://user-images.githubusercontent.com/59854430/122819737-d3854f80-d2a8-11eb-8083-aa6252aac5d9.png)

