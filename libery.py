import os
import sys
import inspect
from typing import List
# from requests.models import parse_url
from requests_html import HTMLSession #для пошуку
import requests
import re # регулярки
from bs4 import BeautifulSoup # парсинг сторіки
from collections import OrderedDict
import json

main_url='https://animevost.org'
my_wl={"v":1,"list":{}}#список тайтлів 
my_wl_name="my_watch_list.json"

class taytl_base:
    def __init__(self,url,name=""):
        self.name=name
        self.short_name=''
        self.url=url
    def give_short_name(self):
        if self.short_name!='':
            return self.short_name
        else:
            return self.name[:self.name.find('/')][:-1]
    def giv_kl_ep(self):
        name=self.name
        i1=name.find('[')
        i2=name.find(']')
        name=name[i1+1:i2]
        if name=='Анонс':
            return 0
        i1=name.find('-')
        if i1==-1:
            return 1
        i2=name.find(' ',i1)
        return int(name[i1+1:i2])


class taytl(taytl_base):
    def giv_kl_ep(self):
        return self.kl_ep
    def set_list_episod(self):
        for item in self.soup.find_all('script'):
            if 'var data = {' in item.text:
                text=item.text
                break
        ft='var data = '
        i1=text.find(ft)
        i2=text.find('}',i1)		
        text2=text[i1+len(ft)+1:i2-1]
        sps=text2.split(',')
        s=[]
        dop=[]
        
        for i in sps:
            e=i.split(':')
            e[0]=e[0][1:-1]
            e[1]=e[1][1:-1]
            if re.fullmatch(r"^(?!0.*$)([0-9]{1,4} серия)",e[0]):
                s.append(e)
            else:
                dop.append(e)
        self.kl_ep=len(s)+len(dop)
        self.kl_dop_ep=len(dop)        
        self.list_ep=s  
        self.list_dop_ep=dop  

    def give_all_taytl(self):
        if self.all_taytl!=None:
            return self.all_taytl
        item=self.soup.find('ol')
        if item==None:
            return None
        item=item.find_all('li')
        s=[]
        for i in item:
            s.append(taytl_base(main_url+i.next['href'],i.text))
        self.all_taytl=s
        return s
        
    def __init__(self, url, name=None,kl_ep=0,list_ep=None,list_dop_ep=None,soup=None,r=None):
        
        super().__init__(url,name)
        if r==None:
            # print(url)
            r = requests.get(url)
        if r.status_code!=200:
            print("Error conect to site(information about the series): "+str(r.status_code))
        soup=BeautifulSoup(r.content, 'html.parser')
        self.kl_dop_ep=0
        self.all_taytl=None
        if list_ep==None:
            self.list_ep=None
        if list_dop_ep==None:
            self.list_dop_ep=None
        if kl_ep==0:
            self.kl_ep=0
        
        self.soup=soup
        items = soup.find('h1')
        # print(url)
        name=items.text
        while name[0]==' ' or name[0]=='\n' :
            name=name[1:]
        while name[-1]==' ' or name[-1]=='\n' :
            name=name[:-1]
        self.name=name
        self.kl_ep=super().giv_kl_ep()

def get_source(url):#search def
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):#search def
    url=f"https://www.google.com/search?&q=site%3A{main_url}+" + query
    # print('url: ',url)
    response = get_source(url)
    
    return response

def parse_results(response):#search def
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
        }
        if(len(output)<3):
            output.append(item)
        else:
            break
        
    return output

def google_search(query):#search def
    response = get_results(query)
    return parse_results(response)

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)
def print_taytl(list,min=0,max=None):
    print()
    if max==None:
        max=len(list)
    for i in range(0,len(list)):
        if(i<max):
            print(f'[{i+1+min}] '+list[i].name)
        else:
            break
    print()

def quesBool(text,priority=1):
    if priority:
        yesorno=' [Д/н]'
    else:
        yesorno=' [д/Н]'		

    inp=input(text+yesorno)

    if inp=='':
        return priority
    
    if inp=='Y'  or inp=='y' or inp=='Д' or inp=='д' or inp=='Т' or inp=='т' or inp=='yes' or inp=='Yes' :
        return True
    else:
        return False

def is_taytl(url):
    if url.find('.html')!=-1:
        return True
    else:
        return False
    # if url.find('page')!=-1:
    #     return False 
    # if url.find('tip')!=-1:
    #     return True
    # else:
    #     return False

def give_taytl_whits_page(url):
    r=requests.get(url)
    if r.status_code!=200:
        print("Error conect to site(find video): "+str(r.status_code))
    soup=BeautifulSoup(r.content, 'html.parser')
    item=soup.find('div',id='dle-content')
    item=item.find_all('div',class_='shortstoryHead')
    ll=[]
    for i in item:
        i=i.find('h2')
        i=i.find('a')
        ll.append(taytl_base(i['href'],i.text))
        # ll.append(i['href'])
        # print(i.text)
    return ll
def clear_url(url):
    lis=['dev.']
    i1=url.find(lis[0])

    if i1!=-1:
        return url[:i1]+url[i1+len(lis[0]):]
    else:
        return url
def give_search_list(req,all=False,stat_bar=False):
    print_name=""
    if stat_bar:
        print('Пошук...')
    vd=google_search(req)
    if vd==[]:
        return False
    all_list=[]
    if all:
        done=0
        dl=0
        total_length=len(vd)
        for i in vd:
            # print(i['link'])
            done = int(50 * dl / total_length)
            if stat_bar:
                sys.stdout.write(f"\r[%s%s]  {print_name[:60]}... " % ('#' * done, '-' * (50-done)) )	
                sys.stdout.flush()
            if is_taytl(clear_url(clear_url(i['link']))):
                all_list.append(taytl(clear_url(i['link'])))
            else:
                ll=give_taytl_whits_page(clear_url(i['link']))
                for j in ll:
                    print_name=j.name
                    # print('-',j)
                all_list=all_list+ll
            dl+=1        
        return all_list
    else:
        for i in vd:            
            if is_taytl(clear_url(i['link'])):
                all_list.append(taytl(clear_url(i['link'])))
    all_list=list(OrderedDict.fromkeys(all_list))
    if all_list==[] and all==False:
        if stat_bar:
            print('Активація додаткового пошуку...')
        return give_search_list(req,True,stat_bar)
    else:
        return all_list

def write_mylist():
    with open(my_wl_name, "w") as jsonfile:
        json.dump(my_wl, jsonfile) # Writing to the file
        jsonfile.close()

def read_mylist():
    with open(my_wl_name, "r") as jsonfile:
        data = json.load(jsonfile) # Reading the file
        jsonfile.close()
        print(data)
        data["list"]['hz']={}
        data["list"]['1']={}
        print(data)

def test():
    read_mylist()

if __name__ == '__main__':
    test()
