import pytest
from app import app, db, User

# This sets up a temporary, blank test environment so we don't mess up your real database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Uses temporary RAM database
    app.config['WTF_CSRF_ENABLED'] = False 

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# TEST 1: Integration Test - Does the home page load?
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"MediBook" in response.data

# TEST 2: Integration Test - Does the login page load?
def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

# TEST 3: Security Test - Does the dashboard block logged-out users?
def test_dashboard_requires_login(client):
    response = client.get('/dashboard')
    # 302 means "Redirect", proving Flask-Login kicked them back to the login page
    assert response.status_code == 302 
    assert b"/login" in response.data