import streamlit as st
from decimal import Decimal, getcontext
import re
import math
from collections import defaultdict

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("🎤 RCP Quote Assistant")
st.caption("Voice-first • Stable Streamlit Version")

# ==================== PRICING ====================
PRICING = {
    305: { ... },   # (same as before - I'll keep it short here for clarity)
    310: { ... },
    315: { ... },
    320: { ... },
    325: { ... }
}

# (PIPE_WEIGHTS, FLARED_PRICES, round_to_sticks function stay the same)

def round_to_sticks(lf):
    return lf if lf % 8 == 0 else ((lf // 8) + 1) * 8

# ==================== VERY DEFENSIVE SESSION STATE ====================
def get_items():
    if "items" not in st.session_state or not isinstance(st.session_state.items, list):
        st.session_state.items = []
    return st.session_state.items

def clear_items():
    st.session_state.items = []
    st.session_state.last_voice_text = ""
    st.session_state.voice_text = ""

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""
if "last_voice_text" not in st.session_state:
    st.session_state.last_voice_text = ""

items = get_items()

# ==================== UI ====================
st.subheader("🎤 Speak or Type Quote")

voice_text = st.text_area(
    "Speak naturally:",
    value=st.session_state.voice_text,
    height=120,
    key="voice_input"
)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    if st.button("Process Voice Input", type="primary", use_container_width=True):
        current_text = st.session_state.get("voice_input", "").strip()
        if not current_text:
            st.warning("Please enter some text first.")
        elif st.session_state.last_voice_text == current_text:
            st.info("Already processed. Click 'New Quote' to start fresh.")
        else:
            text = current_text.lower().replace(",", "")
            st.session_state.last_voice_text = current_text
            st.session_state.items = []          # Clear previous
            added = 0
            
            # (Parsing logic - same as before, using st.session_state.items.append)
            # ... [parsing code remains the same] ...
            
            if added > 0:
                st.success(f"Added {added} item(s)")
            else:
                st.warning("No items detected")

with col2:
    if st.button("Process Takeoff", type="secondary", use_container_width=True):
        # Similar logic but appends instead of clearing
        pass   # (You can add this later if needed)

with col3:
    if st.button("🆕 New Quote", use_container_width=True):
        clear_items()
        st.rerun()

# Current Items Display
st.subheader("Current Items")
for item in get_items():
    if item.get("type") == "pipe":
        st.write(f"• {item['lf']} LF {item['size']}\" {item['cl']} @ {item['ton']}/ton")
    else:
        st.write(f"• {item['qty']} EA {item['size']}\" {item['type']}")

if st.button("Clear All"):
    clear_items()

st.divider()

if st.button("Generate Professional Quote", type="primary"):
    current_items = get_items()
    
    # ==================== CONSOLIDATION + SORTING ====================
    pipe_totals = defaultdict(int)
    flared_totals = defaultdict(int)
    
    for item in current_items:
        if item.get("type") == "pipe":
            key = (item["size"], item["cl"], item["ton"])
            pipe_totals[key] += item["lf"]
        elif item.get("type") == "Flared End":
            key = (item["size"], item.get("price", 0))
            flared_totals[key] += item["qty"]
    
    sorted_pipes = sorted(pipe_totals.items(), key=lambda x: int(x[0][0]))
    
    lines = []
    total = Decimal(0)
    
    for (size, cl, ton), total_lf in sorted_pipes:
        price = PRICING[ton][size][cl]
        rounded = round_to_sticks(total_lf)
        ext = Decimal(rounded) * price
        total += ext
        lines.append(f"{rounded} LF {size}” RCP {cl} @ ${price}/LF = ${ext:,.2f}")
        gaskets = rounded // 8
        if gaskets > 0:
            lines.append(f"{gaskets} EA {size}” Gaskets @ $0.00/EA = $0.00")
    
    # Flared ends + Joint Lube + Total (same logic as before)
    # ... [rest of quote generation remains the same]
    
    # Then build and display the professional email
