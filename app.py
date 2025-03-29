# app.py
import streamlit as st
import subprocess

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Sentiment-Based Movie Recommender")
movie_title = st.text_input("Enter a movie title:", value="The Prestige")

top_n = st.slider("Number of recommendations", 5, 25, 10)

if st.button("Find Similar Movies"):
    with st.spinner("Crunching review vibes..."):
        result = subprocess.run(
            ["python", "tmdb_recommender.py", movie_title, "--top", str(top_n)],
            capture_output=True, text=True
        )
        st.code(result.stdout)
