import os
import csv
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'securecare.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ============================
#     MONGO DB ATLAS FIX
# ============================
username = quote_plus("nvc-victor")
password = quote_plus("victorgerald")

uri = f"mongodb+srv://{username}:{password}@cluster0.wve7its.mongodb.net/"

# TLS FIX FOR MacOS + Python 3.13 + OpenSSL 3.x
mongo = MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True,
    tlsAllowInvalidHostnames=True
)

patient_db = mongo["securecare"]
patient_collection = patient_db["patients"]

# ============================
#       SQL DATABASE
# ============================
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# ============================
#       USER MODEL
# ============================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='patient')


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ============================
#       ROUTES
# ============================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


# ============================
#       USER AUTH
# ============================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not username or not password or not confirm:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed, role='patient')
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            session['user'] = user.username
            session['role'] = user.role
            flash('Logged in successfully!', 'success')

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('patient_dashboard'))

        flash('Invalid username or password.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/create-admin')
def create_admin():
    if User.query.filter_by(username='admin').first():
        return "Admin already exists."

    admin = User(username='admin', password_hash=generate_password_hash('admin123'), role='admin')
    db.session.add(admin)
    db.session.commit()
    return "Admin created successfully!"


# ============================
#   PATIENT REGISTRATION
# ============================
@app.route('/patient/register', methods=['GET', 'POST'])
@login_required
def register_patient():
    if session.get('role') != 'patient':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')

        if not patient_id:
            flash('Patient ID is required.', 'danger')
            return redirect(request.url)

        if patient_collection.find_one({"patient_id": patient_id}):
            flash('This Patient ID is already registered.', 'danger')
            return redirect(request.url)

        data = {
            "patient_id": patient_id,
            "user_id": current_user.id,
            "gender": request.form.get('gender'),
            "age": int(request.form.get('age') or 0),
            "hypertension": int(request.form.get('hypertension') or 0),
            "ever_married": request.form.get('ever_married'),
            "work_type": request.form.get('work_type'),
            "residence_type": request.form.get('residence_type'),
            "avg_glucose_level": float(request.form.get('avg_glucose_level') or 0),
            "bmi": float(request.form.get('bmi') or 0),
            "smoking_status": request.form.get('smoking_status'),
            "stroke": int(request.form.get('stroke') or 0)
        }

        patient_collection.insert_one(data)
        flash(f'Patient registered successfully with ID #{patient_id}!', 'success')
        return redirect(url_for('patient_dashboard'))

    return render_template('patient.html')


@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    if session.get('role') != 'patient':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    patient = patient_collection.find_one({"user_id": current_user.id})
    return render_template('patient_dashboard.html', patient=patient)


# ============================
#     ADMIN DASHBOARD
# ============================
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page

    total_patients = patient_collection.count_documents({})
    patients = list(patient_collection.find().skip(skip).limit(per_page))

    return render_template(
        'admin_dashboard.html',
        patients=patients,
        page=page,
        total=total_patients,
        per_page=per_page
    )


# ============================
#   EDIT PATIENT (ADMIN)
# ============================
@app.route('/patient/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    patient = patient_collection.find_one({"patient_id": str(patient_id)})
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        update = {
            "gender": request.form.get('gender'),
            "age": int(request.form.get('age') or 0),
            "hypertension": int(request.form.get('hypertension') or 0),
            "ever_married": request.form.get('ever_married'),
            "work_type": request.form.get('work_type'),
            "residence_type": request.form.get('residence_type'),
            "avg_glucose_level": float(request.form.get('avg_glucose_level') or 0),
            "bmi": float(request.form.get('bmi') or 0),
            "smoking_status": request.form.get('smoking_status'),
            "stroke": int(request.form.get('stroke') or 0)
        }

        patient_collection.update_one({"patient_id": str(patient_id)}, {"$set": update})
        flash('Patient updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_patient.html', patient=patient)


# ============================
#     DELETE PATIENT
# ============================
@app.route('/patient/<int:patient_id>/delete', methods=['POST'])
@login_required
def delete_patient(patient_id):
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    patient_collection.delete_one({"patient_id": str(patient_id)})
    flash('Patient deleted successfully.', 'info')
    return redirect(url_for('admin_dashboard'))


# ============================
#    CSV LOADER
# ============================
def run_loader():
    try:
        with open('dummy_patients.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row['ID']:
                    print("⚠️ Skipping row with missing ID:", row)
                    continue

                if patient_collection.find_one({"patient_id": row['ID']}):
                    print(f"⚠️ Patient ID {row['ID']} already exists. Skipping.")
                    continue

                patient = {
                    "user_id": None,
                    "patient_id": row['ID'],
                    "gender": row['gender'],
                    "age": int(row['age']),
                    "hypertension": int(row['hypertension']),
                    "ever_married": row['ever_married'],
                    "work_type": row['work_type'],
                    "residence_type": row['Residence_type'],
                    "avg_glucose_level": float(row['avg_glucose_level']),
                    "bmi": float(row['bmi']) if row['bmi'] != 'N/A' else None,
                    "smoking_status": row['smoking_status'],
                    "stroke": int(row['stroke'])
                }

                patient_collection.insert_one(patient)

            print("✅ Dummy patients loaded successfully.")
    except FileNotFoundError:
        print("❌ dummy_patients.csv not found.")
    except Exception as e:
        print("❌ Error loading dummy patients:", e)


# ============================
#      START APP
# ============================
if __name__ == '__main__':
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

    with app.app_context():
        db.create_all()
        if patient_collection.count_documents({}) == 0:
            run_loader()

    print("✅ Flask app running on http://127.0.0.1:5000")
    app.run(debug=True)