from sqlalchemy.orm import Session

from app.models import Category, Rule


def resolve_category(db: Session, description: str) -> int | None:
    """Простая категоризация по ключевым словам из таблицы rules."""
    text = description.lower()
    for rule in db.query(Rule).all():
        if rule.keyword.lower() in text:
            return rule.category_id
    return None


def get_or_create_category(db: Session, name: str) -> Category:
    cat = db.query(Category).filter(Category.name == name).first()
    if not cat:
        cat = Category(name=name)
        db.add(cat)
        db.flush()
    return cat
