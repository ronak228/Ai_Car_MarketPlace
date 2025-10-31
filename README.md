# 🚗 CarCrafter AI – Intelligent Car Price Prediction System

## 📖 Project Overview
CarCrafter AI is an intelligent, machine-learning–driven web platform that predicts the market price of a car using real-world parameters such as brand, model year, mileage, fuel type, engine capacity, and ownership history.  
It leverages supervised learning algorithms to analyze historical datasets and estimate fair car values under real-life market conditions.  
Built with **Python**, **Flask**, and **Bootstrap**, the system provides a clean, interactive dashboard where users can input details and instantly receive AI-generated price predictions along with analytical visualizations.  
This project aims to make automobile valuation transparent, data-driven, and accessible for buyers, sellers, and dealerships alike.

---

## ✨ Key Features
- **AI-Powered Price Prediction:**  
  Uses regression algorithms like Linear Regression, Random Forest, and XGBoost to estimate car prices accurately.
- **Interactive Dashboard:**  
  Displays predictions, comparison graphs, and trend analytics using Matplotlib and Seaborn.
- **User-Friendly Interface:**  
  Responsive design created with HTML, CSS, JavaScript, and Bootstrap.
- **Dataset Management:**  
  Handles large automotive datasets (CSV-based) containing essential vehicle parameters.
- **Real-Time Model Integration:**  
  Machine-learning model serialized with Joblib for quick inference.
- **Secure Backend:**  
  Server-side computations in Flask ensure data security and integrity.
- **Modular Design:**  
  Three-tier structure for easy maintenance, scalability, and feature expansion.

---

## 🧩 System Architecture
CarCrafter AI follows a **three-layer architecture**:

1. **Data Layer** – Handles dataset storage, preprocessing, and feature extraction.  
2. **Logic Layer** – Hosts the ML engine (Scikit-learn) for model training, evaluation, and prediction.  
3. **Presentation Layer** – Provides the Flask-based web interface for input, prediction, and analytics display.

This architecture enables smooth data flow, modular development, and reliable performance across all modules.

---

### ⚙️ Functional Roles
**Users:** Enter car details and receive instant AI-based price predictions through the dashboard.  
**Administrator:** Manages datasets, retrains models, and monitors system performance.  
**Background Tasks:** Automate dataset updates, log tracking, and model maintenance without affecting UI performance.

---

### 🔐 Authentication & Security
All core logic runs on the **server side** to prevent model or data exposure.  
Flask session handling, parameterized queries, and environment-variable storage (`.env`) protect sensitive credentials.  
HTTPS and CORS configurations secure communications, while input validation prevents SQL injection and unauthorized requests.  
Regular logging and exception monitoring ensure stable and trustworthy operation.

---

### 🎨 User Experience & Interface Design
The interface focuses on clarity and responsiveness, developed with **Bootstrap** and **JavaScript**.  
The dashboard includes live data visualization, prediction summaries, and trend charts.  
Interactive inputs, instant feedback, and intuitive navigation make it easy for users to analyze and understand results.  
Every UI component maintains visual consistency, ensuring a professional and engaging experience.

---

## 💻 Technology Stack & Infrastructure Overview

### 🧠 Core Technologies
- **Languages:** Python, HTML, CSS, JavaScript  
- **Frameworks & Libraries:** Flask, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Bootstrap  
- **Tools:** Visual Studio Code, Jupyter Notebook, Postman, Git  
- **Database:** CSV / SQLite  
- **Model Deployment:** Joblib for serialization and real-time integration  

### 🧩 Infrastructure Details
1. **Local Development:**  
   Runs via Flask server at `http://localhost:5000` with auto-reload for rapid testing.  
2. **Model & Data Pipeline:**  
   Includes preprocessing, encoding, model training, and serialization (`model.pkl`).  
3. **Testing:**  
   APIs validated using Postman and Flask’s test client for reliability.  
4. **Environment Configuration:**  
   All credentials (model paths, dataset locations) securely stored in `.env`.  

---

## 🧠 Methodology
1. **Data Collection:** Real-world automotive datasets from Kaggle and other sources.  
2. **Data Cleaning:** Handling missing values, removing duplicates, encoding categorical data.  
3. **Feature Engineering:** Selecting parameters influencing price such as brand, mileage, and fuel type.  
4. **Model Training:** Applying regression algorithms (Linear Regression, Random Forest, XGBoost).  
5. **Evaluation:** Metrics like R² Score, MAE, RMSE used to assess accuracy.  
6. **Deployment:** Integrated trained model with Flask backend for real-time predictions.  
7. **Visualization:** Dashboard plots relationships between variables and predicted outcomes.

---

## 📊 Performance Evaluation
| Algorithm | R² Score | MAE | RMSE |
|------------|-----------|------|------|
| Linear Regression | 0.87 | 1.15 | 2.05 |
| Decision Tree | 0.91 | 0.92 | 1.60 |
| Random Forest | 0.94 | 0.75 | 1.28 |
| XGBoost | **0.96** | **0.62** | **1.04** |

The **XGBoost Regressor** achieved the best overall accuracy and is used in deployment.

---

## 🚀 Installation & Setup

### Step 1 – Clone the Repository
```bash
git clone https://github.com/ronak228/CarCRafter-A_Car_Price_Predictor.git
cd CarCrafter-AI
