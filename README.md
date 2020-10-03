# v1.0

Suitable for beginners and novices, adopt djangorestframework interface development and template function development, mainly for novices to practice and consolidate
There are knowledge points, which leads to bloated code. The next version is refactored to a simple version, and the version is also upgraded. Use django3 version, adopt redis cache, etc., websocket chat and other next versions are all developed in interface mode


﻿# website
**django web project developed**
(I like the trouble to move your little hand to start, thank you)

Python>=3.6

Django>=2.0.12


celery>=3.1.25

coreschema>=0.0.4

django-appconf>=1.0.3

django-celery>=3.2.2

django-filter>=2.0.0

django-haystack>=2.8.1

django-pure-pagination>=0.3.0

django-ranged-response==0.2.0

django-shortuuidfield>=0.1.3

django-simple-captcha>=0.5.9

djangorestframework>=3.9.1

redis>=2.10.6



Features：

**V1:**

1、Multi-user registration currently uses QQ quick login and email registration login to send verification token valid for 60 minutes.

2、Include user attention, view articles I follow, view users, etc.

3、The article contains comments, message tips.
4、The tutorial module is used to recruit authors, you can go to the background admin system to publish tutorials.
5、Mail is sent asynchronously by Celery.
6、Have a timed task Use Celery redis as a message queue to collect data every 30 minutes, and process the database in a week. If there is an error, the administrator will be notified by email in time.

7，Community function.
# admin
Currently in another project, please move to https://github.com/fengjinqi/website-admin. Follow-up completion will be packaged and configured to this project.

Use vue iview-admin template development, interface with drf, the author has the ability to publish articles in admin, of course, can also publish in the foreground, and has the function of publishing tutorials
Login using JWT method.

# Mobile
The project has started development, using react development,

**Architecture**

react, react-router-dom, redux, react-redux, redux-thunk, antd-mobile, project address: https://github.com/fengjinqi/website-react-webapp.
# Instructions

1. Download python3 and install

2. Enter the project root directory pip3 install requirements.txt in the virtual environment

3. Install redis and start it

4. Settings for various configurations such as database

5. Create a password configuration file such as congfig.ini in the project root directory and fill in it.
```cython

[email]

password = xxx

[QQ]

client_id = xxx

key = xxx

[AppKey] #此key是聚合数据的，若想使用其它的需要去apps/article/tasks文件中getApi方法修改地址并且修改getApi方法中对应的获取字段

key = xxx
```
# 6、***Because the sender field is currently required in the message table, create a super administrator account before registering a new user***

#7, **Because I have configured seo locally, an error may be reported during the first visit because seo is not configured**

The sqlite database currently used in the test environment, if you use other databases, please modify the settings yourself

Please migrate before running

Timed tasks: Appkey needs to be configured
Celery -A website worker -l info

Celery -A website beat -l info

supervisord -c conf/supervisord.conf

pip installation supervisord
pip install supervisor



Generate configuration file
echo_supervisord_conf > /etc/supervisord.conf



Start：supervisord -c /etc/supervisord.conf


Shut down：supervisorctl shutdown



service mysqld start
[Process Management]

1. Start all processes managed by supervisord

supervisorctl start all

2.Stop all processes managed by supervisord

supervisorctl stop all

3. Start a specific process managed by supervisord

supervisorctl start program-name // program-name is xx in [program:xx]

4. Stop a specific process managed by supervisord

supervisorctl stop program-name // program-name is xx in [program:xx]

5. Restart all processes or all processes

supervisorctl restart all // restart all

supervisorctl reatart program-name // Restart a process, program-name is xx in [program:xx]

6. View the status of all processes currently managed by supervisord

supervisorctl status

[Encountered problems and solutions]

When using the command supervisorctl start all to start the control process, the following error is encountered

unix:///tmp/supervisor.sock no such file

The reason for the above error is that supervisord has not been started. Just use the command sudo supervisord to start supervisord on the command line.


ps aux | grep redis-server

./bin/redis-server /usr/local/redis/etc/redis.conf

#(ps: If you have better suggestions or features, please contact me qq:1218525402, email: fengjinqi@fengjinqi.com)
