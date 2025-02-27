from flask import Flask
from flask import url_for, render_template, request, redirect
import json
import re

app = Flask(__name__)

def make_massive():
    with open('result.txt', 'r', encoding='utf-8') as res:
        data = res.read()
        data = data.split('\n')
        massive=[]
        for line in data:
            line=line.split(',')
            slov = {}
            slov[line[0]]=line[1:]
            massive.append(slov)
    data_json = json.dumps(massive, ensure_ascii = False, indent = 4)
    with open('data.json','w',encoding='utf-8') as d:
        d.write(data_json)
    return massive

@app.route('/json')
def page_json():
    data_massive = make_massive()
    data_json = json.dumps(data_massive, ensure_ascii=False, indent=4)
    with open('data.json','w',encoding='utf-8') as d:
        d.write(data_json)
        return render_template('json.html', data_json=data_json)

@app.route('/')
def form():
    if request.args:
        name = request.args['username']
        age = request.args['age']
        city = request.args['city']
        language = request.args['language']
        stressG = request.args['stressG']
        stressS = request.args['stressS']
        with open('result.txt', 'a', encoding='utf-8') as res:
            res.write(name+','+age+','+city+','+language+','+stressG+','+stressS+'\n')
    return render_template('form1.html')

@app.route('/search')
def search():
    if request.args:
        name = request.args['nameneeded']
        stressneeded = request.args['stressneeded']
        for d in make_massive():
            if name in d:
                result=d[name]
                otvet = str(result)
                if stressneeded==('stressneededG'):
                    otvet=str(result)
                    if otvet[-15]=='1':
                        resultstress='гУглить'
                        print(otvet)
                    else:
                        resultstress = 'гуглИть'
                else:
                    if otvet[-3]=='1':
                        resultstress='спОйлерить'
                        print(otvet)
                    else:
                        resultstress = 'спойлерИть'
                return render_template('result.html', name=name, resultstress=resultstress)
    return render_template('search.html')
@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/stats')
def statistics():
    with open('result.txt', 'r', encoding='utf-8') as stat:
        data = stat.readlines()
        number=len(data)
        all_age=0
        stressG1=0
        stressG2=0
        stressS1=0
        stressS2=0
        for line in data:
            age=re.search(',..,',line,flags=re.DOTALL)
            age=age.group(0)
            age=age[1:3]
            age=int(age)
            all_age=all_age+age
            whatstressS=line[-2]
            whatstressG=line[-11]
            if whatstressS=='1':
                stressS1+=1
            else:
                stressS2+=1
            if whatstressG=='1':
                stressG1 += 1
            else:
                stressG2 += 1
        if stressG1>stressG2:
            stressG=('гУглить')
            nostressG = ('гуглИть')
        elif stressG2>stressG1:
            stressG = ('гуглИть')
            nostressG =('гУглить')
        else:
            stressG = ('-')
            nostressG = ('- (говорят одинаково и так и так)')
        if stressS1>stressS2:
            stressS=('спОйлерить')
            nostressS = ('спройлерИть')
        elif stressS2>stressS1:
            stressS = ('спойлерИть')
            nostressS =('спОйлерить')
        else:
            stressS = ('-')
            nostressS = ('- (говорят одинаково и так и так)')
    mid_age=all_age//number
    return render_template ('statistics.html',number=number,mid_age=mid_age,stressG=stressG,nostressG=nostressG,stressS=stressS,nostressS=nostressS)

if __name__ == '__main__':
     app.run(debug=True)
