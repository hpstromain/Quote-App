import streamlit as st
from decimal import Decimal, getcontext
import re

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("🎤 RCP Quote Assistant")
st.caption("Voice-first • Speak naturally while driving or in the field")

# ==================== PRICING DATA ====================
PRICING = {
    315: { ... (keep your full pricing dict here) ... },
    320: { ... (keep your full pricing dict here) ... }
}

FLARED_PRICES = {'15': 875, '18': 1030, '24': 1725, '30': 1895, '36': 2895, '42': 3895}
SAFETY_PRICES = {'15': 1360, '18': 1495, '24': 2670, '30': 4360}

def round_to_sticks(lf):
    return lf if lf % 8 == 0 else ((lf // 8) + 1) * 8

items = st.session_state.setdefault("items", [])

# ==================== VOICE / NATURAL LANGUAGE INPUT ====================
st.subheader("🎤 Speak or Type Here (Recommended)")

voice_text = st.text_area(
    "Speak naturally using your phone's voice-to-text:",
    height=140,
    placeholder="Example: Customer Fortis Siteworks project Sandersville Kaolin Park expansion 424 feet of 18 inch class three 144 feet of 24 inch class three at 310 per ton"
)

if st.button("Process Voice Input", type="primary"):
    text = voice_text.lower()
    
    # Detect price per ton
    ton_match = re.search(r'(\d{3})\s*(per ton|dollars? per ton|ton)', text)
    detected_ton = int(ton_match.group(1)) if ton_match else 315
    
    added_count = 0
    
    # Improved pipe detection (handles "424 feet of 18 inch class three")
    pipe_pattern = r'(\d+)\s*(feet|lf|linear feet)?\s*of\s*(\d+)\s*inch\s*(class\s*([345]|three|four|five))?'
    for match in re.finditer(pipe_pattern, text):
        qty = int(match.group(1))
        size = match.group(3)
        cl_raw = match.group(5) or "3"
        
        # Convert word classes to numbers
        cl_map = {"three": "3", "four": "4", "five": "5"}
        cl_num = cl_map.get(cl_raw, cl_raw)
        cl = f"CL{cl_num}"
        
        if size in PRICING.get(detected_ton, {}):
            items.append({
                "type": "pipe",
                "size": size,
                "cl": cl,
                "lf": qty,
                "ton": detected_ton
            })
            added_count += 1
    
    # Detect flared ends
    flared_match = re.search(r'(\d+)\s*(15|18|24|30|36|42)\s*inch\s*flared', text)
    if flared_match:
        qty = int(flared_match.group(1))
        size = flared_match.group(2)
        items.append({
            "type": "Flared End",
            "size": size,
            "qty": qty,
            "price": FLARED_PRICES.get(size, 0)
        })
        added_count += 1
    
    if added_count > 0:
        st.success(f"Added {added_count} item(s) from voice input!")
    else:
        st.warning("Could not understand any items. Try being more specific (e.g. '424 feet of 18 inch class three at 310 per ton').")

# ==================== CURRENT ITEMS + QUOTE ====================
st.subheader("Current Items")
for item in items:
    if item["type"] == "pipe":
        st.write(f"• {item['lf']} LF {item['size']}\" {item['cl']} @ {item['ton']}/ton")
    else:
        st.write(f"• {item['qty']} EA {item['size']}\" {item['type']}")

if st.button("Clear All"):
    st.session_state.items = []

st.divider()

if st.button("Generate Professional Quote", type="primary"):
    # (Same quote generation logic as before - it will now work with the added items)
    st.subheader("Quote")
    total = Decimal(0)
    lines = []
    gasket_lines = []

    for item in items:
        if item["type"] == "pipe":
            price = PRICING[item["ton"]][item["size"]][item["cl"]]
            rounded = round_to_sticks(item["lf"])
            ext = Decimal(rounded) * price
            total += ext
            lines.append(f"{rounded} LF {item['size']}\" {item['cl']} @ ${price}/LF = ${ext:,.2f}")
            
            gaskets = rounded // 8
            if gaskets > 0:
                gasket_lines.append(f"{gaskets} EA {item['size']}\" Gaskets @ $0.00 = $0.00")
        else:
            ext = Decimal(item["qty"]) * Decimal(item["price"])
            total += ext
            lines.append(f"{item['qty']} EA {item['size']}\" {item['type']} @ ${item['price']} = ${ext:,.2f}")

    for line in lines:
        st.write(line)
    for line in gasket_lines:
        st.write(line)

    st.write("---")
    st.write(f"**Total = ${total:,.2f}**")

    email = f"""Good morning [Customer],

Please see the pricing below for the project:

"""
    for line in lines + gasket_lines:
        email += line + "\n"
    email += f"""
Freight is included in pipe price.
Total = ${total:,.2f}

Thank you,
Hayden St. Romain
Account Manager | C 678.814.3208
"""
    st.text_area("Copy this into Outlook:", value=email, height=300)
