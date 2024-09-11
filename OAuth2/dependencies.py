from OAuth2.db.db_connection import db_session

def get_db_session():
    with db_session:
        try:
            yield db_session
        finally:
            db_session.close()