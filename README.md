# Attention
This script no longer works because pngix.com is down
~~This script is incomplete due to lack of my knowledge
Some common error cases are not accounted.
It can break sometimes~~
## Requirements
Apart from standart python3 libraries, you will need BeautifulSoup 4 for better html parsing
```
pip install bs4
```
### Info
This script scrapes data from pngix.com and saves it into file in csv format
File name is generated based on date and time and looks like this:
    pngix_data_(weekday)_(month)_(day)_(time)_(year).csv
Note that weekday and month will be names, not numbers, limited by lenth of 3 letters.
Like this:
```
pngix_data_Mon_Dec_31_23:59:59_2000.csv
```

Final file contains image source, resolution, license, size and downloads
This data is taken strait from pngix.com/viewpng/(png name)

Currently it takes about 10 days (Considering quite fast internet connection) to scrape all data. (I had never let this script to finish, but in 24h about 10% was complete)

In detail, this script works in 2 steps:
Step One:
=========
* Get cookie for this session
* Get 1st page of images sorted by top (just requests www.pngix.com, as it returns top images)
* Loop getting N page (www.pngix.com/top/N) until site returns empty page
* For every image it finds on page, writes image_page, image_source to dump.csv
Step Two:
=========
* For every image page in dump.csv request that page and get data about size, resolution, license and downloads
* Saves all data in pngix_data_(date/time).csv
