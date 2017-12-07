Overview : This program is designed to predict audience of Nut Job2 and Nam Han San Sung(³²ÇÑ»ê¼º, It's a korean movie) and King's Man2 at 10th September. The day of the forecast is September 29th.
Considering that September 29th is the 8th day after the release of Namhansan and Nut Job2, and the 14th day after the release of King's Man 2, we will use the programs that use eight days of data (With the suffix "_d8" appended to the file name) and programs using 14 days of data (appended with the suffix "_d14").
At first this program collects movie data(name of director and actors, movie code(used as primary key), movie name, name of movie distributor, movie scores and audience at 8days after opening. 
I took the data from the API, removed the anomaly, trimmed it, made it into a csv file, and then used the csv file created in the next program. So we have program and csv file for each step.
And then my DNN.py finds correlation between movie data and audience so that learns with Deep Neural Network making weight matrix.
Now we can predict audience of Nut Job2 and Nam Han San Sung by using learned network. When I made this program in part of getting data from the Korean Film Council API, I took a look at the following open source (MIT licensed).
References : https://github.com/cyh132/movie



movie0.py : The box office list of the year(2004~2016) of Korean Film Council API is brought into a file and it is merged into one file. It is saved as "boxoffice.csv". <- This is training set.
movie0_d8.py : It gets movie data(about Nut Job2 and Nam Han San Sung) from API of Korean Film Council and makes it into pandas dataframe and then save as "boxoffice_d8.csv". (d8 means day after 8) <- This is test set

movie1.py : It reads boxoffice.csv, which made from movie0.py, and then gets more detailed information(seats, audience(day by day)...) about movies listed in boxoffice.csv, and merge each other so that save merged one as "total_movie.csv".
movie1_d8.py : It does same procedure on Nut Job2 and Nam Han San Sung as movie1.py

movie2.py : It gets movie star score(netizen evaluated and gave scores on movies, this program gets information about that) and made dataframe and then save it as "star_score.csv".

DNN.py : Using collected data(total_movie.csv and star_score.csv), it fits the neural network and predict audience. Note that there are not only continuous features but also categorical features. We treat them differently.

Made by Hoon Seo, Kyung Hee Univ, Dept. of Physics (contact : seohoon0409@gmail.com)

