# Technical_Article_Spider

#### 一个爬取国内技术站点的技术文章

为了方便之后的搜索引擎搭建,改用`elasticsearch`

开发环境:

- python3


- Scrapy ==1.4.0
- elasticsearch-rtf

#### 最新版本安装

- Linux安装

> sudo apt-get install python3-pip git
>
> sudo pip install scrapy mysqlclient selenium
>
> git clone https://github.com/medcl/elasticsearch-rtf.git
>
> git clone https://github.com/smile0304/Technical_Article_Spider.git

- Windows安装

>pip install scrapy PIL mysqlclient selenium
>
>git clone https://github.com/smile0304/Technical_Article_Spider.git
>
>git clone https://github.com/medcl/elasticsearch-rtf.git

#### 使用方法

> python3 Technical_Article_Spider/models/elsticsearch_type_4hou.py
>
> python3 Technical_Article_Spider/models/elsticsearch_type_anquanke.py
>
> cd Technical_Article_Spider
>
> scrapy crawl [ 4hou | anquanke360 ]

#### 如果你想要使用`Mysql`存储数据

- Linux下的安装

  > """ ubuntu下
  >
  > sudo apt-get install python3-pip libmysqlclient-dev
  >
  > """
  >
  > """centos下
  >
  > yum install python-devel mysql-devel python3-pip
  >
  > """
  >
  > sudo pip install scrapy mysqlclient selenium
  >
  > git clone https://github.com/smile0304/Technical_Article_Spider.git



- Windows下的安装

  > pip install scrapy PIL mysqlclient selenium
  >
  > git clone https://github.com/smile0304/Technical_Article_Spider.git

  ​

- 配置数据库:

  > vim Technical_Artical_Spider/Technical_Artical_Spider/settings.py

  ```python
  MYSQL_HOST = "127.0.0.1"
  MYSQL_DBNAME = "sql_dbname"
  MYSQL_USER = "root"
  MYSQL_PASSWORD = "password"
  ```

  修改数据库名为自己想要的，密码改自己的mysql密码

- 导入数据表结构:

  连接到数据库中后

  > use dbname
  >
  > source ~/Technical_Artical_Spider/4hou_Article-struct.sql



#### 还可以修改的一些配置

```python
AUTOTHROTTLE_ENABLED   #设置是否延迟

AUTOTHROTTLE_START_DELAY = 2	#请求的延时(需要AUTOTHROTTLE_ENABLED=True)

AUTOTHROTTLE_MAX_DELAY = 60   #如果网络差的最大等待时长(需要AUTOTHROTTLE_ENABLED=True)

IMAGES_STORE = os.path.join(project_dir, 'images')	#images为图片的默认存放地址

EXECUTABLE_PATH="路径信息"
```



#### 数据

- 2017年12月8日抓取的数据

  > 链接：https://pan.baidu.com/s/1miOjuRI 密码：7ucx


- 2017年12月5日爬去的第一份数据

  > 链接：https://pan.baidu.com/s/1jI3U6Y6 密码：i9fc

  ​

  导入数据

  > source ~/4hou_Article.sql

  如果你想要修改图片的路径信息可以使用如下`sql`语句

  > update 4hou_Article set image_local = REPLACE(image_local,'full','图片地址')

#### 更新日志

- 2017年12月15日
  - 弃用`Mysql`保存数据库
  - 使用`elasticsearch`保存数据


- 2017年12月8日更新
  - 对安全客进行爬去

  - 完成图片的分类

  - 优化代码性能,降低冗余性

    ​
- 2017年12月5日首次提交
  - 当前版本仅对嘶吼的文章进行爬取