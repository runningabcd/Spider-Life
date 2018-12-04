1.分享自己面试和群友面试的相关心得

### 群友某位爬虫小哥哥去36kr(36氪 鲸准) 面试的题目(据说是两道算法题)

### 1. a='201', b='102', a是19的三进制的字符串,b是11的三进制的字符串,要求:输入 a, b, 输出a+b和的三进制 比如 输入 a，b 输出'1010'

#### 面试官推荐做法 >>>>> 性能测试

![image](https://user-images.githubusercontent.com/8281035/49361985-5f99f080-f718-11e8-9c91-f934249d72e5.png)

#### 递归实现 >>>>> 性能测试

![image](https://user-images.githubusercontent.com/8281035/49362063-a851a980-f718-11e8-9565-edacad0f1352.png)


### 2.不使用内置函数int,输入a='201', b='102', a是19的三进制的字符串， b是11的三进制的字符串，输出30，要求：输入 a, b, 输出a的十进制与b的十进制之和


#### 面试官推荐做法dict >>>>> 性能测试

![image](https://user-images.githubusercontent.com/8281035/49360112-3165e200-f713-11e8-8633-7150451c32e9.png)

#### eval >>>>> 性能测试

![image](https://user-images.githubusercontent.com/8281035/49360203-75f17d80-f713-11e8-894f-a3ddbaddeb01.png)

#### ord >>>>> 性能测试

![image](https://user-images.githubusercontent.com/8281035/49360246-96b9d300-f713-11e8-8b29-ff9177385e35.png)

#### 嵌套for >>>>> 性能测试

![image](https://user-images.githubusercontent.com/8281035/49360292-b9e48280-f713-11e8-9213-adcfb2fe73be.png)