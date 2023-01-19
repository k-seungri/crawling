import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from openpyxl import Workbook
from selenium.webdriver.common.keys import Keys




print(os.getcwd())

# chromedriver.exe 위치
path = "/Users/HANILN/chromedriver.exe"
url = 'https://map.naver.com/v5/search/'
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--start-fullscreen')

# #브라우저 창 숨기기
# chrome_options.add_argument('headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('lang=ko_KR')

# #브라우저 실행 및 탭 추가
driver = webdriver.Chrome( executable_path=path, chrome_options=chrome_options )

#driver = webdriver.Chrome(executable_path=path, chrome_options=options)

# 크롤링 내용 파일로 저장
wb = Workbook()
ws = wb.active
ws.append(['Name','Category','Address','Number'])
now = time.localtime()
s = '%04d%02d%02d_%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
f_name = 'naver_map_crawling_' + s + '.xlsx'


driver.get(url + '서교동')
time.sleep(2)

#음식점 클릭
if driver.find_element_by_class_name('bubble_filter_list').find_element_by_tag_name('li').text == '음식점':
    driver.find_element_by_class_name('bubble_filter_list').find_element_by_tag_name('li').click()
    time.sleep(3)
else:
    print("첫번째 리스트 '음식점'이 아님")




n = 0
while n <= 6:
    # searchIframe 스크롤바 내려서 숨겨진 tag 열기
    driver.switch_to.default_content()
    driver.switch_to.frame('searchIframe')
    time.sleep(1)
    driver.find_element_by_tag_name('body').click()
    time.sleep(1)

    for i in range(30):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

    driver.switch_to.default_content()
    driver.switch_to.frame('searchIframe')

    for i in driver.find_element_by_id('_pcmap_list_scroll_container').find_elements_by_tag_name('li'):
        driver.switch_to.default_content()
        driver.switch_to.frame('searchIframe')
        i.click()
        driver.switch_to.default_content()
        time.sleep(0.5)
        driver.switch_to.frame('entryIframe')
        time.sleep(0.5)

        # flicking-camera 가 넘어가는 경우
        try:
            driver.find_element_by_xpath('//*[@id="app-root"]/div/div/div/div[5]/div/div/div/a[1]/span').click()
        except:
            pass

        driver.find_element_by_class_name('flicking-camera').find_element_by_tag_name('a').click()
        time.sleep(3)

        if len(driver.find_element_by_id('_title').find_elements_by_tag_name('span')) == 2:
            title = driver.find_element_by_id('_title').find_element_by_tag_name('span').text
            category = driver.find_element_by_id('_title').find_elements_by_tag_name('span')[1].text
        else:
            title = driver.find_element_by_id('_title').find_elements_by_tag_name('span')[1].text
            category = driver.find_element_by_id('_title').find_elements_by_tag_name('span')[2].text

        if '이벤트' in driver.find_elements_by_class_name('place_section_content')[0].text:

            place_section = driver.find_elements_by_class_name('place_section_content')[1]
        else:
            place_section = driver.find_elements_by_class_name('place_section_content')[0]

        for i in place_section.find_elements_by_tag_name('div'):
            if '주소' in i.text:
                store_address = i.text.split('\n')[1]
                break

        for i in place_section.find_elements_by_tag_name('div')[2:]:
            if '복사' in i.text:
                store_number = i.text
                if '안내' in store_number:
                    store_number = store_number.split('안내')[0]
                if '복사' in store_number:
                    store_number = i.text.split('복사')[0]
                store_number = store_number.replace('\n', '')
                break
            else:
                store_number = ''

        store = [title, category, store_address, store_number]
        print(store)
        ws.append(store)
        time.sleep(1)

        # 변수 리셋
        title = ''
        category = ''
        store_address = ''
        store_number = ''
        wb.save(f_name)

    # 다음페이지가 포함된 태그 위치 클릭
    driver.switch_to.default_content()
    driver.switch_to.frame('searchIframe')
    driver.find_element_by_xpath('//span[text()="다음페이지"]/..').click()
    time.sleep(3)
    n += 1

wb.save(f_name)