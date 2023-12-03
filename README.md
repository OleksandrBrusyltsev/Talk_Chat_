# Talk Chat: Real-time Chat Web Application
## Introduction
#### **Talk Chat is a web application developed using the Django rest framework, enabling users to communicate in real-time. Utilizing WebSockets(Django Channels), messages are sent and received instantly.**

### API Documentation
**API documentation is available on the local server or online at [Talk Chat API Docs](https://talk-chat6.onrender.com/api/docs/). Please note that the first request on Render may take longer than usual, so the site may load slower if this is your first visit.**

## Chat Functionality Testing

**You can test the chat functionality on the frontend at [Chat Talk Frontend](https://valerka4052.github.io/chat-talk-front/).**

![chat](https://github.com/OleksandrBrusyltsev/LMS_django/assets/124603897/08e5a5b8-2f7b-4b24-ae69-6bce03bf604f)
![chat](https://user-images.githubusercontent.com/124603897/271301967-952712bd-27c2-432c-a41a-4cafda56576a.jpg)
![chat](https://user-images.githubusercontent.com/124603897/271301964-bd16d6bd-ebf4-4cc4-8b0e-61199e4df4fd.jpg)
![chat](https://user-images.githubusercontent.com/124603897/271301950-fa4763c1-ab6e-40ab-ae2d-c0edce355a7b.jpg)
![docs](https://github.com/OleksandrBrusyltsev/LMS_django/assets/124603897/24505934-c7ab-4dcb-a800-5101645a1b08)
# Key Features
## Authentication
+ User Registration with data validation.
+ User Login with credential verification.
+ Channels and Chats
+ Channel Creation for group conversations.
+ Channel Selection for communication.
+ Instant Text Messaging.
+ User Profile
+ Personal Information Editing.
+ Avatar Change.
+ Installation and Setup
+ Prerequisites
+ Install your own database.
+ Install your own Redis server.
+ Clone the Repository

~~~python
 git clone https://github.com/OleksandrBrusyltsev/Talk_Chat_.git
  ~~~
### + Navigate to Project Directory



~~~python
cd Talk_Chat_
~~~

### Install Dependencies

~~~python
pip install -r requirements.txt
~~~
### Run Database Migrations

~~~python
python manage.py migrate
~~~
Start the Server
~~~python
python manage.py runserver
~~~

After this, the web application will be accessible at http://127.0.0.1:8000/.

#


