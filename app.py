import streamlit as st
import pickle
import requests
import pandas as pd

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e499d330a4d940551f508b84527af398&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        
        # fetch poster from API  
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

st.title("Movie recommendation system")

selected_movies_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommended'):
    names, posters = recommend(selected_movies_name)
    
    num_columns = 5
    
    cols = st.columns(num_columns)


    for i in range(len(names)):
        # with st.container():
        with cols[i % num_columns]:
            st.text(names[i])
            st.image(posters[i])