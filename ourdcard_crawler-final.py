from bs4 import BeautifulSoup
import re
import requests
import time
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from selenium import webdriver

url = "https://www.dcard.tw/search/posts?query=podcast&sort=like"
BOARD = ''
LATEST = False
ARTICLE_NUM = 100

# search keyword
KEYWORD = 'podcast'

# chrome driver

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver=webdriver.Chrome("chromedriver",chrome_options=chrome_options)
driver.get(url)



def Search_Board():
    title_list = []
    href_list = []
    like_list = []
    thing_list = []

    for i in range(15):  
        soup = BeautifulSoup(driver.page_source, 'html.parser') 
        # 文章標題、文章網址
        for entry in soup.select('article a'):
            title_list.append(entry.text)
            href_list.append(entry['href'])
        
        # 按讚數
        for entry in soup.select('article div'):
            if entry.has_attr('class'):
                item = re.search('sc-1kuvyve-3',entry['class'][0])
                if item is not None:
                    like_list.append(int(entry.text))
        # 抓貼文上面那一條(版,學校,時間)
        for entry in soup.select('div span'):
            if entry.has_attr('class'):
                item = re.search('sc-6oxm01-3',entry['class'][0])
                if item is not None:
                    thing_list.append(entry.text)
        #抓上面那一條的時間
        time_list=[]
        for timell in thing_list:
            pattern1 =r"\d+ 月 \d+ 日"
            pattern2 =r"\d+ 年 \d+ 月 \d+ 日"
            if re.fullmatch(pattern1,timell) or re.fullmatch(pattern2,timell):
                time_list.append(timell)
  
        
        # 往下滑
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
    
    #print('title list length = ')
    #print(len(title_list))
    return title_list[0:ARTICLE_NUM], href_list[0:ARTICLE_NUM], like_list[0:ARTICLE_NUM], thing_list[0:ARTICLE_NUM],time_list

#把res = requests.get(url+href)改掉

def Get_Article(href):

    res = requests.get('http://www.dcard.tw'+href)
    soup = BeautifulSoup(res.text, 'html.parser')
    #comment_list = []
    content = ''


    for entry in soup.select('div'):
        if entry.has_attr('class'):
            item = re.search('sc-4ihej7-0',entry['class'][0])
            if item is not None:
                content+=entry.text

    return content


if __name__ == '__main__':

    title_list, href_list, like_list,thing_list,time_list = Search_Board() # Search the board and get article titles and likes number of each article

    ##############################################################################################################
    # Plot the like number of each article as histogram
    ##############################################################################################################
    myfont = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')
  
    ##############################################################################################################
    # Sort the articles according to likes number
    ##############################################################################################################
    #把標題、按讚數、網址，依照按讚數排序
    for i in range(ARTICLE_NUM):
        for j in range(ARTICLE_NUM - i - 1):
            if like_list[j] < like_list[j + 1]:
                title_list[j], title_list[j + 1] = title_list[j + 1], title_list[j]
                href_list[j], href_list[j + 1] = href_list[j + 1], href_list[j]
                like_list[j], like_list[j + 1] = like_list[j + 1], like_list[j]
    #每半年文章數量累加
    for i in range(ARTICLE_NUM):
        print('(' + str(like_list[i]) + ')', end = ' ')
        print(title_list[i], end = ' ')
        print('(' + href_list[i] + ')')

    
    first_half_year_2018=0
    second_half_year_2018=0
    first_half_year_2019=0
    second_half_year_2019=0
    first_half_year_2020=0
    second_half_year_2020=0
    for i in range(ARTICLE_NUM):
        time = time_list[i]
        if '2018' in time:
            if ('12 月' in time) or ('11 月' in time) or ('10 月' in time) or ('9 月' in time) or ('8 月' in time) or ('7 月' in time):
                second_half_year_2018+=1
            else:
                first_half_year_2018+=1
        elif '2019' in time:
            if ('12 月' in time) or ('11 月' in time) or ('10 月' in time) or ('9 月' in time) or ('8 月' in time) or ('7 月' in time):
                second_half_year_2019+=1
            else:
                first_half_year_2019+=1

        else:
             if ('12 月' in time) or ('11 月' in time) or ('10 月' in time) or ('9 月' in time) or ('8 月' in time) or ('7 月' in time):
                second_half_year_2020+=1
             else:
                first_half_year_2020+=1
    #每半年文章數量累加
    total_1 = first_half_year_2018
    total_2 = total_1 + second_half_year_2018
    total_3 = total_2 + first_half_year_2019
    total_4 = total_3 + second_half_year_2019
    total_5 = total_4 + first_half_year_2020
    total_6 = total_5 + second_half_year_2020
    
    print('2018上半年:',first_half_year_2018,
            '2018下半年:',second_half_year_2018,
            '2019上半年:',first_half_year_2019,
            '2019下半年:',second_half_year_2019,
            '2020上半年:',first_half_year_2020,
            '2020下半年:',second_half_year_2020)
    yr=['first half of 2018',
        'second half of 2018',
        'first half of 2019',
        'second half of 2019',
        'first half of 2020',
        'second half of 2020']
    keyword=[first_half_year_2018,
                second_half_year_2018,
                first_half_year_2019,
                second_half_year_2019,
                first_half_year_2020,
                second_half_year_2020]
    keynum=[total_1, total_2, total_3, total_4, total_5, total_6]
    
    keyword_title = "2018~2020討論podcast的文章"
    
    plt.plot(yr,keynum,'-o')
    plt.show()
    plt.savefig("2018~2020發文數-折線圖.jpg")
    
    print('=========================================================================================================')
    def search_function(what):   
        search_what=[]
        what_num=[]
        search_what.append(what)
        #set default of number as 0
        for i in range(len(search_what)):
            what_num.append(0)
        #get the number of keyword in contents             
        for i in range(ARTICLE_NUM):
            content = Get_Article(href_list[i]) #只抓content, no comment
            for j in range(len(search_what)):
                if search_what[j] in content:
                    what_num[j] += 1    
        for i in range(len(search_what)):
            print(search_what[i],'共',what_num[i],'篇')
    
    while 1:
        print("想要找什麼頻道或是關鍵字?(輸入stop則結束輸入)")
        search_what = input()
        #word=input('Please enter the word you want to search(輸入stop則結束輸入):')
        if search_what =="stop":
            break
        else:
            search_function(search_what)
        print("(*´ω`)人(´ω`*)")

        
