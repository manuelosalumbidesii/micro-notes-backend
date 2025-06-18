from app import app

def test_get_notes():
    client = app.test_client()
    response = client.get('/api/notes')
    assert response.status_code == 200
