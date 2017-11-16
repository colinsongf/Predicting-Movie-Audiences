import requests
import pandas as pd
import numpy as np
import time
import json
import datetime
from bs4 import BeautifulSoup


def send_slack(channel, username, icon_emoji, message):
    base_url = "https://hooks.slack.com/services/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"
    payload = {
        "channel": channel,
        "username": username,
        "icon_emoji": icon_emoji,
        "text": message
    }
    response = requests.post(base_url, data=json.dumps(payload))
    print(response.content)


def slack(function):
    def wrapper(*args, **kwargs):
        name = function.__name__
        start_time = time.time()
        current_time = str(datetime.datetime.now())
        send_slack("movie", "databot", ":ghost:", "작업을 실행합니다 - {time}".format(time=current_time))

        try:
            result = function(*args, **kwargs)
            current_time = str(datetime.datetime.now())
            end_time = time.time()
            send_slack("movie", "databot", ":ghost:",
                       "작업이 끝났습니다 - 걸린시간은 {time}s 입니다.".format(time=int(end_time - start_time)))

        except:
            send_slack("movie", "databot", ":ghost:", "오류가 났어요 다시 봐주세요.")
        return result

    return wrapper

boxoffice_df = pd.read_csv("csv/boxoffice.csv",index_col=0)
@slack
def get_audience(boxoffice_df):
    final_audience_df = pd.DataFrame(columns=["movieCd","preview_audience",
                                        "d1_audience","d2_audience","d3_audience","d4_audience","d5_audience","d6_audience","d7_audience",
                                        "d1_screen","d2_screen","d3_screen","d4_screen","d5_screen","d6_screen","d7_screen",
                                        "d1_show","d2_show","d3_show","d4_show","d5_show","d6_show","d7_show",
                                        "d1_seat","d2_seat","d3_seat","d4_seat","d5_seat","d6_seat","d7_seat",
                                        "audience"])
    for j in list(boxoffice_df["movieCd"]):
        try:
            data = {"code":j, "sType": "stat"}
            headers = {"Accept-Encoding":"gzip, deflate",
                    "Accept-Language":"ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4",
                    "Connection":"keep-alive",
                    "Content-Length":24,
                    "Content-Type":"application/x-www-form-urlencoded",
                    "Cookie":"ACEFCID=UID-57832AC44039B8B57BE3DF6B; JSESSIONID=S2J8XM7QzvvL8t56GVYqdfpVH6cd1X28XC39wnTQGy7yLGnWhQFn!1412368483!-1881944657",
                    "Host":"www.kobis.or.kr",
                    "Origin":"http://www.kobis.or.kr",
                    "Referer":"http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
                    "X-Requested-With":"XMLHttpRequest"}
            #r = requests.post("http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do",data=data,headers=headers)
            r = requests.post("http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do", data=data)
            dom = BeautifulSoup(r.content, "html.parser")
            print("################################################################\n dom 입니다 \n################################################################")
            print(dom)
            dom1 = dom.select("td.right")
            print(
                "################################################################\n dom1 입니다 \n################################################################")
            print(dom1)
            dom2 = dom.select("td.bgt2")
            print(
                "################################################################\n dom2 입니다 \n################################################################")
            print(dom2)
            preview_audience = dom1[3].text
            print(
                "################################################################\n preview_audience 입니다 \n################################################################")
            print(preview_audience)
            audience_list = []
            for i in range(9,107,7):
                audience_list.append(dom1[i].text)
            print(
                "################################################################\n audience_list 입니다 \n################################################################")
            print(audience)
            screen_list = []
            for i in range(4,60,4):
                screen_list.append(dom2[i].text)
            print(
                "################################################################\n screen_list 입니다 \n################################################################")
            print(screen_list)
            show_list = []
            for i in range(5,61,4):
                show_list.append(dom2[i].text)
            print(
                "################################################################\n show_list 입니다 \n################################################################")
            print(show_list)
            seat_list = []
            for i in range(7,63,4):
                seat_list.append(dom2[i].text)
            print(
                "################################################################\n seat_list 입니다 \n################################################################")
            print(seat_list)
            audience = dom.select("td")[7].text
            print(
                "################################################################\n audience 입니다 \n################################################################")
            print(audience)
            final_audience_df.loc[len(final_audience_df)] = [
                j,
                preview_audience,
                *audience_list,
                *screen_list,
                *show_list,
                *seat_list,
                audience
            ]
            print(
                "################################################################\n final_audience_df 입니다 \n################################################################")
            print(final_audience_df)
            print("get_audience 성공!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except:
            print("get_audience 함수에서 에러 남")
            print(j)
    return final_audience_df

final_audience_df = get_audience(boxoffice_df)
#print("final_audience_df를 get_audience만 한거")
print(final_audience_df)
#final_audience_df = pd.read_csv("data/final_audience.csv", index_col=0)
#print("final_audience_df에 csv파일을 입력한거")
#print(final_audience_df)

final_audience_df["movieCd"] = final_audience_df["movieCd"].astype(int)

print(final_audience_df["audience"])
final_audience_df["audience"] = final_audience_df["audience"].dropna().apply(lambda x: int(str(x).split("(")[0].replace(",", "")) if str(x).split("(")[0].replace(",", "") != " " else 0)
#final_audience_df["audience"] = final_audience_df["audience"].dropna().apply(lambda x: int(x.split("(").replace(",", "")) if x.split("(")[0].replace(",", "") != " " else 0)
final_audience_df = final_audience_df[final_audience_df["audience"] > 10000]
final_audience_df.fillna("0")
final_audience_df["audience"] = final_audience_df["audience"].astype(int)

def make_number(x):
    try:
        return np.int(x.replace(",", ""))
    except:
        try:
            return np.int(x)
        except:
            return np.int(0)


for i in range(9):
    final_audience_df.ix[:, i] = final_audience_df.ix[:, i].apply(make_number)


def make_float(x):
    try:
        return np.float(x.replace("%", ""))
    except:
        try:
            return np.float(x)
        except:
            return np.float(0)


for i in range(9, 30):
    final_audience_df.ix[:, i] = final_audience_df.ix[:, i].apply(make_float)

final_audience_df = final_audience_df[final_audience_df["d7_audience"]<1500000].reset_index(drop=True)

boxoffice_df = pd.read_csv("csv/boxoffice.csv", index_col=0)

final_audience_df.to_csv("csv/final_audience.csv",encoding="utf-8")

total_movie_df = final_audience_df.merge(boxoffice_df,how="inner",on="movieCd")

total_movie_df = total_movie_df[list(boxoffice_df.columns)+list(final_audience_df.columns[1:])]

total_movie_df.to_csv("csv/total_movie.csv",encoding="utf-8")