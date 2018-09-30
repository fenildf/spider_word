import requests
from bs4 import BeautifulSoup
import json
from threading import Thread

# __URL__ = 'https://www.examword.com/ielts-list/4000-academic-word-{}?la=en'

__BD_FY_URL__ = 'https://fanyi.baidu.com/transapi'

# res = requests.post(__BD_FY_URL__, data={
#     'query': 'amount',
#     'from': 'en',
#     'to': 'zh',
#     'source': 'txt'
# })
#
# print(json.loads(res.json()['result']))
# zh = res.json()['data'][0]['dst']


lists = []


def get_bd_fy(word1, attrs):
    res = requests.post(__BD_FY_URL__, data={
        'query': word1,
        'from': 'en',
        'to': 'zh',
        'source': 'txt'
    })

    result = json.loads(res.json()['result'])

    voice = ''

    if 'voice' in result:
        voice = result['voice']

    content = result['content']

    attrs['voice'] = voice
    attrs['content'] = content

    lists.append(attrs)


def read_word(file_i):
    with open('word_{}'.format(file_i), 'r', encoding='utf8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        span_list_word = soup.select('.listWordWord')
        span_list_explanation = soup.select('.listWordExplanation')

        if len(span_list_word) != len(span_list_explanation):
            print('[Error] a,b长度不一致;a:{},b:{}'.format(span_list_word, span_list_explanation))

        total = len(span_list_word)

        threads = []

        for num, (word, explanation) in enumerate(zip(span_list_word, span_list_explanation), 1):
            word = word.text.strip(':')

            print('[{}/{}]{}'.format(num, total, word))

            t = Thread(target=get_bd_fy, args=(word, {
                'num': num,
                'word': word,
                'explanation': explanation.text
            }))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    with open('word/word_{}.json'.format(file_i), 'w', encoding='utf8') as f1:
        json.dump(lists, f1, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    for i1 in range(1, 18):
        read_word(i1)
