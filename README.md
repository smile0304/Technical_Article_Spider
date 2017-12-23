# Technical_Article_Spider

#### 一个爬取国内技术站点的技术文章

为了方便之后的搜索引擎搭建,改用`elasticsearch`

开发环境:

- python3


- Scrapy ==1.4.0
- elasticsearch-rtf

#### 最新版本安装

- Linux安装

> sudo apt-get install python3-pip git xvfb
>
> sudo pip3 install scrapy mysqlclient selenium fake-useragent
>
> git clone https://github.com/medcl/elasticsearch-rtf.git
>
> git clone https://github.com/smile0304/Technical_Article_Spider.git

- Windows安装

>pip install scrapy pillow mysqlclient selenium pypiwin32 fake-useragent
>
>git clone https://github.com/smile0304/Technical_Article_Spider.git
>
>git clone https://github.com/medcl/elasticsearch-rtf.git

配置ChromeDriver路径

> vim Technical_Artical_Spider/Technical_Artical_Spider/settings.py
>
> """修改
>
> EXECUTABLE_PATH="配置google Driver路径信息"

[ChromeDriver下载地址](http://chromedriver.storage.googleapis.com/index.html?path=2.7/)(自备梯子)


#### 还可以修改的一些配置

```python
AUTOTHROTTLE_ENABLED   #设置是否延迟

AUTOTHROTTLE_START_DELAY = 2	#请求的延时(需要AUTOTHROTTLE_ENABLED=True)

AUTOTHROTTLE_MAX_DELAY = 60   #如果网络差的最大等待时长(需要AUTOTHROTTLE_ENABLED=True)

IMAGES_STORE = os.path.join(project_dir, 'images')	#images为图片的默认存放地址

EXECUTABLE_PATH="配置ChromeDriver路径信息"
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

#### PS：

​	在这个版本更新上来之前发现安全客增加了反爬机制，如果有时间去反~~，还有就是爬`freebuf`的爬虫暂时停一下再写，因为最近一阵子有其他的事情做，搜索引擎的搭建代码也写的差不多了，基于`flask`开发，如果你想要看看源代码，请移步至[Article_Search](https://github.com/smile0304/Article_Search)

#### 更新日志

- 2017年12月23日
  - 增加任意`User-Agent`


- 2017年12月18日
  - 数据分库
  - 设置浏览器为无界面


- 2017年12月15日
  - 弃用`Mysql`保存数据库
  - 使用`elasticsearch`保存数据


- 2017年12月8日更新
  - 对安全客进行爬去

  - 完成图片的分类

  - 优化代码性能,降低冗余性

- 2017年12月5日首次提交
  - 当前版本仅对嘶吼的文章进行爬取