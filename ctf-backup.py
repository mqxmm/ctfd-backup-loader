import requests, wget, os, time
from bs4 import BeautifulSoup
from datetime import datetime

timestmp = str(datetime.now().replace(microsecond=0))

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://localhost:8000/admin/config',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
}

s = requests.Session()
url = "http://localhost:8000/login"

r = s.get(url)
soup = BeautifulSoup(r.content, "html.parser")

nonce = soup.find("input",{"name":"nonce"})['value']

data = {
  'name': 'ADMINLOGIN',
  'password': 'ADMINPASSWORD',
  '_submit': 'Submit',
  'nonce': nonce
}

print('Logging in to '+url+' . .')

s.post(url, data=data, allow_redirects=True)
cookies = s.cookies.get_dict()

print('Downloading the file . .')
backup = requests.get('http://localhost:8000/admin/export', headers=headers, cookies=cookies, allow_redirects=True, stream=True)
path = '/home/kali/backup_dir/'

file_name = os.path.join(path, 'ctfd_backup.zip')

if not os.path.exists(path):
	os.makedirs(path)

open(file_name, 'wb').write(backup.content) 

print('Successfully Exported ['+file_name+']')
