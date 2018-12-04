###### 1.我们打开setup.py发现scrapy 启动函数是 cmdline.py下的execute方法

<img width="1317" alt="main" src="https://user-images.githubusercontent.com/8281035/49266403-108e5a00-f491-11e8-856d-faee4014939e.png">

###### 2.cmdline.py文件中execute函数，该函数运行轨迹如下:

    a.接收sys.argv参数
    b.读取scrapy.conf文件,获取项目settings.py配置文件(若是未找到项目下的settings.py文件，则默认所有的setting为default)
    c.根据settings.py文件相关设置，解析相关配置
    d.解析settings之后，初始化CrawlerProcess(爬虫进程类)
    e.执行crawl.py中的run方法
    
![image](https://user-images.githubusercontent.com/8281035/49267196-4123c300-f494-11e8-9ef1-3b9ccfa0b014.png)

![image](https://user-images.githubusercontent.com/8281035/49267171-1e91aa00-f494-11e8-988f-f1164b2e9b22.png)

![image](https://user-images.githubusercontent.com/8281035/49267244-70d2cb00-f494-11e8-8a33-37d53c179583.png)

###### 3.crawl.py文件中run函数，该函数运行轨迹如下:

    a.解析参数，获取要运行的爬虫名称或者爬虫类
    b.crawl方法首先创建Crawler类，若发现参数是Crawler类，直接返回，参数若是字符串(spidername),则
    根据配置文件查找加载与spidername相对的Spider类，然后初始化CrawlerProcess(爬虫进程类)
    c.运行Crawler类的crawl方法，创建spider类，然后创建引擎engine(此时加载spider middleware 以及 ITEM_PROCESSOR，
    加载download middleware 以及 初始化scheduler类)
    d.获取spider中的start_request函数中的相关request,执行engine中 open_spider方法
    e.open_spider函数中，spider middleware open_spider(绑定spider)，scheduler类open_spider(绑定spider)，
    scraper类open_spider(绑定spider)， stats类open_spider(绑定spider)，single绑定spider
    f.设置slot类的心跳间隔以及运行_next_request方法(Slot类设置了task.LoopingCall，间隔5秒会运行引擎中self._next_request方法)
    g.启动引擎

![image](https://user-images.githubusercontent.com/8281035/49367751-e4403b00-f727-11e8-807d-28d71191ffed.png)

![image](https://user-images.githubusercontent.com/8281035/49367792-00dc7300-f728-11e8-994a-ca8cfce64b40.png)

![image](https://user-images.githubusercontent.com/8281035/49369534-9d087900-f72c-11e8-8e18-02af4d6c079b.png)

![image](https://user-images.githubusercontent.com/8281035/49369569-b5789380-f72c-11e8-8922-316934bbf6f3.png)

![image](https://user-images.githubusercontent.com/8281035/49369596-cb865400-f72c-11e8-9b3e-1b5f6270c714.png)

![image](https://user-images.githubusercontent.com/8281035/49370000-d5f51d80-f72d-11e8-8b22-8785ba2a8456.png)

![image](https://user-images.githubusercontent.com/8281035/49370060-0b9a0680-f72e-11e8-9446-71943441a8cb.png)
    