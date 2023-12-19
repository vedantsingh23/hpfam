from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin


app = Flask(__name__)


#Download Image Functions
def download_image(url, folder_path):
    try:
        response = requests.get(url, stream=True)
        if(response.status_code==200):
            file_name = url.split('/')[-1]
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image Download: {file_name}")
        else:
            print(f"Failed to download image from: {url}")
    except Exception as e:
        print(f"Error downloading image from: {url}:{e}")




#Function to crawl and then download images
def crawl_images(url, folder_path):
    try:
        #Requesting the page information
        response = requests.get(url)
        if(response.status_code == 200):
            #Breakup response into html format
            soup = BeautifulSoup(response.text, 'html.parser')
            #Find all tags with img
            img_tags = soup.find_all(['img', 'video'])
            #Download all those images
            for img_tag in img_tags:
                #Get image url
                img_url = img_tag.get('src')
                #Add image url to relative filepath
                img_url = urljoin(url, img_url)
                download_image(img_url, folder_path)
    except Exception as e:
        print(f'Error downloading images from: {url}: {e}')








target_url = "https://tenor.com/search/tenor-gifs"
save_folder = "C:/Users/vsingh287/Downloads/w"




if not os.path.exists(save_folder):
    os.makedirs(save_folder)


crawl_images(target_url, save_folder)




def crawl(url, depth=2, txtfile = "output.txt"):
    if depth == 0:
        return


    try:
        response = requests.get(url)
        #requests website and saves the response in the variable "reponse"
        soup = BeautifulSoup(response.content, 'html.parser')
        #Takes in content and organizes it using beautifalsoup's parsers
        print(f"Title:{soup.title.string}")


        #Find links on the page by searching through soup
        links = soup.find_all('a',href=True)
        with open(txtfile, 'w') as file:
            for link in links:
                next_url = link['href']
                if(next_url.startswith('http')):
                    file.write(next_url + '/n')
                    crawl(next_url, depth-1)


    except Exception as e:
        print(f"Error crawling {url}: {e}")


crawl("https://replit.com/", depth=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    image_urls = []
    if requests.method == 'POST':
        url = requests.form['url']
        folder_path = 'C:/Users/vsingh287/Downloads/w'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        image_urls = crawl_images(url, folder_path)
        return render_template('index.html',image_urls=image_urls)
        # return 'Images Downloaded Successfully'
    return render_template('index.html',image_urls=image_urls)


if __name__ == '__main__':
    app.run(debug=True)
