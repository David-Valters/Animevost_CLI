print('start program')
#cls; python main.py
#clear ; python ./main.py 
print('start import libery')
from sys import flags 
import requests # відправка запитів дял отримання коу веб сторінки
from bs4 import BeautifulSoup # парсинг сторіки
import inst #мій модуль для завантаження
import traceback  #інформація про помилки
import os #системні команди типу читання і запису
import re # регулярки
import update
import sys

import libery

print('end import libery')

update.isactual()



 
def input_num(min:int,max:int)->int:
    while True:
        try:
            v=int(input())
            if v<min:
                print('Введене число менше допустимого')
                continue
            if v>max:
                print('Введене число більше допустимого')
                continue
        except ValueError:
            print('Введіть число ')  
            continue
        return v

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
class taytl_base:
    def __init__(self,url,name=""):
        self.name=name
        self.url=url
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

        
        
    def __init__(self, url, name=None,kl_ep=0,list_ep=None,list_dop_ep=None,soup=None):
        super().__init__(url,name)
        r= requests.get(url)
        if r.status_code!=200:
            print("Error conect to site(information about the series): "+str(r.status_code))
        soup=BeautifulSoup(r.content, 'html.parser')
        self.kl_dop_ep=0
        if list_ep==None:
            self.list_ep=None
        if list_dop_ep==None:
            self.list_dop_ep=None
        if kl_ep==0:
            self.kl_ep=0

        # file = open('sorc_site.txt',mode='r', encoding='utf-8')
        # cont = file.read()
        # file.close()
        # soup=BeautifulSoup(cont, 'html.parser')

        self.soup=soup
        items = soup.find('h1')
        name=items.text
        while name[0]==' ' or name[0]=='\n' :
            name=name[1:]
        self.name=name
        self.kl_ep=super().giv_kl_ep()
        

        
        
        
    



def giv_end_taytls():# вертає html з даними про остані тайтли
    
    r= requests.get(main_url)
    if r.status_code!=200:
        print("Error conect to site(list taytl): "+str(r.status_code))
        return None
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.find('ul',class_='raspis raspis_fixed')
    el=items.findAll('a')
    return el

def print_list(list,min=0,max=None):
    if max==None:
        max=len(list)
    for i in range(0,len(list)):
        if(i<max):
            print(f'[{i+1+min}] '+list[i].name)
        else:
            break


def giv_end_list_taytls():#вертає список обєктів taytl
    el=giv_end_taytls()
    s=[]
    for i in el:
        s.append(taytl_base(i['href'],i.text))
    return s
def make_ep_url(kod:str,quality:int=720)->str:
    global nom_payer
    urls_player=[f"https://play.agorov.org/{kod}?old=1",f"https://play.animegost.org/{kod}?player=9"]
    while True:
        r= requests.get(urls_player[nom_payer])
        if r.status_code!=200:
            print(f"Error conect to base -{nom_payer+1}-: "+str(r.status_code))
            print("Start use next base")
            if len(urls_player)==nom_payer+1:
                print("E R R O R conect to base`s")
                return None
            else:
                nom_payer=nom_payer+1
        else:
            break
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.findAll('a',class_="butt")

    if quality==480:
        return items[0]["href"]
    elif quality==720:
        return items[1]["href"]
    else:
        print('Немає такої якості')
        return None
    
def choice_episod(taytl_var: taytl):
    taytl_var.set_list_episod()
    print(f"\nName: {taytl_var.name}")
    print(f"Серій {taytl_var.kl_ep} ",end="")
    if taytl_var.kl_dop_ep!=0:
        print(f"({taytl_var.kl_dop_ep} спешлів)")    
    else:
        print()
    if taytl_var.kl_ep==taytl_var.kl_dop_ep:
        number_last_ep=taytl_var.kl_dop_ep
    else:
        number_last_ep=taytl_var.kl_ep-taytl_var.kl_dop_ep

    while True:
        v=input(f"1-Вибрати декілька серій 2-вибрати останню серію - {number_last_ep} 3-вибрати все ({taytl_var.kl_ep}) 0-Головне Меню > ")
        try:
            v=int(v)
        except ValueError:
            print('Введіть число ')  
            continue
        if v==0:
            break
        elif v==1:
            if taytl_var.kl_dop_ep!=0:
                if taytl_var.kl_dop_ep==1:
                    spesh_info=f" {taytl_var.kl_ep}-спешл "
                else:
                    spesh_info=f" {taytl_var.kl_ep-taytl_var.kl_dop_ep+1}-{taytl_var.kl_ep} спешли "
            else:
                spesh_info=""
            print(f"З якої серії начати скачування(1-{taytl_var.kl_ep}){spesh_info}? ")
            start=input_num(1,taytl_var.kl_ep)
            print(f"По яку серію скачувати({start}-{taytl_var.kl_ep}){spesh_info}? ")
            end=input_num(start,taytl_var.kl_ep)
            v_yakist=quesBool("Завантажувати серії в якості 720? інакше 480")
            if v_yakist:
                yak=720
            else:
                yak=480
            zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep

            lll=[[zahal_ep[i-1][0],make_ep_url(zahal_ep[i-1][1],yak)] for i in range(start,end+1)]
            return lll
        elif v==2:
            if taytl_var.kl_ep==taytl_var.kl_dop_ep:
                ep=taytl_var.list_dop_ep[-1]
            else:
                ep=taytl_var.list_ep[-1]
            v_yakist=quesBool("Завантажувати серію в якості 720? інакше 480")
            if v_yakist:
                dow_url=make_ep_url(ep[1],720)
            else:
                dow_url=make_ep_url(ep[1],480)
            return [[ep[0],dow_url]]   
        elif v==3:
            v_yakist=quesBool("Завантажувати серії в якості 720? інакше 480")
            if v_yakist:
                yak=720
            else:
                yak=480
            zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep
            lll=[[zahal_ep[i][0],make_ep_url(zahal_ep[i][1],yak)] for i in range(0,taytl_var.kl_ep)]
            return lll
        else:
            print('Не коректне введення!')

def download(taytl_var: taytl):
    list_down=choice_episod(taytl_var)
    name_tt=taytl_var.name[:taytl_var.name.find('/')][:-1]
    inst.save_from(list_down,name_tt)

def main():
    #-- var
    k_ser=6
   
    #-- 
    while 1:
        print('\n\n1-Останні тайтли на сайті 2-Посилання на тайтл 3-Пошук 4-Ваші нові серії 5-Налаштування 0-Вийти > ')
        v=input_num(0,5)
        if v==1:
            list=giv_end_list_taytls()  
            print_list(list,max=k_ser)  
            flag=True       
            while flag:
                v=input('\nВедіть нормер тайтлу ('+'1-'+str(k_ser)+') або "+" - щоб вивести весь список('+str(len(list))+') 0-Головне Меню> ')
                try:
                    if v == '+':
                        k_ser=len(list)
                        print_list(list,max=k_ser)
                    elif int(v)>0 and int(v)<=k_ser:
                        taytl_buf = list[int(v)-1]
                        if taytl_buf.giv_kl_ep()==0:
                            print('Це Анонс,серій ще немає')
                            flag=False
                        taytl_var = taytl(taytl_buf.url,taytl_buf.name)
                        flag=False
                        download(taytl_var)
                    elif v=='0':
                        flag=False
                    else:
                        print('Не коректне введення!')
                except ValueError:
                    print("Введіть число або '+'")
        elif v==2:
            url=input('Введіть url: ')
            taytl_var=taytl(url)
            download(taytl_var)
        elif v==3:
            print('В розробці')
        elif v==4:
            print('В розробці')
        elif v==5:
            print('В розробці')
        elif v==0:
            return 0
        else:
            print('Не коректне введення!')
    
if __name__ == '__main__':
    try:
        global main_url
        main_url='http://animevost.org'
        global nom_player
        nom_payer=0
        #---
        stan=update.isactual()
        if not stan:
            print('\nДоступне оновлення !!!!\n')
            v=libery.quesBool('Оновити ?')
            if v:
                print('Початок оновлення')                
                update.update()
                os.execv(sys.executable, [sys.executable] + sys.argv)
        main()
    except requests.ConnectionError as e:
        print("OOPS!! Помилка з'єднання. Переконайтеся, що ви підключені до Інтернету.\n")
        print(str(e))			
        
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("\n\nOOPS!! Загальна помилка\nВідправте дані полмилки мені в телеграм @sendmesmebot")
        print(str(e))
        print (traceback.format_exc())
        
    except KeyboardInterrupt:
        print("\nХтось закрив програму")
