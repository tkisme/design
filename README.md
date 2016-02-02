# 车位

### 如何反馈

1. 确保你现在的版本是最新的

切换你的项目目录下,比如我的就是D:/flask,并且执行以下命令

注:以下命令仅适用于powershell,并且请[点击此处](https://git-for-windows.github.io/)安装git
```
cd D:\flask
git pull
pip install -r requirements.txt
python runserver.py
```
2. 确保自己的反馈不重复,对于同样的错误一个方案就可以解决

3. 问题依旧存在的情况下,请详细说明问题怎么出现的,最好能够把出现错误时,终端的输出也一并提交

### 如何安装

1. clone this repo
```
git clone http://git.heyweteam.com/kevin/flask.git
```

2. install all the necessary packages (best done inside of a virtual environment)
```
virtualenv venv
venv/bin/activate
pip install -r requirements.txt
bower install
```

3. deploy database
if use mysql
```
create database heyweteam default charset utf8;
delete from user where user='team';
GRANT ALL PRIVILEGES ON heyweteam.* TO team@localhost IDENTIFIED BY 'heywe' WITH GRANT OPTION;
flush privileges;
```
4. 通用步骤
```
python manage.py db init
python manage.py db migrate
python manage.py deploy
```
5. run the app
```
gunicorn -c gunicorn.ini manage:app
```
6. check it out
```
http://localhost:5002/
```

7. if you already have a venv in another place
```
ln -s  /Users/tk/myApp/data/flasky/venv  /Users/tk/MEGAsync/cloud/gitbucket/flask-angular/venv
```
8. init user to use
```
user=User(username='tkisrainy',password='123',mobile='13917482629')
db.session.add(user)
db.session.commit()
```