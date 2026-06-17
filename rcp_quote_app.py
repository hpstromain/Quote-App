import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("📋 RCP Quote Assistant")
st.caption("Mobile-friendly • Exact pricing from your spreadsheet")

# Initialize session state properly
if "items" not in st.session_state:
    st.session_state.items = []

# Pricing data (you can expand this later)
PRICING = {
    315: {
        '18': {'CL3': Decimal('28.74'), 'CL5': Decimal('29.84')},
        '24': {'CL3': Decimal('44.89'), 'CL5': Decimal('49.38')},
        '30': {'CL3': Decimal('63.79'), 'CL5': Decimal('70.17')},
    },
    320: {
        '18': {'CL3': Decimal('29.20'), 'CL5': Decimal('30.30')},
        '24': {'CL3': Decimal('45.60'), 'CL5': Decimal('50.16')},
        '30': {'CL3': Decimal('64.80'), 'CL5': Decimal('71.28')},
    }
}

ton_price = st.selectbox("Price per Ton ($)", [315, 320], index=0)

st.subheader("Add Pipe")
col1, col2, col3 = st.columns(3)
with col1:
    size = st.selectbox("Size", ["18", "24", "30"])
with col2:
    cl = st.selectbox("Class", ["CL3", "CL5"])
with col3:
    qty = st.number_input("Linear Feet", min_value=0, value=80, step=8)

if st.button("➕ Add Pipe"):
    st.session_state.items.append({
        "size": size, "cl": cl, "qty": qty, "ton": ton_price
    })

st.subheader("Current Items")
for i, item in enumerate(st.session_state.items):
    st.write(f"{i+1}. {item['qty']} LF {item['size']}\" {item['cl']}")

if st.button("Clear All"):
    st.session_state.items = []

st.divider()

if st.button("Generate Quote", type="primary"):
    st.subheader("Quote")
    total = Decimal(0)
    lines = []
    
    for item in st.session_state.items:
        price = PRICING[item["ton"]][item["size"]][item["cl"]]
        ext = Decimal(item["qty"]) * price
        total += ext
        lines.append(f"{item['qty']} LF {item['size']}\" {item['cl']} @ ${price}/LF = ${ext:,.2f}")
    
    for line in lines:
        st.write(line)
    
    st.write("---")
    st.write(f"**Total = ${total:,.2f}**")
    
    email_text = f"""Good morning [Customer],

Please see the pricing below:

"""
    for line in lines:
        email_text += line + "\n"
    email_text += f"""
Freight included.
Total = ${total:,.2f}

Thank you,
Hayden St. Romain
"""
    st.text_area("Copy to Outlook:", value=email_text, height=280)
