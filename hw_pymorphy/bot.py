from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
import pymorphy2
from pymorphy2 import MorphAnalyzer
import random
import re

words = open('words_nkrya.txt','r',encoding='utf-8')
words=words.readlines()
random.shuffle(words)
# prob_words=words[:100]
clear_words=[]
for w in words:
    clear_w=re.sub('[^А-яа-я]','',w)
    clear_words.append(clear_w)

app = Flask(__name__)

@app.route('/')
def form():   
    return render_template('form.html')

@app.route('/result')
def result():
    morph = MorphAnalyzer()
    if request.args:
        sent = request.args['sentence']
        m = Mystem()
        ana = m.analyze(sent)
        new_sent=open('sentence.txt','w',encoding='utf-8')
        for word in ana:
            if 'analysis' in word:
                forma_slova=word['analysis'][0]['gr']
                sent2=clear_words
                for w in sent2:
                    ana2 = m.analyze(w)
                    try:
                        an_word=ana2[0]
                        if 'analysis' in an_word:
                            print(an_word)
                            forma_slova2=an_word['analysis'][0]['gr']
                            if forma_slova == forma_slova2:
                                new_sent.write(w + ' ')
                                break
                    except IndexError:
                        pass
        new_sent.close()
        with open('sentence.txt','r',encoding='utf-8') as f:
            read_sent=f.read()
        return render_template('result.html', sentence=read_sent)
    return render_template('result.html')

        
if __name__ == '__main__':
    app.run(debug=False)
