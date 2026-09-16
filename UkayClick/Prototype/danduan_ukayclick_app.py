import streamlit as st
from ukayclick_auth import login, register
from ukayclick_storage import load_inventory, load_transactions, load_expenses
from ukayclick_ui import apply_style, money
from ukayclick_sales import process_sale
from ukayclick_inventory import add_item, update_item, delete_item
from ukayclick_analytics import sales_summary, inventory_summary, demand_forecast
from ukayclick_ereceipt import receipt_text

st.set_page_config(page_title="UkayClick", page_icon="🛍️", layout="wide")
apply_style()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

def login_screen():
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("## 🛍️ UkayClick")
    st.caption("Thrift Store Manual Transaction & Inventory System")
    tab1, tab2 = st.tabs(["🔐 Log In", "➕ Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In", use_container_width=True):
            user = login(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        username = st.text_input("Create Username", key="reg_username")
        password = st.text_input("Create Password", type="password", key="reg_password")
        confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        if st.button("Create Account", use_container_width=True):
            ok, message = register(username, password, confirm)
            (st.success if ok else st.error)(message)

    st.markdown("</div>", unsafe_allow_html=True)

def dashboard():
    transactions = load_transactions()
    inventory = load_inventory()
    expenses = load_expenses()
    summary = sales_summary(transactions, expenses)
    inv = inventory_summary(inventory)

    st.title("Dashboard")
    st.caption(f"Welcome back, {st.session_state.user['username']}.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Today's Sales", money(summary["today_sales"]))
    c2.metric("Total Sales", money(summary["total_sales"]))
    c3.metric("Expenses", money(summary["total_expenses"]))
    c4.metric("Items in Stock", inv["total_quantity"])

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("📦 Inventory Overview")
        st.write(f"**Unique products:** {inv['unique_items']}")
        st.write(f"**Low-stock items:** {inv['low_stock']}")
        st.write(f"**Inventory value:** {money(inv['inventory_value'])}")
    with right:
        st.subheader("💰 Financial Overview")
        st.write(f"**Net cash flow:** {money(summary['net_cash_flow'])}")
        st.write(f"**Transactions:** {summary['transaction_count']}")
        st.write(f"**Average sale:** {money(summary['average_sale'])}")

    st.info("Use the sidebar to record a sale, manage inventory, record expenses, or review predictive results.")

def sales_page():
    st.title("🧾 Process Sale")
    inventory = load_inventory()
    available = [x for x in inventory if x["quantity"] > 0]

    if not available:
        st.warning("No items are currently available for sale.")
        return

    choices = {f"{x['item_id']} — {x['name']} ({money(x['price'])})": x for x in available}
    selected = st.selectbox("Product", list(choices.keys()))
    item = choices[selected]
    quantity = st.number_input("Quantity", min_value=1, max_value=item["quantity"], value=1)
    customer = st.text_input("Customer name (optional)")
    payment = st.selectbox("Payment Method", ["Cash", "GCash", "Other"])

    total = item["price"] * quantity
    st.metric("Total", money(total))

    if st.button("✓ Complete Sale", use_container_width=True):
        ok, result = process_sale(item["item_id"], quantity, customer, payment)
        if ok:
            st.session_state.last_receipt = result
            st.success("Sale recorded and inventory updated.")
            st.rerun()
        else:
            st.error(result)

    if st.session_state.last_receipt:
        st.divider()
        st.subheader("🧾 E-Receipt")
        st.code(receipt_text(st.session_state.last_receipt), language="text")
        if st.button("Clear Receipt"):
            st.session_state.last_receipt = None
            st.rerun()

def inventory_page():
    st.title("📦 Inventory Management")
    inventory = load_inventory()

    with st.expander("➕ Add New Product", expanded=False):
        with st.form("add_item"):
            name = st.text_input("Product name")
            category = st.selectbox("Category", ["Shirt", "Pants", "Dress", "Jacket", "Shoes", "Accessories", "Other"])
            price = st.number_input("Selling price", min_value=0.01, step=10.0)
            quantity = st.number_input("Quantity", min_value=1, step=1)
            cost = st.number_input("Acquisition cost per item", min_value=0.0, step=10.0)
            submitted = st.form_submit_button("Add Product")
            if submitted:
                ok, msg = add_item(name, category, price, quantity, cost)
                (st.success if ok else st.error)(msg)
                if ok: st.rerun()

    if inventory:
        st.dataframe(inventory, use_container_width=True, hide_index=True)
        st.subheader("Update / Remove Product")
        ids = [x["item_id"] for x in inventory]
        item_id = st.selectbox("Select Item ID", ids)
        item = next(x for x in inventory if x["item_id"] == item_id)
        col1, col2, col3 = st.columns(3)
        with col1:
            new_price = st.number_input("New price", min_value=0.01, value=float(item["price"]), key="newprice")
        with col2:
            new_qty = st.number_input("New quantity", min_value=0, value=int(item["quantity"]), key="newqty")
        with col3:
            st.write("")
            st.write("")
            if st.button("Save Changes"):
                ok, msg = update_item(item_id, new_price, new_qty)
                (st.success if ok else st.error)(msg)
                if ok: st.rerun()
        if st.button("🗑️ Delete Product"):
            ok, msg = delete_item(item_id)
            (st.success if ok else st.error)(msg)
            if ok: st.rerun()
    else:
        st.info("No inventory records yet.")

def ledger_page():
    st.title("📒 Ledger & Transactions")
    transactions = load_transactions()
    expenses = load_expenses()
    tab1, tab2 = st.tabs(["Sales", "Expenses"])
    with tab1:
        if transactions:
            st.dataframe(list(reversed(transactions)), use_container_width=True, hide_index=True)
        else:
            st.info("No sales recorded.")
    with tab2:
        if expenses:
            st.dataframe(list(reversed(expenses)), use_container_width=True, hide_index=True)
        else:
            st.info("No expenses recorded.")

def expenses_page():
    from ukayclick_expenses import record_expense
    st.title("💸 Record Expense")
    category = st.selectbox("Expense category", ["Supplies", "Transportation", "Rent", "Utilities", "Packaging", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.01, step=10.0)
    if st.button("Record Expense", use_container_width=True):
        ok, msg = record_expense(category, description, amount)
        (st.success if ok else st.error)(msg)
        if ok: st.rerun()

def analysis_page():
    st.title("📊 Reports & Product Prediction")
    transactions = load_transactions()
    expenses = load_expenses()
    inventory = load_inventory()
    summary = sales_summary(transactions, expenses)
    forecast = demand_forecast(transactions, inventory)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", money(summary["total_sales"]))
    c2.metric("Total Expenses", money(summary["total_expenses"]))
    c3.metric("Net Cash Flow", money(summary["net_cash_flow"]))

    st.subheader("📈 Product Demand Analysis")
    st.caption("Prototype forecast based on historical units sold. It is an estimate, not a machine-learning model.")
    if forecast:
        st.dataframe(forecast, use_container_width=True, hide_index=True)
    else:
        st.info("Record some sales first so UkayClick can estimate product demand.")

if not st.session_state.logged_in:
    login_screen()
else:
    with st.sidebar:
        st.markdown("## 🛍️ UkayClick")
        st.caption(f"User: {st.session_state.user['username']}")
        page = st.radio("Navigation", [
            "🏠 Dashboard", "🧾 Process Sale", "📦 Inventory",
            "📒 Ledger", "💸 Expenses", "📊 Reports & Prediction"
        ])
        st.divider()
        if st.button("↪ Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    page_name = page.split(" ", 1)[1]
    if page_name == "Dashboard": dashboard()
    elif page_name == "Process Sale": sales_page()
    elif page_name == "Inventory": inventory_page()
    elif page_name == "Ledger": ledger_page()
    elif page_name == "Expenses": expenses_page()
    elif page_name == "Reports & Prediction": analysis_page()
