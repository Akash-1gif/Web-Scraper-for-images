import requests
from bs4 import BeautifulSoup
import os

url=input("enter URL:")
try:
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    images=soup.find_all('img')
    n=len(images)
    c=0
    for image in images:
        try:
            link=(image['src'])
        except:
            try:
                link=(image['data-srcset'])
            except:
                try:
                    link=(image['data-src'])
                except:
                    try:
                        link=(image['data-fallback-src'])
                    except:
                        continue
        try:
            s=requests.get(link).content
            with open(f"image{c+1}.jpg","wb+") as f:
                f.write(s)
            print(f"image{c+1}.jpg downloaded")
            c+=1 
        except:
            continue
    if(c==n):
        print("all images downloaded")
    else:
        print(f"{c} out of {n} images downloaded")
except:
    print("error, please check the url")