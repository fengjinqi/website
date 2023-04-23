# IT学习交流群:284049121

# v1.0

适合初学者新手，采取djangorestframework接口开发以及模版功能开发，主要用于新手练手巩固
知识点都有所以导致代码臃肿，下一版本重构简约版，版本也升级 使用django3版本，采取redis缓存等，websocket聊天等下一版本全部采取接口方式开发
Suitable for beginners and novices, adopt djangorestframework interface development and template function development, mainly used for novices to practice and consolidate knowledge points, which leads to bloated code. The next version is refactored to the simple version, and the version is also upgraded to use django3 version, adopt redis cache, etc., websocket The next version such as chat is all developed by interface.

﻿# website
**django 开发的web项目**

(喜欢麻烦动动你的小手给个start 谢谢,关于后台登录不成功的问题：请使用邮箱登录)

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



功能：

**V1:**

1、多用户注册 目前采用QQ快捷登录以及邮箱注册登录发送验证token 60分钟有效

2、包含用户关注，查看我关注的文章，查看用户等

3、文章包含评论，消息提示

4、教程模块用于招募作者，可以去后台admin系统进行发布教程

5、邮件采用Celery异步发送

6、拥有定时任务 采用Celery redis用做消息队列进行每30分钟采取一次数据，一周进行数据库处理,若出错会及时给管理员发邮件通知

7，社区功能

# admin
目前在另外一个项目里，请移步https://github.com/fengjinqi/website-admin 后续完成会打包配置到本项目

采用 vue iview-admin模板开发 ，接口用drf, 作者拥有可以在admin发布文章，当然也可以在前台发布，同时拥有发布教程的功能
登录采用JWT方式登录


# 移动端
项目已启动开发，采用react开发，

**架构**

react、react-router-dom、redux、react-redux、redux-thunk，antd-mobile，项目地址：https://github.com/fengjinqi/website-react-webapp

# 使用方法

1、下载python3安装

2、在虚拟环境下进入项目根目录 pip3 install requirements.txt

3、安装redis 并进行启动

4、settings进行数据库等各种配置

5、项目根目录下创建 congfig.ini 邮箱等密码配置文件 并填写
```cython

[email]

password = xxx

[QQ]

client_id = xxx

key = xxx

[AppKey] #此key是聚合数据的，若想使用其它的需要去apps/article/tasks文件中getApi方法修改地址并且修改getApi方法中对应的获取字段

key = xxx
```
# 6、***因目前消息表需要发送人字段，所有先创建一个超级管理员账号再注册新用户***

#7、 **因我本地配置了seo，初次访问可能会报错，原因是未配置seo**

目前测试环境用的sqlite数据库，若用其他数据库请自行setting配置修改

运行前请先migrate

定时任务：需配置Appkey

Celery -A website worker -l info

Celery -A website beat -l info

supervisord -c conf/supervisord.conf

pip安装supervisord
pip install supervisor



生成配置文件
echo_supervisord_conf > /etc/supervisord.conf



启动：supervisord -c /etc/supervisord.conf


关闭：supervisorctl shutdown



service mysqld start
【进程管理】

1. 启动supervisord管理的所有进程

supervisorctl start all

2. 停止supervisord管理的所有进程

supervisorctl stop all

3. 启动supervisord管理的某一个特定进程

supervisorctl start program-name // program-name为[program:xx]中的xx

4.  停止supervisord管理的某一个特定进程 

supervisorctl stop program-name  // program-name为[program:xx]中的xx

5.  重启所有进程或所有进程

supervisorctl restart all  // 重启所有

supervisorctl reatart program-name // 重启某一进程，program-name为[program:xx]中的xx

6. 查看supervisord当前管理的所有进程的状态

supervisorctl status

【遇到问题及解决方案】

在使用命令supervisorctl start all启动控制进程时，遇到如下错误

unix:///tmp/supervisor.sock no such file

出现上述错误的原因是supervisord并未启动，只要在命令行中使用命令sudo supervisord启动supervisord即可。


ps aux | grep redis-server

./bin/redis-server /usr/local/redis/etc/redis.conf

#(ps:若有更好的建议或者功能请联系我qq:1218525402,邮箱：fengjinqi@fengjinqi.com)
