
# 🎬 Sentiment-Based Movie Recommender

An AI-powered movie recommendation system that compares the sentiment *vibe* of user reviews across movies — using TMDb data and NLP magic.

> Enter a movie (e.g. _The Prestige_) and get a ranked list of other movies with similar emotional tone based on user reviews.

---

## 🚀 Features

- 🧠 **Sentiment Matching via TF-IDF**
- 🎭 **Automatically pulls genres from TMDb**
- 📖 **Fetches and compares real user reviews**
- 🎬 **Recommends movies with similar emotional feel**
- 🌐 **Mobile-accessible web app (Streamlit UI)**
- 📡 **Live CLI + Web modes**
- 💾 **TMDb API-powered**

---

## 🖥️ Demo (Streamlit UI)

![screenshot](https://via.placeholder.com/800x400.png?text=Streamlit+Movie+Recommender+Demo)

---

## 📦 How to Use

### 🔧 1. Clone the Repo

```bash
git clone https://github.com/your-username/imdb-sentiment-recommender.git
cd imdb-sentiment-recommender
```

### 📦 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file and add your TMDb API key:

```
TMDB_API_KEY=your_key_here
```

### 🧪 3. Run from CLI

```bash
python tmdb_recommender.py "The Prestige" --top 10
```

### 🌐 4. Run the Streamlit Web App

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then open in browser:
```
http://localhost:8501  ← on your computer  
http://your.local.ip:8501  ← on your phone (same Wi-Fi)
```

---

## 📚 Tech Stack

- Python
- Streamlit
- TMDb API
- scikit-learn (TF-IDF + Cosine Similarity)
- dotenv
- Requests

---

## 💡 Future Ideas

- Swap TF-IDF for BERT embeddings
- Add movie posters + metadata
- Export recommendations to CSV
- Deploy to Render or Streamlit Cloud

---

## 🧠 Author

**Noah Solorzano**  
[solorzanoah.com](https://solorzanoah.com)

---

## 🛡️ License

MIT License
