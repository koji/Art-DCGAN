import glob
from PIL import Image, ImageDraw, ImageFont 
import random
import requests
from bs4 import BeautifulSoup
import os
import subprocess

'''
parameter url base url
          local_filename filename
'''
def download_file(url ,local_filename=None):
    # from https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    if local_filename is None:
        local_filename = url.split('/')[-1]
    #local_filename = url.split('/')[-1]
    if os.path.exists(local_filename):
        return local_filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


# def get_images(url):
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'lxml')
#     images = soup.select('img')
#     for image in images:
#         img_url = image.get('src')
#         try:
            
#             filename = download_file(img_url)
#             subprocess.call(['convert', filename, '-solarize', '10', filename+'.solarized.jpg'])
#         except Exception as e:
#             print(e)
#             continue


def get_images(amount):
    imgCounter = 11908
    print('start: get_images')
    maxCounter = amount/20
    tmp = int(amount/20)
    if tmp > 0 :
        maxCounter = tmp + 1
    queryString = input("enter the word: ")
    queryString = queryString.replace(' ', '+')
    # space --> +
    for cnt in range (0,maxCounter):
        start = cnt*20
        print('start :' + str(start))
        url = 'https://www.google.com/search?q={0}&gbv=1&ie=UTF-8&tbm=isch&prmd=ivnsba&ei=K9Z4Wo_qIMjW5gKJq5vQCw&start={1}&sa=N'.format(queryString,start)
        print(url)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        #images = soup.select('img')
        #images = soup.select('.img-wrap img')
        images = soup.select('img')
        for i, image in enumerate(images):
            #img_url = 'https:' + image.get('src')
            img_url = image.get('src')
            #savedname = 'test/' + str(i) + '.jpg'
            savedname = 'test/' + str(imgCounter) + '.jpg'
            imgCounter += 1
            try:
                filename = download_file(img_url,savedname)
                #subprocess.call(['convert', filename, '-solarize', '10', filename+'.solarized.jpg'])
            except Exception as e:
                print(e)
                continue
    #createImage(queryString)



def write_text(imgfilename, text):
    text = text.replace('+', ' ')
    im = Image.open(imgfilename)
    canvas = ImageDraw.Draw(im)
    canvas.rectangle([0, 125, im.size[0], 170], fill=(255,0,0))
    font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 30)
    canvas.text((10,125), text, font=font, fill=(255, 255, 255))
    im.save(imgfilename)


def createImage(fileName):
    blank_image = Image.new('RGBA', (1000,1000), (0,0,0,255))
    #blank_image.save('blank.png')
    x= 0
    y = 0
    jpegs = glob.glob('test/*.jpg')
    for jpg in jpegs:
        #print(jpg)
        im = Image.open(jpg)
        im.thumbnail((100,100))
        width = im.size[0]
        height = im.size[1]
        # x = random.randint(0, 1000)
        # y = random.randint(0, 1000)
        blank_image.paste(im, (x, y))
        x = x + width
        if x > 1000:
            x = 0
            y = y + height
    # put title
    blank_image.save(fileName+'.png')
    write_text(fileName+'.png', fileName)
    

def main():
    # print('start program')
    # google https://www.google.com/search?q=baby+crying&biw=1211&bih=676&gbv=1&tbm=isch&ei=MMyYWufmIaPm_QastKBw&start=0&sa=N
    #        https://www.google.com/search?q=baby+crying&biw=1211&bih=676&gbv=1&tbm=isch&ei=MMyYWufmIaPm_QastKBw&start=20&sa=N
    amount = input("how many images?: ")
    amount = int(amount)
    get_images(amount)
    # print('end program')

if __name__ == '__main__':
    main()
