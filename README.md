# 🛡️ Network Security ML: Phishing Detection System

A production-ready, full-stack Machine Learning application built for real-time phishing URL detection. This architectural overhaul seamlessly integrates a massive dataset (`data/raw`) powered by a highly modular, decoupled FastAPI backend and a clean, Apple-styled vanilla Javascript Single Page Application.

## 🌟 Key Features
* **Real-time URL Scanning:** Paste any website URL and instantly classify it as ✅ Legitimate or ❌ Phishing using 30 heuristic structural features.
* **Batch CSV Processing:** Upload bulk feature datasets through the "Test a Website" modal for mass rapid inference.
* **Single Page Dashboard:** Recruiter Mode provides intuitive visualizations of dataset sizes, Target Class distributions, and Machine Learning Model accuracy curves.
* **Microservices Architecture:** Fully decoupled routes, prediction services, configuration environments, and physical asset dependencies.
* **RAM-Optimized Inference:** The project uses a high-performance Python Singleton class to cache models in memory upon server boot, dramatically reducing API response latencies.

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python 3.10+, Uvicorn, Pandas, Pydantic, Scikit-Learn.
* **Frontend:** Vanilla HTML5, semantic CSS3, Vanilla DOM JavaScript, Chart.js.
* **Model:** Highly tuned categorization classification based on standard UCI phishing patterns.

## 📂 Folder Architecture

```text
Network_Security/
│
├── app/
│   ├── main.py              # FastAPI entry point & router mounting.
│   ├── core/
│   │   └── config.py        # Environment & path configurations.
│   ├── api/v1/
│   │   ├── api_router.py    # Router aggregator.
│   │   └── endpoints/       # Versioned API routes (predict, health).
│   ├── services/            # Business logic (prediction, extraction).
│   └── schemas/             # Pydantic request/response models.
│
├── ml/                      # Core Machine Learning pipeline.
├── data/raw/                # Initial raw datasets.
├── models/                  # Model artifacts and loader singleton.
├── frontend/                # Decoupled UI assets (JS/CSS/HTML).
├── requirements.txt         # Project dependencies.
├── render.yaml              # Render deployment blueprint.
└── README.md
```

## ⚙️ Setup Instructions

### 1. Environment Installation
Ensure you are using Python 3.10+ and install the requirements:
```bash
pip install -r requirements.txt
```

### 2. Spinning Up The Server
The application is pre-optimized for production utilizing Uvicorn standard package conventions.
```bash
uvicorn app.main:app --reload --port 8000
```
> Or simply `python3 -m app.main`
> Navigate to `http://localhost:8000` to view the dashboard.

## 🚀 Deployment (Native via Render)
The project includes a `render.yaml` blueprint for easy deployment:

1. Push this code to your GitHub repository.
2. Connect the repository to [Render](https://render.com/).
3. Render will automatically build via `pip install -r requirements.txt` and start via `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

### ⚠️ Important Note:
Upon your first deployment, ensure you visit the **Recruiter Mode** and click **Run Complete Pipeline** to generate the initial ML model artifacts on the server!

## 🌐 API Usage

### `POST /api/v1/predict_url`
**Request:**
```json
{
    "url": "https://secure-login-example.com"
}
```
**Response:**
```json
{
    "status": "success",
    "prediction": "Legitimate",
    "reasons": ["URL structural components look standard and safe."],
    "confidence": 0.96
}
```
