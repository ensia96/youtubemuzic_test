from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time, csv
from datetime import datetime

def headless():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    return options

#driver = webdriver.Chrome('/Users/ensia96/Documents/chromedriver', options=headless())
driver = webdriver.Chrome('/Users/ensia96/Documents/chromedriver')

def scroll_down(target): # 인자로 온 링크에 대해 스크롤다운
    driver.get(target)

    SCROLL_PAUSE_TIME = 3

    last_height = driver.execute_script("return document.body.scrollHeight;")
    new_height = 0

    while True:
        for i in range(11):
            driver.execute_script(f"window.scrollTo({new_height}, document.body.scrollHeight * {i/10});")
            time.sleep(0.01)
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight;")

        if new_height == last_height:
            return True
        last_height = new_height

def login(target):

    driver.get(target)

    driver.find_element_by_css_selector('#right-content > a').click()

    driver.find_element_by_css_selector('#identifierId').send_keys('manchumgo@gmail.com')
    driver.find_element_by_css_selector('#identifierNext > span > span').click()
    time.sleep(2)

    driver.find_element_by_css_selector('#password > div > div > div > input').send_keys('akdrh1133!')
    time.sleep(2)
    driver.find_element_by_css_selector('#passwordNext > span').click()
    time.sleep(2)

    return True

def for_main(target):

    login(target)

    scroll_down(target)

    time.sleep(5)

    main = driver.find_element_by_css_selector('#contents.ytmusic-section-list-renderer')

    source = main.find_elements_by_css_selector(
        '#contents > ytmusic-immersive-carousel-shelf-renderer'
    )
    source += main.find_elements_by_css_selector(
        '#contents > ytmusic-carousel-shelf-renderer'
    )

    # calling collection collected before

    with open('./ym_data/collection.csv', newline='') as data:
        data_reader = csv.DictReader(data)
        coll = [row['collection'] for row in data_reader]

    # crawling and make data

    for collection in [
        {
            'name': sou.find_element_by_tag_name(
                'h2'
            ).get_attribute(
                'aria-label'
            ),
            'elements': [
                {
                    'name':h.find_element_by_css_selector(
                        '.image-wrapper'
                    ).get_attribute(
                        'title'
                    ),
                    'link':h.find_element_by_css_selector(
                        '.image-wrapper'
                    ).get_attribute(
                        'href'
                    ),
                }
                for i in sou.find_elements_by_tag_name(
                    'ul'
                )
                for h in i.find_elements_by_css_selector(
                    'ytmusic-two-row-item-renderer'
                )
            ]
        }
        for sou in source
    ]:

        if collection['name'] not in os.listdir('./ym_data/collections'):

            coll.append(collection['name'])

            os.mkdir('./ym_data/collections/'+collection['name'])

            print(f"새로운 컬렉션 디렉토리를 생성했습니다 : {collection['name']}")


            os.chdir('./ym_data/collections/'+collection['name'])


            newcsv = open("./playlists.csv", 'w+', encoding='utf-8')

            csv.writer(
                newcsv
            ).writerow(
                [
                    'title',
                    'thumbnail',
                    'description',
                    'type',
                    'artist',
                    'year',
                ]
            )

            newcsv.close()

            print('컬렉션 소속의 list 정보를 담는 csv 를 생성했습니다.')

            i = 0
            for element in collection['elements']:
                for_list(element['link'],i)
                i += 1

            os.chdir('../../../')

    # reset collection.csv

    coll = list(set(coll))

    newcsv = open("./ym_data/collection.csv", 'w+', encoding='utf-8')

    csv.writer(
        newcsv
    ).writerow(
        [
            'collection'
        ]
    )

    for newthings in coll:

        csv.writer(
            newcsv
        ).writerow(
            [
                newthings
            ]
        )

    print('컬렉션 목록을 갱신했습니다')
    print('')
    print('끝!')

def for_hotlist(target):

    scroll_down(target)

    hotlist = driver.find_elements_by_css_selector('ytmusic-full-bleed-item-renderer')

    hot_list = [
        {
            'thumbnail':hot.find_element_by_css_selector('img.yt-img-shadow').get_attribute('src'),
            'title':hot.find_element_by_css_selector('.title.ytmusic-full-bleed-item-renderer').text,
            'artist':hot.find_element_by_css_selector(
                '.subtitle.ytmusic-full-bleed-item-renderer'
            ).get_attribute('title')[
                :hot.find_element_by_css_selector(
                    '.subtitle.ytmusic-full-bleed-item-renderer'
                ).get_attribute('title').find('•')-1
            ],
            'views':hot.find_element_by_css_selector(
                '.subtitle.ytmusic-full-bleed-item-renderer'
            ).get_attribute('title')[
                hot.find_element_by_css_selector(
                    '.subtitle.ytmusic-full-bleed-item-renderer'
                ).get_attribute('title').find('•')+6:-1
            ]
        }
        for hot in hotlist
    ]

    newcsv = open(f"./ym_data/hotlist.csv", 'w+', encoding='utf-8')
    csv.writer(
        newcsv
    ).writerow(
        [
            'thumbnail',
            'title',
            'artist',
            'views',
        ]
    )
    for hot in hot_list:
        csv.writer(
            newcsv
        ).writerow(
            [
                hot['thumbnail'],
                hot['title'],
                hot['artist'],
                hot['views'],
            ]
        )

def for_list(target, i):

    scroll_down(target)

    time.sleep(2)

    if 0<len(driver.find_elements_by_css_selector('ytmusic-detail-header-renderer')):
        list_header = driver.find_element_by_css_selector('ytmusic-detail-header-renderer')
        list_sub    = list_header.find_element_by_class_name('subtitle')

    if 0<len(driver.find_elements_by_css_selector('ytmusic-data-bound-header-renderer')):
        list_header = driver.find_element_by_css_selector('ytmusic-data-bound-header-renderer')
        list_sub    = list_header.find_element_by_class_name('stats')

    itemlist = driver.find_elements_by_css_selector('ytmusic-responsive-list-item-renderer')
    itemlist += driver.find_elements_by_css_selector('ytmusic-section-list-renderer')

    # update playlists

    newcsv = open(
        "./playlists.csv",
        'a',
        encoding='utf-8'
    )

    csv.writer(
        newcsv
    ).writerow(
        [
            list_header.find_element_by_class_name('title').text,
            list_header.find_element_by_tag_name('img').get_attribute('src'),
            list_header.find_element_by_css_selector('.description').text,
            list_sub.text[:list_sub.text.find('•')-1],
            list_sub.text[ list_sub.text.find('•')+2:-7],
            list_sub.text[-4:]
        ]
    )

    newcsv.close()

    # make itemlist csv

    newcsv = open(
        './'+str(i)+'.csv',
        'w+',
        encoding='utf-8'
    )

    csv.writer(
        newcsv
    ).writerow(
        [
            'title',
            'thumbnail',
            'artist',
            'album',
            'length',
        ]
    )

    for i in itemlist:
        items = []
        items.append(i.find_element_by_class_name('title').text)
        if 'data:image' not in i.find_element_by_tag_name('img').get_attribute('src'):
            items.append(i.find_element_by_tag_name('img').get_attribute('src'))
        else:
            items.append('')
        if 0<len(i.find_elements_by_class_name('flex-column')):
            items.append(i.find_elements_by_class_name('flex-column')[0].get_attribute('title'))
            items.append(i.find_elements_by_class_name('flex-column')[1].get_attribute('title'))
        else:
            items.append('')
            items.append('')
        if 0<len(i.find_elements_by_class_name('fixed-column')):
            items.append(i.find_element_by_class_name('fixed-column').text)
        else:
            items.append(i.find_element_by_class_name('duration').text)

        csv.writer(
            newcsv
        ).writerow(
            items
        )

    newcsv.close()

    print(list_header.find_element_by_class_name('title').text+' 에 대한 csv 가 작성되었습니다.')

def for_artist(target):
    driver.get(target)
    time.sleep(3)
    print(driver.find_element_by_css_selector('.image.ytmusic-fullbleed-thumbnail-renderer').get_attribute('src'))
    print(driver.find_element_by_css_selector('.title.ytmusic-immersive-header-renderer').text)

#############################################################################################

for_main('https://music.youtube.com')

#for_hotlist('https://music.youtube.com/hotlist') # 5/14

#for_list('https://music.youtube.com/playlist?list=rdclak5uy_ln9xj1rqgmbltmvrztvhmg-vyvt594kyu') # 구글 DB에서 폐기함
#for_list('https://music.youtube.com/playlist?list=PLWImZYQw4M8ePtdzPMzkeJtuzF9qVchBR')
#for_list('https://music.youtube.com/playlist?list=RDCLAK5uy_kfdjbDJHQEj3DMdo5Qt6hlP-dxVRL26tM')

#more_test('https://music.youtube.com/channel/UCa5qWh5TRLCVFkCO67_gOtw')
#more_test('https://music.youtube.com/playlist?list=RDCLAK5uy_kx8KLdeTpmUxdsdetXKOkT07jEVp2LhDE')

#for_artist('https://music.youtube.com/channel/UC0NqJ6MhRnkRaWAmBgyyjTA')

driver.quit()
