import streamlit as st
from decimal import Decimal, getcontext
import re

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant - Debug", layout="centered")

st.title("RCP Quote Assistant - Debug Mode")

PRICING = {
    315: {
        '18': {'CL3': Decimal('28.74'), 'CL5': Decimal('29.84')},
    },
    320: {
        '18': {'CL3': Decimal('29.20'), 'CL5': Decimal('30.30')},
    }
}

items = st.session_state.setdefault("items", [])

st.subheader("Test Input")

voice_text = st.text_area("Paste or speak here:", height=100)

if st.button("Test Parse", type="primary"):
    text = voice_text.lower().replace(",", "")
    st.write("**Raw text received:**", text)
    
    # Ton detection
    ton_match = re.search(r'(\d{3})\s*(?:per ton|dollars? per ton|ton|priced)', text)
    detected_ton = int(ton_match.group(1)) if ton_match else 315
    st.write("**Detected ton price:**", detected_ton)
    
    added = 0
    
    # Very simple and flexible pipe pattern
    pipe_pattern = r'(\d+)\s*(?:feet|ft)?\s*(?:of)?\s*(\d+)\s*(?:inch|")\s*(?:class|cl)?\s*([345]|three|four|five)'
    
    matches = list(re.finditer(pipe_pattern, text, re.IGNORECASE))
    st.write("**Number of pipe matches found:**", len(matches))
    
    for match in matches:
        qty = int(match.group(1))
        size = match.group(2)
        cl_raw = match.group(3)
        cl_map = {"three": "3", "four": "4", "five": "5"}
        cl = f"CL{cl_map.get(cl_raw, cl_raw)}"
        
        st.write(f"**Match found** → Qty: {qty}, Size: {size}\", Class: {cl}")
        
        if size in PRICING.get(detected_ton, {}):
            items.append({"type": "pipe", "size": size, "cl": cl, "lf": qty, "ton": detected_ton})
            added += 1
    
    if added > 0:
        st.success(f"Successfully added {added} item(s)")
    else:
        st.error("Still no items detected. Please share the exact text you used.")

st.subheader("Current Items")
for item in items:
    st.write(item)

if st.button("Clear"):
    st.session_state.items = []
