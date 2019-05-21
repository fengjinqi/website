# website
**django 开发的web项目**

Python>=3.6

Django>=2.0.8


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
(待续。。。采用React开发)

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

[AppKey] #此key是聚合数据的，若想使用其它的需要去apps/article/tasks文件中getApi方法修改地址

key = xxx
```
定时任务：需配置Appkey

Celery -A website worker -l info

Celery -A website beat -l info

#(ps:项目还在开发中，若有更好的建议或者功能请联系我qq:1218525402,邮箱：fengjinqi@fengjinqi.com)
