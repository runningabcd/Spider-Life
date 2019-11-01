~~~~
0x00 定义与成因

SSRF(Server-Side Request Forgery:服务器端请求伪造) 是一种由攻击者构造形成由服务端发起请求的一个安全漏洞。一般情况下，SSRF攻击的目标是从外网无法访问的内部系统。（正是因为它是由服务端发起的，所以它能够请求到与它相连而与外网隔离的内部系统）
SSRF 形成的原因大都是由于服务端提供了从其他服务器应用获取数据的功能且没有对目标地址做过滤与限制。比如从指定URL地址获取网页文本内容，加载指定地址的图片，下载等等。
注释：除了http/https等方式可以造成ssrf，类似tcp connect 方式也可以探测内网一些ip 的端口是否开发服务，只不过危害比较小而已。

0x01 可能出现的地方
1.社交分享功能：获取超链接的标题等内容进行显示
2.转码服务：通过URL地址把原地址的网页内容调优使其适合手机屏幕浏览
3.在线翻译：给网址翻译对应网页的内容
4.图片加载/下载：例如富文本编辑器中的点击下载图片到本地；通过URL地址加载或下载图片
5.图片/文章收藏功能：主要其会取URL地址中title以及文本的内容作为显示以求一个好的用具体验
6.云服务厂商：它会远程执行一些命令来判断网站是否存活等，所以如果可以捕获相应的信息，就可以进行ssrf测试
7.网站采集，网站抓取的地方：一些网站会针对你输入的url进行一些信息采集工作
8.数据库内置功能：数据库的比如mongodb的copyDatabase函数
9.邮件系统：比如接收邮件服务器地址
10.编码处理, 属性信息处理，文件处理：比如ffpmg，ImageMagick，docx，pdf，xml处理器等
11.未公开的api实现以及其他扩展调用URL的功能：可以利用google 语法加上这些关键字去寻找SSRF漏洞
一些的url中的关键字：share、wap、url、link、src、source、target、u、3g、display、sourceURl、imageURL、domain……
12.从远程服务器请求资源（upload from url 如discuz！；import & expost rss feed 如web blog；使用了xml引擎对象的地方 如wordpress xmlrpc.php）

0x02 漏洞验证

1.排除法：浏览器f12查看源代码看是否是在本地进行了请求
比如：该资源地址类型为 http://www.xxx.com/a.php?image=（地址）的就可能存在SSRF漏洞
2.dnslog等工具进行测试，看是否被访问
--可以在盲打后台用例中将当前准备请求的uri 和参数编码成base64，这样盲打后台解码后就知道是哪台机器哪个cgi触发的请求。
3.抓包分析发送的请求是不是由服务器的发送的，如果不是客户端发出的请求，则有可能是，接着找存在HTTP服务的内网地址
--从漏洞平台中的历史漏洞寻找泄漏的存在web应用内网地址
--通过二级域名暴力猜解工具模糊猜测内网地址
4.直接返回的Banner、title、content等信息
5.留意bool型SSRF

0x03 利用方式

1.让服务端去访问相应的网址
2.让服务端去访问自己所处内网的一些指纹文件来判断是否存在相应的cms
3.可以使用file、dict、gopher[11]、ftp协议进行请求访问相应的文件
4.攻击内网web应用（可以向内部任意主机的任意端口发送精心构造的数据包{payload}）
5.攻击内网应用程序（利用跨协议通信技术）
6.判断内网主机是否存活：方法是访问看是否有端口开放
7.DoS攻击（请求大文件，始终保持连接keep-alive always）

0x04 绕过小技巧

注：参考[8]会有更详细的绕过方式总结
1.http://baidu.com@www.baidu.com/与http://www.baidu.com/请求时是相同的
2.各种IP地址的进制转换
3.URL跳转绕过：http://www.hackersb.cn/redirect.php?url=http://192.168.0.1/
4.短网址绕过 http://t.cn/RwbLKDx
5.xip.io来绕过：http://xxx.192.168.0.1.xip.io/ == 192.168.0.1 (xxx 任意）
指向任意ip的域名：xip.io(37signals开发实现的定制DNS服务)
6.限制了子网段，可以加 :80 端口绕过。http://tieba.baidu.com/f/commit/share/openShareApi?url=http://10.42.7.78:80
7.探测内网域名，或者将自己的域名解析到内网ip
8.例如 http://10.153.138.81/ts.php , 修复时容易出现的获取host时以/分割来确定host，
但这样可以用 http://abc@10.153.138.81/ 绕过

0x05 漏洞示例

1.Wordpress3.5.1以下版本 xmlrpc.php pingback的缺陷与ssrf
2.discuz！的ssrf （利用php的header函数来绕过，其实就是302跳转实现协议转换）
3.weblogic的ssrf

0x06 漏洞修复
1.禁止跳转
2.过滤返回信息，验证远程服务器对请求的响应是比较容易的方法。如果web应用是去获取某一种类型的文件。那么在把返回结果展示给用户之前先验证返回的信息是否符合标准。
3.禁用不需要的协议，仅仅允许http和https请求。可以防止类似于file://, gopher://, ftp:// 等引起的问题
4.设置URL白名单或者限制内网IP（使用gethostbyname()判断是否为内网IP）
5.限制请求的端口为http常用的端口，比如 80、443、8080、8090
6.统一错误信息，避免用户可以根据错误信息来判断远端服务器的端口状态。

0x07 漏洞利用中牵涉的小技巧

crontab -l 显示当前计划任务
crontab -r 清除当前计划任务
端口转发工具 socat
在Apache配置文件中写入下面的内容，就可以将jpg文件当做PHP文件来执行
AddType application/x-httpd-php .jpg**~~``

0x08 相关材料

[1]http://blog.safebuff.com/2016/07/03/SSRF-Tips/
[2]https://paper.seebug.org/393/
[3]https://www.hackerone.com/blog-How-To-Server-Side-Request-Forgery-SSRF
[4]http://blog.blindspotsecurity.com/2017/02/advisory-javapython-ftp-injections.html
[5]https://medium.com/secjuice/php-ssrf-techniques-9d422cb28d51
[6]http://byd.dropsec.xyz/2017/06/04/SSRF%E6%BC%8F%E6%B4%9E%E5%89%96%E6%9E%90%E4%B8%8E%E5%88%A9%E7%94%A8/
[7]https://www.leavesongs.com/PYTHON/defend-ssrf-vulnerable-in-python.html
[8]https://www.secpulse.com/archives/65832.html
[9]https://www.cnblogs.com/s0ky1xd/p/5859049.html
[10]https://www.t00ls.net/articles-41070.html
[11]https://ricterz.me/posts/%E5%88%A9%E7%94%A8%20gopher%20%E5%8D%8F%E8%AE%AE%E6%8B%93%E5%B1%95%E6%94%BB%E5%87%BB%E9%9D%A2
[12]https://ricterz.me/posts/HITCON%202017%20SSRFme
[13]http://bobao.360.cn/learning/detail/240.html
[14]https://github.com/JnuSimba/MiscSecNotes/tree/master/%E6%9C%8D%E5%8A%A1%E7%AB%AF%E8%AF%B7%E6%B1%82%E4%BC%AA%E9%80%A0
[15]https://github.com/ring04h/papers/blob/master/build_your_ssrf_exp_autowork--20160711.pdf