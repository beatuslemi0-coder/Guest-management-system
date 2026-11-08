# app/repositories/customer_repository.py
from sqlalchemy.orm import Session
from typing import Optional
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerRepository:
    @staticmethod
    def get_by_id(db: Session, customer_id: int, user_id: int) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id, Customer.user_id == user_id).first()

    @staticmethod
    def get_by_phone(
        db: Session,
        phone_number: str,
        user_id: int,
        exclude_customer_id: Optional[int] = None,
    ) -> Optional[Customer]:
        query = db.query(Customer).filter(Customer.phone_number == phone_number, Customer.user_id == user_id)
        if exclude_customer_id is not None:
            query = query.filter(Customer.id != exclude_customer_id)
        return query.first()

    @staticmethod
    def get_by_id_number(
        db: Session,
        id_number: str,
        user_id: int,
        exclude_customer_id: Optional[int] = None,
    ) -> Optional[Customer]:
        query = db.query(Customer).filter(Customer.id_number == id_number, Customer.user_id == user_id)
        if exclude_customer_id is not None:
            query = query.filter(Customer.id != exclude_customer_id)
        return query.first()

    @staticmethod
    def get_all_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Customer).filter(Customer.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, customer_in: CustomerCreate, user_id: int) -> Customer:
        db_customer = Customer(
            full_name=customer_in.full_name,
            phone_number=customer_in.phone_number,
            id_number=customer_in.id_number,
            email=customer_in.email,
            origin=customer_in.origin,
            destination=customer_in.destination,
            occupation=customer_in.occupation,
            user_id=user_id,
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def update(db: Session, db_customer: Customer, customer_in: CustomerUpdate) -> Customer:
        update_data = customer_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def delete(db: Session, db_customer: Customer):
        db.delete(db_customer)
        db.commit()
        return db_customer