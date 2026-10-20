# app/api/v1/customers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.repositories.customer_repository import CustomerRepository
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/customers", tags=["Customers Management"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_customer = CustomerRepository.get_by_phone(db, phone_number=customer_in.phone_number)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mteja mwenye namba hii ya simu tayari yupo kwenye mfumo!"
        )
    return CustomerRepository.create(db=db, customer_in=customer_in)

@router.get("/", response_model=List[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CustomerRepository.get_all(db=db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = CustomerRepository.get_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Taarifa za mteja huyu hazikupatikana!"
        )
    return customer

# Endpoint ya Kurekebisha Taarifa za Mteja (Update)
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_in: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = CustomerRepository.get_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mteja aliyekusudiwa hakupatikana kwenye mfumo!"
        )
    return CustomerRepository.update(db=db, db_customer=customer, customer_in=customer_in)

# Endpoint ya Kufuta Mteja (Delete)
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = CustomerRepository.get_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mteja aliyekusudiwa hakupatikana!"
        )
    CustomerRepository.delete(db=db, db_customer=customer)
    return None