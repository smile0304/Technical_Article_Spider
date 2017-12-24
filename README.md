# Technical_Article_Spider

#### 一个爬取国内技术站点的技术文章

为了方便之后的搜索引擎搭建,改用`elasticsearch`

开发环境:

- python3


- Scrapy ==1.4.0
- elasticsearch-rtf
- docker

#### 最新版本安装

- Linux安装

> sudo apt-get install python3-pip git xvfb
>
> sudo pip3 install scrapy mysqlclient scrapy-splash fake-useragent
>
> git clone https://github.com/medcl/elasticsearch-rtf.git
>
> git clone https://github.com/smile0304/Technical_Article_Spider.git

- Windows安装

>pip install scrapy pillow mysqlclient scrapy-splash pypiwin32 fake-useragent
>
>git clone https://github.com/smile0304/Technical_Article_Spider.git
>
>git clone https://github.com/medcl/elasticsearch-rtf.git

`windows`和`linux`相同操作

需要下载安装[`docker`](https://www.docker.com/community-edition)

- 配置docker国内镜像

  > Linux下配置：
  >
  > ​	curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://7db66207.m.daocloud.io
  >
  > Windows下右键setting -> Daemon -> Registry mirrors 添加
  >
  > http://7db66207.m.daocloud.io

- 拉取镜像

  > docker pull scrapinghub/splash

- 用docker运行`scapinghub/splash`服务

  > docker run -p 8050:8050 scrapinghub/splash

#### 还可以修改的一些配置

```python
AUTOTHROTTLE_ENABLED   #设置是否延迟

AUTOTHROTTLE_START_DELAY = 2	#请求的延时(需要AUTOTHROTTLE_ENABLED=True)

AUTOTHROTTLE_MAX_DELAY = 60   #如果网络差的最大等待时长(需要AUTOTHROTTLE_ENABLED=True)

IMAGES_STORE = os.path.join(project_dir, 'images')	#images为图片的默认存放地址

```

#### PS：

​	已突破安全客反爬虫机制，搜索引擎搭建，请移步至[Article_Search](https://github.com/smile0304/Article_Search)

#### 更新日志

- 2017年12月25日
  - 突破安全客反爬机制
  - 弃用`selenium`
  - 增加爬取`freebuf`的数据


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