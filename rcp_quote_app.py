import streamlit as st
from decimal import Decimal, getcontext
import re

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("🎤 RCP Quote Assistant")
st.caption("Voice-first • Mobile optimized • Full features")

# ==================== EXPANDED PRICING ====================
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
        '18': {'CL3': Decimal('28.74'), 'CL4': Decimal('29.79'), 'CL5': Decimal('29.84')},
        '24': {'CL3': Decimal('44.89'), 'CL4': Decimal('47.13'), 'CL5': Decimal('49.38')},
        '30': {'CL3': Decimal('63.79'), 'CL4': Decimal('66.98'), 'CL5': Decimal('70.17')},
        '36': {'CL3': Decimal('90.56'), 'CL4': Decimal('95.09'), 'CL5': Decimal('99.62')},
        '42': {'CL3': Decimal('110.25'), 'CL4': Decimal('115.76'), 'CL5': Decimal('121.28')},
        '48': {'CL3': Decimal('137.81'), 'CL4': Decimal('144.70'), 'CL5': Decimal('151.59')},
        '54': {'CL3': Decimal('189.00'), 'CL4': Decimal('198.45'), 'CL5': Decimal('207.90')},
        '60': {'CL3': Decimal('228.38'), 'CL4': Decimal('239.79'), 'CL5': Decimal('251.30')},
        '66': {'CL3': Decimal('271.69'), 'CL4': Decimal('285.27'), 'CL5': Decimal('298.86')},
        '72': {'CL3': Decimal('318.94'), 'CL4': Decimal('334.88'), 'CL5': Decimal('350.83')},
        '84': {'CL3': Decimal('413.44'), 'CL4': Decimal('434.11'), 'CL5': Decimal('454.78')},
    },
    320: {
        '18': {'CL3': Decimal('29.20'), 'CL4': Decimal('30.25'), 'CL5': Decimal('30.30')},
        '24': {'CL3': Decimal('45.60'), 'CL4': Decimal('47.88'), 'CL5': Decimal('50.16')},
        '30': {'CL3': Decimal('64.80'), 'CL4': Decimal('68.04'), 'CL5': Decimal('71.28')},
        '36': {'CL3': Decimal('92.00'), 'CL4': Decimal('96.60'), 'CL5': Decimal('101.20')},
        '42': {'CL3': Decimal('112.00'), 'CL4': Decimal('117.60'), 'CL5': Decimal('123.20')},
        '48': {'CL3': Decimal('140.00'), 'CL4': Decimal('147.00'), 'CL5': Decimal('154.00')},
        '54': {'CL3': Decimal('192.00'), 'CL4': Decimal('201.60'), 'CL5': Decimal('211.20')},
        '60': {'CL3': Decimal('232.00'), 'CL4': Decimal('243.60'), 'CL5': Decimal('255.20')},
        '66': {'CL3': Decimal('276.00'), 'CL4': Decimal('289.80'), 'CL5': Decimal('303.60')},
        '72': {'CL3': Decimal('324.00'), 'CL4': Decimal('340.20'), 'CL5': Decimal('356.40')},
        '84': {'CL3': Decimal('420.00'), 'CL4': Decimal('441.00'), 'CL5': Decimal('462.00')},
    },
    325: {
        '18': {'CL3': Decimal('29.66'), 'CL5': Decimal('30.76')},
        '24': {'CL3': Decimal('46.31'), 'CL5': Decimal('50.94')},
        '30': {'CL3': Decimal('65.81'), 'CL5': Decimal('72.39')},
    }
}

FLARED_PRICES = {'15': 875, '18': 1030, '24': 1725, '30': 1895, '36': 2895, '42': 3895}
SAFETY_PRICES = {'15': 1360, '18': 1495, '24': 2670, '30': 4360}

def round_to_sticks(lf):
    return lf if lf % 8 == 0 else ((lf // 8) + 1) * 8

items = st.session_state.setdefault("items", [])

# ==================== VOICE INPUT ====================
st.subheader("🎤 Speak or Type Quote")

voice_text = st.text_area(
    "Speak naturally (customer + project + quantities + price):",
    height=140,
    placeholder="Fortis Siteworks Sandersville Kaolin Park 424 feet of 18 inch class three at 310 per ton"
)

if st.button("Process Voice Input", type="primary"):
    text = voice_text.lower().replace(",", "")
    
    if st.session_state.get("last_voice_text") == text:
        st.info("Already processed this text.")
    else:
        st.session_state.last_voice_text = text
        added = 0
        
        # Detect ton price anywhere
        ton_match = re.search(r'(\d{3})\s*(per ton|dollars? per ton|ton)', text)
        detected_ton = int(ton_match.group(1)) if ton_match else 315
        
        # Split into clauses
        clauses = re.split(r'[.!?]+', text)
        
        for clause in clauses:
            # Pipe detection
            pipe_pattern = r'(\d+)\s*(?:feet|lf)?\s*of\s*(\d+)\s*inch\s*(?:class\s*)?([345]|three|four|five)'
            for match in re.finditer(pipe_pattern, clause):
                qty = int(match.group(1))
                size = match.group(2)
                cl_raw = match.group(3)
                
                cl_map = {"three": "3", "four": "4", "five": "5"}
                cl = f"CL{cl_map.get(cl_raw, cl_raw)}"
                
                if size in PRICING.get(detected_ton, {}):
                    items.append({
                        "type": "pipe", "size": size, "cl": cl, 
                        "lf": qty, "ton": detected_ton
                    })
                    added += 1
        
        if added > 0:
            st.success(f"Added {added} item(s)")
        else:
            st.warning("No items detected.")

# ==================== CURRENT ITEMS ====================
st.subheader("Current Items")
for item in items:
    if item.get("type") == "pipe":
        st.write(f"• {item['lf']} LF {item['size']}\" {item['cl']} @ {item['ton']}/ton")

if st.button("Clear All"):
    st.session_state.items = []
    st.session_state.last_voice_text = ""

st.divider()

if st.button("Generate Professional Quote", type="primary"):
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
