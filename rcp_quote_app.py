import streamlit as st
from decimal import Decimal, getcontext
import re
import math
from collections import defaultdict

getcontext().prec = 28

st.set_page_config(
    page_title="RCP Quote Assistant",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🎤 RCP Quote Assistant")
st.caption("Voice-first • Robust parsing • Takeoff mode • Professional quotes | v2 (Improved)")

# ==================== PRICING (Updated with 325 support) ====================
PRICING = {
    305: {
        '15': {'CL5': Decimal('23.07')},
        '18': {'CL3': Decimal('27.83'), 'CL5': Decimal('28.93')},
        '24': {'CL3': Decimal('43.46'), 'CL5': Decimal('47.81')},
        '30': {'CL3': Decimal('61.76'), 'CL4': Decimal('64.85'), 'CL5': Decimal('67.94')},
        '36': {'CL3': Decimal('87.69'), 'CL4': Decimal('92.07'), 'CL5': Decimal('96.46')},
        '42': {'CL3': Decimal('106.75'), 'CL4': Decimal('112.09'), 'CL5': Decimal('117.43')},
        '48': {'CL3': Decimal('133.44'), 'CL4': Decimal('140.11'), 'CL5': Decimal('146.78')},
        '54': {'CL3': Decimal('183.00'), 'CL4': Decimal('192.15'), 'CL5': Decimal('201.30')},
        '60': {'CL3': Decimal('221.13'), 'CL4': Decimal('232.18'), 'CL5': Decimal('243.24')},
        '66': {'CL3': Decimal('263.06'), 'CL4': Decimal('276.22'), 'CL5': Decimal('289.37')},
        '72': {'CL3': Decimal('308.81'), 'CL4': Decimal('324.25'), 'CL5': Decimal('339.69')},
        '84': {'CL3': Decimal('400.31'), 'CL4': Decimal('420.33'), 'CL5': Decimal('440.34')},
    },
    310: {
        '15': {'CL5': Decimal('23.44')},
        '18': {'CL3': Decimal('28.29'), 'CL5': Decimal('29.39')},
        '24': {'CL3': Decimal('44.18'), 'CL5': Decimal('48.59')},
        '30': {'CL3': Decimal('62.78'), 'CL4': Decimal('65.91'), 'CL5': Decimal('69.05')},
        '36': {'CL3': Decimal('89.13'), 'CL4': Decimal('93.58'), 'CL5': Decimal('98.04')},
        '42': {'CL3': Decimal('108.50'), 'CL4': Decimal('113.93'), 'CL5': Decimal('119.35')},
        '48': {'CL3': Decimal('135.63'), 'CL4': Decimal('142.41'), 'CL5': Decimal('149.19')},
        '54': {'CL3': Decimal('186.00'), 'CL4': Decimal('195.30'), 'CL5': Decimal('204.60')},
        '60': {'CL3': Decimal('224.75'), 'CL4': Decimal('235.99'), 'CL5': Decimal('247.23')},
        '66': {'CL3': Decimal('267.38'), 'CL4': Decimal('280.74'), 'CL5': Decimal('294.11')},
        '72': {'CL3': Decimal('313.88'), 'CL4': Decimal('329.57'), 'CL5': Decimal('345.26')},
        '84': {'CL3': Decimal('406.88'), 'CL4': Decimal('427.22'), 'CL5': Decimal('447.56')},
    },
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

# Add 325/ton tier (extrapolated ~+$5/LF from 320 rates; UPDATE with actual spreadsheet values when available)
PRICING[325] = {}
for size, cl_dict in PRICING.get(320, {}).items():
    PRICING[325][size] = {cl: (price + Decimal('5.00')) for cl, price in cl_dict.items()}

PIPE_WEIGHTS = {
    '15': 155, '18': 175, '24': 290, '30': 410,
    '36': 563, '42': 860, '48': 1055, '54': 1270,
    '60': 1505, '66': 1755, '72': 2030, '84': 2655
}

FLARED_PRICES = {'15': 875, '18': 1030, '24': 1725, '30': 1895, '36': 2895, '42': 3895}
SAFETY_PRICES = {'15': 1360, '18': 1495, '24': 2670, '30': 4360}  # kept for future use

def round_to_sticks(lf):
    """Round linear feet up to next multiple of 8 (stick length)."""
    return lf if lf % 8 == 0 else ((lf // 8) + 1) * 8

# ==================== SPOKEN NUMBER SUPPORT ====================
word_to_num = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
    'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
    'hundred': 100, 'thousand': 1000
}

def _parse_num_phrase(phrase: str):
    """Convert spoken number phrase like 'five hundred eighty four' to int."""
    if not phrase:
        return None
    words = [w.strip('.,;:!?') for w in phrase.lower().split() if w.strip()]
    total = 0
    current = 0
    for w in words:
        if w == 'and' or not w:
            continue
        if w.isdigit():
            current += int(w)
            continue
        val = word_to_num.get(w)
        if val is None:
            return None
        if val >= 100:
            if current == 0:
                current = 1
            current *= val
        else:
            current += val
    total += current
    return total if total > 0 else None

def normalize_text(text: str) -> str:
    """Lowercase, remove commas, convert spoken numbers and size words to digits."""
    if not text:
        return ""
    text = text.lower().replace(",", " ").replace("  ", " ").strip()

    # Handle numeric "300 hundred" style if any
    text = re.sub(
        r'(\d+)\s*hundred(?:\s+and)?\s*(\d+)?',
        lambda m: str(int(m.group(1)) * 100 + (int(m.group(2)) if m.group(2) else 0)),
        text
    )

    # Size words to digits (longer phrases first)
    size_map = [
        (r'\btwenty[-\s]?four\b', '24'),
        (r'\bthirty[-\s]?six\b', '36'),
        (r'\bforty[-\s]?two\b', '42'),
        (r'\bforty[-\s]?eight\b', '48'),
        (r'\bfifty[-\s]?four\b', '54'),
        (r'\bsixty[-\s]?six\b', '66'),
        (r'\bseventy[-\s]?two\b', '72'),
        (r'\beighty[-\s]?four\b', '84'),
        (r'\bfifteen\b', '15'),
        (r'\beighteen\b', '18'),
        (r'\bthirty\b', '30'),
        (r'\bsixty\b', '60'),
    ]
    for pat, repl in size_map:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    # Convert spoken qty phrases (e.g. "five hundred eighty four feet" -> "584 feet")
    num_alt = '|'.join(sorted(word_to_num.keys(), key=len, reverse=True))
    unit_lookahead = r'(?=feet|ft\b|lf\b|linear\s*feet?|\d+\s*(?:inch|"))'
    phrase_re = rf'\b((?:{num_alt}\s+){{1,6}})(?={unit_lookahead})'

    replacements = []
    for m in re.finditer(phrase_re, text, re.IGNORECASE):
        phrase = m.group(1).strip()
        val = _parse_num_phrase(phrase)
        if val is not None:
            replacements.append((m.start(1), m.end(1), str(val)))

    for start, end, repl in sorted(replacements, reverse=True):
        text = text[:start] + repl + text[end:]

    return text

# ==================== PARSING LOGIC ====================
def parse_quote_text(text: str):
    """Parse natural language into list of item dicts. Returns (items, detected_ton)."""
    if not text or not text.strip():
        return [], 315

    items = []
    text_l = text.lower()

    # Ton detection: last mentioned XXX per ton wins (handles "priced at 305 per ton")
    ton_matches = re.findall(r'(\d{3})\s*(?:per ton|dollars?\s*per\s*ton|/\s*ton|\bton\b)', text_l)
    detected_ton = int(ton_matches[-1]) if ton_matches else 315
    if detected_ton not in PRICING:
        detected_ton = 315

    text_norm = normalize_text(text)

    clauses = re.split(r'[.!?;\n]+', text_norm + " ")

    for clause in clauses:
        clause = clause.strip()
        if len(clause) < 3:
            continue

        # Pipe pattern: qty + (feet/lf) + size + inch + (class/CL) + (3/4/5 or words)
        pipe_re = r'(\d+)\s*(?:feet|ft|lf|linear\s*feet?)?\s*(?:of\s+)?(\d+)\s*(?:inch|")?\s*(?:rcp|pipe)?\s*(?:class\s*|cl\s*)?([3-5]|three|four|five)'
        for m in re.finditer(pipe_re, clause, re.IGNORECASE):
            try:
                lf = int(m.group(1))
                size = m.group(2)
                cl_raw = m.group(3).lower().strip()
                cl_map = {"three": "3", "four": "4", "five": "5"}
                cl = "CL" + cl_map.get(cl_raw, cl_raw)

                # Class substitution rules
                if size == "15":
                    cl = "CL5"
                elif size in ("18", "24") and cl == "CL4":
                    cl = "CL5"

                if (size in PRICING.get(detected_ton, {}) and
                        cl in PRICING[detected_ton].get(size, {})):
                    items.append({
                        "type": "pipe",
                        "size": size,
                        "cl": cl,
                        "lf": lf,
                        "ton": detected_ton
                    })
            except Exception:
                continue

        # Flared End Sections
        flared_re = r'(?:^|[\s,])(?:one|1)?\s*(?:each)?\s*(\d+)?\s*(15|18|24|30|36|42)\s*(?:inch|")?\s*(?:flared|flared\s*end| fes |flared end section)'
        for m in re.finditer(flared_re, clause, re.IGNORECASE):
            try:
                qty = int(m.group(1)) if m.group(1) else 1
                size = m.group(2)
                if size in FLARED_PRICES:
                    items.append({
                        "type": "Flared End",
                        "size": size,
                        "qty": qty,
                        "price": FLARED_PRICES[size]
                    })
            except Exception:
                continue

    return items, detected_ton

def add_or_update_item(new_item: dict):
    """Add new item or consolidate (sum lf/qty) if same size+cl+ton (pipe) or same size (flared)."""
    items = st.session_state.items
    if new_item.get("type") == "pipe":
        for it in items:
            if (it.get("type") == "pipe" and
                    it["size"] == new_item["size"] and
                    it["cl"] == new_item["cl"] and
                    it.get("ton") == new_item.get("ton")):
                it["lf"] += new_item["lf"]
                return True
        items.append(new_item)
        return True
    elif new_item.get("type") == "Flared End":
        for it in items:
            if it.get("type") == "Flared End" and it["size"] == new_item["size"]:
                it["qty"] += new_item["qty"]
                return True
        items.append(new_item)
        return True
    return False

# ==================== QUOTE BUILDING / CALC LOGIC ====================
def build_quote(items, project_name="Project"):
    """Build sorted, consolidated quote lines + total. Returns (lines, total, lube_buckets)."""
    if not items:
        return [], Decimal(0), 1

    pipe_items = [it for it in items if it.get("type") == "pipe"]
    flared_items = [it for it in items if it.get("type") == "Flared End"]

    # Group for final consolidation + sorting
    pipe_groups = defaultdict(int)  # (size, cl, ton) -> total_lf
    for it in pipe_items:
        key = (it["size"], it["cl"], it.get("ton", 315))
        pipe_groups[key] += it["lf"]

    flared_groups = defaultdict(int)
    for it in flared_items:
        flared_groups[it["size"]] += it["qty"]

    # Joint lube calculation (truckloads based on total pipe weight)
    total_pounds = sum(
        Decimal(lf) * Decimal(PIPE_WEIGHTS.get(sz, 0))
        for (sz, _, _), lf in pipe_groups.items()
    )
    if total_pounds > 0:
        total_tons_f = float(total_pounds / Decimal(2000))
        truckloads = total_tons_f / 24.0
        lube_buckets = math.ceil(truckloads) if (truckloads - int(truckloads) > 0.5) else math.floor(truckloads)
        if lube_buckets < 1:
            lube_buckets = 1
    else:
        lube_buckets = 1
    lube_total = lube_buckets * 60

    lines = []
    total = Decimal(0)

    # Pipes: sort by size asc, then class, then ton
    for key in sorted(pipe_groups.keys(), key=lambda k: (int(k[0]), k[1], k[2])):
        size, cl, ton = key
        lf = pipe_groups[key]
        if ton not in PRICING or size not in PRICING[ton] or cl not in PRICING[ton][size]:
            continue
        price = PRICING[ton][size][cl]
        rounded_lf = round_to_sticks(lf)
        ext = Decimal(rounded_lf) * price
        total += ext
        lines.append(f"{rounded_lf} LF {size}” RCP {cl} @ ${float(price):.2f}/LF = ${ext:,.2f}")
        gaskets = rounded_lf // 8
        if gaskets > 0:
            lines.append(f"    {gaskets} EA {size}” Gaskets @ $0.00/EA = $0.00")

    # Flared End Sections sorted by size
    for size in sorted(flared_groups.keys(), key=int):
        qty = flared_groups[size]
        p = FLARED_PRICES.get(size, 0)
        ext = Decimal(qty) * Decimal(p)
        total += ext
        lines.append(f"{qty} EA {size}” FES @ ${p}/EA = ${ext:,.2f}")

    # Joint Lube
    total += Decimal(lube_total)
    lines.append(f"{lube_buckets} EA 30lb Joint Lube @ $60.00/EA = ${lube_total:,.2f}")

    return lines, total, lube_buckets

# ==================== SESSION STATE ====================
for key, default in [
    ("items", []),
    ("project_name", "Project"),
    ("last_voice_text", ""),
    ("voice_input", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ==================== INPUT UI ====================
st.subheader("🎤 Speak or Type Quote Details")
st.caption("Tip: Include 'Project name XYZ' at start. Mention price tier e.g. 'at 315 per ton'. Use 'Process Takeoff' to accumulate while reading plans.")

voice_text = st.text_area(
    "Voice / Text Input (mobile voice-to-text works here):",
    value=st.session_state.get("voice_input", ""),
    height=130,
    key="voice_input",
    placeholder="e.g. Project name Gold Creek GC 20. 584 feet of 18 inch class three priced at 305 per ton. Also 2 each 24 inch flared ends."
)

# Project name (editable, auto-filled from parse when possible)
pcol1, pcol2 = st.columns([4, 1])
with pcol1:
    pn = st.text_input(
        "Project / Job Name",
        value=st.session_state.project_name,
        key="pn_input",
        help="Auto-extracted from text if 'project name ...' present. Edit anytime."
    )
    if pn != st.session_state.project_name:
        st.session_state.project_name = pn
with pcol2:
    if st.button("Reset", key="reset_proj", help="Reset project name to 'Project'"):
        st.session_state.project_name = "Project"
        if "pn_input" in st.session_state:
            st.session_state["pn_input"] = "Project"
        st.rerun()

# ==================== PROCESSING BUTTONS (Two modes as per spec) ====================
st.markdown("**Processing Mode** — Choose one:")

def do_process(replace_mode: bool):
    """Core processing: normalize, parse, extract project, consolidate-add items."""
    current_text = st.session_state.get("voice_input", "").strip()
    if not current_text:
        st.warning("Please enter or dictate text in the box above first.")
        return

    last = st.session_state.get("last_voice_text", "")
    if current_text == last:
        st.info("Input text is unchanged since last process. Edit the text (change a number, add another item, or rephrase) then click a Process button again.")
        return

    parsed_items, det_ton = parse_quote_text(current_text)
    if not parsed_items:
        st.warning("No valid pipe or flared items detected. Try: '200 LF of 24 inch class 5 at 315 per ton' or 'project name My Job - 120 feet of 36 inch CL3 priced at 310 per ton'.")
        return

    # Try to extract project name from original (raw) text for better capture
    proj_m = re.search(
        r'(?:project|job)\s*(?:name)?\s*[:\-=]?\s*([A-Za-z0-9][A-Za-z0-9\s\.\-&]{2,}?)(?=\s*(?:\.|quantit|they|need|priced|price|LF|feet|inch|add|also))',
        current_text,
        re.IGNORECASE
    )
    if proj_m:
        extracted = proj_m.group(1).strip().rstrip('.,; ')
        if len(extracted) > 1:
            st.session_state.project_name = extracted
            if "pn_input" in st.session_state:
                st.session_state["pn_input"] = extracted

    # Add / merge items (consolidation happens inside)
    for itm in parsed_items:
        add_or_update_item(itm)

    st.success(f"✅ Added/merged {len(parsed_items)} item(s) @ ${det_ton}/ton tier. Duplicates of same size+class+ton were consolidated.")
    st.session_state.last_voice_text = current_text
    st.rerun()

proc_col1, proc_col2 = st.columns(2)
with proc_col1:
    if st.button("🔄 Process Voice Input\n(Replace All)", type="primary", use_container_width=True,
                 help="Clears current items then parses fresh. Use to start a brand new quote."):
        st.session_state.items = []
        do_process(replace_mode=True)

with proc_col2:
    if st.button("➕ Process Takeoff\n(Accumulate)", use_container_width=True,
                 help="Parses and ADDS items to existing list (merges same size+class). Perfect for reading plans incrementally."):
        do_process(replace_mode=False)

# ==================== CURRENT ITEMS ====================
st.subheader("📋 Current Items (auto-consolidated by size + class + ton)")

items = st.session_state.items
if not items:
    st.info("No items yet — speak/type above and use one of the Process buttons.")
else:
    for idx in range(len(items)):
        item = items[idx]
        if item.get("type") == "pipe":
            txt = f"**{item['lf']} LF** {item['size']}\" {item['cl']} @ {item['ton']}/ton"
        else:
            txt = f"**{item['qty']} EA** {item['size']}\" {item['type']}"
        c1, c2 = st.columns([6, 1])
        with c1:
            st.markdown(f"• {txt}")
        with c2:
            if st.button("❌", key=f"del_{idx}", help="Remove this item"):
                st.session_state.items.pop(idx)
                st.rerun()

    total_lf = sum(it.get("lf", 0) for it in items if it.get("type") == "pipe")
    if total_lf > 0:
        st.caption(f"Total pipe footage: {total_lf} LF  |  Est. weight varies by diameter (see lube calc on quote)")

st.divider()

# ==================== GENERATE QUOTE ====================
if st.button("📄 Generate Professional Quote", type="primary", use_container_width=True):
    if not items:
        st.error("Add items first using the voice/text input and Process buttons.")
    else:
        lines, total, lube_b = build_quote(items, st.session_state.project_name)
        proj = st.session_state.project_name or "Project"

        st.subheader(f"Quote for {proj}")
        for ln in lines:
            if ln.startswith("    "):
                st.text(ln)  # preserve indent for gaskets
            else:
                st.write(ln)

        st.write("---")
        st.success("**Freight included in pipe price.**")
        st.write(f"### Total = ${total:,.2f}")

        # Build email body
        email = f"""Good afternoon,

Please see pricing below for {proj}:

"""
        for ln in lines:
            email += ln + "\n"

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

        st.text_area("📧 Email-Ready Quote (click inside, Select All, Copy)", value=email, height=320, key="final_email")
        st.caption("The block above is formatted and ready to paste directly into Outlook/Gmail/etc.")

# ==================== NEW QUOTE / RESET ====================
if st.button("🆕 New Quote (Clear All Items & Project)", use_container_width=True):
    st.session_state.items = []
    st.session_state.project_name = "Project"
    st.session_state.last_voice_text = ""
    st.session_state["voice_input"] = ""
    if "pn_input" in st.session_state:
        st.session_state["pn_input"] = "Project"
    st.rerun()

# Footer
st.caption("RCP Quote Assistant v2 • Stick rounding (×8 LF) • Auto-gaskets (1 per 8 LF) • Joint lube by truckload (24 tons/truck) • Class rules: 15\"=CL5, 18\"/24\" CL4→CL5 • All prices from current rate sheets.")
st.caption("Mobile-optimized • Works great with phone voice-to-text • No data leaves your device")
