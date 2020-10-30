from bs4 import BeautifulSoup
import requests
import os
import json
import time

url = "https://ru.luxuryestate.com/%D1%84%D1%80%D0%B0%D0%BD%D1%86%D0%B8%D1%8F/r%C3%A9gion-%C3%AEle-de-france/paris/paris/%D0%BF%D0%B0%D1%80%D0%B8%D0%B6"

mainpage = requests.get(url)
mainsoup = BeautifulSoup(mainpage.text, "html.parser")
searchList = mainsoup.select(".search-list li")
id = 0
data = {}

i = searchList[0]

def toOnePage(s):
    page = requests.get(s.select('.js_clickable')[0].get('href'))
    soup = BeautifulSoup(page.text, "html.parser")
    price = soup.select('.prices')[0].get_text().replace('₽', '').replace(' ', '').replace('\n', '')
    title = soup.select('.title-property')[0].get_text()
    features = soup.select(' .single-value')
    featuresLabels = []
    for k in features:
        featuresLabels.append(k.get_text().replace('\n','').replace(' ',''))
    phone = soup.select('.agency__contact a')[0].get('data-track-phone-value')
    content = soup.select('span[data-role=description-text-content]')[0].get_text().strip().replace("\n", "")
    address = ''.join(e.get_text() + ' ' for e in soup.select('.breadcrumb-name')[-2:])
    bathrooms = featuresLabels[2]
    bedrooms = featuresLabels[1]
    square = featuresLabels[4]
    print(content)
    #json writing
    data[id] = {
        "title": title,
        "price": price,
        "address": address,
        "phone": phone,
        "mainimg": "/photos/" + str(id) + "/main.jpg",
        "content": content,
        "images": ["/photos/" + str(id) + "/" + str(i) + ".jpg" for i in range(4)],
        "bathrooms": bathrooms,
        "bedrooms": bedrooms,
        "square": square,
        "featuresLabels": featuresLabels
    }
    #end
    saveImages(soup)

#DOWNLOADING IMAGES
def deleteBgImage(str):
    return 'https:' + str.replace('background-image: url(','').replace(')','')

def saveImages(soupchik):
    title = soupchik.select('.title-property')[0].get_text()
    smallGallery =soupchik.select('.small-gallery div')
    mainImage = deleteBgImage(soupchik.select('.img-box__content')[0].get("style"))
    os.mkdir('./photos/' + str(id), 0o666)
    count = 0
    for b in smallGallery:
        file = open("./photos/" + str(id) + "/" + str(count) + ".jpg", "wb")
        res = requests.get("https:" + b.get('data-src'))
        file.write(res.content)
        count += 1
        file.close()
    file = open('./photos/' + str(id) + "/" + "main" + ".jpg", "wb")
    res = requests.get(mainImage)
    file.write(res.content)
    file.close()
#DoWNOLOADING IMAGES END

for i in searchList:
    toOnePage(i)
    id += 1
    print('complete: ' + str(id))
    time.sleep(5)

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
