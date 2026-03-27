# AI Career Growth Platform

A real-time resume analysis and career recommendation engine powered by AI/NLP.

## ✨ Features

- **Resume Upload**: Upload PDF, DOCX, or TXT resumes
- **Skill Detection**: Identifies 15+ technical skills from resume text
- **AI Analysis**: Generates data-driven strengths, weaknesses, and suggestions
- **Career Recommendations**: Suggests suitable roles based on skills
- **Job Matching**: Simulates LinkedIn job matching with skill gap analysis
- **Real Analysis**: No dummy data - all outputs depend on YOUR resume content

## 📋 Project Structure

```
career-ai-platform/
├── backend/
│   ├── app.py                 # Flask application & API endpoints
│   ├── resume_parser.py       # PDF/DOCX/TXT text extraction
│   ├── skill_analyzer.py      # Skill detection & analysis
│   ├── job_matcher.py         # Job matching simulation
│   └── __init__.py
├── frontend/
│   ├── index.html            # Interactive UI
│   ├── style.css             # Beautiful styling
│   └── script.js             # Dynamic interactions
├── uploads/                  # Resume storage
├── app.py                    # Entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

Server runs on `http://localhost:5000`

### 3. Open in Browser
Go to `http://localhost:5000` and upload your resume

## 🛠️ API Endpoints

### POST /api/resume/analyze
Upload and analyze a resume.

**Request:**
```bash
curl -F "file=@resume.pdf" http://localhost:5000/api/resume/analyze
```

**Response:**
```json
{
  "skills_found": ["python", "javascript", "sql"],
  "missing_skills": ["docker", "aws", "kubernetes"],
  "analysis": {
    "strengths": [...],
    "weaknesses": [...],
    "suggestions": [...]
  },
  "role_recommendations": [...],
  "job_matches": [...]
}
```

### POST /api/match
Match resume skills with job requirements.

**Request:**
```json
{
  "resume_skills": ["python", "sql"],
  "job_skills": ["python", "sql", "docker"]
}
```

**Response:**
```json
{
  "matched_skills": ["python", "sql"],
  "missing_skills": ["docker"],
  "match_percentage": 66.7
}
```

## 📊 Skills Database

The system detects these core technical skills:

```
python, java, javascript, react, nodejs, html, css, sql, mongodb, 
machine learning, data science, deep learning, docker, git, aws, linux
```

## 🎯 Recommended Roles

Based on detected skills, the system recommends:

- **Software Developer** - Requires: python, java, javascript, git, docker
- **Frontend Developer** - Requires: javascript, react, html, css, git
- **Backend Developer** - Requires: python, nodejs, sql, docker, git
- **Data Analyst** - Requires: sql, python, data science, excel, mongodb
- **ML Engineer** - Requires: python, machine learning, deep learning, tensorflow, pandas

## 📝 Analysis Output

### Strengths Detection
- Technical expertise (based on skills found)
- Experience count & diversity
- Education & certifications
- Industry specialization
- Career progression

### Weaknesses Detection
- Limited experience
- Low skill count
- Missing education
- Resume quality score
- Missing trending skills

### Suggestions for Improvement
- Add missing core skills
- Get industry certifications
- Gain diverse experience
- Build portfolio projects
- Improve LinkedIn presence

## 💾 File Support

- ✅ **PDF** - Extracts text using PyPDF2
- ✅ **DOCX** - Extracts text using python-docx
- ✅ **TXT** - Plain text files

## ⚙️ Technology Stack

**Backend:**
- Flask (Python web framework)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- pdfplumber (PDF text extraction)

**Frontend:**
- HTML5
- CSS3 (Gradient styling)
- Vanilla JavaScript (no jQuery/React required)

## 📊 Data Flow

```
1. User uploads resume
   ↓
2. Backend extracts text
   ↓
3. Skill analyzer detects skills (scans against skill list)
   ↓
4. Resume analyzer generates insights (based on content)
   ↓
5. Role recommender matches skills to careers
   ↓
6. Job matcher simulates LinkedIn matching
   ↓
7. Frontend displays comprehensive results
```

## 🧪 Testing

### Test with Sample Resume
```bash
curl -F "file=@uploads/sample.txt" http://localhost:5000/api/resume/analyze
```

### Test Skill Matching
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{"resume_skills":["python","sql"],"job_skills":["python","sql","docker"]}'
```

## 🔧 Customization

### Add More Skills
Edit `backend/skill_analyzer.py`:
```python
SKILL_LIST = [
    "python", "java", ..., "new_skill"
]
```

### Add More Recommended Roles
Edit `backend/skill_analyzer.py`:
```python
ROLE_SKILLS = {
    "New Role": ["skill1", "skill2", ...],
}
```

### Add Mock Job Postings
Edit `backend/job_matcher.py`:
```python
JOB_POSTINGS = [
    {
        "title": "New Job",
        "requirements": ["skill1", "skill2"],
        "description": "Job description here"
    },
]
```

## 📈 Key Metrics

- **Skills Detected**: All mentioned in skill list
- **Match Percentage**: (Matched Skills / Total Required Skills) * 100
- **Quality Score**: Based on resume completeness (0-100)
- **Recommendation Accuracy**: Depends on resume content quality

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Analysis**: Instant feedback
- **Color-coded Output**: Easy to read results
- **Progress Indicator**: Shows analysis in progress
- **Error Handling**: Clear error messages

## ⚠️ Important Notes

- **No Dummy Data**: All outputs are generated from resume content
- **Local Processing**: All analysis happens on your machine
- **File Storage**: Resumes stored in `uploads/` folder
- **Development Only**: Use proper WSGI server for production
- **Privacy**: No data sent to external APIs

## 🚀 Deployment

For production deployment:

1. Install WSGI server:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. Use reverse proxy (nginx/Apache)

4. Enable HTTPS

5. Add rate limiting

## 📞 Support

For issues or suggestions, check the code or modify as needed!

---

**Made with ❤️ for Career Growth**
