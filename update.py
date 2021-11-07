import requests
import os
import sys

import libery

ver='v1.0.1'
url_ver='https://api.github.com/repos/David-Valters/Animevost_CLI/releases'
url_file_list='https://api.github.com/repos/David-Valters/Animevost_CLI/git/trees/main?recursive=1'





def give_list_file():
    response=requests.get(url_file_list)
    jsonResponse = response.json()
    list=[]
    for i in jsonResponse['tree']:
        list.append(i['path'])
    return list

def isactual()->bool:
    response=requests.get(url_ver)
    jsonResponse = response.json()
    return jsonResponse[0]['name']==ver

def update(prin=1): 
    if prin:
        print('Початок оновлення') 
    list=give_list_file()
    for i in list:
        _, file_extension = os.path.splitext(i)
        if file_extension=='.py':
            path=os.path.join(libery.get_script_dir(),i)
            r=requests.get(f'https://raw.githubusercontent.com/David-Valters/Animevost_CLI/main/{i}')
            print(i,path)
            with open(path, "wb") as f:
                f.write(r.content)
    if prin:
        print('Файли програми оновлені')

if __name__ == '__main__':
    if len(sys.argv)>1:
        print('тиха')
        update()
        from subprocess import Popen
        Popen(['python',os.path.join(libery.get_script_dir(),'main.py'),'arg2'], shell=True)
        exit()
    else:   
        stan=isactual()
        if stan:
            print('Програма актуальна')
            v=libery.quesBool('Обновити файли (закрийте перед оновленням основну програму)?',0)
            if v:
                update()
        else:
            print('Доступне оновлення !!!')
            v=libery.quesBool('Оновити (закрийте перед оновленням основну програму)?')
            if v:           
                update()
            