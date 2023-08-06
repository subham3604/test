import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json



def get_suggestions():
    data = pd.read_csv('final_data.csv')
    return list(data['title'].str.capitalize())

def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list

def rcmd(data,title):

    count = TfidfVectorizer(stop_words = 'english')

    count_matrix = count.fit_transform(data['soup'])


    cos_sim_matrix = cosine_similarity(count_matrix,count_matrix)
    
    indices = pd.Series(data.index, index=data['title']).drop_duplicates()

    idx = indices[title]

    sim_scores = list(enumerate(cos_sim_matrix[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    movies_recommend = data['title'].iloc[movie_indices]

    return movies_recommend

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/home")
def home():
    suggestions = get_suggestions()
    return render_template('home.html',suggestions=suggestions)

@app.route("/similar_movies",methods=["POST"])
def similar_movies():
    movie_title = request.form['name']
    data = pd.read_csv('final_data.csv')
    

    movie_title = str.lower(movie_title)
    data['title'] = data['title'].apply(lambda x: str.lower(x))

    if movie_title not in data['title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else :
        rcmd_movies = rcmd(data,movie_title)
        arr = []
        for title in rcmd_movies:
            print(title)
            arr.append(title)

        if type(arr)==type('string'):
            return rcmd_movies
        else:
            m_str="---".join(arr)
            return m_str

@app.route("/recommend",methods=["POST"])
def recommend():
    title = request.form['title']
    cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_posters = request.form['rec_posters']

    # get movie suggestions for auto complete
    suggestions = get_suggestions()

    # call the convert_to_list function for every string that needs to be converted to list
    rec_movies = convert_to_list(rec_movies)
    rec_posters = convert_to_list(rec_posters)
    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)

     # convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = cast_ids.split(',')
    cast_ids[0] = cast_ids[0].replace("[","")
    cast_ids[-1] = cast_ids[-1].replace("]","")

    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace('\n', '')
    
    movie_cards = {rec_movies[i]:rec_posters[i] for i in range(len(rec_posters))}
    print(movie_cards)

    casts = { cast_names[i]: [ cast_ids[i], cast_chars[i], cast_profiles[i] ] for i in range(len(cast_profiles))}

    cast_details = { cast_names[i]: [ cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i] ] for i in range(len(cast_bios))}

    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
        vote_count=vote_count,release_date=release_date,runtime=runtime,status=status,genres=genres,
        movie_cards=movie_cards,casts=casts,cast_details=cast_details)


if __name__ == '__main__':
    app.run(debug=True)


    
