
# 🧠 Sales Forecasting using Time Series

This project generates synthetic sales data and performs time series forecasting using Python. It simulates realistic patterns like trend, seasonality (weekly, monthly, yearly), noise, and even special events across multiple product categories.

---

## 📁 Project Structure

```
sales-forecasting/
│
├── app.py                   # Flask backend to serve forecasting interface
├── dataset_generator.py     # Script to generate synthetic sales data
├── requirements.txt         # Project dependencies
├── static/
│   └── css/
│       └── styles.css       # Custom styles
├── templates/
│   └── index.html           # UI page for forecasting
└── README.md                # You're reading it
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/abhi190804/sales-forecasting.git
cd sales-forecasting
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Application

```bash
python app.py
```

It will start a Flask server on `http://127.0.0.1:5000/`.

---

## 🧪 Features

- ✅ Synthetic sales data generator with configurable:
  - Seasonality: Weekly, Monthly, Yearly
  - Trend strength and Noise level
  - Multiple product categories
- ✅ Special events and promotional sales simulation
- ✅ Forecast future sales using statistical modeling
- ✅ Web interface with visualizations using Matplotlib
- ✅ Lightweight, customizable, and extensible codebase

---

## 📊 Libraries Used

- `Flask` - For the web server and routing
- `Pandas` - For time series and data manipulation
- `NumPy` - For numeric computations
- `Matplotlib` - For plotting time series charts
- `Statsmodels` - For statistical modeling (forecasting)
- `SciPy` - For mathematical tools

---

## 📦 Example Usage

To generate custom synthetic data:
```bash
python dataset_generator.py --start_date 2022-01-01 --periods 730 --seasonality yearly --trend_strength 0.7 --noise_level 0.3 --output custom_data.csv
```

---

## 📸 Screenshots (Optional)

![](https://raw.githubusercontent.com/abhi190804/sales-forecasting/main/screenshots/screenshot-5.png)
![](https://raw.githubusercontent.com/abhi190804/sales-forecasting/main/screenshots/screenshot-4.png)
![](https://raw.githubusercontent.com/abhi190804/sales-forecasting/main/screenshots/screenshot-3.png)
![](https://raw.githubusercontent.com/abhi190804/sales-forecasting/main/screenshots/screenshot-2.png)
![](https://raw.githubusercontent.com/abhi190804/sales-forecasting/main/screenshots/screenshot-1.png)


---

## 👨‍💻 Author

Built with ❤️ by Abhishek Kumar
