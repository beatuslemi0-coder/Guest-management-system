from datetime import datetime
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_current_user
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.room import Room
from app.models.user import User


@pytest.fixture
def tenant_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    user_one = User(email="one@example.com", full_name="Business One", hashed_password="test")
    user_two = User(email="two@example.com", full_name="Business Two", hashed_password="test")
    session.add_all([user_one, user_two])
    session.flush()

    room_one = Room(
        user_id=user_one.id,
        room_number="101",
        room_type="Single",
        price_per_night=50,
        is_available=False,
    )
    room_two = Room(
        user_id=user_two.id,
        room_number="101",
        room_type="Single",
        price_per_night=80,
        is_available=False,
    )
    guest_one = Customer(
        user_id=user_one.id,
        full_name="Guest One",
        phone_number="555-0101",
        id_number="ID-101",
    )
    guest_two = Customer(
        user_id=user_two.id,
        full_name="Guest Two",
        phone_number="555-0101",
        id_number="ID-101",
    )
    session.add_all([room_one, room_two, guest_one, guest_two])
    session.flush()
    guest_without_booking = Customer(
        user_id=user_one.id,
        full_name="Guest Without Booking",
        phone_number="555-0102",
        id_number="ID-102",
    )
    session.add(guest_without_booking)

    booking_one = Booking(
        room_id=room_one.id,
        customer_id=guest_one.id,
        check_in_date=datetime(2026, 10, 20, 12),
        check_out_date=datetime(2026, 10, 22, 12),
        total_price=100,
        status="Confirmed",
    )
    booking_two = Booking(
        room_id=room_two.id,
        customer_id=guest_two.id,
        check_in_date=datetime(2026, 10, 20, 12),
        check_out_date=datetime(2026, 10, 22, 12),
        total_price=160,
        status="Confirmed",
    )
    session.add_all([booking_one, booking_two])
    cancelled_booking = Booking(
        room_id=room_one.id,
        customer_id=guest_one.id,
        check_in_date=datetime(2026, 10, 23, 12),
        check_out_date=datetime(2026, 10, 24, 12),
        total_price=900,
        status="Cancelled",
    )
    session.add(cancelled_booking)
    session.commit()

    ids = {
        "user_one": user_one.id,
        "user_two": user_two.id,
        "room_one": room_one.id,
        "room_two": room_two.id,
        "guest_one": guest_one.id,
        "guest_two": guest_two.id,
        "booking_one": booking_one.id,
        "booking_two": booking_two.id,
        "cancelled_booking": cancelled_booking.id,
        "guest_without_booking": guest_without_booking.id,
    }
    session.close()
    identity = {
        "user_id": ids["user_one"],
        "is_superuser": False,
        "email": "one@example.com",
        "full_name": "Business One",
    }

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    def override_current_user():
        db = TestingSession()
        try:
            user = db.get(User, identity["user_id"])
            return SimpleNamespace(
                id=user.id,
                is_superuser=identity["is_superuser"],
                email=user.email,
                full_name=user.full_name,
                guesthouse_name=user.guesthouse_name,
                is_active=user.is_active,
            )
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_current_user
    with TestClient(app) as client:
        yield client, identity, ids, TestingSession
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_room_and_guest_endpoints_are_scoped_to_current_user(tenant_client):
    client, identity, ids, _ = tenant_client

    assert [room["id"] for room in client.get("/api/v1/rooms/").json()] == [ids["room_one"]]
    assert {guest["id"] for guest in client.get("/api/v1/customers/").json()} == {
        ids["guest_one"],
        ids["guest_without_booking"],
    }
    assert client.get(f"/api/v1/rooms/{ids['room_two']}").status_code == 404
    assert client.get(f"/api/v1/customers/{ids['guest_two']}").status_code == 404

    assert client.put(
        f"/api/v1/rooms/{ids['room_two']}",
        json={"description": "Changed by another account"},
    ).status_code == 404
    assert client.delete(f"/api/v1/rooms/{ids['room_two']}").status_code == 404
    assert client.put(
        f"/api/v1/customers/{ids['guest_two']}",
        json={"full_name": "Changed by another account"},
    ).status_code == 404
    assert client.delete(f"/api/v1/customers/{ids['guest_two']}").status_code == 404

    identity["user_id"] = ids["user_two"]
    assert [room["id"] for room in client.get("/api/v1/rooms/").json()] == [ids["room_two"]]
    assert [guest["id"] for guest in client.get("/api/v1/customers/").json()] == [ids["guest_two"]]


def test_accounts_can_reuse_room_numbers_and_guest_identifiers(tenant_client):
    client, identity, ids, session_factory = tenant_client
    session = session_factory()
    try:
        session.add(
            Room(
                user_id=ids["user_one"],
                room_number="102",
                room_type="Double",
                price_per_night=100,
            )
        )
        session.add(
            Customer(
                user_id=ids["user_one"],
                full_name="Guest One Other",
                phone_number="555-0202",
                id_number="ID-202",
            )
        )
        session.commit()
    finally:
        session.close()

    identity["user_id"] = ids["user_two"]

    room = client.post(
        "/api/v1/rooms/",
        json={"room_number": "102", "room_type": "Double", "price_per_night": 100},
    )
    assert room.status_code == 201, room.text

    guest = client.post(
        "/api/v1/customers/",
        json={"full_name": "Another Guest", "phone_number": "555-0202", "id_number": "ID-202"},
    )
    assert guest.status_code == 201, guest.text


def test_room_updates_enforce_number_uniqueness_only_within_the_account(tenant_client):
    client, identity, ids, _ = tenant_client
    created_room = client.post(
        "/api/v1/rooms/",
        json={"room_number": "103", "room_type": "Single", "price_per_night": 50},
    )
    assert created_room.status_code == 201, created_room.text

    duplicate_update = client.put(
        f"/api/v1/rooms/{ids['room_one']}",
        json={"room_number": "103"},
    )
    assert duplicate_update.status_code == 400

    identity["user_id"] = ids["user_two"]
    cross_account_update = client.put(
        f"/api/v1/rooms/{ids['room_two']}",
        json={"room_number": "103"},
    )
    assert cross_account_update.status_code == 200, cross_account_update.text


def test_bookings_and_reports_only_include_the_current_accounts_data(tenant_client):
    client, identity, ids, _ = tenant_client

    bookings = client.get("/api/v1/bookings/").json()
    assert {booking["id"] for booking in bookings} == {ids["booking_one"], ids["cancelled_booking"]}
    report = client.get(
        "/api/v1/reports/",
        params={"period": "monthly", "reference_date": "2026-10-20"},
    ).json()
    assert report["summary"]["booking_count"] == 2
    assert report["summary"]["booking_value"] == 100
    assert {booking["id"] for booking in report["bookings"]} == {ids["booking_one"], ids["cancelled_booking"]}

    pdf = client.get(
        "/api/v1/reports/pdf",
        params={"period": "monthly", "reference_date": "2026-10-20"},
    )
    assert pdf.status_code == 200
    assert b"Guest One" in pdf.content
    assert b"Guest Two" not in pdf.content

    identity["user_id"] = ids["user_two"]
    assert [booking["id"] for booking in client.get("/api/v1/bookings/").json()] == [ids["booking_two"]]
    report = client.get(
        "/api/v1/reports/",
        params={"period": "monthly", "reference_date": "2026-10-20"},
    ).json()
    assert report["summary"]["booking_value"] == 160


def test_guest_house_name_is_saved_per_account_and_used_in_reports(tenant_client):
    client, identity, ids, session_factory = tenant_client

    response = client.put(
        "/api/v1/auth/me/guesthouse-name",
        json={"guesthouse_name": "  Sunset   Guest House  "},
    )
    assert response.status_code == 200, response.text
    assert response.json()["guesthouse_name"] == "Sunset Guest House"
    assert client.get("/api/v1/auth/me").json()["guesthouse_name"] == "Sunset Guest House"

    pdf = client.get(
        "/api/v1/reports/pdf",
        params={"period": "monthly", "reference_date": "2026-10-20"},
    )
    assert pdf.status_code == 200
    assert b"Sunset Guest House" in pdf.content
    assert b"NGINAP" not in pdf.content
    assert "sunset-guest-house-ripoti" in pdf.headers["content-disposition"]

    assert client.put(
        "/api/v1/auth/me/guesthouse-name",
        json={"guesthouse_name": "   "},
    ).status_code == 422
    assert client.put(
        "/api/v1/auth/me/guesthouse-name",
        json={"guesthouse_name": "X" * 61},
    ).status_code == 422

    identity["user_id"] = ids["user_two"]
    assert client.get("/api/v1/auth/me").json()["guesthouse_name"] is None
    session = session_factory()
    try:
        assert session.get(User, ids["user_one"]).guesthouse_name == "Sunset Guest House"
        assert session.get(User, ids["user_two"]).guesthouse_name is None
    finally:
        session.close()


def test_booking_creation_and_checkout_cannot_cross_account_boundaries(tenant_client):
    client, _, ids, session_factory = tenant_client

    response = client.post(
        "/api/v1/bookings/",
        json={
            "room_id": ids["room_one"],
            "customer_id": ids["guest_two"],
            "check_in_date": "2026-10-25T12:00:00",
            "check_out_date": "2026-10-26T12:00:00",
        },
    )
    assert response.status_code == 400
    assert client.post(f"/api/v1/bookings/{ids['booking_two']}/checkout").status_code == 400

    session = session_factory()
    try:
        booking = session.get(Booking, ids["booking_two"])
        room = session.get(Room, ids["room_two"])
        assert booking.status == "Confirmed"
        assert room.is_available is False
    finally:
        session.close()


def test_admin_guest_report_includes_all_guests_and_validates_admin_access(tenant_client):
    client, identity, ids, _ = tenant_client

    assert client.get("/api/v1/auth/me").json()["is_superuser"] is False
    assert client.get("/api/v1/admin/guests/").status_code == 403

    identity["is_superuser"] = True
    response = client.get("/api/v1/admin/guests/", params={"skip": 0, "limit": 3})
    assert response.status_code == 200, response.text
    page = response.json()
    assert page["total"] == 3
    assert page["summary"] == {
        "guest_count": 3,
        "booking_count": 3,
        "revenue": 260,
    }
    assert len(page["guests"]) == 3
    first_guest = next(guest for guest in page["guests"] if guest["id"] == ids["guest_one"])
    assert first_guest["business_name"] == "Business One"
    assert first_guest["booking_count"] == 2
    assert first_guest["revenue"] == 100

    first_page = client.get("/api/v1/admin/guests/", params={"skip": 0, "limit": 2}).json()
    next_page = client.get("/api/v1/admin/guests/", params={"skip": 2, "limit": 2}).json()
    assert len(first_page["guests"]) == 2
    assert len(next_page["guests"]) == 1
    no_booking_guest = next(
        guest
        for guest in first_page["guests"] + next_page["guests"]
        if guest["id"] == ids["guest_without_booking"]
    )
    assert no_booking_guest["booking_count"] == 0
    assert no_booking_guest["revenue"] == 0

    identity["is_superuser"] = False
    identity["user_id"] = ids["user_two"]
    assert client.get("/api/v1/admin/guests/").status_code == 403


def test_admin_guest_houses_include_room_and_daily_activity_summaries(tenant_client):
    client, identity, ids, session_factory = tenant_client

    assert client.get("/api/v1/admin/guest-houses/").status_code == 403

    session = session_factory()
    try:
        today = datetime.now()
        session.add(
            Booking(
                room_id=ids["room_one"],
                customer_id=ids["guest_one"],
                check_in_date=today.replace(hour=10, minute=0, second=0, microsecond=0),
                check_out_date=today.replace(hour=11, minute=0, second=0, microsecond=0),
                total_price=50,
                status="Confirmed",
            )
        )
        session.add(
            Room(
                user_id=ids["user_one"],
                room_number="102",
                room_type="Double",
                price_per_night=75,
                is_available=True,
            )
        )
        session.commit()
    finally:
        session.close()

    identity["is_superuser"] = True
    response = client.get("/api/v1/admin/guest-houses/", params={"skip": 0, "limit": 1})
    assert response.status_code == 200, response.text
    page = response.json()
    assert page["total"] == 2
    assert page["summary"] == {
        "guesthouse_count": 2,
        "room_count": 3,
        "check_ins_today": 1,
        "check_outs_today": 1,
    }
    assert len(page["guest_houses"]) == 1

    all_houses = client.get("/api/v1/admin/guest-houses/", params={"limit": 10}).json()["guest_houses"]
    first_house = next(house for house in all_houses if house["id"] == ids["user_one"])
    assert first_house["guesthouse_name"] == "Business One"
    assert first_house["room_count"] == 2
    assert first_house["occupied_room_count"] == 1
    assert first_house["available_room_count"] == 1
    assert first_house["check_ins_today"] == 1
    assert first_house["check_outs_today"] == 1

    identity["is_superuser"] = False
    assert client.get("/api/v1/admin/guest-houses/").status_code == 403
