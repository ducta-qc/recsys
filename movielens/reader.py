import os
import csv

movielens_dataset_path = "/media/asm/facf0468-acee-415a-8560-384805510931/tmp/dataset/RecSys/movielens-1m"
age_range_dict = {
    '1': 'Under 18',
    '18': '18-24',
    '25': '25-34',
    '35': '35-44',
    '45': '45-49',
    '50': '50-55',
    '56': '56+'
}
age_range_list = age_range_dict.keys()

occupation_dict = {
    '0':  "other",
    '1':  "academic/educator",
    '2':  "artist",
    '3':  "clerical/admin",
    '4':  "college/grad student",
    '5':  "customer service",
    '6':  "doctor/health care",
    '7':  "executive/managerial",
    '8':  "farmer",
    '9':  "homemaker",
    '10':  "K-12 student",
    '11':  "lawyer",
    '12':  "programmer",
    '13':  "retired",
    '14':  "sales/marketing",
    '15':  "scientist",
    '16':  "self-employed",
    '17':  "technician/engineer",
    '18':  "tradesman/craftsman",
    '19':  "unemployed",
    '20':  "writer"
}
occupation_list = occupation_dict.keys()
tags_list = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy',
             'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
             'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
             'Thriller', 'War', 'Western']

class MovielensReader():
    def __init__(self, dataset_path, test_data_ratio=0.2):
        self.dataset_path = dataset_path
        self.split_test = test_data_ratio
        self.movies = {}
        self.users = {}
        self.ratings = {}
        self.rating_train = []
        self.rating_test = []

    def _movies():
        movies_dat = os.path.join(dataset_path, 'movies.dat')
        with open(movies_dat) as f:
            for l in f:
                movie_id, title, tags = l.split("::")
                released_date = title.split()[-1][1:-1]
                self.movies[movie_id] = {
                                'title': title, 
                                'tags':tags.split("|"), 
                                'released_date': released_date}

    def _ratings():
        ratings_dat = os.path.join(dataset_path, 'ratings.dat')
        with open(ratings_dat) as f:
            i = 0
            for l in f:
                user_id, movie_id, rating, timestamp = l.split("::")
                self.ratings[i] = {'user': user_id, 
                                   'movie_id': movie_id, 
                                   'rating': float(rating)/5., 
                                   'timestamp': int(timestamp)}
            num_of_ratings = len(self.ratings.keys())
            test_len = num_of_ratings * 

        pass

    def _users():
        pass

    def graph_build():
        pass

