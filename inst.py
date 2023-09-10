import requests
import os
import sys
import math
import cfg

lb=r'<>:"/\|?*'
MAX_NAME_SIZE=250

def get_str_size(s):
    return len(s.encode('utf-8'))

def get_shortened_name(name,max_size):
    P=name.rfind('(')
    if (P!=-1 and  name.find(')')!=-1):
        dop_len=get_str_size(name[P:])
        p=P
        while (get_str_size(name[:p])>max_size-dop_len-2):
            p-=2
        return name[:p]+"..."+name[P:]
    else:
        pos=len(name)
        while(get_str_size(name[:pos])>max_size):
            pos-=2
        return name[:pos]+'...'

def convert_size(size_bytes,write_type=1):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   s='%.2f' % s
   if(write_type):
       return "%s %s" % (s, size_name[i])
   else:
       return s


def down(episode_number, name_file, folder_path, url):
    path=os.path.join(folder_path,name_file)
    with open(path, "wb") as f:
        response = requests.get(url, stream=True, headers={'User-Agent': ''})
        if response.status_code!=200:
                print("Error download episod: "+str(response.status_code))
                return None
        print("Downloading %s" % episode_number)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            finish=f"Done({convert_size(total_length)})             "
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                status=f"{convert_size(dl)}/{convert_size(total_length)}"

                sys.stdout.write(f"\r[%s%s] {(lambda dl: status if dl!=total_length else finish)(dl)}   " % ('#' * done, '-' * (50-done)) )	
                sys.stdout.flush()
            print()
    return True

 
def save_from(listt,name,path="",trow=False):
    stan=False
    try:
        name=name.replace('\n', '')
        for i in lb:
            if(name.find(i)!=-1):
                name=name.replace(i, '')
        finish_name=""
        if cfg.settings['addName'] is True:
            finish_name=name


        if (get_str_size(name)<=MAX_NAME_SIZE):
            folder_name=name
        else:
            folder_name=get_shortened_name(name, MAX_NAME_SIZE)

        if path=='':
            #path=os.getcwd()+("/Download/"+name)
            path=os.path.join(os.getcwd(),"Download",folder_name)
        else:
            path=os.path.join(path)
        
        if not os.path.exists(path):
            os.makedirs(path)
        print(name+'|')
        print(path)
        if (get_str_size(finish_name)>MAX_NAME_SIZE-4):
            finish_name=get_shortened_name(finish_name, MAX_NAME_SIZE-5-get_str_size(listt[-1][0]))            
        for l in listt:
            url=l[1]
            episode_number=l[0]                     
            name_file=episode_number+" "+finish_name+".mp4"
            try:
                stan=down(episode_number, name_file, path, url)
            except OSError:
                print('OS ERROR')	
    except KeyboardInterrupt:
        if trow:
            raise KeyboardInterrupt
        else:
            print("\nЗавантаження перервано")
    except requests.exceptions.RequestException as e:
        print('Проблема з посиланням для завантаження')
        print(e)	
    finally:
        return stan

def main():
    print('Запустіть main.py')

if __name__ == '__main__':
    main()


