from bs4 import BeautifulSoup
import requests
ganji='http://wei.ganji.com'
url=requests.get(ganji+'/mao/a1/')
# print(url.text)

def get_links_from(who_sells,page):
    urls=[]
    list_views='http://wei.ganji.com/mao/a{}o{}/'.format(str(who_sells), str(page))
    wb_data= requests.get(list_views)
    soup=BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('.list-title'):
        urls.append(ganji+link.get('href'))
    return urls

def get_item_info(url,file):
    wb_data=requests.get(url)
    soup=BeautifulSoup(wb_data.text, 'lxml')

    datetime=soup.select('.pr-5')[0].text.split()
    datetime.remove('发布')

    region=[]
    regionName=soup.select(
        '#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > a')
    for r in regionName:
        region.append(r.text)

    data={
        'title':soup.select('.title-name')[0].text.split()[0],
        'price':soup.select('.dog-price')[0].text,
        'contact':soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(2)')[0].text.split()[1],
        'datetime': datetime,
        'region':region
    }

    if data['contact'].startswith('GJ'):
        data['contact']='未知'

    file.write(str(data)+'\n')
    # print(data)

with open('/home/shantom/Desktop/cat.txt','w') as file:
    for i in range(5):
        for url in get_links_from(1, i+1):
            get_item_info(url,file)
# get_item_info('http://wei.ganji.com/mao/1911875871x.htm')
