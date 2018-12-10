
import base64

class ProxyMiddleware(object):
    def __init__(self):
        self.proxy = 'http://proxy.abuyun.com:9020'
        auth = 'Basic ' + base64.b64encode(('xxxxxxxx' + ':' + 'xxxxxxx').encode()).decode()
        self.Proxy_Authorization = auth

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy
        request.headers['Proxy-Authorization'] = self.Proxy_Authorization