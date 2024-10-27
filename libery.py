try:
    import os
    import sys
    import inspect
    from typing import List
    # from requests.models import parse_url
    import requests
    import re # регулярки
    import cfg
    from collections import OrderedDict
    import json
    import datetime
    from bs4 import BeautifulSoup # парсинг сторіки
    # from duckduckgo_search import DDGS #для пошуку

    from urllib.parse import urlparse, urlunparse
except ImportError as e:
    print(f"Помилка імпорту {e}")

main_url='https://animevost.org'

my_wl_name="my_watch_list.json"
history_file_name="history_list.json"
viewed_file_name="viewed_list.json"
ids_downloaded_taytls_file_name="ids_downloaded_taytls.json"
class taytl_base:
    def __init__(self,url,name=""):
        self.name=name
        self.short_name=''
        self.url=url
    def __repr__(self):
        return "taytl_base({!r}, {!r})".format(self.url, self.name)
    def __eq__(self, other):
        return (self.name) == (other.name)
    def __hash__(self):
        return hash((self.name))

    def give_short_name(self):
        if self.short_name!='':
            return self.short_name
        else:
            i1=self.name.find('~')
            if i1!=-1:                
                while self.name[i1-1]==' ' or self.name[i1-1]=='~':
                    i1-=1                               
                return self.name[:i1]
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
            try:
                kl=int(name.split()[0])
            except ValueError:# на випадок якщо не вийде дізнатись кількість серій
                kl=0
            return kl
        i2=name.find(' ',i1)
        try:
            kl=int(name[i1+1:i2])
        except ValueError:# на випадок якщо не вийде дізнатись кількість серій
            kl=0
        return kl
        
    def giv_end_kl_ep(self)->int:
        name=self.name
        i1=name.find('[')
        i2=name.find(']')
        ep=name[i1+1:i2]
        if ep=='Анонс':
            return 0
        i3=ep.find('из')
        kl_ep=ep[i3+3:i2]
        if kl_ep[-1]=='+':
            kl_ep=kl_ep[:-1]
        return int(kl_ep)


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
            e[0]=e[0].replace('"','')
            e[1]=e[1].replace('"','')
            if e not in s and e not in dop:
                if re.fullmatch(r"^(?!0.*$)([0-9]{1,4} серия)",e[0]):
                    s.append(e)
                else:
                    dop.append(e)
        self.kl_ep=len(s)+len(dop)
        self.kl_dop_ep=len(dop)        
        self.list_ep=s  
        self.list_dop_ep=dop  

    def give_all_taytl(self):
        if self.all_taytl is not None:
            return self.all_taytl
        item=self.soup.find('ol')
        if item is None:
            return None
        item=item.find_all('li')
        s=[]
        for i in item:
            # print(main_url+i.next['href'])
            if i.next['href'][0]=='/':
                s.append(taytl_base(main_url+i.next['href'],i.text))
            else:
                s.append(taytl_base(i.next['href'],i.text))
        self.all_taytl=s
        return s
        
    def __init__(self, url, name=None,kl_ep=0,list_ep=None,list_dop_ep=None,soup=None,r=None):
        
        super().__init__(url,name)
        if r is None:
            # print(url)
            r = requests.get(url)
        if r.status_code!=200:
            print("Error conect to site(information about the series): "+str(r.status_code))
        soup=BeautifulSoup(r.content, 'html.parser')
        self.kl_dop_ep=0
        self.all_taytl=None
        if list_ep is None:
            self.list_ep=None
        if list_dop_ep is None:
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

def giv_end_taytls(url):# вертає html з даними про остані тайтли  
    r= requests.get(url)
    if r.status_code!=200:
        print("Error conect to site(list taytl): "+str(r.status_code))
        return None
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.find('ul',class_='raspis raspis_fixed')
    el=items.findAll('a')
    return el

def get_taytl_id(url):
    i1=url.rfind('/')
    i2=url.find('-',i1)
    return url[i1+1:i2]

def giv_end_list_taytls(url):#вертає список обєктів taytl
    el=giv_end_taytls(url)
    if el is None:
        return None
    s=[]
    for i in el:
        s.append(taytl_base(i['href'],i.text))
    return s

def old_make_ep_url(kod:str,quality:int=720)->str:   
    urls_player=[f"https://animevost.org/frame5.php?play={kod}&player=9",f"http://play.agorov.org/{kod}?old=1",f"http://play.animegost.org/{kod}?player=9"]
    while True:
        r= requests.get(urls_player[cfg.nom_payer])
        if r.status_code!=200:
            print(f"Error conect to base -{cfg.nom_payer+1}-: "+str(r.status_code))
            print("Start use next base")
            if len(urls_player)==cfg.nom_payer+1:
                print("E R R O R conect to base`s")
                return None
            else:
                cfg.nom_payer=+1
        else:
            break
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.findAll('a',class_="butt")#old

    if quality==480:
        return items[0]["href"]
    elif quality==720:
        return items[1]["href"]
    else:
        print('Немає такої якості')
        return None

def make_ep_url(kod:str,quality:int=720)->str:       
    if cfg.settings['NoAPIDownload']:
        return old_make_ep_url(kod,quality)
        
    return f"http://video.animetop.info/{quality}/{kod}.mp4"

def get_source(url):#search def
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

# def duckduckgo_search(query):#search def
#     with DDGS() as ddgs:
#         results = [r for r in ddgs.text(f"site:animevost.org {query}", max_results=10)]
#     return results

def site_search(query)->list: #TODO this ['href':'value']
    results = []
    url = f"{main_url}/index.php?do=search"
    data = {'do':'search','subaction':'search','story':query}
    r = requests.post(url, data=data)
    if r.status_code!=200:
        print("Error conect to site(search): "+str(r.status_code))
        return results
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.find_all('div',class_='shortstory')
    for i in items:
        a=i.find('a')
        results.append({'href':a['href'],'text':a.text})
    return results


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
    if max is None:
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
    if url.find('.html')==-1:
        return False
    elif url.find('page')!=-1:
        return False
    else:
        return True
        

def give_taytl_whits_page(url,r=None):
    if r is None:
        r=requests.get(url)
    if r.status_code!=200:
        return None
        print(f"\nError conect to site(find video): \n{url}\n"+str(r.status_code))
    soup=BeautifulSoup(r.content, 'html.parser')
    item=soup.find('div',id='dle-content')
    item=item.find_all('div',class_='shortstoryHead')
    ll=[]
    for i in item:
        i=i.find('h2')
        i=i.find('a')
        ll.append(taytl_base(i['href'],i.text))
    return ll

def clear_url(url):
    lis=['dev.']
    i1=url.find(lis[0])

    if i1!=-1:
        return url[:i1]+url[i1+len(lis[0]):]
    else:
        return url

def del_doubling(l):
    return list(OrderedDict.fromkeys(l).keys())

def give_search_list(req,all=False,stat_bar=False):
    print_name=""
    if stat_bar:
        print('Пошук...')
    # vd=duckduckgo_search(req)
    vd=site_search(req)
    if vd==[]:
        return False
    all_list=[]
    if all:
        done=0
        dl=0
        total_length=len(vd)
        for i in vd:
            done = int(50 * dl / total_length)
            if stat_bar:
                sys.stdout.write(f"\r[%s%s]  {print_name[:60]}... " % ('#' * done, '-' * (50-done)) )	
                sys.stdout.flush()
            clean_link=clear_url(clear_url(i['href']))
            r=requests.get(clean_link)
            clean_link=r.url
            if is_taytl(clean_link):
                all_list.append(taytl(clean_link,r=r))
            else:
                ll=give_taytl_whits_page(clean_link,r=r)
                if ll is None:
                    continue
                for j in ll:
                    print_name=j.name
                all_list=all_list+ll
            dl+=1        
        return all_list
    else:
        for i in vd:            
            if is_taytl(clear_url(i['href'])):
                all_list.append(taytl(clear_url(i['href'])))
    if all_list==[] and all is False:
        if stat_bar:
            print('Активація додаткового пошуку...')
        all_list= give_search_list(req,True,stat_bar)
    all_list=del_doubling(all_list)
    return all_list

def write_mylist():
    with open(my_wl_name, "w") as jsonfile:
        json.dump(cfg.my_wl, jsonfile) # Writing to the file

def add_id_to_viewed_taytls(id):
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    if date not in cfg.ids_downloaded_taytls:
        cfg.ids_downloaded_taytls[date]=[]
    cfg.ids_downloaded_taytls[date].append(id)

def write_ids_viewed_taytls():
    with open(ids_downloaded_taytls_file_name, "w") as jsonfile:
        json.dump(cfg.ids_downloaded_taytls, jsonfile) # Writing to the file

def read_ids_viewed_taytls():
    try:
        with open(ids_downloaded_taytls_file_name, "r") as jsonfile:
            info = json.load(jsonfile) # Reading the file
            now_date = datetime.datetime.today().strftime("%d.%m.%Y")
            for date in list(info):
                if date!=now_date:
                    info.pop(date,None)
            cfg.ids_downloaded_taytls = info
        write_ids_viewed_taytls()
    except KeyError:  
        print(f'Файл {ids_downloaded_taytls_file_name} пошкоджений')  
    except json.decoder.JSONDecodeError:
        print(f'Файл {ids_downloaded_taytls_file_name} пошкоджений')
    except FileNotFoundError:
        cfg.ids_downloaded_taytls={}
        with open(ids_downloaded_taytls_file_name, "w") as jsonfile:
            json.dump(cfg.ids_downloaded_taytls, jsonfile)

def add_taytl_in_wl(wl_taytl):
    cfg.my_wl['list'].append(wl_taytl)
    write_mylist()

def create_wl_list():
    cfg.my_wl={"v":cfg.v_my_wl,"list":[]}
    write_mylist()

def read_mylist():   
    try:
        with open(my_wl_name, "r") as jsonfile:
            data = json.load(jsonfile) # Reading the file
            parsed_main_url = urlparse(main_url)
            for i in data['list']:
                parsed_url = urlparse(i['url'])
                if parsed_url.netloc != parsed_main_url.netloc:
                    new_url = urlunparse((parsed_main_url.scheme, parsed_main_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
                    i['url']=new_url

            return data
    except KeyError:  
        print(f'Файл {my_wl_name} з списком ваших тайтлів пошкоджений')  
    except json.decoder.JSONDecodeError:
        print(f'Файл {my_wl_name} з списком ваших тайтлів пошкоджений')
    except FileNotFoundError:
        print(f'Файл {my_wl_name} з списком ваших тайтлів не знайдено')

def will_be_downloaded_taytl(t:taytl_base)->bool:
    wanted_id = get_taytl_id(t.url)    
    for i in cfg.wl:
        current_id = get_taytl_id(i["url"])
        if current_id == wanted_id:
            return True

    return False

def print_my_list(my_list,my_def,start=1):
    k=start
    print()
    for i in my_list:
        print(f'[{k}]',my_def(i))
        k+=1
    print()

def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

def give_raspis():
    r=requests.get(main_url)
    soup=BeautifulSoup(r.content, 'html.parser')
    items=soup.findAll('div',class_="raspis")
    list=[]
    day=[]
    for i in items:
        aa=i.findAll('a')
        for j in aa:
            day.append(taytl_base(main_url+j['href'],j.text))
        list.append(day.copy())        
        day.clear()   
    return list

def give_urls(taytl_var,start,end,yak):
    taytl_var.set_list_episod()
    zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep
    lll=[[zahal_ep[i-1][0],make_ep_url(zahal_ep[i-1][1],yak)] for i in range(start,end+1)]
    return lll

def give_my_taytl():
    l=giv_end_list_taytls(main_url)
    raspis=give_raspis()[datetime.datetime.today().weekday()]
    future_titles=[]
    new_in_site=[]    
    if len(cfg.end_taytl)!=0:
        set_difference = set(l) - set(cfg.end_taytl)
        new_in_site = list(set_difference)      
    else:
        new_in_site=l
    if len(new_in_site)!=0:
        index=0   
        done=0
        dl=0
        total_length=len(cfg.my_wl['list'])  
        pr=' '   
        for i in cfg.my_wl['list']:
            dl+=1
            done = int(50 * dl / total_length)
            sys.stdout.write(f"\r[%s%s] {pr}" % ('#' * done, '-' * (50-done)) )	
            sys.stdout.flush()
            o=None
            for j in new_in_site:
                qqq=j.give_short_name()
                if i['name']==qqq:
                    o=j
                    break
            if not o:
                if cfg.settings['allchek']:
                    o=taytl(i['url'])
                    pr='*'
                else:
                    index+=1
                    continue
            else:
                pr=' '

            riz=o.giv_kl_ep()-i['ep']
            if riz!=0:
                cop=i.copy()
                cop['+']=riz
                cop['n_wl']=index
                fl=True
                for q in cfg.wl:
                    if q['name']==cop['name']:
                        fl=False
                        break
                if fl:
                    cfg.wl.append(cop)
            index+=1            
    for g in raspis:
        for c in cfg.my_wl['list']:
            g_id = get_taytl_id(g.url)
            if g_id==get_taytl_id(c['url']):
                future_titles.append(g)
                break
    cfg.f_wl=future_titles
    print()
    print()
    cfg.end_taytl=l 
    return cfg.wl,future_titles

def give_history():
    if cfg.history is None:
        try:
            with open(history_file_name, "r") as jsonfile:
                cfg.history = json.load(jsonfile) # Reading the file
        except KeyError:  
            print(f'Файл {history_file_name} з історією пошкоджений')  
        except json.decoder.JSONDecodeError:
            print(f'Файл {history_file_name} з історією пошкоджений')
        except FileNotFoundError:
            cfg.history=[]
            with open(history_file_name, "w") as jsonfile:
                json.dump(cfg.history, jsonfile)
    return cfg.history

def give_viewed_list():
    if cfg.viewed is None:
        try:
            with open(viewed_file_name, "r") as jsonfile:
                cfg.viewed = json.load(jsonfile) # Reading the file
        except KeyError:  
            print(f'Файл {viewed_file_name} з переглянутими тайтлами пошкоджений')  
        except json.decoder.JSONDecodeError:
            print(f'Файл {viewed_file_name} з переглянутими тайтлами пошкоджений')  
        except FileNotFoundError:
            cfg.viewed=[]
            with open(viewed_file_name, "w") as jsonfile:
                json.dump(cfg.viewed, jsonfile)
    return cfg.viewed

def add_in_history(taytl_var,episod = None):
    give_history()
    tat={}
    tat['name']=taytl_var.give_short_name()
    tat['url']=taytl_var.url
    if episod:
        tat["ep"] = episod
    for i in cfg.history:
        if i['name']==tat['name']:
            cfg.history.remove(i)
            break
    cfg.history.insert(0, tat)
    if len(cfg.history) > 40:
        del cfg.history[40:len(cfg.history)]
    with open(history_file_name, "w") as jsonfile:
        json.dump(cfg.history, jsonfile) 

def add_in_viewed_list(taytl_var):
    give_viewed_list()
    tat={}
    tat['name']=taytl_var.give_short_name()
    tat['url']=taytl_var.url
    for i in cfg.viewed:
        if i['name']==tat['name']:
            cfg.viewed.remove(i)
            break
    cfg.viewed.insert(0, tat)
    with open(viewed_file_name, "w") as jsonfile:
        json.dump(cfg.viewed, jsonfile)


def is_taytl_downloaded(taytl:taytl_base)->bool:
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    return get_taytl_id(taytl.url) in cfg.ids_downloaded_taytls.get(date,[])

def test():
    pass

if __name__ == '__main__':
    print('Запустіть main.py')
    # test()
