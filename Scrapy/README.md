# Scrapy源码剖析

#### Scrapy是个简单好用的爬虫框架，她很容易调教，充分高效发挥scrapy的作用吧


#### Scrapy运行原理是怎么样的呢？

##### scrapy是如何运行的(架构级别理解)？

![image](https://user-images.githubusercontent.com/8281035/49266275-5eef2900-f490-11e8-9715-f6d5417d4f4b.png)

    1.命令行运行scrapy crawl xxxx， spider start
    
    2.spider拿到url之后，生成request对象,然后yield request，引擎此时监控spider的输出，
    发现是request对象后，放入到request scheduler队列中
    
    3.引擎发现scheduler中有request之后，pop request from scheduler
    
    4.引擎拿着request send to downloader(request 要经过各种download middleware)，下载器拿到request之后，然后请求url，
    获取返回的response，下载器send response to engine(response 要经过各种download middleware)
    
    5.引擎拿到response之后，发送给spider中的某个函数(此时response要经过各种spider middlerware)，
    然后处理response(re/xpath/css)等等之类的操作。
    
    6.此时spider 获取到新的数据(字典或者item)或者request，send to engine
    
    7.engine会判断spider返回的是数据还是request，当发现是数据之后，把数据发送给item pipelines，若发现为request，则
    send request to scheduler
    
    8.item pipelines 拿到数据之后，进行一系列的清洗入库操作或者send request to engine
    

##### scrapy是如何运行的(源码级别理解)?

first.md