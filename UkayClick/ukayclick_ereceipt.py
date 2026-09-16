def receipt_text(sale):
    return f"""
UKAYCLICK — E-RECEIPT
------------------------------
Transaction: {sale['transaction_id']}
Date:        {sale['timestamp']}
Customer:    {sale['customer']}

Product:     {sale['product']}
Category:    {sale['category']}
Quantity:    {sale['quantity']}
Unit Price:  ₱{sale['unit_price']:,.2f}
TOTAL:       ₱{sale['total']:,.2f}

Payment:     {sale['payment']}
------------------------------
Thank you for shopping at UkayClick!
""".strip()
