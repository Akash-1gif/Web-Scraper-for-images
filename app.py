from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        url = request.form['web_link']
        messages=[]
        print("url obtained from user")
        try:
            r=requests.get(url)
            print("website obtained")
            soup=BeautifulSoup(r.text,'html.parser')
            print("website parsed")
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
                    print(f"webscraper_image{c+1}.jpg downloaded")
                    c+=1 
                except:
                    continue
                if(c==n):
                    print("all images downloaded")
                    messages.append("All images downloaded")
                else:
                    print(f"{c} out of {n} images downloaded")
                    messages.append(f"{c} out of {n} images downloaded")
        except Exception as e:
            print("error, please check the url")
            messages.append(f"Error: {str(e)}")

    return jsonify({'messages': messages})


if __name__ == '__main__':
    app.run()
