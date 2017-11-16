import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
naver_df = pd.read_csv("csv/total_movie_d14.csv", index_col=0)

naver_df = naver_df[naver_df["movieNm"].str.contains("감독")==False]
naver_df = naver_df[naver_df["movieNm"].str.contains("확장")==False]
naver_df = naver_df.reset_index(drop=True)

def get_star_score_url(naver_df):
    url_df = pd.DataFrame(columns=["movieCd", "movieNm_x", "movieNm_y", "url"])
    for n, i in enumerate(list(naver_df["movieNm"])):

        try:
            data = ("http://movie.naver.com/movie/search/result.nhn?query={movieNm}&section=all&ie=utf8").format(
                movieNm=i)
            r = requests.get(data)
            dom = BeautifulSoup(r.content, "html.parser")
            dom1 = dom.select("p.result_thumb")
            open_year = naver_df["prdtYear"].apply(lambda x: str(x)[0:4])
            if dom1[-1] == dom1[0]:
                for i, data in enumerate(dom1):
                    url = data.select_one("a")["href"]
                    movieNm = dom.select("dt")[i].text
                    url_df.loc[len(url_df)] = [
                        naver_df["movieCd"][n],
                        naver_df["movieNm"][n],
                        movieNm,
                        url, ]
            elif dom1[-1] != dom1[0]:
                num = 0
                for j in range(0, len(dom.select("dd.etc")), 2):
                    year = dom.select("dd.etc")[j].text[-4::]
                    if (year == open_year[n]) & (num == j):
                        num += 10
                        url = dom1[int(j / 2)].select_one("a")["href"]
                        movieNm = dom.select("dt")[int(j / 2)].text
                        url_df.loc[len(url_df)] = [
                            naver_df["movieCd"][n],
                            naver_df["movieNm"][n],
                            movieNm,
                            url, ]
                    num += 2
            print("get_star_score_url 성공")
        except:
            print("get_star_score_url에서 예외발생")
            print(i)
    return url_df

url_df = get_star_score_url(naver_df)

url_df.to_csv("csv/url_d14.csv",encoding="utf-8")

#url_df = pd.read_csv("data/url.csv",index_col=0)

url_df.head()

url_df["code"] = url_df["url"].apply(lambda x:np.int(x.split("=")[1]))

def get_star_score(url_df):
    star_score_df = pd.DataFrame(columns=["movieCd","movieNm","star_score","star_user_count"])#,"scene_score","scene_count"])
    for n, i in enumerate(list(url_df["code"])):
        try:
            data = ("http://movie.naver.com/movie/bi/mi/point.nhn?code={code}").format(code=i)
            r = requests.get(data)
            dom = BeautifulSoup(r.content, "html.parser")
            dom1 = dom.select_one("#beforePointArea")
            dom2 = dom1.select("em")[2:]
            star_user_count = dom2[-1].text
            star_score = ("").join([i.text for i in dom2 [:-1]])
            star_score_df.loc[len(star_score_df)] = [
                url_df["movieCd"][n],
                url_df["movieNm_x"][n],
                star_score,
                star_user_count,
            ]
            print("get_star_score 성공")
        except:
            print("get_start_score에서 에러남")
            print(i)
    return star_score_df

star_score_df = get_star_score(url_df)

star_score_df["star_score"] = star_score_df["star_score"].astype(float)
star_score_df["star_user_count"] = star_score_df["star_user_count"].apply(lambda x: np.int(x.replace(",","")))

star_score_df.to_csv("csv/star_score_d14.csv",encoding="utf-8")