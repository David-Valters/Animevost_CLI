import requests
import os
from clint.textui import progress
#v.1.1
lb=r'<>:"/\|?*'


def save_from(listt,name):

	name  =name.replace('\n', '')
	for i in lb:
		if(name.find(i)!=-1):
			name=name.replace(i, '')
	if not(os.path.isdir(name)):
		os.mkdir(name)
	print(name+'|')
	for l in listt:
		url=l[1]
		name_file=l[0]
		r = requests.get(url, stream=True)
		if r.status_code!=200:
			print("Error conect to player: "+str(r.status_code))
			return None
		print("Start write "+str(name_file))
		with open(name+'/'+name_file+'.mp4', 'wb') as f:
		    total_length = int(r.headers.get('content-length'))
		    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
		        if chunk:
		            f.write(chunk)
		            f.flush()
		print("End write "+str(name_file))

def main():
	url=[['1 серія','https://hd.trn.su/720/2147418055.mp4?md5=cKZR2TSd6M1bGl9E6cXxQA&time=1617988234&d=1']]
	save_from(url,'defaul')

if __name__ == '__main__':
	main()


