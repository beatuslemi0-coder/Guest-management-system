# make_admin.py
import sys
from app.db.session import SessionLocal
from app.models.user import User

def promote_to_admin(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Kosa: Hakuna mtumiaji mwenye email '{email}' kwenye mfumo!")
            return
        
        user.is_superuser = True
        user.is_active = True
        db.commit()
        print(f"Mafanikio! Mtumiaji '{email}' sasa amewekwa kuwa Super Admin.")
    except Exception as e:
        print(f"Hitilafu imetokea: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Tafadhali weka email ya mtumiaji.")
        print("Mfano wa matumizi: python make_admin.py admin@example.com")
    else:
        email_arg = sys.argv[1]
        promote_to_admin(email_arg)