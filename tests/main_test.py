from src import db, app


def test_index():
    db.create_all()

    app.testing = True
    client = app.test_client()

    r = client.get('/', environ_base={'REMOTE_ADDR': '127.0.0.1'})
    assert r.status_code == 200
    assert '127.0' in r.data.decode('utf-8')
