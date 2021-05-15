from jinja2 import Environment, FileSystemLoader
import setting
from requests_oauthlib import OAuth1Session
import json

data_list = []
context = {}
cnt = 0

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('template.html')

API_Key = setting.API_Key
API_Secret_Key = setting.API_Secret_Key
Access_Token = setting.Access_Token
Access_Token_Secret = setting.Access_Token_Secret

twitter = OAuth1Session(API_Key, API_Secret_Key, Access_Token, Access_Token_Secret)
search_api = 'https://api.twitter.com/1.1/search/tweets.json'
oembed_api = 'https://publish.twitter.com/oembed'

params = {
    # 波ダッシュ、全角チルダ
    'q': '#はぁ〜また買っちゃった OR #はぁ～また買っちゃった -filter:retweets',
    'result_type': 'recent',
    'count': 100,
}

print('get res...')
res = twitter.get(search_api, params=params)
tweets = json.loads(res.text)

print('embed...')
for row in tweets['statuses']:
    cnt += 1
    print(cnt, end='\t')
    try:
        is_media = row['entities']['media']
        name = row['user']['name']
        screen_name = row['user']['screen_name']
        id = row['id']

        oembed_url = f'https://twitter.com/{screen_name}/status/{id}'
        oembed_params = {
            'url': oembed_url,
            'maxwidth': 220,
            'align': 'center',
            'hide_thread': 'true',
        }
        print(screen_name)
        request = twitter.get(oembed_api, params=oembed_params)
        e_data = json.loads(request.text)['html']
        data_list.append(e_data)
        context['e_data'] = data_list
    except KeyError:
        print('pass')
        continue

html = tmpl.render(context)
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(str(html))
