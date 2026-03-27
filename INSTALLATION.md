# Installation & Setup Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 512MB minimum
- **Disk**: 100MB free space

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd "c:\Users\Samsung\OneDrive\Desktop\ai-resume analyser\career-ai-platform"
```

Or wherever you cloned/placed the project.

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **flask** - Web framework
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX file handling
- **pdfplumber** - Advanced PDF parsing
- **requests** - HTTP library for testing

### 4. Verify Installation

Check if all packages are installed:
```bash
pip list
```

Should show: flask, PyPDF2, python-docx, pdfplumber, requests

## Running the Application

### Option 1: Simple Run (Development)

```bash
python app.py
```

Output should show:
```
 * Serving Flask app 'backend.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Option 2: Direct Backend Run

```bash
python backend/app.py
```

### Direct Run Backend Script

```bash
cd backend
python -m flask run
```

## Accessing the Application

1. **Open Browser**: Go to `http://localhost:5000`
2. **Upload Resume**: Browse and select a PDF, DOCX, or TXT file
3. **View Results**: Instant analysis with skills, recommendations, and job matches

## Running Tests

With the server running, in a new terminal:

```bash
python test_system.py
```

This runs 4 comprehensive tests:
- ✅ Server availability
- ✅ Resume analysis
- ✅ Skill matching
- ✅ Skill detection accuracy

## Troubleshooting

### Error: "Port 5000 is already in use"

**Solution:** Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=8000, debug=True)  # Change 5000 to 8000
```

Then access: `http://localhost:8000`

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Reinstall dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error: "Cannot extract text from PDF"

**Solution:** 
- Ensure PDF is valid and not image-only
- Try converting to DOCX or TXT format
- Use DOCX or TXT files as fallback

### Sample Resume Analysis Shows No Skills

**Possible Causes:**
1. Resume file is corrupted or image-only
2. Skills not in the detection list
3. Text extraction failed

**Solution:**
- Check the extracted text in browser console
- Add more skills to `backend/skill_analyzer.py` SKILL_LIST
- Try with sample.txt file first

### Frontend Not Loading

**Check:**
1. Server is running: `http://localhost:5000` should show 404 (not connection refused)
2. Frontend files exist: `frontend/index.html`, `frontend/style.css`, `frontend/script.js`
3. No browser console errors (press F12)

## File Upload Limits

- **Max File Size**: 16MB (configurable in `backend/app.py`)
- **Supported Formats**: PDF, DOCX, TXT
- **Storage Location**: `uploads/` folder

## API Testing with cURL

### Test Resume Analysis:
```bash
curl -F "file=@uploads/sample.txt" http://localhost:5000/api/resume/analyze
```

### Test Skill Matching:
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{"resume_skills":["python","sql"],"job_skills":["python","sql","docker"]}'
```

## Environment Variables (Optional)

Create a `.env` file:
```
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

Then use in code:
```python
import os
port = os.getenv('PORT', 5000)
```

## Production Deployment

### Using Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "backend.app:create_app()"
```

### Using Docker (Optional):

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t career-ai .
docker run -p 5000:5000 career-ai
```

## Custom Configuration

### Change Detected Skills

Edit `backend/skill_analyzer.py`:
```python
SKILL_LIST = [
    "python","java","javascript","react",
    "your_new_skill"  # Add here
]
```

### Change Recommended Roles

Edit `backend/skill_analyzer.py`:
```python
ROLE_SKILLS = {
    "Your Job Role": ["required", "skills"],
}
```

### Add More Job Postings

Edit `backend/job_matcher.py`:
```python
JOB_POSTINGS = [
    {
        "title": "New Position",
        "requirements": ["skill1", "skill2"],
        "description": "..."
    }
]
```

## Directory Structure After Installation

```
career-ai-platform/
├── backend/
│   ├── app.py
│   ├── resume_parser.py
│   ├── skill_analyzer.py
│   ├── job_matcher.py
│   └── __init__.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── uploads/              # Created when first file is uploaded
│   └── sample.txt
├── venv/                 # Created by virtual environment
├── app.py
├── requirements.txt
├── test_system.py
├── README.md
└── INSTALLATION.md
```

## Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| Port already in use | Change port number in `app.py` |
| No modules found | Run `pip install -r requirements.txt` |
| Can't upload files | Check `uploads/` folder permissions |
| No skills detected | Verify resume has text (not image) |
| Frontend not showing | Ensure Flask is serving static files |
| Slow response | Close other applications, increase timeout |

## Performance Tips

1. **Use TXT files** for fastest processing
2. **Keep uploads < 5MB** for quick analysis
3. **Close browser tabs** to free up RAM
4. **Restart server** if it gets slow
5. **Run on SSD** for better performance

## Getting Help

1. Check error messages in terminal
2. Review browser console (F12)
3. Look at server logs
4. Test with `test_system.py`
5. Verify all dependencies installed

## Next Steps

After successful installation:

1. ✅ Run the application
2. ✅ Test with sample.txt
3. ✅ Run test_system.py
4. ✅ Upload your own resume
5. ✅ Customize skills and roles
6. ✅ Deploy to production (if needed)

---

**Happy Analyzing! 🚀**
