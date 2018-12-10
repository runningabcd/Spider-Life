import requests
import ujson

url = 'https://apiv5.yangkeduo.com/api/targaryen/query_goods_list_by_opt_id_c?pdduid=0&__json=1'

headers = {
    # 'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'content-type': 'text/plain;charset=UTF-8',
    # 'origin': 'https://mobile.yangkeduo.com',
    # 'referer': 'https://mobile.yangkeduo.com/duo_cms_mall.html',
    # 'authority': 'apiv5.yangkeduo.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

payload = {"optId": 14, "pageNum": 0, "pageSize": 10}

req = requests.post(url=url, data=ujson.dumps(payload), headers=headers)

print(req.content.decode())
