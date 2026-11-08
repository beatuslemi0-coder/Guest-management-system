import sys
import os

# Hakikisha njia ya folda kuu inasomeka vizuri
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User  # Badilisha iendane na mahali ulipoweka Model ya User

def create_initial_admin():
    db = SessionLocal()
    try:
        # Weka taarifa za Admin unayemtaka hapa
        admin_email = os.getenv("FIRST_SUPERUSER", "admin@gmail.com")
        admin_password = os.getenv("FIRST_SUPERUSER_PASSWORD", "admin12345")
        
        # Angalia kama admin tayari yupo
        existing_user = db.query(User).filter(User.email == admin_email).first()
        if existing_user:
            print(f"❌ Akaunti ya Admin yenye email '{admin_email}' tayari ipo!")
            return

        # Unda admin mpya
        hashed_password = get_password_hash(admin_password)
        db_user = User(
            email=admin_email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True,
            # Ongeza nguzo nyingine zinazohitajika na User model yako hapa kama zipo (mfano: full_name, role, n.k)
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"✅ Akaunti ya Admin imetengenezwa kwa mafanikio!")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Kosa limetokea wakati wa kutengeneza admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()