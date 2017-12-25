import urllib.request
import re
import time
def crawler():
    time.sleep(5)
    numbers=[]
    numbers2=[]
    for i in range(161,206):
        numbers.append(str(i))
    for i in range(1,100):
        numbers2.append(str(i))
    d={}
    for n in numbers:
        for n2 in numbers2:
            try:
                req = urllib.request.Request('http://thai-language.com/let/'+n+'.'+n2)
                with urllib.request.urlopen(req) as response:
                    code = response.read().decode('utf-8')
                    regT = re.findall('class=th><a href=\'/id/.*?\'>.*?</a>', code)
                    print(len(regT))
                    print(regT)

                    regE = re.findall('class=pos>.*?</td><td>.*?</td>', code)
                    print(len(regE))
                    print(regE)
            except:
                pass
        clearT=[]
        for s in regT:
            s=s.split('>')
            ns=s[2]
            clears=ns[:-4]
            clearT.append(clears)
        clearE=[]
        for s in regE:
            s = s.split('>')
            ns = s[3]
            clears = ns[:-4]
            print(clears)
            if 'span' in clears:
                print(clears)
                pass
            else:
                clearE.append(clears)
        print(len(clearT))
        print(len(clearE))
        for i in range(len(clearT)-1):
            clearT[i]=d[clearE[i]]
        print(d)
a=crawler()
