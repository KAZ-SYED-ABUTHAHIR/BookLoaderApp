import requests
from requests.exceptions import Timeout
from string import punctuation
import cursor

def downloadFile(fileURL,path=None,fileName=None,fileExtension=None,size=None,numOfTrials=10,barStyle='BAR',proxies=None) -> None:
    """
    Function to download a binary file from the file url supplied as a string in stream mode. Works with CLI.
    <path> is the loaction where the file with name <nm>+'.'+ext  will be stored.
    <fileExtension> is the file extension.
    <fileURL> - url of the file to be downloaded as a string.
    <size> should be in bytes to work with the progress bar stuff.
    <numOfTrials> is the maximum number of repeated trials to be performed in the case of failure to connect.
    <barStyle> - selects the progress bar to be shown  bar can be {'BAR','TEXT','BAR_CHUNKS','NONE'}
    """
    if fileName:
        fileName = (' '.join([''.join(filter(lambda x: x not in punctuation,word)) for word in fileName.split()])).title() + '.' + fileExtension
    CHUNK = 64
    cursor.hide()
    
    for attempt in range(numOfTrials):
        try:
            user_agent = {'User-agent': 'Mozilla/5.0'}
            fl = requests.get(fileURL, headers=user_agent, stream=True, proxies=proxies)
            print(fl.headers)
            print(fl.headers['Content-Length'])
            if not fileName:
                try:
                    fileName = fl.headers['filename']
                except Exception as err:
                    fileName = 'defaultFileName.ext'
                    print(f"Error: {err}")
            if not size:
                try:
                    size = int(fl.headers['Content-Length'])
                except Exception as err:
                    print(f"Error: {err}")
            if fl.ok:
                with open(path+fileName,'wb') as binContent: #Binary Content of the File Object
                    num_chunks = 0	
                    for chunk in fl.iter_content(chunk_size = CHUNK):
                        if chunk:
                            if size is not None:
                                binContent.write(chunk)
                                num_chunks += 1
                                num_bytes = num_chunks*CHUNK
                                part_completed = int(100*num_bytes/size)

                            if barStyle == 'BAR':
                                print('\r'+'█'* part_completed + u'\u2591'*(100-part_completed)+' {:.2%}'.format(num_bytes/size),end='\r')
                            elif barStyle == 'TEXT':
                                print('\r{} bytes of {} bytes downloaded. {:.2%} percent completed.'.format(num_bytes,size,num_bytes/size),end='\r')
                            elif barStyle == 'BAR_CHUNKS':
                                print('█',end='.')
                            elif barStyle == 'NONE':
                                print('\r',end='\r')
                        elif barStyle == 'BAR_CHUNKS':
                            print('X',end='') 
        except Exception as err:
            print(f'Error: {err}')
            print('Connection Timed out.')					
            print('\rError in connection during downlaoding {}. Retrying...{}'.format(fileName,attempt))
            continue
        else:
            break

    print()
    cursor.show()


def downloadSimple(url, pathName):
    """ A Simple download function without streaming
        pathName must be c:\\path\\to\\the\\file\\name.ext
    """
    rspns = requests.get(url)
    if rspns.ok:
        with open(pathName,'wb') as fl:
            fl.write(rspns.content)

def main():
    #https://drive.google.com/uc?export=download&id=1YBKvLugC9uuA67Ya-QwcWPQa40l0XU8b

    pdfLink = "https://drive.google.com/uc?export=download&id=1YBKvLugC9uuA67Ya-QwcWPQa40l0XU8b"
    downloadFile(pdfLink,"C:\\Users\\KAZ\\Desktop\\")
if __name__ == '__main__':
    main()



