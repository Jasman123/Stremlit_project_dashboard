# 🌟 Stremlit_project_dashboard

### *Interactive Data Dashboard built with Streamlit*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit" />
  <img src="https://img.shields.io/badge/Data-Visualization-green" />
</p>

---

# 📘 Overview

**Stremlit_project_dashboard** is an interactive data dashboard built using **Streamlit**, designed to visualize, explore, and analyze datasets quickly and efficiently.  
The app loads data (e.g., `HourlyLineRecord - DataBase Try.csv`) and presents charts, tables, metrics, and interactive filters—all inside a lightweight browser UI.

This project is ideal for rapid data exploration, internal reporting, and sharing insights with both technical and non-technical users.

---

# ⚙️ Features

### 📁 Data Loading
- Built-in CSV loader  
- Supports structured datasets such as hourly logs or operational records  

### 📊 Interactive Visualizations
- Tables  
- Charts (line, bar, etc.)  
- Dynamic filtering  

### 🎨 Clean Streamlit UI
- Responsive layout  
- Sidebar controls  
- Easy-to-extend dashboard sections  

### 🛠 Customizable Structure
- Add new pages, plots, or KPIs easily  
- Modify `app.py` to integrate any dataset  

---

# 🗂 Directory Structure
---
Stremlit_project_dashboard/
├── app.py
├── requirements.txt
├── HourlyLineRecord - DataBase Try.csv
├── README.md
└── .devcontainer/
---


---

# 🚀 Installation & Setup

## 1. Clone the Repository
```bash
git clone https://github.com/Jasman123/Stremlit_project_dashboard
cd Stremlit_project_dashboard
```
## 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## 3. Install Requirements
```bash
pip install -r requirements.txt
```

## 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
Streamlit will launch automatically at:
http://localhost:8501
