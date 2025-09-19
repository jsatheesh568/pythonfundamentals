# Day11.py - FoodieFlow (complete app, PDF unicode-safe)
import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import io
import base64
from fpdf import FPDF

# --------------- Page config & global CSS ---------------
st.set_page_config(page_title="🍜 FoodieFlow - Smart Restaurant",
                   page_icon="🍽️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* Header and banners */
.main-header {
  background: linear-gradient(135deg,#ff6b6b 0%,#ffa726 100%);
  padding:40px; border-radius:25px; color:white;
  text-align:center; margin:20px 0;
  box-shadow:0 8px 30px rgba(0,0,0,0.25);
}
.offer-banner {
  background: linear-gradient(45deg,#ff6b6b,#ffa726);
  color: #fff; padding: 12px 14px; border-radius: 12px; text-align: center;
  font-weight: 700; min-height: 56px; display:flex; align-items:center; justify-content:center;
  margin: 8px 0; box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
.small-header {
  background: linear-gradient(135deg,#4ecdc4 0%,#44a08d 100%);
  color: #fff; padding:10px 14px; border-radius:10px; margin: 18px 0 8px 0;
  font-weight:600;
}

/* Cards / menu */
.menu-grid { display:flex; flex-direction:column; gap:18px; }
.menu-card {
  width:100%; max-width:980px; display:flex; gap:14px; align-items:flex-start;
  background: #fff; color: #111; border-radius:12px; padding:12px;
  box-shadow: 0 6px 20px rgba(15,15,15,0.04); border: 1px solid rgba(0,0,0,0.06);
}
.thumb { flex:0 0 100px; height:100px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:40px; background: linear-gradient(180deg,#fafafa,#f2f2f2); color:#333; }
.meta { flex:1 1 auto; }
.menu-card h4 { margin:0 0 6px 0; font-size:18px; color: inherit; }
.menu-card p { margin:0 0 8px 0; color: rgba(0,0,0,0.65); font-size:13px; line-height:1.3; }
.badges { display:flex; gap:6px; margin-bottom:6px; flex-wrap:wrap; }
.badge { font-size:12px; padding:4px 8px; border-radius:12px; background: rgba(0,0,0,0.05); color:#333; }
.price { font-weight:700; font-size:16px; color: inherit; }
.qty-box { background: rgba(0,0,0,0.03); border-radius:8px; padding:6px 10px; min-width:86px; text-align:center; color: inherit; }

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .menu-card { background: rgba(255,255,255,0.02); color:#e8eef6; border:1px solid rgba(255,255,255,0.03); box-shadow:0 8px 24px rgba(0,0,0,0.6); }
  .menu-card p { color: rgba(232,238,246,0.7); }
  .thumb { background: rgba(255,255,255,0.02); color:#fff; }
  .badge { background: rgba(255,255,255,0.03); color:#eaeff6; }
  .offer-banner { box-shadow: 0 6px 18px rgba(0,0,0,0.6); }
  .small-header { background: linear-gradient(135deg,#3bb79d, #2f8b73); color:#fff; }
  .qty-box { background: rgba(255,255,255,0.02); color:#e8eef6; }
}
.menu-card, .thumb, .meta, .offer-banner { word-wrap: break-word; }
</style>
""", unsafe_allow_html=True)

# --------------- Data ---------------
MENU_DATA = {
    "🍕 Appetizers": [
        {"name": "Crispy Garlic Bread", "description": "Homemade bread with garlic butter and herbs", "price": 199, "rating": 4.5, "cooking_time": "10-15 mins", "dietary": ["veg"], "image": "🍞"},
        {"name": "Chicken Wings", "description": "Spicy buffalo wings with ranch dip", "price": 399, "rating": 4.7, "cooking_time": "15-20 mins", "dietary": ["non-veg","spicy"], "image": "🍗"},
        {"name": "Mozzarella Sticks", "description": "Golden fried cheese sticks with marinara", "price": 299, "rating": 4.3, "cooking_time": "8-12 mins", "dietary": ["veg","bestseller"], "image": "🧀"}
    ],
    "🍔 Burgers & Sandwiches": [
        {"name": "Classic Beef Burger", "description": "Juicy beef patty with lettuce, tomato, and special sauce", "price": 549, "rating": 4.8, "cooking_time": "15-20 mins", "dietary": ["non-veg","bestseller"], "image": "🍔"},
        {"name": "Veggie Delight Burger", "description": "Plant-based patty with fresh vegetables", "price": 449, "rating": 4.4, "cooking_time": "12-18 mins", "dietary": ["veg","vegan"], "image": "🥗"},
        {"name": "Spicy Chicken Sandwich", "description": "Grilled chicken with jalapeños and chipotle mayo", "price": 499, "rating": 4.6, "cooking_time": "15-20 mins", "dietary": ["non-veg","spicy"], "image": "🌶️"}
    ]
}

RESTAURANT_INFO = {
    "name": "FoodieFlow Kitchen",
    "tagline": "Where Flavor Meets Innovation",
    "rating": 4.7,
    "delivery_time": "25-35 mins",
    "minimum_order": 300,
    "delivery_fee": 49,
    "offers": [
        "🎉 20% OFF on orders above ₹800",
        "🍕 Buy 2 Get 1 FREE on Pizzas",
        "🥤 Free Drink with Burger Combo"
    ]
}

# --------------- Session state ---------------
def init_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    if 'order_history' not in st.session_state:
        st.session_state.order_history = []
    if 'customer_info' not in st.session_state:
        st.session_state.customer_info = {}
init_session_state()

def _safe_key(prefix, key):
    return f"{prefix}_{hashlib.md5(key.encode()).hexdigest()[:10]}"

def generate_order_id():
    ts = str(datetime.now().timestamp())
    return f"FF{hashlib.md5(ts.encode()).hexdigest()[:8].upper()}"

def find_item_by_key(item_key):
    for cat, items in MENU_DATA.items():
        for it in items:
            if f"{cat} - {it['name']}" == item_key:
                return cat, it
    return None, None

def calculate_bill(cart):
    subtotal = 0
    for k, q in cart.items():
        _, it = find_item_by_key(k)
        if it:
            subtotal += it['price'] * q
    discount = subtotal * 0.20 if subtotal >= 800 else 0
    tax = round((subtotal - discount) * 0.18, 2)
    delivery = 0 if subtotal >= 500 else RESTAURANT_INFO["delivery_fee"]
    total = round(subtotal - discount + tax + delivery, 2)
    return {"subtotal": round(subtotal, 2), "discount": round(discount, 2),
            "tax": tax, "delivery": round(delivery, 2), "total": total}

# --------------- PDF helpers (safe) ---------------
def _safe_text_for_pdf(s: str) -> str:
    """Convert text to Latin-1 safe text for fpdf by replacing/removing problematic characters."""
    if s is None:
        return ""
    replacements = {
        "₹": "Rs.",
        "—": "-",
        "–": "-",
        "”": "\"",
        "“": "\"",
        "’": "'",
        "…": "...",
        "•": "-",
        "\u200b": "",  # zero width
    }
    out = str(s)
    for k, v in replacements.items():
        out = out.replace(k, v)
    # Remove any remaining characters that can't be encoded in latin-1
    filtered_chars = []
    for ch in out:
        try:
            ch.encode("latin-1")
            filtered_chars.append(ch)
        except UnicodeEncodeError:
            # drop character
            pass
    return "".join(filtered_chars).strip()

def create_pdf_invoice(order, customer, bill):
    """
    Create a PDF invoice using fpdf while forcing Latin-1 safe text.
    This avoids UnicodeEncodeError by cleaning text and encoding with ignore as a final fallback.
    """
    pdf = FPDF()
    pdf.add_page()

    def write_line(text, font="Helvetica", style="", size=10):
        pdf.set_font(font, style, size)
        pdf.cell(0, 6, _safe_text_for_pdf(text), ln=True)

    write_line("FoodieFlow Kitchen", size=16, style="B")
    write_line(f"Invoice #: {order.get('order_id','')}")
    write_line(f"Date: {order.get('date','')}")
    pdf.ln(4)

    write_line("Customer:", style="B")
    for k, v in (customer or {}).items():
        write_line(f"{k.capitalize()}: {v}")

    pdf.ln(4)
    write_line("Items:", style="B")
    for item_key, qty in (order.get("items") or {}).items():
        _, item = find_item_by_key(item_key)
        if item:
            name = item.get("name", "")
            price_each = item.get("price", 0)
            line_total = price_each * qty
            write_line(f"{name} x{qty} - Rs.{line_total}")
        else:
            write_line(f"{item_key} x{qty} - Rs.Unknown")

    pdf.ln(4)
    for title, val in (bill or {}).items():
        write_line(f"{str(title).capitalize()}: Rs.{val}")

    # final output: encode Latin-1 and ignore any remaining non-encodable bytes
    raw = pdf.output(dest='S')
    if isinstance(raw, str):  # older fpdf may return str
        pdf_bytes = raw.encode('latin-1', 'ignore')
    else:
        # raw is bytes-like (fpdf2 or newer)
        try:
            pdf_bytes = raw.decode('latin-1').encode('latin-1', 'ignore')
        except Exception:
            # fallback: ensure bytes
            pdf_bytes = bytes(raw)
    return io.BytesIO(pdf_bytes)

def download_link(buf: io.BytesIO, filename: str):
    data = buf.getvalue()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">⬇️ Download</a>'

# --------------- CSV helpers ---------------
def make_cart_df(cart):
    rows = []
    for k, q in cart.items():
        _, it = find_item_by_key(k)
        if it:
            rows.append({
                "category": k.split(" - ", 1)[0],
                "name": it['name'],
                "qty": q,
                "price_each": it['price'],
                "line_total": it['price'] * q
            })
    return pd.DataFrame(rows)

def make_orders_df(orders):
    rows = []
    for o in orders:
        for k, q in o['items'].items():
            _, it = find_item_by_key(k)
            name = it['name'] if it else k
            price = it['price'] if it else None
            rows.append({
                "order_id": o['order_id'],
                "date": o['date'],
                "customer": o['customer'].get('name',''),
                "item": name,
                "qty": q,
                "line_total": price*q if price else None,
                "order_total": o['bill']['total']
            })
    return pd.DataFrame(rows)

# --------------- Pages ---------------
def home_page():
    st.markdown(f"""
    <div class="main-header">
      <h1>🍜 {RESTAURANT_INFO['name']}</h1>
      <h4>{RESTAURANT_INFO['tagline']}</h4>
      <div>⭐ {RESTAURANT_INFO['rating']} • 🚚 {RESTAURANT_INFO['delivery_time']} • 💳 Min ₹{RESTAURANT_INFO['minimum_order']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎉 Today's Offers")
    offers = RESTAURANT_INFO.get("offers", [])
    if not offers:
        st.info("No offers today.")
    else:
        ncols = min(len(offers), 4)
        cols = st.columns(ncols)
        for i, offer in enumerate(offers[:ncols]):
            with cols[i]:
                st.markdown(f"<div class='offer-banner'>{offer}</div>", unsafe_allow_html=True)

def menu_page():
    st.markdown("""
      <div class="main-header" style="padding:20px;">
        <h2 style="margin:0;">🍽️ Our Menu</h2>
        <p style="margin:6px 0 0 0; opacity:0.95;">Fresh, hot & made with ❤️ — Choose your favorites below</p>
      </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        filt = st.multiselect("Dietary", ["veg", "non-veg", "vegan", "spicy", "bestseller"], help="Filter items by dietary tags")
    with col2:
        search = st.text_input("Search menu", placeholder="Type item name...")

    for cat, items in MENU_DATA.items():
        st.markdown(f'<div class="small-header">{cat}</div>', unsafe_allow_html=True)
        st.markdown('<div class="menu-grid">', unsafe_allow_html=True)
        for it in items:
            if filt and not any(d in it.get("dietary", []) for d in filt):
                continue
            if search and search.strip() and search.lower() not in (it['name'] + " " + it.get('description', '')).lower():
                continue

            key = f"{cat} - {it['name']}"
            qty = st.session_state.cart.get(key, 0)

            badges = ' '.join(f"<div class='badge'>{d}</div>" for d in it.get("dietary", []))
            badges += f" <div class='badge'>⭐ {it['rating']}</div>"

            card_html = f"""
              <div class="menu-card">
                <div class="thumb">{it['image']}</div>
                <div class="meta">
                  <div class="badges">{badges}</div>
                  <h4>{it['name']}</h4>
                  <p>{it['description']}</p>
                  <div><span class="price">₹{it['price']}</span> • {it['cooking_time']}</div>
                </div>
              </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            cols = st.columns([1, 1, 2])
            dec_key = _safe_key("dec", key)
            inc_key = _safe_key("inc", key)
            if cols[0].button("➖", key=dec_key):
                if qty > 0:
                    new_qty = qty - 1
                    if new_qty == 0:
                        st.session_state.cart.pop(key, None)
                    else:
                        st.session_state.cart[key] = new_qty
            cols[1].markdown(f"<div class='qty-box'>Qty: {qty}</div>", unsafe_allow_html=True)
            if cols[2].button("➕ Add", key=inc_key):
                st.session_state.cart[key] = qty + 1
        st.markdown('</div>', unsafe_allow_html=True)

def cart_page():
    st.markdown("""
      <div class="main-header" style="padding:20px;">
        <h2 style="margin:0;">🛒 Cart & Checkout</h2>
      </div>
    """, unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is empty. Go to Menu to add items.")
        return

    bill = calculate_bill(st.session_state.cart)
    st.write("### Items in Cart")
    cart_df = make_cart_df(st.session_state.cart)
    if not cart_df.empty:
        st.dataframe(cart_df)
    else:
        st.write("Cart is empty.")

    st.write("### Bill Summary")
    bill_df = pd.DataFrame.from_dict(bill, orient='index', columns=['Amount'])
    st.table(bill_df)

    csv_buf = io.StringIO()
    cart_df.to_csv(csv_buf, index=False)
    st.download_button("⬇️ Download Cart CSV", csv_buf.getvalue(), file_name="cart.csv", mime="text/csv")

    with st.form("checkout_form"):
        st.write("#### Customer Details")
        name = st.text_input("Name", value=st.session_state.customer_info.get("name", ""))
        phone = st.text_input("Phone", value=st.session_state.customer_info.get("phone", ""))
        email = st.text_input("Email", value=st.session_state.customer_info.get("email", ""))
        address = st.text_area("Delivery Address", value=st.session_state.customer_info.get("address", ""))
        submitted = st.form_submit_button("Place Order")
        if submitted:
            if not name or not phone:
                st.error("Please provide at least name and phone.")
            else:
                order_id = generate_order_id()
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                order = {
                    "order_id": order_id,
                    "date": date_str,
                    "items": dict(st.session_state.cart),
                    "bill": bill,
                    "customer": {"name": name, "phone": phone, "email": email, "address": address}
                }
                st.session_state.order_history.append(order)
                st.session_state.customer_info = order["customer"]
                st.session_state.cart = {}
                st.success(f"✅ Order placed! #{order_id}")
                pdf_buf = create_pdf_invoice(order, order["customer"], bill)
                st.markdown(download_link(pdf_buf, f"Invoice_{order_id}.pdf"), unsafe_allow_html=True)

def orders_page():
    st.markdown("""
      <div class="main-header" style="padding:20px;">
        <h2 style="margin:0;">📦 Order History</h2>
      </div>
    """, unsafe_allow_html=True)

    if not st.session_state.order_history:
        st.info("No orders yet.")
        return

    for order in reversed(st.session_state.order_history):
        with st.expander(f"{order['order_id']} — ₹{order['bill']['total']} — {order['date']}"):
            st.write("Customer:", order["customer"])
            rows = []
            for k, q in order['items'].items():
                _, it = find_item_by_key(k)
                name = it['name'] if it else k
                price = it['price'] if it else None
                rows.append({"item": name, "qty": q, "price_each": price, "line_total": price*q if price else None})
            if rows:
                st.table(pd.DataFrame(rows))
            st.write("Bill:", order["bill"])
            dl_key = _safe_key("dl", order['order_id'])
            if st.button("Download Invoice (PDF)", key=dl_key):
                buf = create_pdf_invoice(order, order["customer"], order["bill"])
                st.markdown(download_link(buf, f"Invoice_{order['order_id']}.pdf"), unsafe_allow_html=True)

    df_orders = make_orders_df(st.session_state.order_history)
    if not df_orders.empty:
        st.download_button("⬇️ Download All Orders CSV", df_orders.to_csv(index=False).encode(), file_name="orders.csv", mime="text/csv")

# --------------- Navigation & sidebar ---------------
PAGES = {"Home": home_page, "Menu": menu_page, "Cart": cart_page, "Orders": orders_page}
choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
PAGES[choice]()

st.sidebar.markdown("---")
st.sidebar.markdown("### Cart Quick View")
if st.session_state.cart:
    for k, v in st.session_state.cart.items():
        _, it = find_item_by_key(k)
        if it:
            st.sidebar.write(f"{it['name']} x {v} — ₹{it['price']*v}")
    st.sidebar.write("**Total:**", calculate_bill(st.session_state.cart)["total"])
    cart_csv = make_cart_df(st.session_state.cart).to_csv(index=False)
    st.sidebar.download_button("Download Cart CSV", cart_csv, file_name="cart.csv", mime="text/csv")
else:
    st.sidebar.write("Cart empty — go to Menu ➜")
