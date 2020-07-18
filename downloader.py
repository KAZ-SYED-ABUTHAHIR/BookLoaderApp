import requests
from requests.exceptions import Timeout
from string import punctuation
import cursor

def downloadFile(flurl: str,size: int,path: str,nm: str,ext: str,numoftrls=10,barstyle='BAR') -> None:
	"""
	Function to download a binary file from the file url supplied as a string in stream mode. Works with CLI.
	<path> is the loaction where the file with name <nm>+'.'+ext  will be stored.
	<ext> is the file extension.
	<flurl> - url of the file to be downloaded as a string.
	<size> should be in bytes to work with the progress bar stuff.
	<numoftrls> is the maximum number of repeated trials to be performed in the case of failure to connect.
	<barstyle> - selects the progress bar to be shown  bar can be {'BAR','TEXT','BAR_CHUNKS','NONE'}
	"""
	flnm = (' '.join([''.join(filter(lambda x: x not in punctuation,word)) for word in nm.split()])).title() + '.' + ext
	CHUNK = 64
	cursor.hide()
	
	for attempt in range(numoftrls):
		try:
			fl = requests.get(flurl,stream = True,timeout = 5.0) 
			if fl:
				with open(path+flnm,'wb') as pdf:
					num_chunks = 0	
					for chunk in fl.iter_content(chunk_size = CHUNK):
						if chunk:
							pdf.write(chunk)
							num_chunks += 1
							num_bytes = num_chunks*CHUNK
							part_completed = int(100*num_bytes/size)

							if barstyle == 'BAR':
								print('\r'+'█'* part_completed + u'\u2591'*(100-part_completed)+' {:.2%}'.format(num_bytes/size),end='\r')
							elif barstyle == 'TEXT':
								print('\r{} bytes of {} bytes downloaded. {:.2%} percent completed.'.format(num_bytes,size,num_bytes/size),end='\r')
							elif barstyle == 'BAR_CHUNKS':
								print('█',end='.')
							elif barstyle == 'NONE':
								print('\r',end='\r')
						elif barstyle == 'BAR_CHUNKS':
							print('X',end='') 
		except Timeout:
			print('Connection Timed out.')					
			print('\rError in connection during downlaoding {}. Retrying...{}'.format(flnm,attempt))
			continue
		else:
			break

	print()
	cursor.show()



def main():
	pass

if __name__ == '__main__':
    main()


