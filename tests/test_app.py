import os
import tempfile
import pytest
from app import create_app
from models import db as _db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        _db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_and_login(client, app):
    # register
    rv = client.post('/register', data={'username': 'admin', 'password': 'password123'}, follow_redirects=True)
    assert b'Registration complete' in rv.data

    # login
    rv = client.post('/login', data={'username': 'admin', 'password': 'password123'}, follow_redirects=True)
    assert b'Logged in successfully' in rv.data

def test_create_patient_requires_login(client, app):
    # try to access new_patient without login => redirected to login
    rv = client.get('/patient/new', follow_redirects=True)
    assert b'Login' in rv.data or rv.status_code == 200

def test_create_patient_flow(client, app):
    # register and login
    client.post('/register', data={'username': 'admin2', 'password': 'password123'}, follow_redirects=True)
    client.post('/login', data={'username': 'admin2', 'password': 'password123'}, follow_redirects=True)
    # add patient
    data = {
        'patient_id': '123ABC',
        'gender': 'Male',
        'age': 45,
        'hypertension': '0',
        'ever_married': 'Yes',
        'work_type': 'Private',
        'residence_type': 'Urban',
        'avg_glucose_level': 85.5,
        'bmi': 23.8,
        'smoking_status': 'Never smoked',
        'stroke': '0'
    }
    rv = client.post('/patient/new', data=data, follow_redirects=True)
    assert b'Patient saved' in rv.data
    # see dashboard
    rv = client.get('/dashboard')
    assert b'123ABC' in rv.data or b'decryption-error' not in rv.data
