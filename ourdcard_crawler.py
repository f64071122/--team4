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
COMMENT_NUM = 3

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
                item = re.search('sc-6oxm01-2',entry['class'][0])
                if item is not None:
                    thing_list.append(entry.text)
        #抓上面那一條的時間
        number=0
        time_list=[]
        for timell in thing_list:
            number+=1
            if(number%3==0):
                number=0
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
    comment_list = []
    content = ''


    for entry in soup.select('div'):
        if entry.has_attr('class'):
            item = re.search('sc-4ihej7-0',entry['class'][0])
            if item is not None:
                content+=entry.text
            
    for entry in soup.select('div#comment-anchor div'):
        if entry.has_attr('class'):
            item = re.search('giORMG',entry['class'][1])
            if item is not None:
                comment_list.append(entry.text)

    return content, comment_list


def DrawBar(x_list, y_list, title, font):
    plt.title(title, fontproperties = font)
    plt.bar(x_list, y_list)
    plt.xticks(x_list,x_list,fontproperties = font,rotation=90)
    return

if __name__ == '__main__':

    title_list, href_list, like_list,thing_list,time_list = Search_Board() # Search the board and get article titles and likes number of each article

    ##############################################################################################################
    # Plot the like number of each article as histogram
    ##############################################################################################################
    myfont = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')
    '''
    title = '每篇文章讚數'
    DrawBar(list(range(1,ARTICLE_NUM + 1)), like_list, title, myfont)
    plt.show()
    '''
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
        time=time_list[i]
        if '2018' in time:
            if ('12月' in time) or ('11月' in time) or ('10月' in time) or ('9月' in time) or ('8月' in time) or ('7月' in time):
                second_half_year_2018+=1
            else:
                first_half_year_2018+=1
        elif '2019' in time:
            if ('12月' in time) or ('11月' in time) or ('10月' in time) or ('9月' in time) or ('8月' in time) or ('7月' in time):
                second_half_year_2019+=1
            else:
                first_half_year_2019+=1

        else:
             if ('12月' in time) or ('11月' in time) or ('10月' in time) or ('9月' in time) or ('8月' in time) or ('7月' in time):
                second_half_year_2020+=1
             else:
                first_half_year_2020+=1

    total_1=first_half_year_2018
    total_2=first_half_year_2018+second_half_year_2018
    total_3=first_half_year_2018+second_half_year_2018+first_half_year_2019
    total_4=first_half_year_2018+second_half_year_2018+first_half_year_2019+second_half_year_2019
    total_5=first_half_year_2018+second_half_year_2018+first_half_year_2019+second_half_year_2019+first_half_year_2020
    total_6=first_half_year_2018+second_half_year_2018+first_half_year_2019+second_half_year_2019+first_half_year_2020+second_half_year_2020
    
    print('2018上半年:',first_half_year_2018,'2018下半年:',second_half_year_2018,'2019上半年:',first_half_year_2019,'2019下半年:',second_half_year_2019,'2020上半年:',first_half_year_2020,'2020下半年:',second_half_year_2020)
    yr=['first half of 2018','second half of 2018','first half of 2019','second half of 2019','first half of 2020','second half of 2020']
    keyword=[first_half_year_2018,second_half_year_2018,first_half_year_2019,second_half_year_2019,first_half_year_2020,second_half_year_2020]
    keynum=[total_1,total_2,total_3,total_4,total_5,total_6]
    
    keyword_title = "2018~2020討論podcast的文章"
    
    plt.plot(yr,keynum,'-o')
    plt.show()
    plt.savefig("2018~2020發文數-折線圖.jpg")
    
    print('=========================================================================================================')

    
    #這是不同人打得喔>< 
    #找關鍵字(a)和頻道(b)
    #找關鍵字和頻道
    
    searchkeyword=[]
    keywordnum=[]
    
    while 1:
        word=input('Please enter the word you want to search(輸入a則完成輸入):')
        if word=="a":
            break
        else:
            searchkeyword.append(word)

            for i in range(len(searchkeyword)):
                keywordnum.append(0)
                
   
    
    for i in range(ARTICLE_NUM):
        content, comment_list = Get_Article(href_list[i])
        for j in range(len(searchkeyword)):
            if searchkeyword[j] in content:     #'關鍵字或頻道名'
                keywordnum[j]+=1
        
    for i in range(len(searchkeyword)):
        print(searchkeyword[i],'共',keywordnum[i],'篇')

    channel=[]
    channelnum=[]
    
    while 1:
        word=input('Please enter the word you want to search(輸入a則完成輸入):')
        if word=="a":
            break
        else:
            channel.append(word)

            for i in range(len(channel)):
                channelnum.append(0)
                
   
    
    for i in range(ARTICLE_NUM):
        content, comment_list = Get_Article(href_list[i])
        for j in range(len(channel)):
            if channel[j] in content:     #'關鍵字或頻道名'
                channelnum[j]+=1
        
    for i in range(len(channel)):
        print(channel[i],'共',channelnum[i],'篇')
        
