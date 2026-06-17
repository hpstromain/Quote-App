# ==================== VOICE INPUT ====================
st.subheader("🎤 Speak or Type Quote")

# Use session state for the text area so we can clear it
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

voice_text = st.text_area(
    "Speak naturally:",
    value=st.session_state.voice_text,
    height=120,
    key="voice_input"
)

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Process Voice Input", type="primary", use_container_width=True):
        text = st.session_state.voice_text.lower().replace(",", "")
        
        if st.session_state.get("last_voice_text") == text:
            st.info("Already processed.")
        else:
            st.session_state.last_voice_text = text
            added = 0
            
            ton_match = re.search(r'(\d{3})\s*(per ton|dollars? per ton|ton)', text)
            detected_ton = int(ton_match.group(1)) if ton_match else 315
            
            # Spoken number conversion
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
        st.session_state.voice_text = ""          # ← Clears the text box
        st.rerun()
