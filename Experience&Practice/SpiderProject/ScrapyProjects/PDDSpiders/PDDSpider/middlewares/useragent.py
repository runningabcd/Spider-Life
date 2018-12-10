import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgentMiddleware(UserAgentMiddleware):
    USER_AGENT_MOBILE_LIST = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) '
        'AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 '
        '(KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/'
        '534.46 (KHTML, like Gecko) Mobile/9A405',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/'
        '534.46 (KHTML, like Gecko) Mobile/9A406',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/'
        '534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/'
        '534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A406 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/'
        '534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534'
        '.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26'
        ' (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/53'
        '6.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/'
        '536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/'
        '536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/'
        '537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_3 like Mac OS X) AppleWebKit/'
        '537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/'
        '537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/'
        '537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/'
        '537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/'
        '537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/'
        '600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4'
        ' (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebK'
        'it/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebK'
        'it/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWe'
        'bKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
        'Mobile/8H7 Safari/6533.18.5',
        'Mozilla/5.0 (iPod; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 '
        '(KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25',
        'Mozilla/5.0 (iphone; U; CPU iPhone OS 4_3_5 like Mac OS X; zh-cn) AppleWe'
        'bKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
        'Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (iphone; cpu iphone os 7_0_2 like mac os x) Applewebkit/537.5'
        '1.1 (khtml, like gecko) version/7.0 mobile/11a501 safari/9537.53',
        'Mozilla/5.0(iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us)AppleWebKit'
        '/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d Safari/6531.22.7',
        'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_0likeMacOSX;en-us)AppleWebKit/532.9(KHT'
        'ML,likeGecko)Version/4.0.5Mobile/8A293Safari/6531.22.7',
        'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) '
        'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) '
        'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) '
        'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
        'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
        'Mozilla/5.0 (Android; Tablet; rv:14.0) Gecko/14.0 Firefox/14.0',
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) '
        'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
        'Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) '
        'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    ]

    def process_request(self, request, spider):
        ua = random.choice(self.USER_AGENT_MOBILE_LIST)
        request.headers.setdefault('User-Agent', ua)
