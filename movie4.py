import pandas as pd
import numpy as np
import scipy as sp
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score


data = pd.read_csv("csv/data.csv", index_col=0)
dd_set = pd.read_csv("csv/value_data.csv", index_col=0)
modeling_data = pd.concat([dd_set,data["audience"]],axis=1)

X = modeling_data.ix[:,:-1]
scaler = StandardScaler(with_mean=False)
X_scaled = scaler.fit_transform(X)

dfX0 = pd.DataFrame(X_scaled, columns=X.columns)
dfX = sm.add_constant(dfX0)
dfy = pd.DataFrame(modeling_data.ix[:,-1], columns=["audience"])
d_df = pd.concat([dfX, dfy], axis=1)
d_df.head()

d_df = d_df[["const","star_score","preview_audience","d1_audience","d3_audience","d4_audience","d5_audience","d6_audience","d1_screen","d4_screen","d7_screen","d2_seat","d7_seat","director_score","actor_score","audience"]]

from sklearn.model_selection import train_test_split
X = d_df.ix[:,:-1]
y = d_df.ix[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)


model = sm.OLS(d_df.ix[:,-1],d_df.ix[:,1:-1])
result = model.fit()
print(result.summary())


model = sm.OLS(y_train,X_train)
result = model.fit()
print(result.summary())

remove_column_list = ["d2_screen","d3_screen","d5_show","d7_show", "showTm_score","d3_seat","openDt_score"]
d_df = d_df.drop(remove_column_list, axis=1)

model = sm.OLS(d_df.ix[:, -1], d_df.ix[:, 1:-1])
result = model.fit()
print(result.summary())

remove_column_list = ["repGenreNm_score"]
d_df = d_df.drop(remove_column_list, axis=1)

model = sm.OLS(d_df.ix[:, -1], d_df.ix[:, 1:-1])
result = model.fit()
print(result.summary())

movie_columns = list(d_df.columns)[:-1]

formula_str = "audience ~ " + " + ".join(movie_columns)
model = sm.OLS.from_formula(formula_str, data=d_df)
result = model.fit()
table_anova = sm.stats.anova_lm(result)
table_anova

remove_column_list = ["d7_audience","d5_screen","d3_show","d4_show","d7_show","d2_seat","d3_seat","d4_seat","d5_seat","openDt_score","prdtYear_score","showTm_score","repGenreNm_score","watchGradeNm_score","repNationNm_score","companyNm_score"]
d_df = d_df.drop(remove_column_list, axis=1)

model = sm.OLS(d_df.ix[:, -1], d_df.ix[:, 1:-1])
result = model.fit()
print(result.summary())

remove_column_list = ['d7_audience']
d_df = d_df.drop(remove_column_list, axis=1)

model = sm.OLS(d_df.ix[:, -1], d_df.ix[:, 1:-1])
result = model.fit()
print(result.summary())

model = LinearRegression()
model.fit(d_df.ix[:, :-1], d_df.ix[:, -1])


LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

def view_result(number):
    a = d_df[d_df["audience"].index==number]
    print(model.predict(a.ix[:,:-1]))
    print(d_df[d_df["audience"].index==number]["audience"])


view_result(1635)