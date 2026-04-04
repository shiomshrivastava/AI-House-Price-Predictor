# 🏠 California House Price Predictor

An end-to-end Machine Learning project that predicts California housing prices using a **Random Forest Regressor** with an interactive **Streamlit web application**.

---

## 🚀 Overview

This project leverages the California Housing dataset to build a robust regression model capable of estimating house prices based on demographic, geographic, and economic features.

It includes:

* Data preprocessing & feature engineering
* Model training with hyperparameter tuning
* Interactive UI for real-time predictions
* Deployment-ready architecture

---

## ✨ Features

* 🔍 **Accurate Predictions** using Random Forest
* ⚙️ **Feature Engineering** for improved performance
* 🎯 **Hyperparameter Tuning** using RandomizedSearchCV
* 🖥️ **Interactive UI** built with Streamlit
* 🗺️ **Location Visualization** using Folium map
* 📊 **Real-time Predictions** with user input
* 🕘 **Prediction History Tracking**

---

## 🧠 Model Details

* **Algorithm:** Random Forest Regressor
* **Dataset:** California Housing Dataset
* **Features Used:** 12 (including engineered features)

  * Rooms per household
  * Bedrooms per room
  * Population per household
* **Evaluation Metric:** RMSE (Root Mean Squared Error)
* **Optimization:** RandomizedSearchCV

---

## 📁 Project Structure

```
project/
│
├── app.py              # Streamlit web application
├── train.py           # Model training & preprocessing
├── model.pkl          # Trained ML model
├── pipeline.pkl       # Data preprocessing pipeline
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/shiomshrivastava/AI-House-Price-Predictor.git
cd AI-House-Price-Predictor
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```
streamlit run app.py
```

---

## 📊 How It Works

1. User inputs housing data (location, population, income, etc.)
2. Feature engineering is applied
3. Data is transformed using the saved pipeline
4. Model predicts the house price
5. Results are displayed with visual insights

---

## 🧪 Model Training

To retrain the model:

```
python train.py
```

This will:

* Perform preprocessing
* Apply feature engineering
* Tune hyperparameters
* Save the trained model and pipeline

---

## 📌 Tech Stack

* Python
* Scikit-learn
* Pandas, NumPy
* Streamlit
* Folium

---

## 💡 Future Improvements

* Add model explainability (SHAP / feature importance)
* Deploy using cloud platforms (AWS / Render / Streamlit Cloud)
* Add user authentication
* Improve UI with more analytics

---

## 👨‍💻 Author

Developed by **[Your Name]**

---

## ⭐ Acknowledgment

* California Housing Dataset
* Scikit-learn Documentation
* Streamlit Community

---

## 📬 Feedback

If you found this project useful, feel free to ⭐ the repository!
