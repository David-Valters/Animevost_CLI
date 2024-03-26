import subprocess

print('start program')
#cls; python main.py
 #clear ; python ./main.py 
try:
    from sys import flags 
    import requests # відправка запитів дял отримання коду веб сторінки
    from bs4 import BeautifulSoup # парсинг сторіки
    import inst #мій модуль для завантаження
    from libery  import * #мій модуль з додатковивми фунуціями
    import traceback  #інформація про помилки
    import update
except ImportError:
        print("Помилка імпорту бібліотеки,введіть 'python -m pip install -r requirements.txt'")
        exit()
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
            if maxx is not None and v>maxx:
                print('Введене число більше допустимого')
                continue
        except ValueError:
            print('Введіть число ')  
            continue
        return v
        
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
        
        if taytl_var.kl_ep==taytl_var.kl_dop_ep:
            number_last_ep=taytl_var.kl_dop_ep
        else:
            number_last_ep=taytl_var.kl_ep-taytl_var.kl_dop_ep
        while True:
            print(f"[1]-Вибрати декілька серій [2]-вибрати останню серію - ({number_last_ep}) [3]-вибрати все ({taytl_var.kl_ep}) [0]-повернутись назад > ",end='')
            v=input_v(0,3)
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
                v_yakist=quesBool("Вибрати серії в якості 720? інакше 480")
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
                v_yakist=quesBool("Вибрати серії в якості 720? інакше 480")
                if v_yakist:
                    dow_url=make_ep_url(ep[1],720)
                else:
                    dow_url=make_ep_url(ep[1],480)
                return [[ep[0],dow_url]]  
            elif v==3:
                v_yakist=quesBool("Вибрати серії в якості 720? інакше 480")
                if v_yakist:
                    yak=720
                else:
                    yak=480
                zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep
                lll=[[zahal_ep[i][0],make_ep_url(zahal_ep[i][1],yak)] for i in range(0,taytl_var.kl_ep)]
                return lll
            # elif v==4:
            #     new_taytl_var=dop_op(taytl_var)
            #     if new_taytl_var!=None:
            #         taytl_var=new_taytl_var
            #         break
            else:
                print('Не коректне введення!')

def download(list_down,taytl_var:taytl):
    inst.save_from(list_down,taytl_var.give_short_name())

def download_wget(listt,name,path="",trow=False):
    isGood=False
    try:
        name=name.replace('\n', '')
        for i in inst.lb:
            if(name.find(i)!=-1):
                name=name.replace(i, '')
        finish_name=""
        if cfg.settings['addName'] is True:
            finish_name=name

        
        if (inst.get_str_size(name)<=inst.MAX_NAME_SIZE):
            folder_name=name
        else:
            folder_name=inst.get_shortened_name(name, inst.MAX_NAME_SIZE)

        if path=='':
            #path=os.getcwd()+("/Download/"+name)
            path=os.path.join(os.getcwd(),"Download",folder_name)
        else:
            path=os.path.join(path)
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        if (inst.get_str_size(finish_name)>inst.MAX_NAME_SIZE-4):
            finish_name=inst.get_shortened_name(finish_name, inst.MAX_NAME_SIZE-5-inst.get_str_size(listt[-1][0]))            
        for l in listt:
            url=l[1]
            episode_number=l[0]                     
            name_file=episode_number+" "+finish_name+".mp4"
            try:
                final_path=os.path.join(path,name_file)
                print(name_file)
                statis_code=subprocess.call(('wget',"-ct","0","-q","--show-progress" ,"-O",final_path,url))
            except OSError:
                print('OS ERROR')
        if statis_code==0:	
            isGood=True
        elif statis_code==8:
            print("Сервер видав відповідь про помилку, cпробуйте встановити параметру NoAPIDownload значення True")
        else:
            print(f"Помилка wget: {statis_code}")
    except KeyboardInterrupt:
        if trow:
            raise KeyboardInterrupt
        else:
            print("\nЗавантаження перервано")
    except FileNotFoundError:
        print("Програму Wget не знайдено")
    except requests.exceptions.RequestException as e:
        print('Проблема з посиланням для завантаження')
        print(e)
    finally:
        return isGood

    
    
def menu_taytl(taytl_var: taytl):
    add_in_history(taytl_var)
    while True:
        print_info_taytl(taytl_var)
        print('\n[1/Enter] - вибрати епізоди\n[2] - додати в мої тайтли\n[3] - додати в переглянуті\n[4] - інші сезони цього тайтлу\n[5] - додаткова інформація(beta)\n[0] - назад\n> ',end='')
        # list,taytl_var=choice_episod(taytl_var)
        v=input_v(0,5,[''])
        if v==0:
            return
        elif v=='' or v==1 :
            if taytl_var.giv_kl_ep()==0:
                print('Це Анонс,серій ще немає')
                continue
            list_down=choice_episod(taytl_var)
            if list_down is None:
                return
            print('\n[1/Enter] - завантажити [2]-завантажити через wget [3]-добавити в плейліст [0]-назад > ',end='')
            v=input_v(0,3,[''])
            if v==''or v==1:
                download(list_down,taytl_var)
                break
            elif v==2:
                download_wget(list_down, taytl_var.give_short_name())
                break
            elif v==3:
                playlist.append([taytl_var,list_down])
                break
            elif v==0:
                continue
            else:
                print('IT`s BUG !!!')
        elif v==2:
            if cfg.my_wl is None:
                print('Відсутній список ваших тайтлів !')
                n=quesBool('Створити файл зі списком ?')
                if n:
                    create_wl_list()
                else:
                    return None
            name=taytl_var.give_short_name()
            
            size_my_wl=len(cfg.my_wl['list'])
            flag=False
            for i in range(size_my_wl):
                if cfg.my_wl['list'][i]['name']==name:
                    print('Цей тайтл вже є в вашому списку "мої тайтли"\n')
                    flag=True
            if flag:
                break

            tat={}
            tat['name']=name
            tat['url']=taytl_var.url
            if taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep>0:
                print(f'Введіть номер останньої серії яку ви переглядали [0-{taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep}]\nабо [Enter] - остання серія [-] - Назад > ',end='')
                n=input_v(0,taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep,['','-'])
                if n!='-':    
                    if n=='':
                        tat['ep']=taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep
                    else:
                        tat['ep']=n
                else:
                    break
            else:
                tat['ep']=0
            add_taytl_in_wl(tat)
            cfg.end_taytl=[]
            print('Добавлено')
            break
        elif v==3:
            add_in_viewed_list(taytl_var)
            print('Добавлено')
        elif v==4:
            ll=taytl_var.give_all_taytl()
            if ll is None:
                print('Немає інших сезонів')
                continue
            print_taytl(ll)
            print(f'Введіть номер тайтлу [1-{len(ll)}] або [0] - повернутись назад > ',end='')
            v=input_v(0,len(ll))
            if v==0:
                continue
            else:
                taytl_var = taytl(taytl_var.give_all_taytl()[v-1].url)
        elif v==5:
            print(taytl_var.url)

def playlist_def():
    while True:
        size=len(playlist)
        if size==0:
            print('Плейліст пустий, виберіть тайтл-епізоди-добавити в плейліст')
            return None
        print()
        for i in range(0,size):
            print(f'[{i+1}] '+playlist[i][0].name)
        print()
        print('[1/Enter] - Завантажити [2] - Завантажити через wget [3]- Очистити плейліст [4]-Видалити один елемент [0] - Назад > ',end='')
        v=input_v(0,5,[''])
        if v==''or v==1:
            for i in playlist:
                download(i[1],i[0])
            playlist.clear()
            break
        elif v==2:
            for i in playlist:
                # download(i[1],i[0])
                isGood=download_wget(i[1],i[0].give_short_name())
                pass
                if not isGood:
                    continue
                playlist.pop(0)
            break
        elif v==3:
            playlist.clear()
            break
        elif v==4:
            print()
            for i in range(0,size):
                print(f'[{i+1}] '+playlist[i][0].name)
            print()
            print(f'Введіть номер елемента [1-{size}] [0]-скасувати> ',end='')
            v=input_v(0,size)
            if v==0:
                continue
            playlist.pop(v-1)
        elif v==0:
            break
def edit_num_ep(num):
    taytl_var=taytl(cfg.my_wl['list'][num]['url'])
    print(f'Введіть номер останньої серії яку ви переглядали [0-{taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep}]\nабо [Enter] - остання серія > ',end='')
    n=input_v(0,taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep,[''])

    if n=='':
        cfg.my_wl['list'][num]['ep']=taytl_var.giv_kl_ep()-taytl_var.kl_dop_ep
    else:
        cfg.my_wl['list'][num]['ep']=n
    write_mylist() 
    cfg.end_taytl=[]   
    cfg.wl=[]
    print('\nЗмінено')


def main():
    #-- var
    k_ser=6
    # global my_wl
    cfg.my_wl= read_mylist()
    read_ids_viewed_taytls()
    #-- 
    while 1:
        print('\n[1]-Останні тайтли на сайті\n[2]-Посилання на тайтл\n[3]-Пошук\n[4]-Мої тайтли\n[5]-Плейліст\n[6]-Розклад\n[7]-Додатково\n[0]-Вийти\n> ',end='')
        v=input_v(0,7)
        if v==1:
            list=giv_end_list_taytls(main_url)
            if list is None:
                continue  
            print_taytl(list,max=k_ser)  
            flag=True       
            while flag:
                v=input('\nВедіть нормер тайтлу ('+'1-'+str(k_ser)+') або "+" - щоб вивести весь список('+str(len(list))+') 0-Головне Меню > ')
                try:
                    if v == '+':
                        k_ser=len(list)
                        print_taytl(list,max=k_ser)
                    elif int(v)>0 and int(v)<=k_ser:
                        taytl_buf = list[int(v)-1]
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
                    if req=='0':
                        break
                search=give_search_list(req,full,True)
                full=False
                if search is False:
                    print('Нічого ненайдено')
                else:
                    print_taytl(search)  
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
            if cfg.my_wl is None:
                print('Відсутній список ваших тайтлів !')
                n=quesBool('Створити файл зі списком ?')
                if n:
                    create_wl_list()
                else:
                    continue
            print()
            if len(cfg.my_wl['list'])==0:
                print('Ви не добавили ні одного тайтла в "мої тайтли"')
                continue
            print('Завантаження...')
            give_my_taytl()
            fll=True
            if len(cfg.wl)==0:
                print('\nНемає нових серій\n')
                fll=False
            if fll:
                print_my_list(cfg.wl,lambda x:f"{x['name']} - ({x['+']})")            
            print('-----------# Тайтли які сьогодні вийдуть #-----------')
            if len(cfg.f_wl)==0:
                print('\nСьогодні нових серій не буде :(')
            else:
                print_my_list(cfg.f_wl,lambda x:strike(x.name) if is_taytl_downloaded(x) else x.name)
            while True:
                if fll:
                    print('\n[1/Enter] - Завантажити\n[2] - Завантажити через wget\n[3] - Редагувати список моїх тайтлів\n[0] - Головне меню\n> ',end='')
                else:
                    print('\n[3] - Редагувати список моїх тайтлів\n[0] - Головне меню\n> ',end='')
                if fll:
                    v=input_v(0,3,[''])
                else:
                    v=input_v(3,3,['0'])
                if v==0 or v=='0':
                    break
                elif v==1 or v=='':
                    try:
                        print("Завантаження даних...")
                        name_folder=datetime.datetime.today().strftime("%d.%m.%Y")
                        name_folder=os.path.join(os.getcwd(),"Download","My taytls",name_folder)
                        cop_wl=cfg.wl.copy()
                        for j in cop_wl:
                            taytl_var=taytl(j['url'])
                            add_in_history(taytl_var, j['ep'])
                            taytl_var.set_list_episod()          
                            zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep
                            lll=[[zahal_ep[i-1][0],make_ep_url(zahal_ep[i-1][1],720)] for i in range(j['ep']+1,j['ep']+j['+']+1)]
                            stan=inst.save_from(lll,taytl_var.give_short_name(),name_folder,True)
                            if not stan:
                                continue
                            cfg.my_wl['list'][j['n_wl']]['ep']=(j['ep']+j['+'])
                            cfg.wl.remove(j)
                            write_mylist()
                            add_id_to_viewed_taytls(get_taytl_id(j['url']))
                            write_ids_viewed_taytls()
                        break
                    except KeyboardInterrupt:
                        print("\nЗавантаження перервано")
                elif v==2:
                    print("Завантаження даних...")
                    name_folder=datetime.datetime.today().strftime("%d.%m.%Y")
                    name_folder=os.path.join(os.getcwd(),"Download","My taytls",name_folder)
                    cop_wl=cfg.wl.copy()
                    for j in cop_wl:
                        taytl_var=taytl(j['url'])
                        add_in_history(taytl_var, j['ep'])
                        taytl_var.set_list_episod()          
                        zahal_ep=taytl_var.list_ep+taytl_var.list_dop_ep
                        if j['ep']+1 > len(zahal_ep):
                            print(f"\Остання серія ще не доступна ({j['name']})")
                            continue
                        lll=[[zahal_ep[i-1][0],make_ep_url(zahal_ep[i-1][1],720)] for i in range(j['ep']+1,j['ep']+j['+']+1)]
                        # isGood=inst.save_from(lll,taytl_var.give_short_name(),name_folder,True)
                        isGood=download_wget(lll, taytl_var.give_short_name(), name_folder,True)
                        if not isGood:
                            continue
                        cfg.my_wl['list'][j['n_wl']]['ep']=(j['ep']+j['+'])
                        cfg.wl.remove(j)
                        write_mylist()
                        add_id_to_viewed_taytls(get_taytl_id(j['url']))
                        write_ids_viewed_taytls()
                    break
                elif v==3:
                    print('\n[1] - Видалити по номеру\n[2] - Видалити тайтли які вже завершились\n[3] - Змінити номер останньої серії\n[0] - Назад\n> ',end='')
                    v=input_v(0,3)
                    if v==1:
                        while True:
                            count=len(cfg.my_wl['list'])
                            if count==0:
                                print('\nСписок ваших тайтлів пустий\n')
                                break
                            print()
                            print_my_list(cfg.my_wl['list'],lambda i:f"{i['name']} {i['ep']}" )
                            print(f'\nВведіть номер тайтла [1-{count}] щоб видалити зі списку або [0] - Назад  > ',end='')
                            v=input_v(0,count)
                            if v==0:
                                break
                            else:
                                name=cfg.my_wl['list'][v-1]['name']
                                cfg.my_wl['list'].pop(v-1)
                                cfg.end_taytl=[]
                                write_mylist()
                                print(f'Видалено:\n- {name}\n')
                    elif v==2:
                        if cfg.my_wl is None:
                            print('Відсутній список ваших тайтлів !')
                            n=quesBool('Створити файл зі списком ?')
                            if n:
                                create_wl_list()
                            else:
                                continue
                        print()
                        if len(cfg.my_wl['list'])==0:
                            print('Ви не добавили ні одного тайтла в "мої тайтли"')
                            continue
                        done=0
                        dl=0
                        total_length=len(cfg.my_wl['list'])  
                        new_in_site=giv_end_list_taytls(main_url) 
                        list_end=[]
                        for i in cfg.my_wl['list']:
                            dl+=1
                            done = int(50 * dl / total_length)
                            if len(i['name'])>40:
                                print_name=i['name'][:37]+'...'
                            else:
                                print_name=i['name'].ljust(40)                                

                            sys.stdout.write(f"\r[%s%s] {print_name}" % ('#' * done, '-' * (50-done)) )	
                            sys.stdout.flush()
                            if i["ep"]==0:
                                continue
                            o=None
                            for j in new_in_site:
                                if i['name']==j.give_short_name():
                                    o=j
                                    break
                            if not o:
                                o=taytl(i['url'])
                            if o.giv_kl_ep()>=o.giv_end_kl_ep() and o.giv_kl_ep()!=0 :
                                list_end.append(i)
                                add_in_viewed_list(o)

                        if len(list_end)==0:
                            print('\nНемає тайтлів які завершились в вашому списку')
                        else:                            
                            print('\nОбробка...')
                            for g in list_end:                                
                                cfg.my_wl['list'].remove(g)
                            write_mylist()        
                            print_my_list(list_end,lambda x:x['name'])                            
                            print('Ці тайтли видалені з "мої татйли" і переміщені в "Переглянуті"')
                    elif v==3:
                        count=len(cfg.my_wl['list'])
                        while True:
                            print()
                            print_my_list(cfg.my_wl['list'],lambda i:f"{i['name']} {i['ep']}" )
                            print(f'\nВведіть номер тайтла [1-{count}] щоб змінити серію або [0] - Назад  > ',end='')
                            v=input_v(0,count)
                            if v==0:
                                break
                            else:
                                edit_num_ep(v-1)   
                            cfg.end_taytl=[]                    
        elif v==5:
            playlist_def()
        elif v==6:
            ll=give_raspis()
            size_rozk=0
            zagal=[]
            name_day=['Понеділок','Вівторок','Середа','Четвер',"П'ятниця",'Субота','Неділя']
            for i in range(7):
                print(f"-------------------{name_day[i]}-------------------")
                print_my_list(ll[i],lambda x:x.name,size_rozk+1)
                size_rozk+=len(ll[i])
                zagal.extend(ll[i])
            while True:
                print(f'\nВедіть номер тайтла [1-{size_rozk}] щоб вибрати його або [0] - Вийти > ',end='')
                n=input_v(0,size_rozk)
                if n==0:
                    break
                else:
                    var=zagal[n-1]
                    menu_taytl(taytl(var.url))                
        elif v==7:
            print("\n[1] - Історія [2] - Переглянуті [3] - Налаштування(NONE) [0] - Назад > ",end="")
            v=input_v(0,3)
            if v==1:
                hl=give_history()
                if len(hl)>0:
                    print_my_list(hl,lambda x:x['name'])
                    print(f'Ведіть номер тайтла [1-{len(cfg.history)}] або [0] - Назад > ',end="")
                    n=input_v(0,len(cfg.history))
                    if n!=0:
                        n-=1
                        tay=cfg.history[n]
                        tayt=taytl(tay['url'])
                        menu_taytl(tayt)
                else:
                    print('\nВаша історія пуста')
            elif v==2:
                hl=give_viewed_list()
                if len(hl)>0:
                    print_my_list(hl,lambda x:x['name'])
                    print(f'Ведіть номер тайтла [1-{len(cfg.viewed)}] або [0] - Назад > ',end="")
                    n=input_v(0,len(cfg.viewed))
                    if n!=0:
                        n-=1
                        tay=cfg.viewed[n]
                        tayt=taytl(tay['url'])
                        menu_taytl(tayt)
                else:
                    print('\nСписок переглянутих тайтлів пустий')
            elif v==3:
                print('В розробці')
            else:
                pass            
        elif v==0:
            print()
            return 0
        else:
            print('Не коректне введення!')
    
if __name__ == '__main__':
    #pipreqs --force
    #clear; python main.py
    try:
        #global nom_player
        
        global playlist
        playlist=[]

        ex_cod=1
        #TOD upda
        stan=update.isactual()
        if not stan:
            print('\nДоступне оновлення !!!!\n')
            v=quesBool('Оновити ?')
            if v:
                print('Початок оновлення')                
                update.update()
                print('\nПрограму оновлено, запустіть її щераз')
                exit()
        ex_cod=main()
    except ImportError:
        print(' ')
        print("Помилка імпорту бібліотеки,введіть 'python -m pip install -r requirements.txt' якщо не допоможt то примусовов обновіть файли 'python update.py'")
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
        ex_cod=0
    
    if ex_cod!=0:    
        input()