import requests
import pandas as pd
import numpy as np
import os
import time
import datetime
import json

csv_list = ['BOlist/'+file for file in os.listdir('BOlist/')]
for i, data in enumerate(csv_list):
    if i == 0:
        df = pd.read_csv(data)
    else:
        small_df = pd.read_csv(data)
        df = pd.concat([df, small_df]).reset_index(drop=True)
df["관객수"] = df["관객수"].str.replace(",","")
df["관객수"] = df["관객수"].astype(int)
movie_df = df[df["관객수"] > 10000].reset_index(drop=True)
movie_df = movie_df.drop(movie_df.index[[3191]])
movie_df = movie_df.drop_duplicates("영화명").reset_index(drop=True)
movie_df.to_csv("csv/movie.csv",encoding="utf-8")

movieNm = movie_df["영화명"][:100]
print("movieNm 모양은: ", movieNm.shape)
print(movieNm)

def get_movie_data(movieNm):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    params = {"key":"f8263d769ce9213bf757a83d044b7060", "movieNm":movieNm}
    r = requests.get(url, params=params)
    return r.json()
def make_movie_df(movieNm):
    movie_df = pd.DataFrame(columns = ["movieCd", "movieNm", "director","prdtYear", "openDt", "typeNm", "repNationNm", "repGenreNm", "companyNm"])
    for i in list(movieNm):
        try:
            for data in get_movie_data(i)['movieListResult']['movieList']:
                if len(data["directors"]) >= 2:
                    director = data["directors"][0]["peopleNm"]
                elif len(data["directors"]) == 1:
                    director = data["directors"][0]["peopleNm"]
                if len(data["companys"]) >= 2:
                    companyNm = data["companys"][0]["companyNm"]
                elif len(data["companys"]) == 1:
                    companyNm = data["companys"][0]["companyNm"]
                movie_df.loc[len(movie_df)] = [
                    data["movieCd"],
                    data["movieNm"],
                    director,
                    data["prdtYear"],
                    data["openDt"],
                    data["typeNm"],
                    data["repNationNm"],
                    data["repGenreNm"],
                    companyNm
                ]
        except:
            print(i)
    return movie_df
movie_info_df = make_movie_df(movieNm)

print("movie_info_df의 모양: ", movie_info_df.shape)

movie_info_df = movie_info_df[~movie_info_df["movieNm"].str.contains("시네마정동")].reset_index(drop=True)
movie_info_df = movie_info_df[movie_info_df["repNationNm"] != "기타"].reset_index(drop=True)
movie_info_df = movie_info_df.drop_duplicates("movieCd").reset_index(drop=True)
movie_info_df = movie_info_df.drop_duplicates("movieNm").reset_index(drop=True)
movie_info_df = movie_info_df[movie_info_df["openDt"] != ""].reset_index(drop=True)
print("movie_info_df의 모양2: ", movie_info_df.shape)
movie_info_df.to_csv("csv/movie_info.csv",encoding="utf-8")

movieCd = movie_info_df["movieCd"]

def get_movie_detail(movieCd):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
    params = {"key":"f8263d769ce9213bf757a83d044b7060", "movieCd":movieCd}
    r = requests.get(url, params=params)
    return r.json()
def make_movie_detail_df(movie_info_df):
    movie_detail_df = pd.DataFrame(columns=["movieCd",
                                            "movieNm",
                                            "showTm",
                                            "watchGradeNm",
                                            "actor_1",
                                            "actor_2",
                                            "actor_3",
                                            "companyNm"
                                            ])
    for i in list(movieCd):
        try:
            data = get_movie_detail(i)['movieInfoResult']['movieInfo']
            actor_list = []
            if len(data["audits"]) >= 2:
                watchGradeNm = data["audits"][0]["watchGradeNm"]
            elif len(data["audits"]) == 1:
                watchGradeNm = data["audits"][0]["watchGradeNm"]
            if len(data["companys"]) >= 2:
                companyNm = data["companys"][0]["companyNm"]
            elif len(data["companys"]) == 1:
                companyNm = data["companys"][0]["companyNm"]
            if len(data["actors"]) >= 3:
                actor_list = [
                    data["actors"][0]["peopleNm"],
                    data["actors"][1]["peopleNm"],
                    data["actors"][2]["peopleNm"]
                ]
            else:
                for i in range(len(data["actors"])):
                    actor_list.append(data["actors"][i]["peopleNm"])
                for i in range(3-len(data["actors"])):
                    actor_list.append("")
            movie_detail_df.loc[len(movie_detail_df)] = [
                data["movieCd"],
                data["movieNm"],
                data["showTm"],
                watchGradeNm,
                *actor_list,
                companyNm
            ]
        except:
             print(i)
    return movie_detail_df

movie_detail = make_movie_detail_df(movieCd)
print("movie_detail의 모양: ", movie_detail.shape)

boxoffice_df = movie_info_df.merge(movie_detail, left_on="movieCd", right_on="movieCd")[[
        "movieCd",
        "movieNm_x",
        "director",
        "openDt",
        "prdtYear",
        "repNationNm",
        "repGenreNm",
        "showTm",
        "watchGradeNm",
        "actor_1",
        "actor_2",
        "actor_3",
        "companyNm_y"
    ]]
boxoffice_df = boxoffice_df.rename(columns={"movieNm_x":"movieNm", "companyNm_y":"companyNm"})
print("최종 boxoffice_df 모양: ", boxoffice_df.shape)
print(boxoffice_df)

boxoffice_df.to_csv("csv/boxoffice.csv",encoding="utf-8")