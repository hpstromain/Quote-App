import streamlit as st
from decimal import Decimal, getcontext
import re

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("🎤 RCP Quote Assistant")
st.caption("Voice-first • Mobile optimized")

# ==================== PRICING ====================
PRICING = {
    315: {
        '15': {'CL5': Decimal('23.50')},
        '18': {'CL3': Decimal('28.74'), 'CL4': Decimal('29.79'), 'CL5': Decimal('29.84')},
        '24': {'CL3': Decimal('44.89'), 'CL4': Decimal('47.13'), 'CL5': Decimal('49.38')},
        '30': {'CL3': Decimal('63.79'), 'CL4': Decimal('66.98'), 'CL5': Decimal('70.17')},
        '36': {'CL3': Decimal('90.56'), 'CL4': Decimal('95.09'), 'CL5': Decimal('99.62')},
        '42': {'CL3': Decimal('110.25'), 'CL4': Decimal('115.76'), 'CL5': Decimal('121.28')},
        '48': {'CL3': Decimal('137.81'), 'CL4': Decimal('144.70'), 'CL5': Decimal('151.59')},
        '54': {'CL3': Decimal('189.00'), 'CL4': Decimal('198.45'), 'CL5': Decimal('207.90')},
        '60': {'CL3': Decimal('228.38'), 'CL4': Decimal('239.79'), 'CL5': Decimal('251.21')},
        '66': {'CL3': Decimal('271.69'), 'CL4': Decimal('285.27'), 'CL5': Decimal('298.86')},
        '72': {'CL3': Decimal('318.94'), 'CL4': Decimal('334.88'), 'CL5': Decimal('350.83')},
    },
    320: {
        '15': {'CL5': Decimal('24.20')},
        '18': {'CL3': Decimal('29.20'), 'CL5': Decimal('30.30')},
        '24': {'CL3': Decimal('45.60'), 'CL5': Decimal('50.16')},
        '30': {'CL3': Decimal('64.80'), 'CL4': Decimal('68.04'), 'CL5': Decimal('71.28')},
        '36': {'CL3': Decimal('92.00'), 'CL4': Decimal('96.60'), 'CL5': Decimal('101.20')},
        '42': {'CL3': Decimal('112.00'), 'CL4': Decimal('117.60'), 'CL5': Decimal('123.20')},
        '48': {'CL3': Decimal('140.00'), 'CL4': Decimal('147.00'), 'CL5': Decimal('154.00')},
        '54': {'CL3': Decimal('192.00'), 'CL4': Decimal('201.60'), 'CL5': Decimal('211.20')},
        '60': {'CL3': Decimal('232.00'), 'CL4': Decimal('243.60'), 'CL5': Decimal('255.20')},
        '66': {'CL3': Decimal('276.00'), 'CL4': Decimal('289.80'), 'CL5': Decimal('303.60')},
        '72': {'CL3': Decimal('324.00'), 'CL4': Decimal('340.20'), 'CL5': Decimal('356.40')},
    }
}

FLARED_PRICES = {'15': 875, '18': 1030, '24': 1725, '30': 1895, '36': 2895, '42': 3895}
SAFETY_PRICES = {'15': 1360, '18': 1495, '24': 2670, '30': 4360}

def round_to_sticks(lf):
    return lf if lf % 8 == 0 else ((lf // 8) + 1) * 8

items = st.session_state.setdefault("items", [])

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "last_voice_text" not in st.session_state:
    st.session_state.last_voice_text = ""

# ==================== VOICE INPUT ====================
st.subheader("🎤 Speak or Type Quote")

voice_text = st.text_area(
    "Speak naturally:",
    value=st.session_state.voice_text,
    height=120,
    key="voice_input"
)

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Process Voice Input", type="primary", use_container_width=True):
        current_text = st.session_state.get("voice_input", "").strip()
        
        if not current_text:
            st.warning("Please enter some text first.")
        elif st.session_state.last_voice_text == current_text:
            st.info("Already processed. Click 'New Quote' if you want to process the same text again.")
        else:
            text = current_text.lower().replace(",", "")
            st.session_state.last_voice_text = current_text
            
            added = 0
            ton_match = re.search(r'(\d{3})\s*(per ton|dollars? per ton|ton)', text)
            detected_ton = int(ton_match.group(1)) if ton_match else 315
            
            text = re.sub(r'(\d+)\s*hundred(?:\s+and)?\s*(\d+)?', 
                         lambda m: str(int(m.group(1))*100 + (int(m.group(2)) if m.group(2) else 0)), text)
            
            clauses = re.split(r'[.!?]+', text)
            
            for clause in clauses:
                pipe_pattern = r'(\d+)\s*(?:feet|lf|linear feet)?\s*(?:of)?\s*(\d+)\s*inch\s*(?:class\s*)?([345]|three|four|five)'
                for match in re.finditer(pipe_pattern, clause):
                    qty = int(match.group(1))
                    size = match.group(2)
                    cl_raw = match.group(3)
                    
                    cl_map = {"three": "3", "four": "4", "five": "5"}
                    cl = f"CL{cl_map.get(cl_raw, cl_raw)}"
                    
                    if size == '15':
                        cl = 'CL5'
                    elif size == '18' and cl == 'CL4':
                        cl = 'CL5'
                    elif size == '24' and cl == 'CL4':
                        cl = 'CL5'
                    
                    if size in PRICING.get(detected_ton, {}):
                        items.append({
                            "type": "pipe", "size": size, "cl": cl, 
                            "lf": qty, "ton": detected_ton
                        })
                        added += 1
                
                flared_pattern = r'(?:one|1)?\s*(?:each)?\s*(\d+)?\s*(15|18|24|30|36|42)\s*inch\s*(?:flared|flared end)'
                flared_match = re.search(flared_pattern, clause)
                if flared_match:
                    qty = int(flared_match.group(1)) if flared_match.group(1) else 1
                    size = flared_match.group(2)
                    items.append({
                        "type": "Flared End",
                        "size": size,
                        "qty": qty,
                        "price": FLARED_PRICES.get(size, 0)
                    })
                    added += 1
            
            if added > 0:
                st.success(f"Added {added} item(s)")
            else:
                st.warning("No items detected.")

with col2:
    if st.button("🆕 New Quote", use_container_width=True):
        st.session_state.items = []
        st.session_state.last_voice_text = ""
        st.session_state.voice_text = ""
        st.rerun()

# ==================== CURRENT ITEMS ====================
st.subheader("Current Items")
for item in items:
    if item.get("type") == "pipe":
        st.write(f"• {item['lf']} LF {item['size']}\" {item['cl']} @ {item['ton']}/ton")
    else:
        st.write(f"• {item['qty']} EA {item['size']}\" {item['type']}")

if st.button("Clear All"):
    st.session_state.items = []
    st.session_state.last_voice_text = ""
    st.session_state.voice_text = ""

st.divider()

if st.button("Generate Professional Quote", type="primary"):
    st.subheader("Quote")
    total = Decimal(0)
    lines = []

    for item in items:
        if item.get("type") == "pipe":
            price = PRICING[item["ton"]][item["size"]][item["cl"]]
            rounded = round_to_sticks(item["lf"])
            ext = Decimal(rounded) * price
            total += ext
            lines.append(f"{rounded} LF {item['size']}” RCP {item['cl']} @ ${price}/LF = ${ext:,.2f}")
            
            gaskets = rounded // 8
            if gaskets > 0:
                lines.append(f"{gaskets} EA {item['size']}” Gaskets @ $0.00/EA = $0.00")
        
        elif item.get("type") == "Flared End":
            ext = Decimal(item["qty"]) * Decimal(item["price"])
            total += ext
            lines.append(f"{item['qty']} EA {item['size']}” FES @ ${item['price']}/EA = ${ext:,.2f}")

    for line in lines:
        st.write(line)

    st.write("---")
    st.write("**Freight included in pipe price.**")
    st.write(f"**Total = ${total:,.2f}**")

    # Project name
    project_name = "Project"
    text_original = st.session_state.voice_text.strip()
    match = re.search(r'project name\s+(?:is\s+)?(.+?)(?:\.|they need|priced at)', text_original, re.IGNORECASE)
    if match:
        project_name = match.group(1).strip()
    else:
        match = re.search(r'project\s+(?:is\s+)?(.+?)(?:\.|they need|priced at)', text_original, re.IGNORECASE)
        if match:
            project_name = match.group(1).strip()

    # ==================== EMAIL (Correct Format) ====================
    email = f"""Good afternoon,

Please see pricing below for {project_name}:

"""
    for line in lines:
        email += line + "\n"

    email += f"""
Freight included in pipe price.
Total = ${total:,.2f}

Please let me know if you have any questions or concerns.

Thank you,

Hayden St. Romain
Account Manager
C 678.814.3208
148 Rock Quarry Rd
Stockbridge, GA 30281
RinkerPipe.com
Hayden.st.romain@rinkerpipe.com
"""

    st.text_area("Generated Quote:", value=email, height=280)
    st.code(email, language="text")
