import streamlit as st
from decimal import Decimal, getcontext
import re

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("🎤 RCP Quote Assistant")
st.caption("Improved parser • Better large number handling")

# ==================== PRICING ====================
PRICING = { ... (keep your full pricing data here) ... }

FLARED_PRICES = {'15': 875, '18': 1030, '24': 1725, '30': 1895, '36': 2895, '42': 3895}
SAFETY_PRICES = {'15': 1360, '18': 1495, '24': 2670, '30': 4360}

def round_to_sticks(lf):
    return lf if lf % 8 == 0 else ((lf // 8) + 1) * 8

items = st.session_state.setdefault("items", [])

# ==================== VOICE INPUT ====================
st.subheader("🎤 Speak or Paste Quote Here")

voice_text = st.text_area("Full quote text:", height=160)

if st.button("Process Voice Input", type="primary"):
    text = voice_text.lower().replace(",", "")   # ← Remove commas from numbers
    
    # Prevent re-processing the exact same text
    if st.session_state.get("last_voice_text") == text:
        st.info("This text was already processed.")
    else:
        st.session_state.last_voice_text = text
        added = 0
        
        # Detect ton price
        ton_match = re.search(r'(\d{3})\s*(per ton|dollars? per ton|ton)', text)
        detected_ton = int(ton_match.group(1)) if ton_match else 315
        
        # Split into clauses
        clauses = re.split(r'[.!?]+', text)
        
        for clause in clauses:
            # Improved pipe pattern (more flexible)
            pipe_pattern = r'(\d+)\s*(?:feet|lf)?\s*of\s*(\d+)\s*inch\s*(?:class\s*)?([345]|three|four|five)'
            for match in re.finditer(pipe_pattern, clause):
                qty = int(match.group(1))
                size = match.group(2)
                cl_raw = match.group(3)
                
                cl_map = {"three": "3", "four": "4", "five": "5"}
                cl = f"CL{cl_map.get(cl_raw, cl_raw)}"
                
                if size in PRICING.get(detected_ton, {}):
                    items.append({
                        "type": "pipe",
                        "size": size,
                        "cl": cl,
                        "lf": qty,
                        "ton": detected_ton
                    })
                    added += 1
        
        if added > 0:
            st.success(f"Added {added} item(s)")
        else:
            st.warning("Still no items detected.")

# ==================== CURRENT ITEMS + QUOTE ====================
st.subheader("Current Items")
for item in items:
    if item.get("type") == "pipe":
        st.write(f"• {item['lf']} LF {item['size']}\" {item['cl']} @ {item['ton']}/ton")

if st.button("Clear All"):
    st.session_state.items = []
    st.session_state.last_voice_text = ""

st.divider()

if st.button("Generate Professional Quote", type="primary"):
    # (Same quote generation code as before)
    st.subheader("Quote")
    total = Decimal(0)
    lines = []
    gasket_lines = []

    for item in items:
        if item.get("type") == "pipe":
            price = PRICING[item["ton"]][item["size"]][item["cl"]]
            rounded = round_to_sticks(item["lf"])
            ext = Decimal(rounded) * price
            total += ext
            lines.append(f"{rounded} LF {item['size']}\" {item['cl']} @ ${price}/LF = ${ext:,.2f}")
            
            gaskets = rounded // 8
            if gaskets > 0:
                gasket_lines.append(f"{gaskets} EA {item['size']}\" Gaskets @ $0.00 = $0.00")

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
