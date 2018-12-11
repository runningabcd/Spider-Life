2018/12/04

今天线上的爬虫业务出了点小插曲，偶发现对方一个网站开始改变反爬措施了，sentry or email 都可以及时通知我们，
后来测试发现，该网站对部分ip反爬啊，所以换了几个proxy server，问题算是解决了

2018/12/05

经过测试发现昨天的部分问题发现强制headers referer，今天加了headers referer，成功率已经是O(log n)

2018/12/06

今天搞了下拼多多

2018/12/07

单机单进程几小时搞了拼多多几百万商品详细数据，包含成交量、sku等等，准备做数据分析

2018/12/10

继续更新，最近这几天一直在忙着分析拼多多的数据

拼多多各行业销量状况，有双单价12.8的情侣鞋，居然卖了370多万双，杂耍的

![image](https://user-images.githubusercontent.com/8281035/49719746-02aeb500-fc99-11e8-8e55-470aae2e9a4a.png)

当天各行业销量状况

![image](https://user-images.githubusercontent.com/8281035/49720891-dc3e4900-fc9b-11e8-9b01-27c897279b5b.png)

24h各行业销量状况

![image](https://user-images.githubusercontent.com/8281035/49720894-dea0a300-fc9b-11e8-862d-da57334c2ca0.png)

各行业销量前1万名商品成交额统计

![image](https://user-images.githubusercontent.com/8281035/49781811-0e5cb300-fd4f-11e8-9e35-04f754df7ab6.png)

各行业销量前1万名成交额统计

![image](https://user-images.githubusercontent.com/8281035/49781812-10bf0d00-fd4f-11e8-8b31-837aa8ee6eca.png)