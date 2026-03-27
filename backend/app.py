import os
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from pathlib import Path

from models import db, User
from resume_parser import extract_text
from skill_analyzer import analyze_skills

# ------------------ CONFIG ------------------

BASE_DIR = Path(__file__).parent.parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
FRONTEND_FOLDER = BASE_DIR / "frontend"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}


# ------------------ APP FACTORY ------------------

def create_app():

    app = Flask(
        __name__,
        static_folder=str(FRONTEND_FOLDER / 'static'),
        static_url_path='/static'
    )

    # ✅ SESSION SECRET
    app.secret_key = "supersecretkey"

    # ------------------ DATABASE ------------------

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ------------------ CONFIG ------------------

    app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    CORS(app)

    # ------------------ ROUTES ------------------

    @app.route('/')
    def serve_login():
        if 'user_id' in session:
            return send_from_directory(str(FRONTEND_FOLDER), 'index.html')
        return send_from_directory(str(FRONTEND_FOLDER), 'login.html')

    @app.route('/home')
    def serve_home():
        if 'user_id' not in session:
            return send_from_directory(str(FRONTEND_FOLDER), 'login.html')
        return send_from_directory(str(FRONTEND_FOLDER), 'index.html')

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(str(FRONTEND_FOLDER), filename)

    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "ok"})

    # ------------------ AUTH ------------------

    @app.route('/api/signup', methods=['POST'])
    def signup():
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 400

        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Signup successful'})

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # ✅ SESSION STORE
        session['user_id'] = user.id
        session['user_name'] = user.name

        return jsonify({
            'message': 'Login successful',
            'name': user.name
        })

    @app.route('/api/logout')
    def logout():
        session.clear()
        return jsonify({'message': 'Logged out'})

    # ------------------ RESUME ANALYSIS ------------------

    @app.route('/api/resume/analyze', methods=['POST'])
    def analyze_resume():

        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return jsonify({'error': 'Unsupported file type'}), 400

        save_path = UPLOAD_FOLDER / file.filename
        file.save(str(save_path))

        try:
            resume_text = extract_text(str(save_path))
        except Exception as e:
            return jsonify({'error': f'Text extraction failed: {str(e)}'}), 500

        if not resume_text or len(resume_text.split()) < 20:
            return jsonify({'error': 'Could not extract meaningful text'}), 400

        try:
            analysis = analyze_skills(resume_text)

            return jsonify({
                "resume_score": analysis.get("resume_score", 0),
                "domain": analysis.get("domain", "Unknown"),
                "detected_skills": analysis.get("detected_skills", []),
                "missing_skills": analysis.get("missing_skills", []),
                "suggestions": analysis.get("suggestions", []),
                "recommended_jobs": analysis.get("recommended_jobs", []),
                "strengths": analysis.get("strengths", []),
                "weaknesses": analysis.get("weaknesses", []),
                "summary": analysis.get("summary", "")
            })

        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

    return app


# ------------------ RUN ------------------

if __name__ == '__main__':
    app = create_app()
    import os

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)