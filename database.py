from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Integer, Boolean, String
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str]
    name: Mapped[str]
    desc: Mapped[str]
    price: Mapped[int]

    def __repr__(self):
        return f"Name of Product: {self.name}"


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    phone: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str]
    state: Mapped[str]
    localgovt: Mapped[str]
    city: Mapped[str] = mapped_column(String(70))
    address: Mapped[str]
    registered_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    confirmed: Mapped[bool] = mapped_column(default=False, nullable=False)
    confirmed_on: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_cart: Mapped[str] = relationship("Cart", back_populates="cart_user")
    user_order: Mapped[str] = relationship("Order", back_populates="order_user")

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"


class Cart(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    subtotal: Mapped[int]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    cart_user: Mapped[str] = relationship("User", back_populates="user_cart")
    product: Mapped[str] = relationship("Product", back_populates=None)

    def __repr__(self):
        return f"{self.cart_user.firstname}'s cart"


class Order(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    subtotal: Mapped[int]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[str]
    reference: Mapped[str]
    order_user: Mapped[str] = relationship("User", back_populates="user_order")
    product: Mapped[str] = relationship("Product", back_populates=None)

    def __repr__(self):
        return f"{self.cart_user.firstname}'s order"
