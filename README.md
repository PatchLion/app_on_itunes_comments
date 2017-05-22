
  拉取App Store上的评论，并且发送邮件通知最新评论
======

  实现的功能
-----------

- 定时拉取指定App的评论（多国家地区） √
- 增量保存到本地数据库 √
- 自动发送最新评论到指定邮箱 √
- 可配置哪些邮箱接收哪些App的评论 √
- 翻译非中文地区评论为中文  √
- 持续的优化，使代码更Pythonic...

已知需要优化的问题
-----------
- 网页模板需要更优化更美观
- ~~json数据不包含评论日期(xml格式中没有评论星数，所以用json)，还需要从xml格式中解析出日期数据并保存~~ 使用xml解析 √
- ~~需要设为后台运行?~~
- 安装和部署代码



特殊文件说明
-----------
- 需复制email_bk.config并更名为 email.config， 该文件配置了email的发送需要的账号和服务器,以及哪些邮箱监听哪些App的配置
- setting.py 的说明

  UPDATE_COMMENTS_INTERVAL: 评论拉取周期（秒）
  
  NEW_ITEMS_CHECK_INTERVAL: 新评论检查并发送文件周期（秒）
  
  TRANSLATE_CHECK_INTERVAL： 翻译任务周期（秒）
  
  ITUNES_AREAS： 拉取哪些地区的评论
  
  ITUNES_APPIDS： 拉取哪些App的评论

  MAIL_FROM： 邮件发件地址
  
  MAIL_HOST: 发件服务器
  
  MAIL_PORT: 发件服务器端口
  
  MAIL_USER： 邮箱账户
  
  MAIL_PASS： 邮箱密码
  
  
  
  
使用到的库(包)
-----------
- rq / [rq-win](https://github.com/michaelbrooks/rq-win)
- apscheduler
- scrapy
- redis
- BeautifulSoup
- [googletrans](https://github.com/ssut/py-googletrans)


怎么使用
-----------
```bash
创建数据库及表(如果没有): $ python db_tables_creator.py
```
```bash
启动任务调度: $ python myworker.py
```
```bash
启动任务生产者(定时循环):$ python taskproducer.py
```
