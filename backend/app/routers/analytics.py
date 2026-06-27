from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CategoryAmount, MonthlyPoint

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/by-category", response_model=list[CategoryAmount])
def by_category(db: Session = Depends(get_db)):
    """Сумма расходов по категориям (amount < 0)."""
    sql = text(
        """
        SELECT COALESCE(c.name, 'Без категории') AS category,
               ABS(SUM(t.amount)) AS total
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.amount < 0
        GROUP BY c.name
        ORDER BY total DESC
        """
    )
    rows = db.execute(sql).all()
    return [CategoryAmount(category=r.category, total=Decimal(r.total)) for r in rows]


@router.get("/monthly", response_model=list[MonthlyPoint])
def monthly(db: Session = Depends(get_db)):
    """Доход/расход по месяцам + накопительный остаток (оконная функция)."""
    sql = text(
        """
        WITH monthly AS (
            SELECT date_trunc('month', occurred_on) AS month,
                   SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
                   SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS expense,
                   SUM(amount) AS net
            FROM transactions
            GROUP BY 1
        )
        SELECT to_char(month, 'YYYY-MM') AS month,
               income,
               expense,
               SUM(net) OVER (ORDER BY month) AS running_balance
        FROM monthly
        ORDER BY month
        """
    )
    rows = db.execute(sql).all()
    return [
        MonthlyPoint(
            month=r.month,
            income=Decimal(r.income),
            expense=Decimal(r.expense),
            running_balance=Decimal(r.running_balance),
        )
        for r in rows
    ]
