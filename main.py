print('start program')
#cls; python main.py
 #clear ; python ./main.py 
try:
    from sys import flags 
    import requests # відправка запитів дял отримання коу веб сторінки
    from bs4 import BeautifulSoup # парсинг сторіки
    import inst #мій модуль для завантаження
    from libery  import * #мій модуль з додатковивми фунуціями
    import traceback  #інформація про помилки
    import update
except ImportError as e:
        print("Помилкаа імпорту бібліотеки,введіть 'python -m pip install -r requirements.txt' якщо не допоможк то примусовов обновіть файли")
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

def giv_end_taytls(url):# вертає html з даними про остані тайтли  
    r= requests.get(url)
    if r.status_code!=200:
        print("Error conect to site(list taytl): "+str(r.status_code))
        return None
    soup=BeautifulSoup(r.content, 'html.parser')
    items = soup.find('ul',class_='raspis raspis_fixed')
    el=items.findAll('a')
    return el
    
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
            print(f'Введіть номер тайтлу [1-{len(ll)}] або [0] - вернутись назад > ',end='')
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
            full=False
            while 1 :
                if not full:
                    req=input('(Введіть назву) або [0] - вийти > ')
                    if v=='0':
                        break
                search=give_search_list(req,full,True)
                full=False
                if search==False:
                    print('Нічого ненайдено')
                else:
                    print_list(search)  
                    if full:
                        dop=""
                    else:
                        dop="[+] - більше результатів"                  
                    print(f'Введіть номер тайтлу [1-{len(search)}] {dop} [-] - новий пошук [0]-вихід > ',end='')
                    v=input_v(0,len(search),['+','-'])
                    if v==0:
                        break
                    elif v=='+':
                        full=True
                    elif v=='-':
                        continue
                    else:
                        taytl_var=taytl(search[v-1].url)
                        menu_taytl(taytl_var)
                        break                
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
    #pipreqs --force
    try:
        # global main_url
        # main_url='http://animevost.org'
        global nom_player
        nom_payer=0
        #---
        stan=update.isactual()
        if not stan:
            print('\nДоступне оновлення !!!!\n')
            v=quesBool('Оновити ?')
            if v:
                print('Початок оновлення')                
                update.update()
                print('\nПрограму оновлено, запустіть її щераз')
                exit()
        main()
    except ImportError as e:
        print("Помилкаа імпорту бібліотеки,введіть 'python -m pip install -r requirements.txt' якщо не допоможк то примусовов обновіть файли")
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

