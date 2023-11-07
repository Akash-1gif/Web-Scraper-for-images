from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        url = request.form.get('web_link')
        messages = []
        errors = []
        total = 0
        try:
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            images = soup.find_all('img')
            total = len(images)
            for c, image in enumerate(images):
                try:
                    link = image.get('src') or image.get('data-srcset') or image.get('data-src') or image.get('data-fallback-src')
                    if link:
                        s = requests.get(link).content
                        with open(f"image{c}.jpg", "wb+") as f:
                            f.write(s)
                        messages.append(f"Downloaded image {c}")
                        print(f'downloaded {c} of {total}')
                    else:
                        errors.append(f"Skipped image {c}")

                except Exception as e:
                    errors.append(f"Error downloading image {c}: {str(e)}")
                    print("All images downloaded")

        except requests.exceptions.RequestException as e:
            errors.append(f"Error: {str(e)}")

    return jsonify({'messages': messages, 'total': total})

if __name__ == '__main__':
    app.run()

