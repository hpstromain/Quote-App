import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("📋 RCP Quote Assistant")
st.caption("Mobile-friendly field pricing tool • Hardcoded exact pricing")

# Exact pricing from your spreadsheet
PRICING = {
    300: {
        '18': {'CL3': Decimal('27.60'), 'CL5': Decimal('28.48')},
        '24': {'CL3': Decimal('43.10'), 'CL5': Decimal('47.03')},
        '30': {'CL3': Decimal('61.20'), 'CL5': Decimal('67.32')},
    },
    305: {
        '18': {'CL3': Decimal('28.02'), 'CL5': Decimal('28.93')},
        '24': {'CL3': Decimal('43.85'), 'CL5': Decimal('47.81')},
        '30': {'CL3': Decimal('62.25'), 'CL5': Decimal('68.42')},
    },
    310: {
        '18': {'CL3': Decimal('28.45'), 'CL5': Decimal('29.39')},
        '24': {'CL3': Decimal('44.60'), 'CL5': Decimal('48.59')},
        '30': {'CL3': Decimal('63.30'), 'CL5': Decimal('69.52')},
    },
    315: {
        '18': {'CL3': Decimal('28.74'), 'CL5': Decimal('29.84')},
        '24': {'CL3': Decimal('44.89'), 'CL5': Decimal('49.38')},
        '30': {'CL3': Decimal('63.79'), 'CL5': Decimal('70.17')},
    },
    320: {
        '18': {'CL3': Decimal('29.20'), 'CL5': Decimal('30.30')},
        '24': {'CL3': Decimal('45.60'), 'CL5': Decimal('50.16')},
        '30': {'CL3': Decimal('64.80'), 'CL5': Decimal('71.28')},
    },
    325: {
        '18': {'CL3': Decimal('29.66'), 'CL5': Decimal('30.76')},
        '24': {'CL3': Decimal('46.31'), 'CL5': Decimal('50.94')},
        '30': {'CL3': Decimal('65.81'), 'CL5': Decimal('72.39')},
    }
}

if 'items' not in st.session_state:
    st.session_state.items = []

ton = st.selectbox("Price per Ton ($)", [300, 305, 310, 315, 320, 325], index=3)

st.subheader("Add Pipe")
col1, col2, col3 = st.columns(3)
with col1:
    size = st.selectbox("Size", list(PRICING[ton].keys()))
with col2:
    cl = st.selectbox("Class", list(PRICING[ton][size].keys()))
with col3:
    qty = st.number_input("Linear Feet", min_value=0, value=80, step=8)

if st.button("➕ Add Pipe"):
    st.session_state.items.append({"size": size, "cl": cl, "qty": qty, "ton": ton})
    st.success(f"Added {qty} LF {size}\" {cl}")

st.subheader("Current Items")
for item in st.session_state.items:
    st.write(f"• {item['qty']} LF {item['size']}\" {item['cl']}")

if st.button("🗑️ Clear All"):
    st.session_state.items = []

st.divider()

if st.button("📝 Generate Quote", type="primary"):
    st.subheader("Quote")
    total = Decimal(0)
    lines = []
    for item in st.session_state.items:
        price = PRICING[item['ton']][item['size']][item['cl']]
        ext = Decimal(item['qty']) * price
        total += ext
        lines.append(f"{item['qty']} LF {item['size']}\" {item['cl']} @ ${price}/LF = ${ext:,.2f}")
    
    for line in lines:
        st.write(line)
    st.write("---")
    st.write(f"**Total = ${total:,.2f}**")
    
    email = f"""Good morning [Customer],

Please see the pricing below:

"""
    for line in lines:
        email += line + "\n"
    email += f"""
Freight included.
Total = ${total:,.2f}

Thank you,
Hayden St. Romain
"""
    st.text_area("Copy this into Outlook:", value=email, height=280)