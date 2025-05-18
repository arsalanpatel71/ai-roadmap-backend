# 🚀 AI Roadmap Generation Tool

An AI-powered roadmap generator built for consultancies to streamline project planning. Users can submit business details, interact with an AI assistant in real-time, and receive a customized roadmap PDF via email.

---

## 📌 Features

- 🧠 AI-driven chat powered by OpenAI Assistant
- 📄 Automatic PDF generation of roadmaps
- 📧 Email delivery using SendGrid
- 🧾 Full chat export as downloadable PDF
- 🗂 MongoDB-based storage of all submissions and history
- 🔒 CORS-enabled secure WebSocket communication

---

## ✅ Before you start

- I have used my own credentials for mongodb(atlas) and sendgrid, and i will be diabling it in some days, so please if you can create your own credentials and use that, that would be great.
- Also i am using sendgrid for email delivery, it is very slow and sometimes takes time so please be patient.

## ✅ Prerequisites

- Python **3.8 or higher**
- [`wkhtmltopdf`](https://wkhtmltopdf.org/downloads.html) installed and accessible
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account
- A [SendGrid](https://sendgrid.com/) account (with verified sender email)
- An [OpenAI API Key](https://platform.openai.com/account/api-keys)

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
# for more reference i have pasted the how the structure of the project is, you can refer to that.


# Create the environment
python -m venv venv

# Activate (choose your OS)
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# create .env file and add the credentials but if you want to use my credentials, you can use that.

# run the app
uvicorn app.main:app --reload --port 8000


## 📡 API Endpoints

### 📋 Form Submission

POST /api/form/submit

Collects user and company info

Returns a request_id for chat session tracking

### 💬 WebSocket Chat

WS /ws/{request_id}

Real-time AI assistant chat

Responds to business inputs and returns strategic steps

Triggers PDF roadmap generation after final phase

### 📄 PDF Generation (Single Response)

POST /api/pdf/generate/{request_id}/{message_id}

Generates PDF for a specific AI response

Sends the PDF to the user via email

### 📁 Export Chat History

POST /api/pdf/export-chat-history/{request_id}

Compiles entire chat session into a PDF

Sends the full transcript to the user
```

## 🔒 Security Highlights

🔒 CORS-protected frontend access

🛡️ Pydantic input validation

🔐 Encrypted MongoDB credentials

🔌 Secure WebSocket communication

🧩 Environment variables for API keys and secrets

## 📡 Local Development Info

Backend runs locally on http://localhost:8000

Frontend (recommended): Deploy on Vercel or run locally on http://localhost:8080

Adjust CORS and API base URL accordingly

# Project Structure

project_root/
├── app/
│ ├── api/
│ │ ├── chat.py
│ │ ├── form.py
│ │ ├── pdf.py
│ │ └── websocket.py
│ ├── core/
│ │ ├── config.py
│ │ └── database.py
│ ├── schemas/
│ │ ├── chat.py
│ │ ├── form.py
│ │ └── pdf.py
│ ├── services/
│ │ ├── chat.py
│ │ ├── form.py
│ │ ├── pdf.py
│ │ └── sendgrid_email.py
│ ├── templates/
│ │ ├── ai_roadmap.html
│ │ └── chat_export_template.html
│ ├── utils/
│ │ └── format.py
│ └── main.py
├── .env
├── requirements.txt
└── venv(your virtual environment)
