import os
import csv
import random
import imdb
import codecs
import re


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
age_range_to_idx = dict(zip(age_range_list, range(len(age_range_list))))

occupation_dict = {
    '0': "other",
    '1': "academic/educator",
    '2': "artist",
    '3': "clerical/admin",
    '4': "college/grad student",
    '5': "customer service",
    '6': "doctor/health care",
    '7': "executive/managerial",
    '8': "farmer",
    '9': "homemaker",
    '10': "K-12 student",
    '11': "lawyer",
    '12': "programmer",
    '13': "retired",
    '14': "sales/marketing",
    '15': "scientist",
    '16': "self-employed",
    '17': "technician/engineer",
    '18': "tradesman/craftsman",
    '19': "unemployed",
    '20': "writer"
}
occupation_list = occupation_dict.keys()
occupation_to_idx = dict(zip(occupation_list, range(len(occupation_list))))

tags_list = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy',
             'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
             'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
             'Thriller', 'War', 'Western']
tags_to_idx = dict(zip(tags_list, range(len(tags_list))))


def create_one_array(index, max_length):
    b = np.zeros((1, max_length))
    b[index] = 1
    return b


class MovielensReader():
    def __init__(self, dataset_path, test_data_ratio=0.2):
        self.dataset_path = dataset_path
        self.split_test = test_data_ratio
        self.movies = {}
        self.users = {}
        self.ratings = {}
        self.ratings_train = {}
        self.ratings_test = {}

    def _movies(self):
        movies_dat = os.path.join(self.dataset_path, 'movies.dat')
        with open(movies_dat) as f:
            for l in f:
                movie_id, title, tags = l.split("::")
                print("Loading movie `%s`" % title)
                matches = re.match(r'([^\(]+?)((\([^\(]+\)) (\([^\(]+\)))', title)
                if matches:
                    title = "%s %s" % (matches.groups()[0], matches.groups()[-1])
                    
                released_date = title.split()[-1][1:-1]
                self.movies[movie_id] = {
                                'title': title, 
                                'tags': tags.split("|"), 
                                'released_date': released_date
                            }
                try:
                    movie = imdb.get_movie(title)
                    for k, v in movie.items():
                        self.movies[movie_id][k] = v
                except:
                    print("Error `%s`" % title)

    def _ratings(self):
        ratings_dat = os.path.join(self.dataset_path, 'ratings.dat')
        with open(ratings_dat) as f:
            i = 0
            for l in f:
                user_id, movie_id, rating, timestamp = l.split("::")
                self.ratings[i] = {'user': user_id, 
                                   'movie_id': movie_id, 
                                   'rating': float(rating)/5., 
                                   'timestamp': int(timestamp)}
                i += 1
            num_of_ratings = len(self.ratings.keys())
            ratings_id = set(self.ratings.keys())
            test_len = int(num_of_ratings * self.split_test)
            ratings_test = random.sample(ratings_id, test_len)
            ratings_train = list(ratings_id.different(set(self.rating_test)))
            for rid in ratings_test:
                self.ratings_test[rid] = self.ratings[rid]
            for rid in ratings_train:
                self.ratings_train[rid] = self.ratings[rid]

    def _users(self):
        users_dat = os.path.join(self.dataset_path, 'users.dat')
        with open(users_dat) as f:
            i = 0
            for l in f:
                user_id, gender, age, occupation, zipcode = l.split("::")
                self.users[user_id] = {
                        "gender": gender, 
                        "age": age_range_dict[age],
                        "occupation": occupation_dict[occupation],
                        "zipcode": zipcode}

    def load(self, from_raw=True):
        if from_raw:
            self._movies()
            self._users()
            self._ratings()
        else:
            with open("movies.json") as f:
                self.movies = json.load(f)
            with open("users.json") as f:
                self.users = json.load(f)
            with open("ratings_test.json") as f:
                self.ratings_test = json.load(f)
            with open("ratings_train.json") as f:
                self.ratings_train = json.load(f)

    def save(self):
        with codecs.open("movies.json", "wb", "utf-8") as f:
            buf = json.dumps(self.movies, indent=2, sort_keys=True)
            f.write(buf)
        with codecs.open("users.json", "wb", "utf-8") as f:
            buf = json.dumps(self.users, indent=2, sort_keys=True)
            f.write(buf)
        with codecs.open("ratings_test.json", "wb", "utf-8") as f:
            buf = json.dumps(self.ratings_test, indent=2, sort_keys=True)
            f.write(buf)
        with codecs.open("ratings_train.json", "wb", "utf-8") as f:
            buf = json.dumps(self.ratings_train, indent=2, sort_keys=True)
            f.write(buf)


movie_len_1m = MovielensReader(movielens_dataset_path)
movie_len_1m.load()
movie_len_1m.save()

# build tinkerpop graph for query k-hop
def graph_build():
    pass

