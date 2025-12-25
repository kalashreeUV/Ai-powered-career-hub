from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, flash
import sqlite3, os
from werkzeug.utils import secure_filename
import PyPDF2
import docx
import math

app = Flask(__name__)
app.secret_key = "careerhub_secret"

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "careerhub.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
init_db()

# ---------- Helpers ----------
def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def analyze_resume(text):
    score = 50
    strengths, improvements, skill_gaps, ai_tips = [], [], [], []

    sections = {
        "Technical Skills": 0,
        "Soft Skills": 0,
        "Formatting & ATS Match": 70
    }

    career_insights = []
    keywords = {
        "python": "Python experience",
        "java": "Java experience",
        "sql": "SQL / Database experience",
        "communication": "Strong communication",
        "leadership": "Leadership skills",
        "project": "Project experience",
        "team": "Team collaboration",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "nlp": "Natural Language Processing",
        "javascript": "JavaScript",
        "react": "React.js",
        "html": "HTML",
        "css": "CSS"
    }

    text_lower = text.lower()
    is_fresher = "experience" not in text_lower or "internship" in text_lower

    for word, desc in keywords.items():
        if word in text_lower:
            score += 5
            strengths.append(desc)
            if word in ["python", "java", "sql"]:
                sections["Technical Skills"] += 20
            elif word == "communication":
                sections["Soft Skills"] += 40
            elif word == "leadership" and not is_fresher:
                sections["Leadership"] = sections.get("Leadership", 0) + 40
        else:
            improvements.append(f"Consider adding {word} experience")
            skill_gaps.append(word)
            ai_tips.append(f"Include {word} in your resume to improve your score.")

    score = min(score, 100)
    sections = {k: min(v, 100) for k, v in sections.items()}

    if any(x in text_lower for x in ["python", "java"]):
        career_insights.append("Eligible for Software Developer roles")
    if "sql" in text_lower:
        career_insights.append("Eligible for Data / Database roles")
    if "communication" in text_lower:
        career_insights.append("Suitable for Client-facing / Team roles")
    if "leadership" in text_lower and not is_fresher:
        career_insights.append("Good for Team Lead / Project roles")
    if any(x in text_lower for x in ["machine learning", "deep learning", "tensorflow", "pytorch"]):
        career_insights.append("Great fit for AI / ML Developer roles")
    if "javascript" in text_lower or "react" in text_lower:
        career_insights.append("Suitable for Frontend Developer roles")

    if not career_insights:
        career_insights.append("Consider adding key technical and soft skills for better job matching")

    return {
        "score": score,
        "strengths": strengths,
        "improvements": improvements,
        "skill_gaps": skill_gaps,
        "ai_tips": ai_tips,
        "section_scores": sections,
        "career_insights": career_insights
    }

# ---------- Roles ----------
roles_db = [
    {"title": "Python Developer", "keywords": ["python", "django", "flask"], "description": "Design and build applications using Python."},
    {"title": "Data Analyst", "keywords": ["sql", "excel", "python", "tableau"], "description": "Analyze and interpret data."},
    {"title": "Java Backend Developer", "keywords": ["java", "spring", "sql"], "description": "Develop server-side logic with Java."},
    {"title": "Business Analyst", "keywords": ["communication", "analysis", "documentation"], "description": "Work with clients to gather requirements."},
    {"title": "AI Developer", "keywords": ["machine learning", "deep learning", "tensorflow", "pytorch", "nlp", "ai"], "description": "Build intelligent applications using AI/ML models and frameworks."},
    {"title": "Data Scientist", "keywords": ["python", "pandas", "numpy", "machine learning", "statistics"], "description": "Extract insights from data and build predictive models."},
    {"title": "Frontend Developer", "keywords": ["javascript", "react", "css", "html"], "description": "Design and develop user interfaces for web applications."}
]

def generate_role_matches(skills):
    skills_lower = [s.lower() for s in skills]
    matched_roles = []
    for role in roles_db:
        match_count = sum(1 for k in role["keywords"] if any(k in sk.lower() for sk in skills_lower))
        if match_count > 0:
            missing_skills = [k for k in role["keywords"] if all(k not in sk.lower() for sk in skills_lower)]
            matched_roles.append({
                "title": role["title"],
                "description": role["description"],
                "match_score": int((match_count / len(role["keywords"])) * 100),
                "missing_skills": missing_skills
            })
    matched_roles.sort(key=lambda x: x["match_score"], reverse=True)
    return matched_roles

# ---------- Learning Paths ----------
learning_paths = {
    "Python Developer": {
        1: {"title": "Python Basics", "summary": "Learn Python fundamentals.", "topics": ["Syntax", "Functions", "OOP", "Modules"], "link": ("Python Tutorial", "https://www.learnpython.org/")},
        2: {"title": "Frameworks", "summary": "Flask & Django for real apps.", "topics": ["Flask", "Django", "REST APIs"], "link": ("Flask Docs", "https://flask.palletsprojects.com/")}
    },
    "Data Analyst": {
        1: {"title": "Foundations", "summary": "Data analytics & Excel basics.", "topics": ["Intro to Data Analytics", "Excel Basics", "SQL Intro"], "link": ("Data Analytics", "https://www.coursera.org/learn/introduction-to-data-analytics")},
        2: {"title": "SQL & Databases", "summary": "SQL queries & data cleaning.", "topics": ["Joins", "Data Cleaning", "Database Design"], "link": ("SQL Tutorial", "https://www.w3schools.com/sql/")},
        3: {"title": "Visualization", "summary": "Learn Tableau & Power BI dashboards.", "topics": ["Power BI", "Tableau", "Excel Advanced"], "link": ("Tableau Training", "https://www.tableau.com/learn/training")},
        4: {"title": "Python & Projects", "summary": "Python libraries for analysis.", "topics": ["Pandas", "NumPy", "Capstone Project"], "link": ("Kaggle Learn", "https://www.kaggle.com/learn")}
    },
    "Java Backend Developer": {
        1: {"title": "Java Core", "summary": "Java fundamentals.", "topics": ["OOP", "Collections", "Multithreading"], "link": ("Java Tutorial", "https://www.javatpoint.com/java-tutorial")},
        2: {"title": "Spring Framework", "summary": "Backend with Spring Boot.", "topics": ["Spring Boot", "REST APIs", "Hibernate"], "link": ("Spring Docs", "https://spring.io/guides")}
    },
    "Business Analyst": {
        1: {"title": "BA Foundations", "summary": "Basics of business analysis.", "topics": ["Requirement Gathering", "Process Mapping"], "link": ("BA Basics", "https://www.coursera.org/learn/business-analysis")},
        2: {"title": "Tools & Techniques", "summary": "BA tools like JIRA & Visio.", "topics": ["JIRA", "Confluence", "Wireframing"], "link": ("BA Tools", "https://www.udemy.com/course/business-analysis-fundamentals/")},
        3: {"title": "Advanced BA", "summary": "Advanced stakeholder management.", "topics": ["Agile BA", "User Stories", "Case Studies"], "link": ("Agile BA", "https://www.coursera.org/learn/agile-business-analysis")}
    },
   
    "AI Developer": {
        1: {"title": "ML Basics", "summary": "Machine learning fundamentals.", "topics": ["Regression", "Classification"], "link": ("ML Course", "https://www.coursera.org/learn/machine-learning")},
        2: {"title": "Deep Learning", "summary": "Neural networks & frameworks.", "topics": ["CNNs", "RNNs", "TensorFlow", "PyTorch"], "link": ("Deep Learning", "https://www.coursera.org/specializations/deep-learning")},
        3: {"title": "NLP", "summary": "Text-based AI applications.", "topics": ["Tokenization", "Embeddings", "Transformers"], "link": ("NLP Course", "https://huggingface.co/course")},
        4: {"title": "AI Projects", "summary": "Real-world AI projects.", "topics": ["Chatbot", "Image Classification", "Capstone"], "link": ("AI Projects", "https://github.com/topics/machine-learning-projects")}
    },
    "Data Scientist": {
        1: {"title": "Data Science Foundations", "summary": "Statistics and Python for data.", "topics": ["Statistics", "Pandas", "NumPy"], "link": ("Data Science Intro", "https://www.coursera.org/specializations/data-science-python")},
        2: {"title": "ML for DS", "summary": "Apply ML to data problems.", "topics": ["Regression", "Classification", "Clustering"], "link": ("ML DS", "https://www.kaggle.com/learn")},
        3: {"title": "Projects", "summary": "Complete DS projects.", "topics": ["EDA", "Prediction Models"], "link": ("DS Projects", "https://github.com/topics/data-science-projects")}
    },
    "Frontend Developer": {
        1: {"title": "Frontend Basics", "summary": "HTML, CSS & JS basics.", "topics": ["HTML", "CSS", "JavaScript"], "link": ("HTML/CSS/JS", "https://www.w3schools.com/")},
        2: {"title": "React.js", "summary": "Learn React for dynamic UIs.", "topics": ["React Components", "Hooks", "State Management"], "link": ("React Docs", "https://react.dev/")},
        3: {"title": "Frontend Projects", "summary": "Build and deploy apps.", "topics": ["Portfolio Website", "Todo App"], "link": ("Frontend Projects", "https://github.com/topics/frontend-project")}
    }
}

# ---------- Role Aliases ----------
role_aliases = {
    "Team Project": "Team Lead / Project Manager",
    "Project Manager": "Team Lead / Project Manager",
    "Team Lead": "Team Lead / Project Manager"
}

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)", (name, email, password))
            conn.commit()
            session["user"] = name
            flash("✅ Registration successful!", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("⚠️ Email already exists!", "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user"] = user[0]
            flash("✅ Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Invalid email or password!", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("⚠️ Please login first.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/resume")
def resume():
    if "user" not in session:
        flash("⚠️ Please login first.", "warning")
        return redirect(url_for("login"))
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        flash("⚠️ No file selected!", "danger")
        return redirect(url_for("resume"))
    file = request.files["resume"]
    if file.filename == "":
        flash("⚠️ Please upload a valid file.", "danger")
        return redirect(url_for("resume"))
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        flash("⚠️ Only PDF or DOCX resumes are allowed.", "danger")
        return redirect(url_for("resume"))

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    text = extract_text(file_path)

    if not any(word in text.lower() for word in ["education", "skills", "experience", "project"]):
        flash("⚠️ This file doesn’t look like a resume. Please upload a valid resume.", "danger")
        return redirect(url_for("resume"))

    result = analyze_resume(text)
    session["resume_analysis"] = result
    return render_template("resume_result.html", **result)

@app.route("/job_matching")
def job_matching():
    if "user" not in session:
        flash("⚠️ Please login first.", "warning")
        return redirect(url_for("login"))

    resume_data = session.get("resume_analysis")
    if not resume_data:
        flash("⚠️ Please analyze a resume first.", "warning")
        return redirect(url_for("resume"))

    skills = resume_data.get("strengths", [])
    career_insights = resume_data.get("career_insights", [])
    role_matches = generate_role_matches(skills)
    return render_template("job_matching.html", skills=skills, career_insights=career_insights, role_matches=role_matches)

# ---------- Learning Path & Prep Schedule ----------
@app.route("/learning_path/<role>")
def role_learning_path(role):
    if "user" not in session:
        flash("⚠️ Please login first.", "warning")
        return redirect(url_for("login"))

    role = role_aliases.get(role, role)
    if role not in learning_paths:
        flash("⚠️ No learning path available for this role.", "danger")
        return redirect(url_for("dashboard"))

    contents = learning_paths[role]

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{role}} Learning Path</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #f4f6f9; font-family: 'Segoe UI', sans-serif; }
            .container { margin-top: 40px; margin-bottom: 60px; }
            .card { border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px; padding: 20px; background: #fff; }
            .card h4 { font-weight: 700; margin-bottom: 12px; }
            .summary { font-style: italic; color: #555; }
            ul { margin-top: 10px; }
            .btn-custom { margin-right: 10px; }
            .path-title { color: #007bff; text-align: center; margin-bottom: 30px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="path-title">{{role}} Learning Path</h2>
            {% for step, details in contents.items() %}
            <div class="card">
                <h4>Step {{step}}: {{details.title}}</h4>
                <p class="summary">{{details.summary}}</p>
                <ul>
                    {% for topic in details.topics %}
                    <li>{{topic}}</li>
                    {% endfor %}
                </ul>
                <a href="{{details.link[1]}}" class="btn btn-primary btn-custom" target="_blank">📘 {{details.link[0]}}</a>
            </div>
            {% endfor %}
            <h3 class="mt-5">📅 Prepare for {{role}}</h3>
            <p>Select a timeline to get a personalized schedule:</p>
            <a href="{{ url_for('prep_schedule', role=role, duration='10days') }}" class="btn btn-success btn-sm">10 Days</a>
            <a href="{{ url_for('prep_schedule', role=role, duration='1month') }}" class="btn btn-info btn-sm">1 Month</a>
            <a href="{{ url_for('prep_schedule', role=role, duration='2months') }}" class="btn btn-warning btn-sm">2 Months</a>
            <a href="{{ url_for('prep_schedule', role=role, duration='3months') }}" class="btn btn-danger btn-sm">3 Months</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, role=role, contents=contents)

def generate_dynamic_schedule(role, duration):
    path = learning_paths.get(role)
    if not path:
        return None

    mapping = {
        "10days": (10, "Day"),
        "1month": (4, "Week"),
        "2months": (8, "Week"),
        "3months": (12, "Week"),
    }
    if duration not in mapping:
        return None

    slots, label = mapping[duration]

    # Collect all topics
    all_topics = []
    for step, details in path.items():
        for topic in details["topics"]:
            all_topics.append(f"{details['title']} → {topic}")

    schedule = {}
    index = 0
    total_topics = len(all_topics)

    for i in range(slots):
        if index >= total_topics:
            index = 0  # repeat topics if slots > topics
        schedule[f"{label} {i+1}"] = [all_topics[index]]
        index += 1

    return schedule



@app.route("/prep_schedule/<role>/<duration>")
def prep_schedule(role, duration):
    if "user" not in session:
        flash("⚠️ Please login first.", "warning")
        return redirect(url_for("login"))
    role = role_aliases.get(role, role)
    if role not in learning_paths:
        flash("⚠️ No learning path available for this role.", "danger")
        return redirect(url_for("dashboard"))
    schedule = generate_dynamic_schedule(role, duration)
    if not schedule:
        flash("⚠️ Invalid schedule duration.", "danger")
        return redirect(url_for("dashboard"))
    path = learning_paths[role]
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{role}} Prep Schedule</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #eef2f7; font-family: 'Segoe UI', sans-serif; }
            .container { margin-top: 40px; margin-bottom: 60px; }
            .schedule-card { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 12px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
            h2 { text-align: center; color: #333; margin-bottom: 30px; }
            h4 { color: #007bff; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{{role}} Prep Schedule ({{duration}})</h2>
            {% for slot, topics in schedule.items() %}
            <div class="schedule-card">
                <h4>Slot {{slot}}</h4>
                <ul>
                    {% for topic in topics %}
                    <li>{{topic}}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
            <a href="{{ url_for('role_learning_path', role=role) }}" class="btn btn-secondary mt-3">⬅ Back to Learning Path</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, role=role, path=path, schedule=schedule, duration=duration)

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("✅ Logged out successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


