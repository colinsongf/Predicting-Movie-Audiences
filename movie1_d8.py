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
        send_slack("movie", "databot", ":ghost:", "작업 실행 - {time}".format(time=current_time))

        try:
            result = function(*args, **kwargs)
            current_time = str(datetime.datetime.now())
            end_time = time.time()
            send_slack("movie", "databot", ":ghost:",
                       "작업 끝 - 걸린시간{time(s)}: {time}s.".format(time=int(end_time - start_time)))

        except:
            send_slack("movie", "databot", ":ghost:", "오류 발생.")
        return result

    return wrapper

boxoffice_df = pd.read_csv("csv/boxoffice_d8.csv",index_col=0)

@slack
def get_audience(boxoffice_df):
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
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                    "X-Requested-With":"XMLHttpRequest"}
            #r = requests.post("http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do",data=data,headers=headers)
            r = requests.post("http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do",data=data)

            dom = BeautifulSoup(r.content, "html.parser")
            dom1 = dom.select("td.right")
            dom2 = dom.select("td.bgt2")
            preview_audience = dom1[3].text




            final_audience_df.loc[len(final_audience_df)] = [
                j,
                preview_audience

            ]
            print('성공')
        except:
            print('get_audience에서 실패')
            print(j)
    return final_audience_df

final_audience_df = get_audience(boxoffice_df)

#final_audience_df = pd.read_csv("data/final_audience.csv", index_col=0)



#final_audience_df["audience"] = final_audience_df["audience"].dropna().apply(lambda x: int(str(x).split("(")[0].replace(",", "")) if str(x).split("(")[0].replace(",", "") != " " else 0)
#final_audience_df = final_audience_df[final_audience_df["audience"] > 10000]
final_audience_df.fillna("0")
#final_audience_df["audience"] = final_audience_df["audience"]

def make_number(x):
    try:
        return np.int(x.replace(",", ""))
    except:
        try:
            return np.int(x)
        except:
            return np.int(0)

for i in range(10):
    final_audience_df.ix[:, i] = final_audience_df.ix[:, i].apply(make_number)

def make_float(x):
    try:
        return np.float(x.replace("%", ""))
    except:
        try:
            return np.float(x)
        except:
            return np.float(0)

for i in range(10, 34):
    final_audience_df.ix[:, i] = final_audience_df.ix[:, i].apply(make_float)

#final_audience_df = final_audience_df[final_audience_df["d7_audience"]<1500000].reset_index(drop=True)
boxoffice_df = pd.read_csv("csv/boxoffice_d8.csv", index_col=0)
final_audience_df.to_csv("csv/test_final_audience_d8.csv",encoding="utf-8")
total_movie_df = final_audience_df.merge(boxoffice_df,how="inner",on="movieCd")
total_movie_df = total_movie_df[list(boxoffice_df.columns)+list(final_audience_df.columns[1:])]
total_movie_df.to_csv("csv/test_total_movie_d8.csv",encoding="utf-8")