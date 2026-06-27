import io

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.categorize import get_or_create_category, resolve_category
from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionOut

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _serialize(t: Transaction) -> TransactionOut:
    return TransactionOut(
        id=t.id,
        occurred_on=t.occurred_on,
        description=t.description,
        amount=t.amount,
        category=t.category.name if t.category else None,
    )


@router.get("", response_model=list[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    rows = db.query(Transaction).order_by(Transaction.occurred_on.desc()).all()
    return [_serialize(t) for t in rows]


@router.post("", response_model=TransactionOut)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    category_id = None
    if data.category:
        category_id = get_or_create_category(db, data.category).id
    else:
        category_id = resolve_category(db, data.description)
    tx = Transaction(
        occurred_on=data.occurred_on,
        description=data.description,
        amount=data.amount,
        category_id=category_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return _serialize(tx)


@router.post("/import", response_model=dict)
def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Импорт CSV с колонками: date, description, amount."""
    raw = file.file.read()
    df = pd.read_csv(io.BytesIO(raw))
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["amount"] = pd.to_numeric(df["amount"])

    inserted = 0
    for _, row in df.iterrows():
        description = str(row["description"]).strip()
        tx = Transaction(
            occurred_on=row["date"],
            description=description,
            amount=row["amount"],
            category_id=resolve_category(db, description),
        )
        db.add(tx)
        inserted += 1
    db.commit()
    return {"inserted": inserted}
