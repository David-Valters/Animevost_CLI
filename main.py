print('start program')
import requests
from bs4 import BeautifulSoup
import inst
#v.0.8.0.2

def gethtml(url,name_file):
	r= requests.get(url)#,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'})
	return r
	
def get_list_ep(name_file):
	with open(name_file, 'r',encoding='utf-8') as f:
		text=f.read()
		ft='var data = '
		i1=text.find(ft)
		i2=text.find('}',i1)
		
		text2=text[i1+len(ft)+1:i2-1]

		sps=text2.split(',')
		return sps
		#print(sps[-2])
		#print(text[i1+len(ft)+1:i2-1])

def get_url(n_ser,yakist):
	#print("***",n_ser)
	if not(yakist==480 or yakist == 720):
		print('nemaye takoi yakosti: '+str(yakist))
		return None
	n_ser=n_ser.split(':')[1][1:-1]
	ss='https://play.animegost.org/'+str(n_ser)+'?player=9'
	r= requests.get(ss)
	if r.status_code!=200:
		print("Error conect to player: "+str(r.status_code))
		return None
	soup=BeautifulSoup(r.content, 'html.parser')
	items = soup.find('a',class_='butt')
	if yakist==720:
		items=items.next.next.next
	url=items.get('href')
	return url
def all_url(kl_ep):
	print('Формується список url для загрузки')
	
def giv_list_taytls():
	main_url='http://animevost.org'
	r= requests.get(main_url)
	if r.status_code!=200:
		print("Error conect to site(list taytl): "+str(r.status_code))
		return None
	soup=BeautifulSoup(r.content, 'html.parser')
	items = soup.find('ul',class_='raspis raspis_fixed')
	el=items.findAll('a')#[0].next.text#get('href')
	return el
def give_name(url):
	r= requests.get(url)
	if r.status_code!=200:
		print("Error conect to site(name taytl): "+str(r.status_code))
		return None
	soup=BeautifulSoup(r.content, 'html.parser')
	items = soup.find('h1')
	el=items.text#.find('a')#[0].next.text#get('href')
	while el[0]==' ' or el[0]=='\n' :
		el=el[1:]
	return el

def giv_kl_ep(name):
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

def the_end(n_f):
	with open(n_f, 'w') as f:
		f.write("ss")

def main():
	n_f="a.out"
	k_ser=6
	while 1:		
		v=input('\n1-остані тайтли на сайті 2-силка на тайтл 3-вийти ')
		if v=='2':
			html=input('url:')
			name_title=give_name(html)
			print(f'''/-----------------------------------\n{name_title}\n/-----------------------------------''')
			html=gethtml(html,n_f)

		elif v=='1':
			list_tt=giv_list_taytls()
			if(list_tt==None):
				return			
			while 1:
				for i in range (0,k_ser):
					print(str(i+1)+'# '+list_tt[i].text)
				print('\nВедіть нормер тайтлу ('+'1-'+str(k_ser)+') або\n+ - щоб вивести весь список('+str(len(list_tt))+')')
				v=input()			
				if v == '+':
					for i in range (0,len(list_tt)):
						print(str(i+1)+'# '+list_tt[i].text)
						k_ser=len(list_tt)
				elif int(v)>0 and int(v)<=k_ser:#len(list_tt):
					html=gethtml(list_tt[int(v)-1].get('href'),n_f)	
					name_title=list_tt[int(v)-1].text
					break	
				else:
					print('Не коректне введення!')		
		elif v=='3':
			break
		else:
			print('Не коректне введення!')
			continue

		if html.status_code==200:
			with open(n_f, 'w',encoding='utf-8') as f:
				f.write(html.text)	
		else:
		 	print("Error conect to site : "+str(html.status_code))
		 	the_end(n_f)
		 	return None
		list_ep=get_list_ep(n_f)
		the_end(n_f)
		kl=giv_kl_ep(name_title)
		if kl==0:
			print('Ще немає серій, це Анонс')
			continue
		name_tt=name_title
		name_tt=name_tt[:name_tt.find('/')][:-1]
		#print(name_tt)
		while 1 :
			v=int(input('0-Вихід 1-Скачати серії 2-получити силку на потік 3-на головну : '))
			if v ==1:
				#print('номер серії ',ppp)
				#print('силка ',url_ep)
				#print('назва тайтла ',name_tt)

				start=int(input(f"З якої серії начти скачування(1-{kl})? "))
				end=int(input(f"По яку серію скачувати(1-{kl})? "))
				lll=[[f'{i} серія',get_url(list_ep[i-1],720)] for i in range(start,end+1)]
				inst.save_from(lll,name_tt)
				#https://animevost.org/tip/tv/2582-shaman-king-2021.html
				#inst.save_from([[ppp,url_ep]],name_tt)
				#inst.save_from(url_ep,ppp+' '+name_tt+".mp4")
			elif v==2:
				#import os
				while 1 :
					v=int(input('Ведіть номер серії (1-'+str(kl)+') : '))
					if v >= 1 and v <= kl:
						break
					else:
						print('Немає такої серії')

				url_ep=get_url(list_ep[v-1],720)
				if(url_ep==None):
					return
				print(url_ep)
				#os.system(r'"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"'+url_ep)
			elif v==0:
				return 1
			elif v==3:
				break
			else:
				print('Не коректне введення!')
'''
	n_f="a.out"
	
	list_tt=giv_list_taytls()
	if(list_tt==None):
		return
	k_ser=6
	for i in range (0,k_ser):
		print(str(i+1)+'# '+list_tt[i].text)

	while 1:
		print('Ведіть нормер тайтлу ('+'1-'+str(k_ser)+') або\n+ - щоб вивести весь список('+str(len(list_tt))+') \n0 - щоб вийти')
		v=input()
		if v == '+':
			for i in range (0,len(list_tt)):
				print(str(i+1)+'# '+list_tt[i].text)
				k_ser=len(list_tt)
		elif int(v)==0:
			break
		elif int(v)>0 and int(v)<=k_ser:#len(list_tt):
			html=gethtml(list_tt[int(v)-1].get('href'),n_f)
		# # print('cod '+str(html.status_code))
			if html.status_code==200:
				with open(n_f, 'w',encoding='utf-8') as f:
					f.write(html.text)	
			else:
			 	print("Error conect to site : "+str(html.status_code))
			 	the_end(n_f)
			 	return None

			list_ep=get_list_ep(n_f)
			the_end(n_f)
			kl=giv_kl_ep(list_tt[int(v)-1].text)
			if kl==0:
				print('Ще немає серій, це Анонс')
				continue
			name_tt=list_tt[int(v)-1].text
			name_tt=name_tt[:name_tt.find('/')][:-1]
			#print(name_tt)
			while 1 :
				v=int(input('Ведіть номер серії (1-'+str(kl)+') : '))
				if v >= 1 and v <= kl:
					break
				else:
					print('Немає такої серії')
			
			url_ep=get_url(list_ep[v-1],720)
			if(url_ep==None):
				return
			print(url_ep)
			ppp=list_ep[v-1].split(':')[0][1:-1]
			while 1 :
				v=int(input('0-Вихід 1-Скачати серію 2-запустити в vlc 3-Повторити : '))
				if v ==1:
					#print('номер серії ',ppp)
					#print('силка ',url_ep)
					#print('назва тайтла ',name_tt)
					inst.save_from([[ppp,url_ep]],name_tt)
					#inst.save_from(url_ep,ppp+' '+name_tt+".mp4")
				elif v==2:
					#import os
					print('в розробці')
					#os.system(r'"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"'+url_ep)
				elif v==0:
					return 1
				elif v==3:
					break
				else:
					print('Не коректне введення!')
		else:
			print('Не коректне введення!')
'''


	#url='https://animevost.org/tip/tv/1894-black-clover5.html'
	# url='https://animevost.org/tip/tv/2553-243-seiin-koukou-danshi-volley-bu.html'

	# html=gethtml(url,n_f)
	# # print('cod '+str(html.status_code))
	# if html.status_code==200:
	# 	with open(n_f, 'w',encoding='utf-8') as f:
	# 		f.write(html.text)	
	# else:
	#  	print("Error conect to site(): "+str(html.status_code))
	#  	return None

	# list_ep=get_list_ep(n_f)

	# url_ep=get_url(list_ep[-2],480)
	# if(url_ep==None):
	# 	return

	# print(url_ep)


	# with open(n_f, 'w') as f:
	# 	f.write("ss")


if __name__ == '__main__':
	main()