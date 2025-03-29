import os
import argparse
import requests
import numpy as np
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === Load API Key ===
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"

# === TMDb API Wrappers ===

def search_movie(title):
    url = f"{TMDB_BASE}/search/movie"
    params = {
        "query": title,
        "include_adult": False,
        "language": "en-US",
        "page": 1,
        "api_key": API_KEY
    }
    response = requests.get(url, params=params).json()
    results = response.get("results", [])
    return results[0] if results else None

def get_movie_genre_ids(movie_id):
    url = f"{TMDB_BASE}/movie/{movie_id}"
    params = {
        "language": "en-US",
        "api_key": API_KEY
    }
    response = requests.get(url, params=params).json()
    genres = response.get("genres", [])
    return [g["id"] for g in genres]

def get_movie_reviews(movie_id):
    url = f"{TMDB_BASE}/movie/{movie_id}/reviews"
    params = {
        "language": "en-US",
        "page": 1,
        "api_key": API_KEY
    }
    response = requests.get(url, params=params).json()
    return [review["content"] for review in response.get("results", [])]

def get_movies_by_genres(genre_ids, pages=3):
    all_movies = []
    for page in range(1, pages + 1):
        url = f"{TMDB_BASE}/discover/movie"
        params = {
            "with_genres": ",".join(map(str, genre_ids)),
            "primary_release_date.lte": "2022-01-01",
            "sort_by": "vote_average.desc",
            "vote_count.gte": 50,
            "with_original_language": "en",
            "language": "en-US",
            "page": page,
            "api_key": API_KEY
        }
        response = requests.get(url, params=params).json()
        all_movies.extend(response.get("results", []))
    return all_movies

# === Core Logic ===

def recommend_similar_movies(title, top_n=25, pages=3):
    print(f"\n🔍 Searching for '{title}'...")
    target = search_movie(title)
    if not target:
        print("❌ Movie not found.")
        return

    target_id = target["id"]
    genre_ids = get_movie_genre_ids(target_id)
    if not genre_ids:
        print("⚠️ No genres found for this movie.")
        return

    target_reviews = get_movie_reviews(target_id)
    if not target_reviews:
        print("⚠️ No reviews found for the target movie.")
        return

    print(f"📖 Pulled {len(target_reviews)} reviews for {target['title']}")
    print(f"🎯 Using genres: {genre_ids}")

    movie_pool = get_movies_by_genres(genre_ids, pages)
    candidates = []

    for movie in movie_pool:
        if movie["id"] == target_id:
            continue
        reviews = get_movie_reviews(movie["id"])
        if reviews:
            candidates.append({
                "id": movie["id"],
                "title": movie["title"],
                "reviews": reviews
            })

    print(f"🎬 Comparing with {len(candidates)} similar-genre movies...")

    all_docs = [" ".join(target_reviews)] + [" ".join(m["reviews"]) for m in candidates]
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.85)
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    target_vec = tfidf_matrix[0]
    other_vecs = tfidf_matrix[1:]
    similarities = cosine_similarity(target_vec, other_vecs).flatten()

    ranked = sorted(zip(candidates, similarities), key=lambda x: x[1], reverse=True)

    print(f"\n🔥 Top {top_n} review-vibe matches to '{target['title']}':\n")
    for movie, score in ranked[:top_n]:
        print(f"[{score:.3f}] {movie['title']}")

# === CLI ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find movies with similar review vibe.")
    parser.add_argument("title", type=str, help="Movie title in quotes")
    parser.add_argument("--top", type=int, default=25, help="How many matches to show")
    args = parser.parse_args()

    recommend_similar_movies(args.title, top_n=args.top)
