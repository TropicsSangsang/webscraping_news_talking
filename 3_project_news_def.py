import re
import requests
from bs4 import BeautifulSoup

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
        print("{}.{}".format(index, title))
        print("  (링크 : {})".format(link))

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%96%89%EC%8B%A0%EB%8F%99+%EB%82%A0%EC%94%A8&oquery=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&tqi=i7aSzdprvhGsseajB24sssssttC-177516"
    soup = create_soup(url)
    # 어제보다 0.6° 낮아요 흐림
    cast = soup.find("p", attrs={"class":"summary"}).get_text()
    # 현재 온도
    curr_temp = soup.find("div",attrs={"class":"temperature_text"}).get_text() # .replace("도씨", "")-> 도씨 반복 없애려고...
    # 최자 온도 최고 온도
    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text()
    max_temp = soup.find("span", attrs={"class":"highest"}).get_text()
    # 체감온도
    sensory_temp = soup.find("dd", attrs={"class":"desc"}).get_text() 
    # # 오전 오후 강수 확률
    rain_rate = soup.find("div", attrs={"class":"day_data"}) #.strip()을 통해서 공백제거(우리는 필요X)
    morning_rain_rate = rain_rate.find_all("span", attrs={"class":"rainfall"})[0].get_text()
    afternoon_rain_rate = rain_rate.find_all("span", attrs={"class":"rainfall"})[1].get_text()  
    # 미세 초미세
    dust = soup.find("ul", attrs={"class":"today_chart_list"})
    fine_dust = dust.find_all("li")[0].get_text()
    ultra_fine_dust = dust.find_all("li")[1].get_text()

    # (주의) 클래스가 2개를 참조할때는...
    #  dust = soup.find("ul", attrs={"class":["today_chart_list", "title"]})  -> class를 list로 감싸서...
    #  클래스 와 함꼐 text까지 참조할때는...
    #  dust = soup.find("ul", attrs={"class":"today_chart_list", "id"="title"})  -> 이렇게 하면 OK 



    # 출력
    print(cast)
    print("{}/{}/{} ".format(curr_temp, min_temp, max_temp))
    print(" 체감 온도 {} ".format(sensory_temp))
    print(" 강수 확률 : 오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate))
    print("{} / {}".format(fine_dust, ultra_fine_dust))
    print()  # 한 칸 띄우기

def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.daum.net"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"list_newsissue"}).find_all("li", limit=3)  # limit = 3 : 3개까지 가져옴
    for index, news in enumerate(news_list, 1):
        # title = news.div.a.get_text().strip()
        title = news.find("a", attrs={"class":"link_txt"}).get_text().strip()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()    

def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.daum.net/digital#1"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"list_newsmajor"}).find_all("li", limit=3)  # limit = 3 : 3개까지 가져옴
    for index, news in enumerate(news_list, 1):
        # title = news.div.a.get_text().strip()
        title = news.find("a", attrs={"class":"link_txt"}).get_text().strip()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()  

def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
    soup = create_soup(url)  
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]:   # 8 문장이 있다고 가정할 때, index 기준 4~7까지
        print(sentence.get_text().strip())
    print() # 한칸 띄우기

    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2]:  # 8 문장이 있다고 가정할 때, index 기준 0~3까지
        print(sentence.get_text().strip())    



    print()





# 오늘의 날씨 정보 가져오기
if __name__ == "__main__": # 이곳에서 직접 실행하면 scrape_weather()이부분이 실행되고
    scrape_weather()       # 다른곳에서 호출해서 쓰면 scrape_weather()이부분은 실행 안됨
    scrape_headline_news()   # 헤드라인 뉴스 정보 가져오기
    scrape_it_news()   # IT 뉴스 정보 가져오기
    scrape_english()    # 오늘의 영어 회화 가져오기