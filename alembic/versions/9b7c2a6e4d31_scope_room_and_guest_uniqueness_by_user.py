"""Scope room and guest uniqueness to each account.

Revision ID: 9b7c2a6e4d31
Revises: e4e362c64cf5
Create Date: 2026-10-20
"""

from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa


revision: str = "9b7c2a6e4d31"
down_revision: Union[str, Sequence[str], None] = "e4e362c64cf5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if context.is_offline_mode():
        op.drop_index("ix_rooms_room_number", table_name="rooms")
        op.create_index("ix_rooms_room_number", "rooms", ["room_number"], unique=False)
        op.create_unique_constraint(
            "uq_rooms_user_room_number",
            "rooms",
            ["user_id", "room_number"],
        )
        op.drop_index("ix_customers_phone_number", table_name="customers")
        op.create_index("ix_customers_phone_number", "customers", ["phone_number"], unique=False)
        op.drop_constraint("customers_id_number_key", "customers", type_="unique")
        op.create_unique_constraint(
            "uq_customers_user_phone",
            "customers",
            ["user_id", "phone_number"],
        )
        op.create_unique_constraint(
            "uq_customers_user_id_number",
            "customers",
            ["user_id", "id_number"],
        )
        return

    inspector = sa.inspect(op.get_bind())
    room_indexes = {index["name"]: index for index in inspector.get_indexes("rooms")}
    room_constraints = {
        constraint["name"]
        for constraint in inspector.get_unique_constraints("rooms")
    }
    if room_indexes.get("ix_rooms_room_number", {}).get("unique"):
        op.drop_index("ix_rooms_room_number", table_name="rooms")
        del room_indexes["ix_rooms_room_number"]
    if "ix_rooms_room_number" not in room_indexes:
        op.create_index("ix_rooms_room_number", "rooms", ["room_number"], unique=False)
    if "uq_rooms_user_room_number" not in room_constraints:
        op.create_unique_constraint(
            "uq_rooms_user_room_number",
            "rooms",
            ["user_id", "room_number"],
        )

    customer_indexes = {index["name"]: index for index in inspector.get_indexes("customers")}
    customer_constraints = {
        constraint["name"]
        for constraint in inspector.get_unique_constraints("customers")
    }
    if customer_indexes.get("ix_customers_phone_number", {}).get("unique"):
        op.drop_index("ix_customers_phone_number", table_name="customers")
        del customer_indexes["ix_customers_phone_number"]
    if "ix_customers_phone_number" not in customer_indexes:
        op.create_index("ix_customers_phone_number", "customers", ["phone_number"], unique=False)
    if "customers_id_number_key" in customer_constraints:
        op.drop_constraint("customers_id_number_key", "customers", type_="unique")
    if "uq_customers_user_phone" not in customer_constraints:
        op.create_unique_constraint(
            "uq_customers_user_phone",
            "customers",
            ["user_id", "phone_number"],
        )
    if "uq_customers_user_id_number" not in customer_constraints:
        op.create_unique_constraint(
            "uq_customers_user_id_number",
            "customers",
            ["user_id", "id_number"],
        )


def downgrade() -> None:
    op.drop_constraint("uq_customers_user_id_number", "customers", type_="unique")
    op.drop_constraint("uq_customers_user_phone", "customers", type_="unique")
    op.create_unique_constraint(
        "customers_id_number_key",
        "customers",
        ["id_number"],
    )
    op.drop_index("ix_customers_phone_number", table_name="customers")
    op.create_index("ix_customers_phone_number", "customers", ["phone_number"], unique=True)

    op.drop_constraint("uq_rooms_user_room_number", "rooms", type_="unique")
    op.drop_index("ix_rooms_room_number", table_name="rooms")
    op.create_index("ix_rooms_room_number", "rooms", ["room_number"], unique=True)
