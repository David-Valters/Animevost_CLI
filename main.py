print('start program')
#cls; python main.py
 #clear ; python ./main.py 
from sys import flags 
import requests # відправка запитів дял отримання коу веб сторінки
from bs4 import BeautifulSoup # парсинг сторіки
import inst #мій модуль для завантаження
import libery #мій модуль з додатковивми фунуціями
import traceback  #інформація про помилки
import re # регулярки
import update

 
def input_v(min:int,maxx:int=None,list=[])->int:
    while True:
        try:
            v=input()
            if list!=[]:
                for i in list:
                    if i==v:
                        return i
            v=int(v)
            if v<min:
                print('Введене число менше допустимого')
                continue
            if maxx!=None and v>maxx:
                print('Введене число більше допустимого')
                continue
        except ValueError:
            print('Введіть число ')  
            continue
        return v
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
        
    def __init__(self, url, name=None,kl_ep=0,list_ep=None,list_dop_ep=None,soup=None):
        
        super().__init__(url,name)
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

def giv_end_taytls(url):# вертає html з даними про остані тайтли  
    r= requests.get(url)
    if r.status_code!=200:
        print("Error conect to site(list taytl): "+str(r.status_code))
        return None
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.find('ul',class_='raspis raspis_fixed')
    el=items.findAll('a')
    return el

def print_list(list,min=0,max=None):
    print()
    if max==None:
        max=len(list)
    for i in range(0,len(list)):
        if(i<max):
            print(f'[{i+1+min}] '+list[i].name)
        else:
            break
    print()


def giv_end_list_taytls(url):#вертає список обєктів taytl
    el=giv_end_taytls(url)
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
def print_info_taytl(taytl_var: taytl):
    print(f"\nName: {taytl_var.name}")
    print(f"Серій {taytl_var.kl_ep} ",end="")
    if taytl_var.kl_dop_ep!=0:
        print(f"({taytl_var.kl_dop_ep} спешлів)")    
    else:
        print()

def choice_episod(taytl_var: taytl):
    while True:
        taytl_var.set_list_episod()
        print_info_taytl(taytl_var)
        if taytl_var.kl_ep==taytl_var.kl_dop_ep:
            number_last_ep=taytl_var.kl_dop_ep
        else:
            number_last_ep=taytl_var.kl_ep-taytl_var.kl_dop_ep
        while True:
            print(f"[1]-Вибрати декілька серій [2]-вибрати останню серію - ({number_last_ep}) [3]-вибрати все ({taytl_var.kl_ep}) [4] - додаткові можливочті [0]-Головне Меню > ",end='')
            v=input_v(0,4)
            if v==0:
                print()
                return None
            elif v==1:            
                if taytl_var.kl_dop_ep!=0:
                    if taytl_var.kl_dop_ep==1:
                        spesh_info=f" {taytl_var.kl_ep}-спешл "
                    else:
                        spesh_info=f" {taytl_var.kl_ep-taytl_var.kl_dop_ep+1}-{taytl_var.kl_ep} спешли "
                else:
                    spesh_info=""
                print(f"З якої серії почати завантажування(1-{taytl_var.kl_ep}){spesh_info}? ",end='')
                start=input_v(1,taytl_var.kl_ep)
                print(f"По яку серію завантажувати({start}-{taytl_var.kl_ep}){spesh_info}? ",end='')
                end=input_v(start,taytl_var.kl_ep)
                v_yakist=libery.quesBool("Завантажувати серії в якості 720? інакше 480")
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
                v_yakist=libery.quesBool("Завантажувати серію в якості 720? інакше 480")
                if v_yakist:
                    dow_url=make_ep_url(ep[1],720)
                else:
                    dow_url=make_ep_url(ep[1],480)
                return [[ep[0],dow_url]]   
            elif v==3:
                v_yakist=libery.quesBool("Завантажувати серії в якості 720? інакше 480")
                if v_yakist:
                    yak=720
                else:
                    yak=480
                zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep
                lll=[[zahal_ep[i][0],make_ep_url(zahal_ep[i][1],yak)] for i in range(0,taytl_var.kl_ep)]
                return lll
            elif v==4:
                new_taytl_var=dop_op(taytl_var)
                if new_taytl_var!=None:
                    taytl_var=new_taytl_var
                    break
            else:
                print('Не коректне введення!')

def dop_op(taytl_var: taytl):
    while True:
        print('[1] - інші сезони цього тайтлу [2] - (NEW) [3]-(NEW) [0] - вернутись назад > ',end='')
        v=input_v(0,2)
        if v==1:
            # print('hzz',taytl_var.name)
            ll=taytl_var.give_all_taytl()
            if ll==None:
                print('Немає інших сезонів')
                continue
            print_list(ll)
            print(f'Введіть номер тайтлу [1]-{len(ll)} або [0] - вернутись назад > ',end='')
            v=input_v(0,len(ll))
            if v==0:
                return None
            else:
                taytl_var = taytl(taytl_var.give_all_taytl()[v-1].url)
                return taytl_var
        elif v==2:
            # додаткова інформація
            print(' В розробці :)')
        elif v==3:
            # добавити в дивлюся
            print(' В розробці :)')
        elif v==0:
            print()
            return None

def menu_episods(list_down,taytl):
    download(list_down,taytl)
def download(list_down,taytl_var):
    name_tt=taytl_var.name[:taytl_var.name.find('/')][:-1]
    inst.save_from(list_down,name_tt)

def menu_taytl(taytl_var: taytl):
    list=choice_episod(taytl_var)
    if list==None:
        return
    menu_episods(list,taytl_var)
def main():
    #-- var
    k_ser=6
   
    #-- 
    while 1:
        print('\n\n[1]-Останні тайтли на сайті [2]-Посилання на тайтл [3]-Пошук [4]-Ваші нові серії [5]-Налаштування [0]-Вийти > ',end='')
        v=input_v(0,5)
        if v==1:
            list=giv_end_list_taytls(main_url)  
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
                            continue
                        taytl_var = taytl(taytl_buf.url,taytl_buf.name)
                        flag=False
                        menu_taytl(taytl_var)
                    elif v=='0':
                        flag=False
                    else:
                        print('Не коректне введення!')
                except ValueError:
                    print("Введіть число або '+'")
        elif v==2:
            url=input('Введіть url: ')
            taytl_var=taytl(url)
            menu_taytl(taytl_var)
        elif v==3:
            print('В розробці')
        elif v==4:
            print('В розробці')
        elif v==5:
            print('В розробці')
        elif v==0:
            print()
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
                print('\nПрограму оновлено, запустіть її щераз')
                exit()
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

