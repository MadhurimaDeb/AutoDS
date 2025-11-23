# AutoData

**By Madhurima Deb**

AutoData is my personal brainchild — a project born from the idea of creating a fully modular, scalable, and intelligent **no‑code + low‑code Data Science platform**, built almost entirely in Python. I am designing and developing AutoData as a long‑term, evolving system that grows with my knowledge, experiences, and the needs of users who want to perform data science without writing code, while still having the power to customize everything manually.

This repository documents my vision and ongoing development of AutoData: a tool that blends automation, control, explainability, and guided learning — all within a clean Streamlit interface.

---

## 🚀 Project Vision

AutoData is being developed around one clear philosophy:

> **Every stage of the data science pipeline must have two modes — Manual Mode for full control, and Automatic Mode for intelligent one‑click execution.**

This structure ensures that AutoData remains:

* Beginner‑friendly
* Analyst‑friendly
* Developer‑friendly
* Scalable for future advanced ML/DL integrations

The goal is to create a unified platform where anyone — regardless of skill level — can seamlessly:

* Import data
* Prepare and clean datasets
* Perform full EDA
* Generate visualizations
* Engineer features
* Build ML/DL models
* Evaluate and export outputs
* Understand everything through an AI assistant

And do all of this using either **guided automation** or **full manual control**.

---

## 🧩 Current & Planned Features

AutoData is being built as a continuously expanding system. Below are the key components — some already implemented, others planned on the roadmap.

### ⭐ 1. Dataset Import & Version Management

* Upload multiple formats (CSV, Excel, JSON, Parquet)
* Auto‑detect schema, dtypes, missing patterns
* Versioned dataset storage (raw → cleaned → engineered)
* Reload any version in any module
* Foundation for dataset lineage

### ⭐ 2. Data Preparation Module

#### Manual Mode (Current + Planned)

* Drop/rename columns
* Filtering & conditional logic
* Scaling, normalization, transformation
* Missing value strategies
* Outlier detection and fixing

#### Automatic Mode (Planned)

* Smart cleaning pipeline
* AI‑driven suggestions
* One‑click preprocessing

### ⭐ 3. Feature Engineering Module

#### Manual Mode

* Encoding (One‑Hot, Label, Target, etc.)
* Polynomial features
* Date/time extraction
* Text preprocessing
* Custom formula‑based feature creation

#### Automatic Mode

* Auto‑feature generation
* Feature selection based on correlation & importance
* Multicollinearity diagnostics

### ⭐ 4. EDA & Visualization Module

#### Manual Mode

* Customizable plot builder
* Statistical summaries
* Column‑wise exploration tools

#### Automatic Mode

* Auto‑EDA report (Sweetviz)
* AI‑generated insight report
* Recommendation engine for next steps

### ⭐ 5. Machine Learning Module

#### Manual Mode

* Classification / Regression selection
* Algorithm selector
* Hyperparameter tuning
* Manual feature selection
* Multiple evaluation metrics

#### Automatic Mode

* AutoML engine
* Multi‑model comparison
* Automated hyperparameter optimization
* Natural‑language model explanation

### ⭐ 6. Model Evaluation & Explainability

* SHAP, LIME (manual)
* Automated evaluation report (planned)
* AI explanation of performance strengths and weaknesses

### ⭐ 7. Model Export

* Export trained model + preprocessing pipeline
* ONNX export planned
* Metadata packaging

### ⭐ 8. Integrated AI Assistant

Powered by Gemini Pro Vision:

* Explains each operation
* Suggests next steps
* Performs guided EDA
* Helps beginners learn DS concepts
* Identifies pipeline issues early

---

## 🌱 Future Scope & Scalability

AutoData is intentionally designed for **long‑term expansion**. Planned future enhancements include:

* Deep learning model builder UI
* Time‑series automation
* NLP transformations and embeddings
* Cloud dataset hosting & syncing
* User authentication & personalized workspace
* Exporting full pipelines as Python scripts
* Workflow orchestration and scheduling

Suggestions, ideas, and collaborative improvements are always welcome — AutoData will grow stronger with community input.

---

## 🧑‍💻 Tech Stack

AutoData prioritizes Python‑first development using:

* Streamlit (UI)
* Pandas, NumPy, PyArrow (data engine)
* Scikit‑learn, XGBoost, CatBoost (ML)
* Matplotlib, Seaborn, Plotly (visuals)
* Sweetviz (auto‑EDA)
* Google Generative AI (chatbot & insights)
* Parquet‑based dataset versioning

---

## 🛠️ Installation

```
git clone <repo-url>
cd AutoData
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

---

## 🤝 Contributions & Ideas

Although this is my personal project, I am completely open to suggestions, ideas, feature requests, and even future open‑source collaboration.

If you have thoughts, feel free to open an issue or reach out.

---

## 🖊️ Author

**Madhurima Deb**
Data Scientist | ML Engineer | Creator of AutoData

This project represents my passion for merging automation, usability, and deep data science knowledge into a single, powerful platform.
