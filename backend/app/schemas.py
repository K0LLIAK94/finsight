from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    occurred_on: date
    description: str
    amount: Decimal
    category: str | None = None


class TransactionOut(BaseModel):
    id: int
    occurred_on: date
    description: str
    amount: Decimal
    category: str | None = None
    model_config = ConfigDict(from_attributes=True)


class CategoryAmount(BaseModel):
    category: str
    total: Decimal


class MonthlyPoint(BaseModel):
    month: str
    income: Decimal
    expense: Decimal
    running_balance: Decimal
