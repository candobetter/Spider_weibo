import requests
import json
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from requests.exceptions import RequestException


def get_page(page):
    base_url = 'https://m.weibo.cn/api/container/getIndex?'
    params = {
        'type': 'uid',
        'value': '1197161814',
        'containerid': '1076031197161814',
        'page': page
    }
    url = base_url + urlencode(params)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://m.weibo.cn/u/1197161814',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
    except RequestException:
        print('not response', res.status_code)


def parse_page(response):
    content = response.get('data')
    items = content.get('cards')
    for item in items:
        item = item.get('mblog')
        if item:                          # item 有None
            yield {
                'created_at': item.get('created_at'),
                'reposts': item.get('reposts_count'),
                'comments': item.get('comments_count'),
                'attitudes': item.get('attitudes_count'),
                'text': pq(item.get('text')).text()
            }


def write_json(result):
    with open('weibo_li.json', 'a', encoding='utf-8') as file:
        file.write((json.dumps(result, ensure_ascii=False)+'\n'))


if __name__ == '__main__':
    for page in range(1, 3):
        response = get_page(page)
        results = parse_page(response)
        for result in results:
            # print(result)
            write_json(result)

    print('Done')





