from flask import Flask
from flask import render_template, request
import urllib.request
import re
import os

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
