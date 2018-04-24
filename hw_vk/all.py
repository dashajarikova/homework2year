import urllib.request
import json
offsets=[0,100,200]
clear_data=[]
for off in offsets:
    req = urllib.request.Request(
        'https://api.vk.com/method/wall.get?owner_id=-36941068&count=50&v=5.74&access_token=e710108be710108be710108b35e7723cb5ee710e710108bbdd1de6023989f2a50d061c4&offset=' + str(
            off))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data=json.loads(result)
    data = data['response']['items']
    clear_data.append(data)
    #print(clear_data)
    #for n in clear_data:
        #clear_data['response']['items'].append(n)
new_clear_data=[]
for part in clear_data:
    for p in part:
        new_clear_data.append(p)
id_chela=[]
all_texts={}
post_id=[]
post_len=[]
sl_dlin={}
for item in new_clear_data:
    post_id.append(item['id'])
    post_len=(len(item['text'].split()))
    for i in post_id:
        text_com=[]
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-36941068&post_id='+str(i)+'&v=5.74&count=100&access_token=e710108be710108be710108b35e7723cb5ee710e710108bbdd1de6023989f2a50d061c4')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        len_com=int(result['response']['count'])
        result=result['response']['items']
        #print(result)
        #len_com=result['response']['count']
        #print(len_com)
        len_text=[]
        for r in result:
             if r['from_id'] in id_chela:
                 pass
             else:
                 id_chela.append(r['from_id'])  
            text_com=r['text']
            len_text.append(len(text_com.split()))
            #print(len_text)
        if len_com ==0:
            mean_len_com = 0
        else:
            mean_len_com=sum(len_text)/len_com
        #print(mean_len_com)
    sl_dlin[post_len]=mean_len_com
import matplotlib.pyplot as plt
plt.bar(sl_dlin.keys(), sl_dlin.values())
plt.ylabel('Средняя длина комментариев')
plt.xlabel('Длина поста')
plt.show()
plt.savefig('posts_and_comments.png', format='png', dpi=100)

birthdays={}
for user in id_chela[:500]:
    req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids='+str(user)+'&v=5.74&fields=city,bdate&access_token=e710108be710108be710108b35e7723cb5ee710e710108bbdd1de6023989f2a50d061c4')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    data=data['response']
    if 'bdate' not in data[0]:
            continue
    date=data[0]['bdate']
    date=date.split('.')
    if len(date)==3:
        year=date[2]
        age=2018-int(year)
        birthdays[user]=age
    else:
        pass
    if 'city' not in data[0]:
            continue
    cities[user]=data[0]['city']['title']

texts_post=[]
for item in new_clear_data:
    texts.append(item['text'])
with open('text_post.txt', 'w', encoding='utf-8') as source:
        source.write(str(texts_post))
