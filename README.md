# 🎵 Music Agent API

This Django-based REST API uses **Gemini AI** to recommend songs based on user input.  
If the AI is unavailable or rate-limited, it falls back to a built-in list of curated recommendations.

---

## 🚀 Features

- AI-powered music recommendations using **Gemini AI**
- Fallback logic when API quota is exceeded
- JSON-based REST endpoint compatible with Postman or A2A
- Built with **Django 5**, **Python 3.10+**

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/musicagent.git
cd musicagent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

In the root directory, create a `.env` file with:

```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
GEMINI_API_KEY=your_gemini_api_key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Server

```bash
python manage.py runserver
```

Your API should now be running at:
👉 `http://127.0.0.1:8000/api/music-agent/`

---

## 🧪 Testing with Postman

1. Open Postman and create a **POST** request to:
   ```
   http://127.0.0.1:8000/api/music-agent/
   ```
2. In the **Body** tab, choose **raw** and **JSON**, then send:
   ```json
   {
     "message": "Recommend an afrobeat song"
   }
   ```

You’ll receive a JSON response like:
```json
{
  "response": {
    "title": "Essence",
    "artist": "Wizkid ft. Tems"
  },
  "status": "success"
}
```

---

## ☁️ Deployment on Railway or Render

Include this **Procfile** in your root folder:

```
web: gunicorn musicagent.wsgi:application
```

Make sure your environment variables (especially `GEMINI_API_KEY`) are set in your hosting dashboard.

---

## 📁 Project Structure

```
musicagent/
│
├── recommender/
│   ├── ai_agent.py
│   ├── views.py
│   ├── urls.py
│
├── musicagent/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
├── requirements.txt
├── Procfile
└── .env
```

---

## 🧠 Example Response

**Request:**
```json
{"message": "love song"}
```

**Response:**
```json
{
  "response": {
    "title": "All of Me",
    "artist": "John Legend"
  },
  "status": "success"
}
```

---

## 🛠 Tech Stack

- **Backend:** Django + Django REST Framework  
- **AI Model:** Gemini API  
- **Language:** Python 3.10+  
- **Database:** SQLite (default)

---

## 🧾 License

This project is open-source under the MIT License.