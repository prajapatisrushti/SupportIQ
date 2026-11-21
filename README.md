
# SupportIQ 🎧
### Intelligent Customer Support Management System

SupportIQ is a web-based customer support management system built with Python and Streamlit. It helps support teams manage customer queries, track ticket progress, organize support requests, and monitor performance through an interactive dashboard.

The application also includes an NLP-powered FAQ assistant that matches user questions with relevant predefined answers using TF-IDF and cosine similarity.

## 🚀 Features

- **Interactive Dashboard** – Monitor total, open, in-progress, and resolved tickets.
- **Support Assistant** – Find relevant FAQ answers using NLP text similarity.
- **Ticket Creation** – Create support tickets with customer details, descriptions, and priority levels.
- **Automatic Category Suggestion** – Suggest ticket categories based on description similarity.
- **Ticket Management** – Search, track, and update ticket statuses.
- **Resolution Notes** – Record and save notes when resolving customer issues.
- **Data Visualization** – View ticket statistics and category distribution through interactive charts.
- **SQLite Database** – Store customer and ticket information locally.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| SQLite | Database management |
| Pandas | Data handling and analysis |
| Plotly | Interactive visualizations |
| Scikit-learn | NLP text matching using TF-IDF and cosine similarity |

## 📸 Application Screenshots

### 1. Dashboard
<!-- Add dashboard screenshot here -->

### 2. Create Support Ticket
<!-- Add create ticket screenshot here -->

### 3. Support Assistant
<!-- Add support assistant screenshot here -->

### 4. Manage Tickets
<!-- Add manage tickets screenshot here -->

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/prajapatisrushti/SupportIQ.git
```

### 2. Navigate to the project directory

```bash
cd SupportIQ
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your default browser.

## 🗄️ Database

SupportIQ uses SQLite for local data storage.

The database is initialized automatically when the application starts. Customer information, support tickets, ticket statuses, and resolution notes are stored locally.

## 🧠 How the Support Assistant Works

The Support Assistant uses Natural Language Processing (NLP) techniques:

1. Predefined FAQ questions and answers are stored in the application.
2. TF-IDF converts text into numerical feature vectors.
3. Cosine similarity compares the user's query with existing FAQ questions.
4. The most relevant matching answer is returned.

This is a similarity-based FAQ assistant, not a generative AI chatbot.

## 🔮 Future Improvements

- User authentication and role-based access.
- Email notifications for ticket updates.
- Advanced support analytics.
- Integration with generative AI APIs.
- Cloud database deployment.
- Multi-agent customer support workflows.

## 👩‍💻 Author

**Srushti Prajapati**

B.Sc. Computer Science Student | AI & Software Development Enthusiast

GitHub: [@prajapatisrushti](https://github.com/prajapatisrushti)

---

⭐ If you find this project interesting, consider giving it a star!
