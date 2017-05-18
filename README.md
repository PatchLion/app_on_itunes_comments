
拉取App Store上的评论，并且发送邮件通知最新评论
======

实现的功能
-----------

- 定时拉取指定App的评论（多国家地区） √
- 增量保存到本地数据库 √
- 自动发送最新评论到指定邮箱 √
- 可配置哪些邮箱接收哪些App的评论 √
- 持续的优化，使代码更Pythonic...

**已知需要优化的问题**
- 网页模板需要更优化更美观
- ~~json数据不包含评论日期(xml格式中没有评论星数，所以用json)，还需要从xml格式中解析出日期数据并保存~~ 使用xml解析 √
- ~~需要设为后台运行?~~
- 安装和部署代码



~~**特殊文件说明**~~
- ~~需复制email_bk.config并更名为 email.config， 该文件配置了email的发送需要的账号和服务器,以及哪些邮箱监听哪些App的配置
- itunes.config 的说明
  areas： 要拉取哪些地区的评论
  appids: 拉取的App的ID（可在itunes的App管理后台查看ID）
  delay：爬取活动的时间间隔(单位:小时)
- email_template.html： 最终生成评论的html模板
- row_template.html: 单个评论的html模板~~

2017/5/18 Update
**使用到的库(包)**
- rq / [rq-win](https://github.com/michaelbrooks/rq-win)
- apscheduler
- scrapy
- redis
- BeautifulSoup

**怎么使用**
```bash
$ python myworker.py
```
```bash
$ python taskproducer.py
```
