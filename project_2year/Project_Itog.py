
# coding: utf-8

# In[1]:

import urllib.request
import urllib.parse
import json
from math import floor
import re
from collections import Counter
from flask import Flask
from flask import url_for, render_template, request, redirect


# In[2]:

def detect_id (name):
    name=name.lower()
    name_right=urllib.parse.quote(name, safe='')
    users = set()
    req = urllib.request.Request('https://api.vk.com/method/groups.search?q='+ name_right +'&offset=0&count=20&v=5.23&access_token=021bb0b9933eefa9a4e28dffa66dfeb76ac186baf8d6f4a8e877aded998b913988fdc780667f8b3fe3578')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    for gr in data['response']['items']:
        maybe_name = gr['name']
        maybe_name=maybe_name.lower()
        if maybe_name==name:
            name_group = gr['name']
            id_group = str(gr['id'])
            break
        else:
            pass
    try:
        id_group
    except NameError:
        id_group=''
    return(id_group)


# In[3]:

def detect_offsets(id_group):
    offsets=[0]
    users = set()
    req = urllib.request.Request('https://api.vk.com/method/groups.getMembers?group_id='+ id_group +'&v=5.23&offset=0&access_token=021bb0b9933eefa9a4e28dffa66dfeb76ac186baf8d6f4a8e877aded998b913988fdc780667f8b3fe3578')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    numb_users = data['response']['count']
    if numb_users<1000:
        pass
    else:
        thousends=floor(numb_users/1000)
        if thousends==1:
            offsets.append(1000)
            pass
        else:
            offsets.append(thousends*1000)
            if numb_users<3000:
                pass
            else:
                offsets.append(numb_users//2)
    return(offsets,numb_users)


# In[4]:

def users_data(id_group,offsets):
    users=[]
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/groups.getMembers?group_id='+ id_group +'&v=5.23&offset=' + str(off) + '&count=1000&fields=bdate,city&access_token=021bb0b9933eefa9a4e28dffa66dfeb76ac186baf8d6f4a8e877aded998b913988fdc780667f8b3fe3578')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        for user_data in data['response']['items']:
            users.append(user_data)
    return (users)


# In[5]:

def users_ages (users):
    users_years=0
    numb_users_with_age=0
    for user in users:
        if 'bdate' in user:
            bdate_user=user['bdate'].split('.')
            if len(bdate_user)==3:
                age_user=2018-int(bdate_user[2])
                users_years=users_years+age_user
                numb_users_with_age+=1
            else:
                pass
    mid_age=users_years/numb_users_with_age
    mid_age=round(mid_age)
    return(mid_age)


# In[6]:

def users_cities(users,numb_users):
    users_city={}
    for user in users:
        if 'city' in user:
            city_user=user['city']['title']
            if city_user in users_city:
                users_city[city_user]+=1
            else:
                users_city[city_user]=1
    users_city_sort=sorted(users_city.items(), key=lambda item: item[1], reverse=True)
    if numb_users<2000:    
        good_cities=str(users_city_sort)
        good_cities=good_cities.replace('(', '')
        good_cities=good_cities.replace('),', '\n')
        result_city='Так как в сообществе менее 2000 участников, вот список всех городов, где проживают участники сообщества'+ '\n' + good_cities
    else:
        most_popular=[]
        most_popular=str(users_city_sort[:15])
        most_popular_cities=str(re.findall('\'[А-Яа-я]*\'', most_popular))
        most_popular_cities=re.sub('\"','', most_popular_cities)
        most_popular_cities=re.sub('\'','', most_popular_cities)
        most_popular_cities=re.sub(',','\n', most_popular_cities)
        result_city='Так как в сообществе более 2000 участников, вот список городов, где проживает большинство участников (в порядке убывания):'+ '\n' + str(most_popular_cities)
    return(result_city)


# In[7]:

def posts(id_group):
    texts_posts=[]
    posts_id=[]
    id_group_new='-'+ id_group
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id='+ id_group_new +'&v=5.23&offset=0&count=15&filter=all&access_token=021bb0b9933eefa9a4e28dffa66dfeb76ac186baf8d6f4a8e877aded998b913988fdc780667f8b3fe3578')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    for el in data['response']['items']:
        posts_id.append(el['id'])
        if el['text'] != '':
            texts_posts.append(el['text'])
        else:
            pass
    clear_texts_post=str(texts_posts)
    clear_texts_post=re.sub('[\.,\?!\'\)\(:;]','', clear_texts_post)
    clear_texts_post=re.sub('\d','', clear_texts_post)
    clear_texts_post=re.sub(' +',' ', clear_texts_post)
    count_post=clear_texts_post.split(' ')
    count_post=Counter(count_post)
    count_post = dict(count_post)
    count_post_sort=sorted(count_post.items(), key=lambda item: item[1], reverse=True)
    count_post_sort_50=count_post_sort[:50]
    if len(count_post_sort)<10:
        popular_words_post='В данном сообществе нет текста постов'
    else:
        popular_words_post=[]
        for i in count_post_sort_50:
            if len(i[0])<4:
                pass
            else:
                popular_words_post.append(i[0])
        popular_words_post=popular_words_post[:10]
    return(id_group_new, posts_id, popular_words_post)


# In[8]:

def comments(id_group_new, posts_id):
    text_comm=[]
    for i in posts_id:
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id='+ id_group_new +'&post_id='+ str(i) +'&v=5.74&count=10&access_token=021bb0b9933eefa9a4e28dffa66dfeb76ac186baf8d6f4a8e877aded998b913988fdc780667f8b3fe3578')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        try:
            for tx in data['response']['items']:
                text_comm.append(tx['text'])
        except:
            pass
    clear_texts_com=str(text_comm)
    clear_texts_com=re.sub('[\.,\?!\'\)\(:;]','', clear_texts_com)
    clear_texts_com=re.sub('\[.*?\]','', clear_texts_com)
    clear_texts_com=re.sub(' +',' ', clear_texts_com)
    count_com=clear_texts_com.split(' ')
    count_com=Counter(count_com)
    count_com = dict(count_com)
    count_com_sort=sorted(count_com.items(), key=lambda item: item[1], reverse=True)
    count_com_sort_50=count_com_sort[:50]
    if len(count_com_sort)<10:
        popular_words_comm='В данном сообществе нет комментариев'
    else:
        popular_words_com=[]
        for i in count_com_sort_50:
            if len(i[0])<4:
                pass
            else:
                popular_words_com.append(i[0])
        popular_words_comm=popular_words_com[:10]
    return (popular_words_comm)


# In[ ]:

app = Flask(__name__)

@app.route('/')
def form():   
    return render_template('form.html')

@app.route('/result')
def result():
    if request.args:
        name = request.args['name']
        id_group=detect_id (name)
        if id_group=='':
            name=name+', однако мы его не смогли найти'
            numb_users='нет'
            mid_age='неизвестен'
            result_city=''
            popular_words_post='неизвестно'
            popular_words_comm='неизвестно'
        else:    
            print(id_group)
            offsets=detect_offsets(id_group)[0]
            numb_users=detect_offsets(id_group)[1]
            print(offsets)
            print(numb_users)
            users=users_data(id_group,offsets)
            print(len(users))
            mid_age=users_ages(users)
            print(mid_age)
            result_city=users_cities(users,numb_users)
            print(result_city)
            id_group_new=posts(id_group)[0]
            posts_id=posts(id_group)[1]
            popular_words_post=posts(id_group)[2]
            print(id_group_new) 
            print (posts_id)
            print(popular_words_post)
            popular_words_comm=comments(id_group_new, posts_id)
            print(popular_words_comm)
        return render_template('result.html', name=name, numb_users=numb_users, mid_age=mid_age, result_city=result_city,popular_words_post=popular_words_post, popular_words_comm=popular_words_comm)
    return render_template('result.html')

        
if __name__ == '__main__':
    app.run(debug=False)


# In[ ]:



