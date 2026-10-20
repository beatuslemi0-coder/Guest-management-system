# reset_db.py
from app.db.session import engine
from app.db.base import Base

print("Inafuta meza zote za zamani na kutengeneza mpya...")

# Hii itafuta meza zote na kuziunda upya kulingana na Models zako za sasa
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Imekamilika! Meza zote zimetengenezwa upya zikiwa na safu zote sahihi.")