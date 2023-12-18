import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d36885fd36c59b1118d8745307c85e25"
    data = requests.get(url)
    data = data.json()
    
    # Check if 'poster_path' is available in the response
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    else:
        return None

movies= pickle.load(open("movies_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
movies_list = movies['original_title'].values

st.header("Movies Recommendation system")

#create a drop down to select a movie.
selected_movie = st.selectbox("Select a movie:", movies_list)

import streamlit.components.v1 as components

def recommend (movie):
    index = movies[movies['original_title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse = True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id 
        recommend_movie.append(movies.iloc[i[0]].original_title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie,recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(movie_name[i])
            st.image(movie_poster[i])