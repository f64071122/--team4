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

<<<<<<< HEAD
    
    #這是不同人打得喔>< 
    #找關鍵字(a)和頻道(b)
    keyword_1,keyword_2,keyword_3,keyword_4,keyword_5,keyword_6,keyword_7,keyword_8,keyword_9,keyword_10,keyword_11,keyword_12,keyword_13,keyword_14,keyword_15,keyword_16,keyword_17,keyword_18,keyword_19,keyword_20,keyword_21,keyword_22,keyword_23,keyword_24,keyword_25=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
=======
    #這是不同人打得喔><
    #找關鍵字(a)和頻道(b)
    a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
>>>>>>> master
    for i in range(ARTICLE_NUM):
        content, comment_list = Get_Article(href_list[i])
        #'關鍵字'
        if '新聞' in content:     
<<<<<<< HEAD
            keyword_1=keyword_1+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '好笑' in content:     
            keyword_2=keyword_2+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '聲音' in content:     
            keyword_3=keyword_3+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '有幫助' in content:    
            keyword_4=keyword_4+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '生活' in content:     
            keyword_5=keyword_5+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '學習' in content:     
            keyword_6=keyword_6+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '有趣' in content:     
            keyword_7=keyword_7+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '知識' in content:     
            keyword_8=keyword_8+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '充實' in content:     
            keyword_9=keyword_9+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '歌' in content:     
            keyword_10=keyword_10+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '輕鬆' in content:     
            keyword_11=keyword_11+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '聊天' in content:    
            keyword_12=keyword_12+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '資訊' in content:     
            keyword_13=keyword_13+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '旅遊' in content:     
            keyword_14=keyword_14+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '通勤' in content:     
            keyword_15=keyword_15+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '工作' in content:     
            keyword_16=keyword_16+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '時間' in content:    
            keyword_17=keyword_17+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '正能量' in content:    
            keyword_18=keyword_18+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '故事' in content:     
            keyword_19=keyword_19+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '沒負擔' in content:     
            keyword_20=keyword_20+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '時事' in content:     
            keyword_21=keyword_21+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '議題' in content:    
            keyword_22=keyword_22+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '成長' in content:    
            keyword_23=keyword_23+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '新知' in content:     
            keyword_24=keyword_24+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '幽默' in content:     
            keyword_25=keyword_25+1
=======
            a1=a1+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '好笑' in content:    
            a2=a2+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '聲音' in content:     
            a3=a3+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '有幫助' in content:     
            a4=a4+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '生活' in content:     
            a5=a5+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '學習' in content:     
            a6=a6+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '有趣' in content:     
            a7=a7+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '知識' in content:     
            a8=a8+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '充實' in content:     
            a9=a9+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '歌' in content:   
            a10=a10+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '輕鬆' in content:    
            a11=a11+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '聊天' in content:    
            a12=a12+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '資訊' in content:    
            a13=a13+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '旅遊' in content:     
            a14=a14+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '通勤' in content:     
            a15=a15+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '工作' in content:    
            a16=a16+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '時間' in content:     
            a17=a17+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '正能量' in content:    
            a18=a18+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '故事' in content:     
            a19=a19+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '沒負擔' in content:    
            a20=a20+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '時事' in content:    
            a21=a21+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '議題' in content:    
            a22=a22+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '成長' in content:    
            a23=a23+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '新知' in content:    
            a24=a24+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '幽默' in content:    
            a25=a25+1
>>>>>>> master
            #print('(' +title_list[i]+ ')' + '\n')
 
    print('新聞共有'+str(keyword_1)+'篇','好笑共有'+str(keyword_2)+'篇','聲音共有'+str(keyword_3)+'篇','有幫助共有'+str(keyword_4)+'篇')
    print('生活共有'+str(keyword_5)+'篇','學習共有'+str(keyword_6)+'篇','有趣共有'+str(keyword_7)+'篇','知識共有'+str(keyword_8)+'篇')
    print('充實共有'+str(keyword_9)+'篇','歌共有'+str(keyword_10)+'篇','輕鬆共有'+str(keyword_11)+'篇','聊天共有'+str(keyword_12)+'篇')
    print('資訊共有'+str(keyword_13)+'篇','旅遊共有'+str(keyword_14)+'篇','通勤共有'+str(keyword_15)+'篇','工作共有'+str(keyword_16)+'篇')
    print('時間共有'+str(keyword_17)+'篇','正能量共有'+str(keyword_18)+'篇','故事共有'+str(keyword_19)+'篇','沒負擔共有'+str(keyword_20)+'篇')
    print('時事共有'+str(keyword_21)+'篇','議題共有'+str(keyword_22)+'篇','成長共有'+str(keyword_23)+'篇','新知共有'+str(keyword_24)+'篇','幽默共有'+str(keyword_25)+'篇')
    print('=========================================================================================================')
<<<<<<< HEAD
    
    chanel = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    chanel_label=['台灣通勤第一品牌','百靈果','股癌','科技島讀','敏迪選讀','馬力歐陪你喝一杯','佐邊茶水間','Firstory Lab','TED Talks','財報狗','馬克信箱','心理學','法客電台']
=======

    #b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14
    b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    b_label=['台灣通勤第一品牌','百靈果','股癌','科技島讀','敏迪選讀','馬力歐陪你喝一杯','佐邊茶水間','Firstory Lab','TED Talks','財報狗','馬克信箱','心理學','法客電台']
>>>>>>> master
    for i in range(ARTICLE_NUM):
        content, comment_list = Get_Article(href_list[i])
        #print('content'+str(i))
        #print(content)
        #'頻道名'
        if '台灣通勤第一品牌' in content:     
<<<<<<< HEAD
            chanel[0]=chanel[0]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '百靈果' in content:     
            chanel[1]=chanel[1]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '股癌' in content:     
            chanel[2]=chanel[2]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '科技島讀' in content:     
            chanel[3]=chanel[3]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '敏迪選讀' in content:     
            chanel[4]=chanel[4]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '馬力歐陪你喝一杯' in content:     
            chanel[5]=chanel[5]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '佐邊茶水間' in content:     
            chanel[6]=chanel[6]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '轉角國際 種磅廣播' in content:     
            chanel[7]=chanel[7]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif 'Firstory Lab' in content:     
            chanel[8]=chanel[8]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif 'TED Talks' in content:     
            chanel[9]=chanel[9]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '財報狗' in content:     
            chanel[10]=chanel[10]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '馬克信箱' in content:     
            chanel[11]=chanel[11]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '心理學' in content:     
            chanel[12]=chanel[12]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '法客電台' in content:     
            chanel[13]=chanel[13]+1
            #print('(' +title_list[i]+ ')' + '\n')
    print('台灣通勤第一品牌共有'+str(chanel[0])+'篇','百齡果共有'+str(chanel[1])+'篇','股癌共有'+str(chanel[2])+'篇','科技島讀'+str(chanel[3])+'篇')
    print('敏迪選讀共有'+str(chanel[4])+'篇','馬力歐陪你喝一杯共有'+str(chanel[5])+'篇','佐邊茶水間共有'+str(chanel[6])+'篇','轉角國際 種磅廣播'+str(chanel[7])+'篇')
    print('Firstory Lab共有'+str(chanel[8])+'篇','TED Talks共有'+str(chanel[9])+'篇','財報狗共有'+str(chanel[10])+'篇','馬克信箱共有'+str(chanel[11])+'篇')
    print('心理學共有'+str(chanel[12])+'篇','法客電台共有'+str(chanel[13])+'篇')
=======
            b[0]=b[0]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '百靈果' in content:     
            b[1]=b[1]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '股癌' in content:     
            b[2]=b[2]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '科技島讀' in content:     
            b[3]=b[3]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '敏迪選讀' in content:     
            b[4]=b[4]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '馬力歐陪你喝一杯' in content:     
            b[5]=b[5]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '佐邊茶水間' in content:     
            b[6]=b[6]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '轉角國際 種磅廣播' in content:     
            b[7]=b[7]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif 'Firstory Lab' in content:     
            b[8]=b[8]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif 'TED Talks' in content:     
            b[9]=b[9]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '財報狗' in content:     
            b[10]=b[10]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '馬克信箱' in content:     
            b[11]=b[11]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '心理學' in content:     
            b[12]=b[12]+1
            #print('(' +title_list[i]+ ')' + '\n')
        elif '法客電台' in content:     
            b[13]=b[13]+1
            #print('(' +title_list[i]+ ')' + '\n')
            
    print('台灣通勤第一品牌共有'+str(b[0])+'篇','百齡果共有'+str(b[1])+'篇','股癌共有'+str(b[2])+'篇','科技島讀'+str(b[3])+'篇')
    print('敏迪選讀共有'+str(b[4])+'篇','馬力歐陪你喝一杯共有'+str(b[5])+'篇','佐邊茶水間共有'+str(b[6])+'篇','轉角國際 種磅廣播'+str(b[7])+'篇')
    print('Firstory Lab共有'+str(b[8])+'篇','TED Talks共有'+str(b[9])+'篇','財報狗共有'+str(b[10])+'篇','馬克信箱共有'+str(b[11])+'篇')
    print('心理學共有'+str(b[12])+'篇','法客電台共有'+str(b[13])+'篇')
>>>>>>> master
