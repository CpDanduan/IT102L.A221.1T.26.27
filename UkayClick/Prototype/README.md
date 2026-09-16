# UkayClick Prototype

A Streamlit prototype for the **Thrift Store (Ukay-Ukay) Manual Transaction System** proposal.

## Main prototype features

- User registration and login
- Dashboard
- Sales / transaction processing
- Automatic inventory deduction after a sale
- Inventory add, update, and delete
- Expense recording
- Digital ledger
- E-receipt generation
- Sales and expense summaries
- Basic product demand prediction using historical sales
- JSON-based local storage

## Project structure

- `app.py` — Streamlit interface
- `ukayclick_auth.py` — authentication
- `ukayclick_storage.py` — JSON data storage
- `ukayclick_inventory.py` — inventory operations
- `ukayclick_sales.py` — sales transactions
- `ukayclick_expenses.py` — expense records
- `ukayclick_analytics.py` — reports and prototype demand analysis
- `ukayclick_ereceipt.py` — e-receipts
- `ukayclick_ui.py` — styling/helpers
- `data/` — local prototype data

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

This is a classroom prototype, not a production accounting or security system.
