# FinSight

Дашборд личных финансов с аналитикой — пет-проект для резюме.

**Стек:** React + TypeScript + Vite + Recharts (фронт), FastAPI + SQLAlchemy + pandas (бэк), PostgreSQL.

## Что демонстрирует

- Обработка данных на Python: импорт и нормализация CSV через pandas, автокатегоризация.
- Нетривиальный SQL: агрегаты, `GROUP BY`, оконные функции (накопительный остаток), `date_trunc`.
- React + TypeScript: интерактивные графики и фильтры.

## Структура

```
backend/   FastAPI + pandas + SQL-аналитика
frontend/  React + TS + Recharts
```

## Запуск

```bash
docker compose up -d            # PostgreSQL
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload   # http://localhost:8000/docs
```

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

## API (кратко)

| Метод | Путь | Описание |
| --- | --- | --- |
| POST | `/transactions` | Добавить транзакцию |
| POST | `/transactions/import` | Импорт CSV |
| GET | `/analytics/by-category` | Расходы по категориям |
| GET | `/analytics/monthly` | Динамика по месяцам (оконные функции) |

## Дальнейшее развитие

- [ ] Бюджеты с уведомлениями
- [ ] Прогноз на следующий месяц
- [ ] Экспорт отчётов
