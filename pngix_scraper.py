import bs4
from requests import get
from time import sleep,asctime
import csv
target_link='https://www.pngix.com/'

#Header for final csv file to store all data we need
data_header=['image_page','image_link','resolution','image_license','size','downloads']

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.5',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'DNT':'1',
    'Referer':target_link,
    'Host':'www.pngix.com',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Android 11; Mobile; LG-M255; rv:88.0) Gecko/88.0 Firefox/88.0',
        }

def LinkPairs(page):
    soup=bs4.BeautifulSoup(page, 'html.parser')
    pairs = [(png.attrs['href'], png.find_all('img', class_='lazy2')[0].attrs['data-original']) for png in soup.find_all('a', class_='img-part')]
    return pairs

def DataExtractor(page):
    soup=bs4.BeautifulSoup(page, 'html.parser')
    datlist=soup.find_all('table', id='details')[0].find_all('tr')
    datdict={}
    for item in datlist:
        title=item.find_all('th')[0].string
        data=item.find_all('td')[0].string
        datdict[title]=data
    print(datdict)
    return datdict
def FindingLinks():
    #first reaching pngix.com for cookie and first top images page
    ping = get(target_link, allow_redirects=True)
    cookie = ping.headers['Set-Cookie']
    print(cookie)
    headers['Cookie'] = cookie
    print(ping.headers)
    print(headers)
    #Step 1: gather image page and plain image links in pairs
    links=LinkPairs(ping.text)
    imgs_count=len(links)
    print(f'page:1, images found:{len(links)}, total:{imgs_count}')
    #loop until images end
    page=2
    errs=0
    #prev_imgs = links
    dump=open('dump.csv', 'a')
    csv.writer(dump).writerows(links)
    while len(links)>0:
        current_headers=headers
        current_headers['Referer'] = target_link+f'top/{page-1}/'
        try:
            response = get(target_link+f'top/{page}/', allow_redirects=True)
            print(response.status_code, response.url)        
            test=open('testdump.html', 'w')
            test.write(ping.text)
            test.close
            links=LinkPairs(response.text)
            imgs_count+=len(links)
            print(f'page:{page}, images found:{len(links)}, total:{imgs_count}')
            page+=1
    #        if prev_imgs==img_parser.PageLinksList: #if pages repeat
    #            print("Images are repeating, quitting")
    #            endlist = prev_imgs+img_parser.PageLinksList
    #            print([item for item, count in collections.Counter(endlist).items() if count > 1])
    #            print(target_link+f'top/{page-1}/')
    #            break
            csv.writer(dump).writerows(links)
    #        prev_imgs = img_parser.PageLinksList
        except Exception as exc:
            dump.close()
            errs+=1
            print(f"{exc} encountered, waiting to repeat")
            sleep(20)
            dump=open('dump.csv', 'a')
        if errs>10:
            print("Too many errors encountered, quitting.")
            break
    dump.close()
def AddingData():
    #Step 2: getting data for each link
    load=open('dump.csv', 'r')
    #Using asctime for unique, but human readable file name
    final_dump_name='pngix_data_'+'_'.join(asctime().split())+'.csv'
    final_dump=open(final_dump_name, 'w')
    #Getting file lenth
    file_lenth = sum(1 for line in load)
    load.close()
    load=open('dump.csv', 'r')
    #reader=csv.reader(load)
    print(f'Getting additional data about {file_lenth} images')
    print()
    for row in range(file_lenth):
        img_links=load.readline()
        img_links=img_links.split(',')
        img_page_link=img_links[0]
        print((row/file_lenth)*100, '% ', img_page_link, sep='')
        img_src=img_links[1]
        current_headers=headers
        current_headers['Referer']=f'{target_link}top/{row//60}'
        img_page_text = get(img_page_link, headers=current_headers)
        img_data=DataExtractor(img_page_text.text)
        data_list=[img_src, img_data['Resolution'], img_data['Image License'], img_data['Size'], img_data['Downloads\xa0\xa0']]
        csv.writer(final_dump).writerow(data_list)
    final_dump.close()
    removing_tmp_dump=open('dump.csv', 'w')
    removing_tmp_dump.close()

FindingLinks()
AddingData()

print('Program finished successfully.')

