from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy import Column

from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="category")


class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)  # подстрока в описании
    category_id = Column(ForeignKey("categories.id"), nullable=False)

    category = relationship("Category")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    occurred_on = Column(Date, nullable=False, default=date.today)
    description = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)  # отрицательное = расход
    category_id = Column(ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="transactions")
