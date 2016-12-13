#!/usr/bin/env python
# coding: utf-8

"""
@author: VegetableCat
"""
import argparse,sys,os,requests,re
from bs4 import BeautifulSoup

url = "https://www.javbus.com/"


#proxy default config
proxy = {
        'http':'socks5://127.0.0.1:1080',
        'https':'socks5://127.0.0.1:1080',
}




def main():
    # get avID
    parser = argparse.ArgumentParser(description='Find magnetlink and download cover image via javID')
    parser.add_argument('-i','--id',help='avcode you want to download' ,dest='id',default=None)
    parser.add_argument('-p','--proxy',help='set your own HTTP/socks5',dest='proxy',default=None)

    args = parser.parse_args()

    avcode = args.id
    proxies = args.proxy


    if avcode == None:
        parser.print_help()
        sys.exit(-1)
    #insert '-'
    if avcode.find("-") == -1:
        i=0
        l = list(avcode)
        for a in l:
            if a.isdigit():
                l.insert(i,'-')
                break
            i=i+1
        if not l[0]=='n':#tokyohot
            avcode = ''.join(l)

    #set proxy address
    if not proxies == None:
        proxy['http'] = proxies
        proxy['https'] = proxies
        print '[*] proxyurl set to ' + proxies


    #change directory to library

    cwd = os.getcwd()
    print "[*] Current working directory",cwd
    wd = cwd+"/"+"library"
    if not os.path.exists(wd):
        os.mkdir(wd)

    os.chdir(wd)



    get_av_magnet(avcode)


def download_image_over_socks5(img_src):

    ir = requests.get(img_src,proxies=proxy)
    if ir.status_code == 200:
        open(img_src.split(".")[-2].split("/")[-1]+os.path.splitext(img_src)[1], 'wb').write(ir.content)
    print '[-] '+img_src.split(".")[-2].split("/")[-1]+" done!"



def download_image(avcode):

    s = requests.Session()

    r = s.get(url+avcode, proxies=proxy)
    gid = re.findall(r'[\d]{10,11}',r.text)
    #gid 10-11

    soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'),'html.parser')

    #get name
    name_node = soup.find('h3')

    name = name_node.text
    print '[*] '+name

    cwd = os.getcwd()
    wd = cwd+"/"+name
    if not os.path.exists(wd):
        os.mkdir(wd)
    os.chdir(wd)

    print "[*] Downloading cover image"
    img_node = soup.find('a', attrs={"class":"bigImage"})
    img_src = img_node.get('href')
    download_image_over_socks5(img_src)

    #sample picture
    print '[*] Downloading sample image'
    sample_node = soup.findAll('a',class_="sample-box")
    for sample in sample_node:
        sample_src = sample.get('href')
        download_image_over_socks5(sample_src)


    return gid


    #todo：download image
def get_av_magnet(avcode):



    uc = 0 #?
    lang = "zh"
    Referer={
    "Referer": "123"
    }

    s = requests.Session()
    gid = download_image(avcode)

    r2 = s.get("http://www.javbus.com/ajax/uncledatoolsbyajax.php?gid="+str(gid[0])+"&lang=zh&uc=0", proxies=proxy, headers=Referer)
    soup = BeautifulSoup(r2.content.decode('utf-8', 'ignore'),'html.parser')

    trs  = soup.findAll('tr',attrs={"height":"35px"})
    print '[*] get magnet link'
    for tr in trs:
        trsoup = BeautifulSoup(str(tr).decode('utf-8', 'ignore'),'html.parser')
        td2 = trsoup.findAll('td',attrs={"style":"text-align:center;white-space:nowrap"})
        a = td2[0].find('a')
        magnet = a.get("href") #unicode object
        size = a.text.strip()
        print '[*] '+magnet,size

    os.chdir("../..")






if __name__ == '__main__':
    main()
