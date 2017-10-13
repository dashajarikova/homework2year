import urllib.request
import re
import os
import shutil
import time

def everythings(articles):
    time.sleep(5)
    for site in articles:
        siteNumber=re.findall('id=(.*)', site, flags=re.DOTALL)
        siteNumber=str(siteNumber[0])
        print('№' + siteNumber)
        req = urllib.request.Request(str(site))
        with urllib.request.urlopen(req) as source:
            code=source.read().decode('utf-8')
        title=ftitle(code)
        date=fdate(code)
        year=date[-4:]
        month=date[-7:-5]
        print (month)
        print (year)
        author=fauthor(code)
        
        regTag=re.compile('<.*?>', re.DOTALL)  
        regScript=re.compile('<script.*?>.*?</script>', re.DOTALL) 
        regComment=re.compile('<!--.*?-->', re.DOTALL)  
        regSpace=re.compile('\s{2,}', re.DOTALL)
        regElse=re.compile('[a-zA-Z0-9_#;&/\№|=\{\}:\."\?\(\)\-;@]', re.DOTALL)

        clean_t = regScript.sub("", code)
        clean_t = regComment.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)             
        clean_t = regSpace.sub ("", clean_t)
        clean_t = regElse.sub("", clean_t)
        
        fileName=siteNumber+'-'+str(date)+'.txt'
        path=puti(fileName)
        
        with open(fileName, 'a', encoding='utf-8') as article:
            article.write('@au '+author+'\n')
            article.write('@ti '+title+'\n')
            article.write('@da '+date+'\n')
            article.write('@url '+site+'\n')
            article.write(clean_t)
            
        mkdirs('plain',year,month)  
        shutil.move('.\\'+fileName, '.\\plain\\'+year+'\\'+month)

        mkdirs('mystem-xml',year,month)
        firstfilepath=shutil.copy('.\\plain\\'+year+'\\'+month+'\\'+fileName, '.\\mystem-xml\\'+year+'\\'+month)
        xmlfiles=mystemxml(firstfilepath)
        
        mkdirs('mystem-plain',year,month)
        firstfilepath2=shutil.copy('.\\plain\\'+year+'\\'+month+'\\'+fileName, '.\\mystem-plain\\'+year+'\\'+month)
        xmlfiles2=mystemplain(firstfilepath2)
        
        row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tреспубликанская\t%s\tгазета "Якутия"\t\t%s\tгазета\tРоссия\tЯкутия\tru'
        meta=str(row%(path,author,title,date,site,year))
        with open('metadata.csv', 'a', encoding='utf-8') as metadata:
            metadata.write(meta+'\n')      
    return
def mkdirs(typedir,year,month):
    if not os.path.exists(typedir+'\\'+year):
            os.makedirs(typedir+'\\'+year+'\\'+month)
    if not os.path.exists(typedir+'\\'+year+'\\'+month):
            os.makedirs(typedir+'\\'+year+'.\\'+month)

def cr():
    articles=[]
    begining='http://sprostor.ru/?module=articles&action=view&id='  
    for i in range(2400,2500):
        article=begining+str(i)
        try:
            req = urllib.request.Request(str(article))
            with urllib.request.urlopen(req) as source:
                code=source.read().decode('utf-8')
            popitka=re.search('strong',code, flags=re.DOTALL)#потому что на этом сайте существуют пустые страницы, без статей. Но если нет статьи-нет тега strong
            if popitka != None:
                articles.append(article)
            else:
                pass
        except:
            pass
    return articles
def ftitle(text):
    title=re.findall('<h1>(.*?)</h1>', text, flags=re.DOTALL)
    title=str(title[0])
    return title
def fdate(text):
    date=re.findall('</span><span class=\'date_start\'>(.*?)</span>', text, flags=re.DOTALL)
    date=str(date[0])
    date=date.split('-')
    dateend=str(date[2]+'.'+date[1]+'.'+date[0])
    return dateend
def fauthor(text):
    author=re.findall('<strong>([А-Я]\. [а-яА-Я]+,?)</strong>', text, flags=re.DOTALL)
    if len(author)==0:
        return 'Noname'
    else:
        author=str(author[0])
        if author[-1]==',':
            author=author[:-1]
        return author

def puti(fileName):
    year=fileName[-4:]
    month=fileName[-6:-4]
    path='.\\plain\\'+str(year)+'\\'+str(month)+'\\'+str(fileName)+'.txt'
    return path

def mystemxml(firstfile):
    xml=re.sub('\.txt', '', firstfile, flags=re.DOTALL)
    secondfile=os.system('C:\\Users\\123\\Desktop\\mystem.exe -nid --format xml '+firstfile+' '+xml)
    os.remove(firstfile)
    return (secondfile)
def mystemplain(firstfile):
    mystem=re.sub('\.txt', '', firstfile, flags=re.DOTALL)
    secondfile=os.system('C:\\Users\\123\\Desktop\\mystem.exe -nid '+firstfile+' '+mystem)
    os.remove(firstfile)
    return (secondfile)
def maindirs():
    os.mkdir('plain')
    os.mkdir ('mystem-xml')
    os.mkdir ('mystem-plain')
    return 
a=maindirs()
b=everythings(cr())

