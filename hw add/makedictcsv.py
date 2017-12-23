import urllib.request
import re
import time
def crawler():
    time.sleep(5)
    req = urllib.request.Request('http://slovnik.narod.ru/old/slovar/a.html')
    with urllib.request.urlopen(req) as response:
        code = response.read().decode('utf-8')
    reg = re.findall('<a href="..?.html">', code)
    links = list(reg)
    all_links=[]
    for link in links:
        link=link[9:-2]
        linkEnd=('http://slovnik.narod.ru/old/slovar/' + link)
        if linkEnd in all_links:
            pass
        else:
            all_links.append(linkEnd)
            # print(all_links)
    for l in all_links:
        req1 = urllib.request.Request(l)
        with urllib.request.urlopen(req1) as response1:
            code1 = response1.read().decode('utf-8')
        words = re.findall('<td>.*</td>', code1)
        clearwords = []
        for w in words:
            clearw = w[4:-5]
            if '=' in clearw:
                pass
            elif ',' in clearw:
                cl = clearw.split(',')
                cclearw = cl[0]
                clearwords.append(cclearw)
            # elif ' ' in clearw:
            #     cl = clearw.split(' ')
            #     cclearw = cl[0]
            #     clearwords.append(cclearw)
            elif clearw in clearwords:
                pass
            else:
                clearwords.append(clearw)
        # print(clearwords)
        clwords=[]
        for w in clearwords:
            if '&#1123;' in w:
                w=w.replace('&#1123;','ѣ')
                clwords.append(w)
            if '&#1139;' in w:
                w=w.replace('&#1139;', 'ѳ')
            if '&#1138;' in w:
                w=w.replace('&#1138;', 'Ѳ')
            clwords.append(w)
        # print(clwords)
        for i in range(len(clwords) - 1):
            if i % 2 == 0:
                with open('dict.csv', 'a', encoding='utf-8') as file:
                    text = file.write(clwords[i] + ',' + clwords[i + 1] + '\n')
a=crawler()
