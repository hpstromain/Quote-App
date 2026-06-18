import { useState, useRef, useCallback } from "react";

const PRICING = {
  305: {
    "15": { CL5: 23.07 },
    "18": { CL3: 27.83, CL5: 28.93 },
    "24": { CL3: 43.46, CL5: 47.81 },
    "30": { CL3: 61.76, CL4: 64.85, CL5: 67.94 },
    "36": { CL3: 87.69, CL4: 92.07, CL5: 96.46 },
    "42": { CL3: 106.75, CL4: 112.09, CL5: 117.43 },
    "48": { CL3: 133.44, CL4: 140.11, CL5: 146.78 },
    "54": { CL3: 183.0, CL4: 192.15, CL5: 201.3 },
    "60": { CL3: 221.13, CL4: 232.18, CL5: 243.24 },
    "66": { CL3: 263.06, CL4: 276.22, CL5: 289.37 },
    "72": { CL3: 308.81, CL4: 324.25, CL5: 339.69 },
    "84": { CL3: 400.31, CL4: 420.33, CL5: 440.34 },
  },
  310: {
    "15": { CL5: 23.44 },
    "18": { CL3: 28.29, CL5: 29.39 },
    "24": { CL3: 44.18, CL5: 48.59 },
    "30": { CL3: 62.78, CL4: 65.91, CL5: 69.05 },
    "36": { CL3: 89.13, CL4: 93.58, CL5: 98.04 },
    "42": { CL3: 108.5, CL4: 113.93, CL5: 119.35 },
    "48": { CL3: 135.63, CL4: 142.41, CL5: 149.19 },
    "54": { CL3: 186.0, CL4: 195.3, CL5: 204.6 },
    "60": { CL3: 224.75, CL4: 235.99, CL5: 247.23 },
    "66": { CL3: 267.38, CL4: 280.74, CL5: 294.11 },
    "72": { CL3: 313.88, CL4: 329.57, CL5: 345.26 },
    "84": { CL3: 406.88, CL4: 427.22, CL5: 447.56 },
  },
  315: {
    "15": { CL5: 23.5 },
    "18": { CL3: 28.74, CL4: 29.79, CL5: 29.84 },
    "24": { CL3: 44.89, CL4: 47.13, CL5: 49.38 },
    "30": { CL3: 63.79, CL4: 66.98, CL5: 70.17 },
    "36": { CL3: 90.56, CL4: 95.09, CL5: 99.62 },
    "42": { CL3: 110.25, CL4: 115.76, CL5: 121.28 },
    "48": { CL3: 137.81, CL4: 144.7, CL5: 151.59 },
    "54": { CL3: 189.0, CL4: 198.45, CL5: 207.9 },
    "60": { CL3: 228.38, CL4: 239.79, CL5: 251.21 },
    "66": { CL3: 271.69, CL4: 285.27, CL5: 298.86 },
    "72": { CL3: 318.94, CL4: 334.88, CL5: 350.83 },
  },
  320: {
    "15": { CL5: 24.2 },
    "18": { CL3: 29.2, CL5: 30.3 },
    "24": { CL3: 45.6, CL5: 50.16 },
    "30": { CL3: 64.8, CL4: 68.04, CL5: 71.28 },
    "36": { CL3: 92.0, CL4: 96.6, CL5: 101.2 },
    "42": { CL3: 112.0, CL4: 117.6, CL5: 123.2 },
    "48": { CL3: 140.0, CL4: 147.0, CL5: 154.0 },
    "54": { CL3: 192.0, CL4: 201.6, CL5: 211.2 },
    "60": { CL3: 232.0, CL4: 243.6, CL5: 255.2 },
    "66": { CL3: 276.0, CL4: 289.8, CL5: 303.6 },
    "72": { CL3: 324.0, CL4: 340.2, CL5: 356.4 },
  },
  325: {
    "15": { CL5: 24.57 },
    "18": { CL3: 29.65, CL5: 30.75 },
    "24": { CL3: 46.31, CL5: 50.94 },
    "30": { CL3: 65.81, CL4: 69.1, CL5: 72.39 },
    "36": { CL3: 93.44, CL4: 98.11, CL5: 102.78 },
    "42": { CL3: 113.75, CL4: 119.44, CL5: 125.13 },
    "48": { CL3: 142.19, CL4: 149.3, CL5: 156.41 },
    "54": { CL3: 195.0, CL4: 204.75, CL5: 214.5 },
    "60": { CL3: 235.63, CL4: 247.41, CL5: 259.19 },
    "66": { CL3: 280.0, CL4: 294.0, CL5: 308.0 },
    "72": { CL3: 329.0, CL4: 345.45, CL5: 361.9 },
  },
};

const PIPE_WEIGHTS = {
  "15": 155, "18": 175, "24": 290, "30": 410,
  "36": 563, "42": 860, "48": 1055, "54": 1270,
  "60": 1505, "66": 1755, "72": 2030, "84": 2655,
};

const FLARED_PRICES = {
  "15": 875, "18": 1030, "24": 1725, "30": 1895, "36": 2895, "42": 3895,
};

function roundToSticks(lf) {
  return lf % 8 === 0 ? lf : (Math.floor(lf / 8) + 1) * 8;
}

function applyClassSub(size, cl) {
  if (size === "15") return "CL5";
  if ((size === "18" || size === "24") && cl === "CL4") return "CL5";
  return cl;
}

function calcLubeBuckets(pipeItems) {
  if (!pipeItems.length) return 1;
  const totalLbs = pipeItems.reduce((sum, item) => {
    return sum + item.lf * (PIPE_WEIGHTS[item.size] || 0);
  }, 0);
  const totalTons = totalLbs / 2000;
  const truckloads = totalTons / 24;
  const frac = truckloads - Math.floor(truckloads);
  let buckets = frac > 0.5 ? Math.ceil(truckloads) : Math.floor(truckloads);
  return Math.max(1, buckets);
}

function consolidateItems(items) {
  const pipeMap = {};
  const flared = [];
  items.forEach((item) => {
    if (item.type === "pipe") {
      const key = `${item.size}|${item.cl}|${item.ton}`;
      if (pipeMap[key]) {
        pipeMap[key].lf += item.lf;
      } else {
        pipeMap[key] = { ...item };
      }
    } else {
      const existing = flared.find((f) => f.size === item.size);
      if (existing) existing.qty += item.qty;
      else flared.push({ ...item });
    }
  });
  const pipes = Object.values(pipeMap).sort((a, b) => parseInt(a.size) - parseInt(b.size));
  return { pipes, flared };
}

function generateEmail(projectName, customerName, items) {
  const { pipes, flared } = consolidateItems(items);
  const lubeBuckets = calcLubeBuckets(pipes);
  const lubeTotal = lubeBuckets * 60;
  let grandTotal = lubeTotal;
  const lines = [];

  pipes.forEach((item) => {
    const priceTable = PRICING[item.ton];
    if (!priceTable || !priceTable[item.size] || !priceTable[item.size][item.cl]) return;
    const price = priceTable[item.size][item.cl];
    const rounded = roundToSticks(item.lf);
    const ext = rounded * price;
    grandTotal += ext;
    lines.push(`${rounded} LF ${item.size}" RCP ${item.cl} @ $${price.toFixed(2)}/LF = $${ext.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
    const gaskets = Math.floor(rounded / 8);
    if (gaskets > 0) {
      lines.push(`  ${gaskets} EA ${item.size}" Gaskets @ $0.00/EA = $0.00`);
    }
  });

  flared.forEach((item) => {
    const price = FLARED_PRICES[item.size] || 0;
    const ext = item.qty * price;
    grandTotal += ext;
    lines.push(`${item.qty} EA ${item.size}" FES @ $${price.toFixed(2)}/EA = $${ext.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
  });

  lines.push(`${lubeBuckets} EA 30lb Joint Lube @ $60.00/EA = $${lubeTotal.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);

  const greeting = customerName ? `Good afternoon ${customerName},` : "Good afternoon,";
  const projectRef = projectName ? `for ${projectName}` : "";

  const email = `${greeting}

Please see pricing below ${projectRef}:

${lines.join("\n")}

Freight included in pipe price.
Total = $${grandTotal.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}

Please let me know if you have any questions or concerns.

Thank you,

Hayden St. Romain
Account Manager
C 678.814.3208
148 Rock Quarry Rd
Stockbridge, GA 30281
RinkerPipe.com
Hayden.st.romain@rinkerpipe.com`;

  return { email, grandTotal, lines };
}

const SYSTEM_PROMPT = `You are a parsing engine for an RCP (Reinforced Concrete Pipe) quoting tool used by a field salesperson. Your ONLY job is to extract structured data from natural language input about pipe quantities and project details.

Return ONLY valid JSON — no markdown, no explanation, no preamble. The JSON must follow this exact schema:

{
  "projectName": string or null,
  "customerName": string or null,
  "pricePerTon": number (must be one of: 305, 310, 315, 320, 325) or null (default to 315),
  "items": [
    {
      "type": "pipe",
      "size": string (e.g. "18", "24", "30"),
      "cl": string (e.g. "CL3", "CL4", "CL5"),
      "lf": number (linear feet, integer)
    },
    {
      "type": "flared",
      "size": string,
      "qty": number
    }
  ]
}

Rules:
- Valid pipe sizes: 15, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 84
- Valid classes: CL3, CL4, CL5. Convert spoken words: "three"→CL3, "four"→CL4, "five"→CL5, "class 3"→CL3, etc.
- 15" pipe is ALWAYS CL5 regardless of what was said
- 18" or 24" CL4 must be changed to CL5
- Convert spoken numbers to integers: "five hundred" → 500, "seven hundred and forty four" → 744
- Handle abbreviations: "ft", "LF", "linear feet", "feet" all mean linear footage
- "FES" or "flared end section" or "flared end" = flared item
- pricePerTon: look for phrases like "305 per ton", "priced at 310", "$315/ton", etc. Default to 315 if not found.
- projectName: look for "project name X", "project X", "job name X", job codes like "GC 20"
- customerName: look for "customer", "for", contractor names
- If no items are found, return items as empty array []
- Extract ALL pipe entries mentioned, even multiple sizes/classes in one statement`;

export default function RCPQuoteAssistant() {
  const [input, setInput] = useState("");
  const [items, setItems] = useState([]);
  const [projectName, setProjectName] = useState("");
  const [customerName, setCustomerName] = useState("");
  const [status, setStatus] = useState(null);
  const [parsing, setParsing] = useState(false);
  const [quote, setQuote] = useState(null);
  const [copied, setCopied] = useState(false);
  const [mode, setMode] = useState("replace");
  const textRef = useRef(null);

  const parseInput = useCallback(async () => {
    const text = input.trim();
    if (!text) {
      setStatus({ type: "warn", msg: "Enter some text first." });
      return;
    }
    setParsing(true);
    setStatus(null);
    setQuote(null);
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-6",
          max_tokens: 1000,
          system: SYSTEM_PROMPT,
          messages: [{ role: "user", content: text }],
        }),
      });
      const data = await response.json();
      const raw = data.content?.map((b) => b.text || "").join("").trim();
      const clean = raw.replace(/```json|```/g, "").trim();
      const parsed = JSON.parse(clean);

      if (parsed.projectName) setProjectName(parsed.projectName);
      if (parsed.customerName) setCustomerName(parsed.customerName);

      const newItems = (parsed.items || []).map((item) => {
        if (item.type === "pipe") {
          return {
            type: "pipe",
            size: String(item.size),
            cl: applyClassSub(String(item.size), item.cl || "CL3"),
            lf: Math.round(item.lf),
            ton: parsed.pricePerTon && PRICING[parsed.pricePerTon] ? parsed.pricePerTon : 315,
          };
        } else {
          return {
            type: "flared",
            size: String(item.size),
            qty: Math.round(item.qty || 1),
          };
        }
      }).filter((item) => {
        if (item.type === "pipe") {
          const tier = PRICING[item.ton];
          return tier && tier[item.size] && tier[item.size][item.cl];
        }
        return FLARED_PRICES[item.size] !== undefined;
      });

      if (mode === "replace") {
        setItems(newItems);
      } else {
        setItems((prev) => [...prev, ...newItems]);
      }

      if (newItems.length > 0) {
        setStatus({ type: "ok", msg: `Added ${newItems.length} item${newItems.length > 1 ? "s" : ""}` });
      } else {
        setStatus({ type: "warn", msg: "No valid pipe items detected. Try again." });
      }
    } catch (err) {
      setStatus({ type: "err", msg: "Parse error. Check your input and try again." });
    } finally {
      setParsing(false);
    }
  }, [input, mode]);

  const generateQuote = () => {
    if (!items.length) {
      setStatus({ type: "warn", msg: "Add items first before generating a quote." });
      return;
    }
    const result = generateEmail(projectName, customerName, items);
    setQuote(result);
  };

  const copyEmail = () => {
    if (!quote) return;
    navigator.clipboard.writeText(quote.email).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const newQuote = () => {
    setItems([]);
    setProjectName("");
    setCustomerName("");
    setInput("");
    setStatus(null);
    setQuote(null);
  };

  const removeItem = (idx) => {
    setItems((prev) => prev.filter((_, i) => i !== idx));
    setQuote(null);
  };

  const { pipes: consolidatedPipes, flared: consolidatedFlared } = consolidateItems(items);

  const s = {
    wrap: { fontFamily: "var(--font-sans)", color: "var(--color-text-primary)", paddingBottom: "2rem" },
    header: { background: "#1a2e1a", padding: "1rem 1.25rem", borderRadius: "var(--border-radius-lg)", marginBottom: "1rem" },
    headerTitle: { fontSize: 20, fontWeight: 500, color: "#a8d5a2", margin: 0, letterSpacing: "-0.3px" },
    headerSub: { fontSize: 12, color: "#6b9e67", margin: "2px 0 0", fontFamily: "var(--font-mono)" },
    section: { marginBottom: "1rem" },
    label: { fontSize: 12, fontWeight: 500, color: "var(--color-text-secondary)", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.06em" },
    textarea: { width: "100%", minHeight: 90, resize: "vertical", fontSize: 15, padding: "10px 12px", background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-secondary)", borderRadius: "var(--border-radius-md)", color: "var(--color-text-primary)", boxSizing: "border-box", fontFamily: "var(--font-sans)", lineHeight: 1.5 },
    row: { display: "flex", gap: 8, marginBottom: "0.75rem" },
    modeBtn: (active) => ({
      flex: 1, padding: "8px 4px", fontSize: 13, fontWeight: active ? 500 : 400,
      background: active ? "#1a2e1a" : "var(--color-background-secondary)",
      color: active ? "#a8d5a2" : "var(--color-text-secondary)",
      border: active ? "0.5px solid #3a5e3a" : "0.5px solid var(--color-border-tertiary)",
      borderRadius: "var(--border-radius-md)", cursor: "pointer",
    }),
    primaryBtn: (disabled) => ({
      flex: 1, padding: "11px 12px", fontSize: 14, fontWeight: 500,
      background: disabled ? "var(--color-background-secondary)" : "#1a2e1a",
      color: disabled ? "var(--color-text-secondary)" : "#a8d5a2",
      border: "none", borderRadius: "var(--border-radius-md)", cursor: disabled ? "not-allowed" : "pointer",
    }),
    secondaryBtn: { flex: "0 0 auto", padding: "11px 14px", fontSize: 13, background: "var(--color-background-secondary)", color: "var(--color-text-secondary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", cursor: "pointer" },
    statusBox: (type) => ({
      padding: "8px 12px", borderRadius: "var(--border-radius-md)", fontSize: 13, marginBottom: "0.75rem",
      background: type === "ok" ? "var(--color-background-success)" : type === "warn" ? "var(--color-background-warning)" : "var(--color-background-danger)",
      color: type === "ok" ? "var(--color-text-success)" : type === "warn" ? "var(--color-text-warning)" : "var(--color-text-danger)",
      border: `0.5px solid ${type === "ok" ? "var(--color-border-success)" : type === "warn" ? "var(--color-border-warning)" : "var(--color-border-danger)"}`,
    }),
    itemCard: { background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", padding: "8px 12px", marginBottom: 6, display: "flex", justifyContent: "space-between", alignItems: "center" },
    itemText: { fontSize: 13, fontFamily: "var(--font-mono)", color: "var(--color-text-primary)" },
    itemSub: { fontSize: 11, color: "var(--color-text-secondary)", marginTop: 2 },
    removeBtn: { background: "none", border: "none", color: "var(--color-text-secondary)", cursor: "pointer", fontSize: 16, lineHeight: 1, padding: "2px 4px" },
    metaRow: { display: "flex", gap: 8, marginBottom: "0.75rem" },
    metaInput: { flex: 1, fontSize: 13, padding: "8px 10px", background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", color: "var(--color-text-primary)", fontFamily: "var(--font-sans)" },
    divider: { border: "none", borderTop: "0.5px solid var(--color-border-tertiary)", margin: "1rem 0" },
    quoteBox: { background: "#0d1a0d", borderRadius: "var(--border-radius-lg)", padding: "1rem 1.25rem", marginTop: "0.75rem" },
    quoteLine: { fontFamily: "var(--font-mono)", fontSize: 12, color: "#8fcf8a", lineHeight: 1.7, whiteSpace: "pre-wrap", wordBreak: "break-word" },
    totalLine: { fontFamily: "var(--font-mono)", fontSize: 14, fontWeight: 500, color: "#c0e8ba", marginTop: 8, borderTop: "0.5px solid #2a4a2a", paddingTop: 8 },
    copyBtn: { width: "100%", padding: "11px", fontSize: 14, fontWeight: 500, background: "#1a2e1a", color: "#a8d5a2", border: "none", borderRadius: "var(--border-radius-md)", cursor: "pointer", marginTop: 10 },
    emptyState: { textAlign: "center", padding: "1.5rem 1rem", color: "var(--color-text-secondary)", fontSize: 13, background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", border: "0.5px dashed var(--color-border-tertiary)" },
    spinner: { display: "inline-block", width: 14, height: 14, border: "2px solid #a8d5a240", borderTopColor: "#a8d5a2", borderRadius: "50%", animation: "spin 0.7s linear infinite", marginRight: 6, verticalAlign: "middle" },
  };

  return (
    <div style={s.wrap}>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      <div style={s.header}>
        <p style={s.headerTitle}>RCP Quote Assistant</p>
        <p style={s.headerSub}>RINKER PIPE · HAYDEN ST. ROMAIN</p>
      </div>

      <div style={s.section}>
        <p style={s.label}>Input mode</p>
        <div style={s.row}>
          <button style={s.modeBtn(mode === "replace")} onClick={() => setMode("replace")}>
            ↺ Quick Replace
          </button>
          <button style={s.modeBtn(mode === "accumulate")} onClick={() => setMode("accumulate")}>
            + Accumulate (Takeoff)
          </button>
        </div>
      </div>

      <div style={s.section}>
        <p style={s.label}>Speak or type quantities</p>
        <textarea
          ref={textRef}
          style={s.textarea}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Example: "Project Gold Creek GC 20. 584 feet of 18 inch class 3 and 320 feet of 24 inch class 5, priced at 315 per ton"`}
        />
        <div style={{ ...s.row, marginTop: 8 }}>
          <button style={s.primaryBtn(parsing)} onClick={parseInput} disabled={parsing}>
            {parsing && <span style={s.spinner} />}
            {parsing ? "Parsing…" : mode === "replace" ? "Process Input" : "Add to Takeoff"}
          </button>
          <button style={s.secondaryBtn} onClick={newQuote} title="Start new quote">
            New
          </button>
        </div>
      </div>

      {status && (
        <div style={s.statusBox(status.type)}>{status.msg}</div>
      )}

      <div style={s.section}>
        <p style={s.label}>Project details</p>
        <div style={s.metaRow}>
          <input
            style={s.metaInput}
            placeholder="Project name"
            value={projectName}
            onChange={(e) => { setProjectName(e.target.value); setQuote(null); }}
          />
          <input
            style={s.metaInput}
            placeholder="Customer name"
            value={customerName}
            onChange={(e) => { setCustomerName(e.target.value); setQuote(null); }}
          />
        </div>
      </div>

      <div style={s.section}>
        <p style={s.label}>Current items ({items.length})</p>
        {items.length === 0 ? (
          <div style={s.emptyState}>No items yet. Speak or type quantities above.</div>
        ) : (
          <>
            {consolidatedPipes.map((item, i) => {
              const price = PRICING[item.ton]?.[item.size]?.[item.cl];
              const rounded = roundToSticks(item.lf);
              const ext = price ? rounded * price : 0;
              return (
                <div key={`p-${i}`} style={s.itemCard}>
                  <div>
                    <div style={s.itemText}>{item.lf} LF {item.size}" RCP {item.cl} @ ${item.ton}/ton</div>
                    {price && <div style={s.itemSub}>→ {rounded} LF rounded · ${ext.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>}
                  </div>
                  <button style={s.removeBtn} onClick={() => {
                    const idx = items.findIndex(it => it.type === "pipe" && it.size === item.size && it.cl === item.cl && it.ton === item.ton);
                    if (idx > -1) removeItem(idx);
                  }}>×</button>
                </div>
              );
            })}
            {consolidatedFlared.map((item, i) => (
              <div key={`f-${i}`} style={s.itemCard}>
                <div>
                  <div style={s.itemText}>{item.qty} EA {item.size}" Flared End Section</div>
                  <div style={s.itemSub}>${(item.qty * (FLARED_PRICES[item.size] || 0)).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
                </div>
                <button style={s.removeBtn} onClick={() => {
                  const idx = items.findIndex(it => it.type === "flared" && it.size === item.size);
                  if (idx > -1) removeItem(idx);
                }}>×</button>
              </div>
            ))}
          </>
        )}
      </div>

      <hr style={s.divider} />

      <button
        style={{ ...s.primaryBtn(items.length === 0), width: "100%", marginBottom: "0.75rem" }}
        onClick={generateQuote}
        disabled={items.length === 0}
      >
        Generate Professional Quote
      </button>

      {quote && (
        <div>
          <div style={s.quoteBox}>
            <pre style={s.quoteLine}>{quote.email}</pre>
            <div style={s.totalLine}>
              TOTAL: ${quote.grandTotal.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </div>
          </div>
          <button style={s.copyBtn} onClick={copyEmail}>
            {copied ? "✓ Copied to clipboard" : "Copy email to clipboard"}
          </button>
        </div>
      )}
    </div>
  );
}
