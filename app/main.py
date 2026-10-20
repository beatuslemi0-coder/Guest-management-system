# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db, engine
from app.db.base import Base
from app.api.v1.auth import router as auth_router
from app.api.v1.rooms import router as rooms_router
from app.api.v1.customers import router as customers_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.reports import router as reports_router

# Hii itatengeneza meza kwenye Database moja kwa moja kwa kuanzia 
# (Baadae tutaanza kutumia Alembic kwa ajili ya migrations kamili)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Unaweza kuweka ["*"] kwa ajili ya kufanyia majaribio (development)
    allow_credentials=True,
    allow_methods=["*"],  # Ruhusu GET, POST, PUT, DELETE, n.k.
    allow_headers=["*"],  # Ruhusu headers zote ikiwemo Authorization Bearer token
)

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(rooms_router, prefix=settings.API_V1_STR)
app.include_router(customers_router, prefix=settings.API_V1_STR)
app.include_router(bookings_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Karibu kwenye Guest House Management System API"}

# Endpoint ya kupima kama Database imeunganishwa vizuri
@app.get("/health/db", tags=["Health Check"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Jaribu kuendesha query rahisi ya SQL
        db.execute(text("SELECT 1"))
        return {
            "status": "success", 
            "database": "PostgreSQL",
            "message": "Umeunganishwa vizuri sana na Database ya PostgreSQL!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Imeshindikana kuunganisha na Database: {str(e)}"
        )