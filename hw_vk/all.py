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

birthdays={} #запасаные словари
cities={}
for user in id_chela:
    req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids='+str(user)+'&v=5.74&fields=city,bdate&access_token=e710108be710108be710108b35e7723cb5ee710e710108bbdd1de6023989f2a50d061c4')
    response = urllib.request.urlopen(req)
    result1 = response.read().decode('utf-8')
    data = json.loads(result1)
    try:
        if 'bdate' not in data['response'][0]:
            big_dict[user].append(0)
        date=data['response'][0]['bdate']
        date=date.split('.')
        if len(date)==3:
            year=date[2]
            age=2018-int(year)
            birthdays[user]=age
            big_dict[user].append(age)
        else:
            big_dict[user].append(0)
        if 'city' not in data['response'][0]:
                big_dict[user].append(0)
        cities[user]=data['response'][0]['city']['title']
        big_dict[user].append(data['response'][0]['city']['title'])
    except: 
        continue
# print(big_dict)

texts_post=[]
texts_comm=[]
for item in new_clear_data:
    texts_post.append(item['text'])
for i in result:
    texts_comm.append(i['text'])
with open('text_post.txt', 'w', encoding='utf-8') as source:
        source.write(str(texts_post))
with open('text_comm.txt', 'w', encoding='utf-8') as source:
        source.write(str(texts_comm))

t_age={}
t_city={}
for el in big_dict:
    if len(big_dict[el])==3:
#         print(big_dict[el][2])
        a=big_dict[el][1]
        c=big_dict[el][2]
        if a in t_age:
            t_age[a].append(big_dict[el][0])
        else:
            t_age[a]=[]
            t_age[a].append(big_dict[el][0])
        if c in t_city:
            t_city[c].append(big_dict[el][0])
        else:
            t_city[c]=[]
            t_city[c].append(big_dict[el][0])
    else:
        pass

def mean(dic):
    dict_new={}
    for el in dic:
#         print(dic[el])
        if len(dic[el])>1:
            mean_len=sum(dic[el])/len(dic[el])
#             print(mean_len)
        else:
            mean_len=dic[el]
        dict_new[el]=mean_len
    return dict_new

dict_age = mean(t_age)
dict_city = mean(t_city)
for el in dict_age:
    if type(dict_age[el])==list:
        for l in dict_age[el]:
            dict_age[el]=int(l)
    else:
        pass
for el in dict_city:
    if type(dict_city[el])==list:
        for l in dict_city[el]:
            dict_city[el]=int(l)
    else:
        pass
    
    
plt.bar(dict_age.keys(), dict_age.values())
plt.title('Как соотносится возраст и длинна комментария')
plt.ylabel('Средняя длина комментариев')
plt.xlabel('Возраст')
# plt.show()
plt.savefig('age_and_comments.png', format='png', dpi=100)

plt.bar(dict_age.keys(), dict_age.values())
plt.title('Как соотносится город и длинна комментария')
plt.ylabel('Средняя длина комментариев')
plt.xlabel('Город')
# plt.show()
plt.savefig('city_and_comments.png', format='png', dpi=100)
