# AutoDS

**By Madhurima Deb**

AutoDS is my personal brainchild — a project born from the idea of creating a fully modular, scalable, and intelligent **no-code + low-code Data Science platform**, built almost entirely in Python. I am designing and developing AutoDS as a long-term, evolving system that grows with my knowledge, experiences, and the needs of users who want to perform data science without writing code, while still having the power to customize everything manually.

This repository documents the vision and active development of AutoDS — a tool that blends automation, control, explainability, and guided learning, packaged within a modern Streamlit interface.

---

## 🚀 Project Vision

AutoDS is built on one core philosophy:

> **Every stage of the data science pipeline must provide two modes: Manual Mode (full control) and Automatic Mode (intelligent one-click execution).**

This ensures that AutoDS remains:

- Beginner-friendly  
- Analyst-friendly  
- Developer-friendly  
- Scalable for future advanced ML/DL integrations  

The goal is to create a unified platform where anyone — regardless of skill level — can seamlessly:

- Import datasets  
- Clean and preprocess data  
- Perform exploratory data analysis  
- Generate customizable visualizations  
- Engineer features  
- Build ML/DL models  
- Evaluate and explain results  
- Export pipelines and models  
- Learn concepts through an integrated AI assistant  

All of this available through both **guided automation** and **full manual control**.

---

## 🧩 Current & Planned Features

Below is a detailed overview of AutoDS’s modular design — a continuously expanding system.

### ⭐ 1. Dataset Import & Versioning
- CSV, Excel, Parquet, JSON support  
- Auto schema/dtype detection  
- Versioned dataset storage (raw → cleaned → engineered)  
- Ability to load any version into any module  

### ⭐ 2. Data Preparation

#### Manual Mode
- Drop/rename columns  
- Conditional filtering  
- Scaling & normalization  
- Missing value handling  
- Outlier detection  

#### Automatic Mode
- Smart preprocessing pipeline  
- AI-generated cleaning suggestions  
- One-click transformations  

### ⭐ 3. Feature Engineering

#### Manual Mode
- Encoding (One-Hot, Label, Target, etc.)  
- Polynomial features  
- Date/time feature extraction  
- Text preprocessing  
- Custom formula-based features  

#### Automatic Mode
- Auto-feature generation  
- Multicollinearity detection  
- AI-assisted feature selection  

### ⭐ 4. EDA & Visualization

#### Manual Mode
- Custom plot builder  
- Statistical summaries  
- Column-wise exploration  

#### Automatic Mode
- Sweetviz report  
- AI-generated insights  
- Next-step recommendations  

### ⭐ 5. Machine Learning

#### Manual Mode
- Classification & Regression  
- Algorithm selector  
- Hyperparameter tuning  
- Feature selection  
- Evaluation metrics  

#### Automatic Mode
- AutoML engine  
- Multi-model comparison  
- Automated hyperparameter tuning  
- Natural-language explanations  

### ⭐ 6. Evaluation & Explainability
- SHAP & LIME support  
- Model comparison tables  
- Automated evaluation report (planned)  
- AI-based performance reasoning  

### ⭐ 7. Model Export
- Export pickle model + preprocessing pipeline  
- ONNX export (planned)  
- Metadata packaging  

### ⭐ 8. Integrated AI Assistant

Powered by Gemini Pro Vision:
- Explain operations  
- Provide next-step recommendations  
- Guide EDA & data preparation  
- Help beginners understand DS concepts  
- Interpret model results  

---

## 🌱 Future Scope

Long-term planned expansions:

- Deep learning model builder  
- Time-series workflows  
- NLP embeddings & transformations  
- Cloud dataset sync & storage  
- Multi-user workspaces  
- Script/pipeline export to Python  
- Automated workflow orchestration  

---

## 🧑‍💻 Tech Stack

- Streamlit  
- Pandas, NumPy, PyArrow  
- Scikit-learn, XGBoost, LightGBM, CatBoost  
- Matplotlib, Seaborn, Plotly  
- Sweetviz (Auto-EDA)  
- Google Generative AI (AI assistant)  
- Parquet versioning system  

---

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repo-url>
cd AutoDS
```

# Create virtual environment (Python 3.11 recommended)
```bash
python3.11 -m venv .venv
```
# Activate environment
```bash
source .venv/bin/activate # for mac
.venv\Scripts\activate # for windows
```

# Install Required System Packages (macOS only)
```bash
brew install libomp
brew link libomp --force
```

# Upgrade pip and install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
# Run AutoDS
```bash
streamlit run app.py
```

---

## 🤝 Contributions & Ideas

Although this is my personal project, I am completely open to suggestions, ideas, feature requests, and even future open‑source collaboration.

If you have thoughts, feel free to open an issue or reach out- especially in:

- UI/UX improvements

- AutoML enhancements

- EDA automation

- New ML/DL modules

- Bug fixes & performance optimization

---

## 🔐 Branch Policy

main is protected

All changes must come from feature branches

Pull requests must pass CI and receive approval before merging

---

## 📬 How to Contribute

1. Fork this repository

1. Create a new branch:

```bash
git checkout -b feature/<feature-name>
```


3. Commit your changes:

```bash
git add .
git commit -m "Describe your update"
```

4. Push the branch:

```bash
git push -u origin feature/<feature-name>
```


5. Open a Pull Request

---

## 🖊️ Author

**Madhurima Deb**
Data Scientist | ML Engineer | Creator of AutoData

This project represents my passion for merging automation, usability, and deep data science knowledge into a single, powerful platform.
