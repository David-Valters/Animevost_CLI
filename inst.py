import requests
import os
import sys
import math
#from clint.textui import progress
#v.1.1
lb=r'<>:"/\|?*'

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

def down(file_name,path,url):
	with open(path, "wb") as f:
		response = requests.get(url, stream=True)
		if response.status_code!=200:
				print("Error conect to player: "+str(r.status_code))
				return None
		print("Downloading %s" % file_name)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)
			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = int(50 * dl / total_length)
				sys.stdout.write(f"\r[%s%s] {convert_size(dl,0)}/{convert_size(total_length)}   " % ('#' * done, '-' * (50-done)) )	
				sys.stdout.flush()
			print()

def save_from(listt,name,path=""):
	name=name.replace('\n', '')
	for i in lb:
		if(name.find(i)!=-1):
			name=name.replace(i, '')

	if path=='':
		#path=os.getcwd()+("/Download/"+name)
		path=os.path.join(os.getcwd(),"Download",name)
	else:
		path=os.path.join(path,name)
	
	if not os.path.exists(path):
		os.makedirs(path)
	print(name+'|')
	print(path)
	for l in listt:
		url=l[1]
		name_file=l[0]
		
		
		#print("Start write "+str(name_file))
		path_name=os.path.join(path,name_file+".mp4")
		down(name_file,path_name,url)		
		# with open(path_name, 'wb') as f:
		#     total_length = int(r.headers.get('content-length'))
		#     for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
		#         if chunk:
		#             f.write(chunk)
		#             f.flush()
		# print("End write "+str(name_file))

def main():
	url=[['1 серія','https://hd.trn.su/720/2147418055.mp4?md5=cKZR2TSd6M1bGl9E6cXxQA&time=1617988234&d=1']]
	save_from(url,'defaul')

if __name__ == '__main__':
	main()


