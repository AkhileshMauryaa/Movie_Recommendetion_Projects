import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    
    if 'poster_path' in data and data['poster_path']:  
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    
    return "https://via.placeholder.com/500x750?text=No+Image"  # Default placeholder

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# ---- Streamlit App ----
st.title('🎬 Movie Recommender System')

# Load models
try:
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
except FileNotFoundError:
    st.error("Error: Required files ('movies.pkl' and 'similarity.pkl') not found. Please check file locations.")
    st.stop()

# Ensure 'movie_id' column exists
if 'movie_id' not in movies.columns:
    st.error("Error: 'movie_id' column not found in movies DataFrame.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Select or type a movie", movie_list)

if st.button('🎥 Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)  # Create 5 columns for movie recommendations
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
