import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import os
import time

start_page = 1

_begin_date = '1990-01-01'
_end_date = '2019-12-31'

#MAKE DIR FOR SAVING DATA
#os.mkdir(_begin_date+"_"+_end_date)

driver = webdriver.Chrome('/Users/soyeon/dev/NewsCrawler/chromedriver')
driver.implicitly_wait(3)


driver.get('https://www.bigkinds.or.kr/')

#공지사항 끄기
driver.find_element_by_xpath('/html/body/div[13]/div[3]/div/div[2]/div/div[2]/button').click()

#기간 접근
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[1]/button').click()

#기간 입력
begin_date = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[1]/div/div[3]/div[1]/input')
begin_date.send_keys(Keys.DELETE)
begin_date.send_keys(_begin_date)

end_date = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[1]/div/div[3]/div[2]/input')
end_date.send_keys(Keys.DELETE)
end_date.send_keys(_end_date)
end_date.send_keys(Keys.ENTER)

#적용
driver.find_element_by_xpath('//*[@id="date-confirm-btn"]').click()

#언론사
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[2]/button').click()
#경향신문 선택
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[2]/div/div[1]/div[3]/div[2]/div/button[1]').click()
#적용
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[2]/div/div[3]/button[2]').click()
#상세검색
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[5]/button').click()
#검색어범위
select_title = Select(driver.find_element_by_id("search-scope-type"))
select_title.select_by_index(1)
#키워드입력
word = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[5]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]/input')
word.click()
word.send_keys('인공지능, AI, 人工知能')  #'인공지능, AI, 人工知能'
#검색
driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/form/div/div/div/div[3]/div[5]/div/div[2]/div[1]/div/div[6]/div/div[2]/button').click()


#분석기사선택
driver.find_element_by_xpath('//*[@id="filter-tm-use"]').click()
#100건씩보기
#select_number = Select(driver.find_element_by_id("select2"))
#select_number.select_by_index(3)


print(len(driver.find_elements_by_css_selector('div.news-item__content.news-detail')))


a = driver.find_elements_by_css_selector('div.news-item__content.news-detail')

# for news in a:
#     time.sleep(1)
#     news.click()
#     time.sleep(1)
#     driver.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[3]/button').click()

#1에서 2로 넘어가는 코드 짜기
time_interval  = 5 
news_data_all = []
time.sleep(time_interval)




while True:
    time.sleep(time_interval)
    pagination = driver.find_element_by_css_selector("ul.pagination")
    a_link = pagination.find_elements_by_css_selector("a")

    page_dict = {}

    for a in a_link:
        page_dict[a.text] = a
        
    if page_dict.get(str(start_page)) == None:
        a_link[-1].click()
    else:
        break


i = start_page

while True:
    time.sleep(time_interval)
    pagination = driver.find_element_by_css_selector("ul.pagination")
    a_link = pagination.find_elements_by_css_selector("a")

    page_dict = {}
    for a in a_link:
        page_dict[a.text] = a
        
    if page_dict.get(str(i)) == None:
        if pagination.find_elements_by_css_selector("li")[-1].get_attribute("class") == "disabled":
            break
        a_link[-1].click()
        time.sleep(time_interval)
    else:
        print(i)
        page_dict[str(i)].click()
        
        ######
        #Code#
        ######
        time.sleep(time_interval)
        main_container = driver.find_elements_by_css_selector('div.news-item')            
        for _idx, news in enumerate(main_container):
            print("page_num:", i , " news_num: ",_idx)
            news_data = []
            time.sleep(1)
            news_data.append(news.find_element_by_css_selector('span.news-item__category').text)
            news_data.append(news.find_element_by_css_selector('span.news-item__date').text)
            news_data.append(news.find_element_by_css_selector('span.news-item__byline').text)

            news = news.find_element_by_css_selector('div.news-item__content.news-detail')            
            print(news_data)
            news.click()
            #collect news contents
            time.sleep(1)
            content = driver.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[2]')
            title = driver.find_element_by_xpath('/html/body/div[12]/div/div/div[1]/h4')
            news_data.append(title.text)
            news_data.append(content.text)
            driver.find_element_by_xpath('//*[@id="news-detail-modal"]/div/div/div[3]/button').click()

            news_data_all.append(news_data)
        
        ######       
        result = pd.DataFrame(news_data_all)
        result.to_csv(os.path.join(_begin_date+"_"+_end_date,"data_"+str(start_page).zfill(3)+"_"+str(i).zfill(3)+".csv"))
        i = i+1

print("Done")

result = pd.DataFrame(news_data_all)
result.to_csv("test.csv")



# time.sleep(10)
# driver.close()


## PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
driver = webdriver.PhantomJS('/Users/soyeon/dev/NewsCrawler/phantomjs')