from flask import Flask
from flask import render_template, request
import urllib.request
import re
import os
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
#             elif clearw in clearwords:
#                 pass
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
def mystemAll(w):
    with open('input.txt', 'w', encoding='utf-8') as source1:
        source1.write(w)
    os.system('/Users/darazharikova/Desktop/mystem -nid input.txt output.txt')
    with open('output.txt', 'r', encoding='utf-8') as source2:
        mystemAll=source2.read()
    print('mystemAll: '+mystemAll)
    return(mystemAll)
def mystemlemma(w):
    lemma=re.compile(r'{(.*?)=', flags=re.DOTALL)
    lemmasearch=re.search(lemma, w)
    if lemmasearch != None:
        neededlemma=lemmasearch.group(1)
    print('mystemNeeded: '+ neededlemma)
    return(neededlemma)
def mystemCase(allmystem):
    case=re.compile(r'од=(пр)|(дат),', flags=re.DOTALL)
    casesearch=re.search(case, allmystem)
    if casesearch !=None:
        return 'yescase'
    else:
        return 'nocase'
#
# domystem('мыши')
def dictopen():
    with open('dict.csv', 'r', encoding='utf-8') as source3:
        file=source3.read()
        file=file.split('\n')
#        print(dictUlt)
    dict={}
    for d in file:
        d=d.split(',')
#        print(d)
        if len(d)==2:
            rus, old=d[0], d[1]
            dict[rus]=old
    # print(dict)
    return dict
# d=dictopen()

def transleter(w):
    dictall=dictopen()
    print(dictall)
    print('input: '+w)
    if w in dictall:
        finalword=dictall[w]
        return(finalword)
    else:
        infinite=mystemlemma(mystemAll(w))
        print(infinite)
        infinitelist = list(infinite)
        base=[]
        ending=[]
        wlist=list(w)
        j=len(infinitelist)-1
        for i in range(len(wlist)):
            if i<=j:
                if wlist[i]==infinitelist[i]:
                    base.append(wlist[i])
                else:
                    ending.append(wlist[i])
            else:
                ending.append(wlist[i])
        base=''.join(base)
        lenbase=len(base)
        ending=''.join(ending)
        if infinite in dictall:
            dorbase=dictall[infinite][:lenbase]
            da=mystemCase(mystemAll)
            if da=='yescase' and ending =='е':
                ending='ѣ'
            finalword=dorbase+ending

        else:
            da = mystemCase(mystemAll(w))
            if da == 'yescase' and ending == 'е':
                ending = 'ѣ'
                base=w[:-1]
                finalword = base + ending
            else:
                finalword=w
        glasn='АаОоУуЫыЭэЯяЁёЮюИиЕе'
        soglasn='цкнгшщзхфвпрлджчсмтб'
        for l in range(len(finalword)-1):
            if finalword[l] == 'и' and finalword[l+1] in glasn and finalword[l-1] != 'i':
                finalword = finalword[:l] + 'i' + finalword[l+1:]
        if finalword[-1] in soglasn:
            finalword=finalword +'ъ'
        return(finalword)

# print(transleter('дом'))
app = Flask(__name__)

@app.route('/')
def translate():
    if request.args:
        word = request.args['word']
        dorefword = transleter(word)
        return render_template('result.html', dorefword=dorefword)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
