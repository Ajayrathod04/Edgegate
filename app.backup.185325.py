import json
import hashlib
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import streamlit as st
import openvino as ov

# ============================================================
# EDGEGATE — Evidence-Gated Physical AI Runtime
# Team Shunya Code
# ============================================================

st.set_page_config(
    page_title="EdgeGate — Physical AI Runtime",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# DESIGN SYSTEM
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #070914;
    --surface: #0d1220;
    --surface-2: #11182a;
    --surface-3: #151e32;
    --line: #27324a;
    --text: #f4f7ff;
    --muted: #94a2bc;
    --cyan: #67e8f9;
    --cyan-2: #22d3ee;
    --violet: #8b7cff;
    --violet-2: #6d5dfc;
    --coral: #ff7b72;
    --amber: #f6c76b;
    --green: #54d39b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(103,232,249,.10), transparent 25%),
        radial-gradient(circle at 92% 8%, rgba(139,124,255,.12), transparent 28%),
        linear-gradient(145deg, #050710 0%, #080b16 45%, #070914 100%);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding: 1.2rem 2rem 3rem 2rem;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #080b16 0%, #0a0e19 100%);
    border-right: 1px solid #1b2437;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

div[data-testid="stMetric"] {
    background: transparent;
}

/* top navigation */
.topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:9px 4px 18px 4px;
}

.brand {
    display:flex;
    align-items:center;
    gap:11px;
}

.brand-mark {
    width:36px;
    height:36px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#061018;
    background:linear-gradient(135deg,var(--cyan),var(--violet));
    font-family:'Space Grotesk';
    font-weight:700;
    box-shadow:0 0 28px rgba(103,232,249,.20);
}

.brand-name {
    font-family:'Space Grotesk';
    font-size:1rem;
    font-weight:700;
    letter-spacing:-.02em;
}

.brand-sub {
    color:var(--muted);
    font-size:.68rem;
    margin-top:-2px;
}

.status-pill {
    border:1px solid #23445a;
    color:var(--cyan);
    background:#0b1722;
    padding:7px 11px;
    border-radius:999px;
    font-size:.69rem;
    font-weight:700;
    letter-spacing:.08em;
}

/* hero */
.hero {
    position:relative;
    overflow:hidden;
    min-height:280px;
    padding:34px 38px;
    border:1px solid #26344d;
    border-radius:28px;
    background:
        radial-gradient(circle at 85% 20%, rgba(103,232,249,.12), transparent 25%),
        radial-gradient(circle at 65% 100%, rgba(139,124,255,.13), transparent 28%),
        linear-gradient(135deg,#10192a 0%,#0b101c 55%,#080b14 100%);
    box-shadow:0 25px 80px rgba(0,0,0,.34);
}

.hero-grid {
    position:absolute;
    inset:0;
    opacity:.16;
    background-image:
        linear-gradient(#60708d 1px, transparent 1px),
        linear-gradient(90deg,#60708d 1px, transparent 1px);
    background-size:44px 44px;
    mask-image:linear-gradient(90deg,transparent,#000 35%,#000 80%,transparent);
}

.hero-content {
    position:relative;
    z-index:2;
}

.eyebrow {
    color:var(--cyan);
    font-size:.69rem;
    letter-spacing:.19em;
    font-weight:800;
    margin-bottom:12px;
}

.hero-title {
    font-family:'Space Grotesk';
    font-size:4rem;
    line-height:.96;
    letter-spacing:-.065em;
    font-weight:700;
    margin:0;
}

.hero-title span {
    color:var(--cyan);
}

.hero-desc {
    max-width:850px;
    color:#b6c2d6;
    font-size:1.02rem;
    line-height:1.6;
    margin-top:16px;
}

.hero-desc strong {
    color:#f4f7ff;
}

.hero-tags {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    margin-top:22px;
}

.tag {
    padding:7px 10px;
    border:1px solid #33445e;
    border-radius:999px;
    background:#0b111eaa;
    color:#c4d0e2;
    font-size:.65rem;
    font-weight:700;
    letter-spacing:.08em;
}

/* metrics */
.metric-card {
    border:1px solid #202c42;
    border-radius:18px;
    padding:17px 18px;
    background:linear-gradient(145deg,#111827,#0b101b);
    min-height:102px;
    box-shadow:0 10px 35px rgba(0,0,0,.16);
}

.metric-label {
    color:#71819b;
    font-size:.64rem;
    letter-spacing:.14em;
    font-weight:800;
}

.metric-value {
    font-family:'Space Grotesk';
    color:#f5f8ff;
    font-size:1.55rem;
    font-weight:700;
    margin-top:8px;
}

.metric-note {
    color:#687892;
    font-size:.68rem;
    margin-top:3px;
}

/* decision */
.decision {
    min-height:270px;
    border-radius:24px;
    padding:30px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    border:1px solid;
    box-shadow:0 20px 60px rgba(0,0,0,.24);
}

.decision.good {
    background:
        radial-gradient(circle at 80% 15%, rgba(84,211,155,.13), transparent 28%),
        linear-gradient(145deg,#0c211b,#091510);
    border-color:#285844;
}

.decision.warn {
    background:
        radial-gradient(circle at 80% 15%, rgba(246,199,107,.13), transparent 28%),
        linear-gradient(145deg,#211b0e,#130f08);
    border-color:#68552b;
}

.decision.bad {
    background:
        radial-gradient(circle at 80% 15%, rgba(255,123,114,.13), transparent 28%),
        linear-gradient(145deg,#241016,#13090d);
    border-color:#71323a;
}

.decision-label {
    color:#8593aa;
    font-size:.67rem;
    letter-spacing:.15em;
    font-weight:800;
}

.decision h1 {
    font-family:'Space Grotesk';
    font-size:3.2rem;
    line-height:1;
    letter-spacing:-.055em;
    margin:12px 0 10px;
}

.decision-text {
    color:#abb8ca;
    line-height:1.55;
}

.reason {
    padding:10px 12px;
    margin:7px 0;
    border:1px solid #222e43;
    border-radius:12px;
    background:#0a0f19;
    color:#c2ccdc;
    font-size:.82rem;
}

/* section */
.section-title {
    font-family:'Space Grotesk';
    font-size:1.05rem;
    font-weight:700;
    margin:25px 0 10px;
}

.section-sub {
    color:#75849c;
    font-size:.78rem;
    margin-bottom:15px;
}

/* architecture cards */
.arch-card {
    height:100%;
    border:1px solid #202c42;
    border-radius:18px;
    padding:18px;
    background:#0c111c;
}

.arch-number {
    color:var(--cyan);
    font-family:'Space Grotesk';
    font-size:.68rem;
    font-weight:700;
}

.arch-name {
    font-family:'Space Grotesk';
    font-size:1rem;
    font-weight:700;
    margin-top:8px;
}

.arch-desc {
    color:#78879e;
    font-size:.76rem;
    line-height:1.45;
    margin-top:6px;
}

/* policy */
.policy-card {
    border:1px solid #202c42;
    border-radius:18px;
    background:#0c111c;
    padding:17px;
}

.policy-row {
    display:flex;
    justify-content:space-between;
    gap:20px;
    padding:10px 0;
    border-bottom:1px solid #1a2436;
    font-size:.78rem;
}

.policy-row:last-child {
    border-bottom:0;
}

.policy-name { color:#9ba9bd; }
.policy-value { color:#edf3ff; font-weight:700; }

/* evidence */
.evidence {
    border:1px solid #293652;
    border-radius:18px;
    background:#090e18;
    padding:16px;
}

.hash {
    color:var(--cyan);
    font-family:monospace;
    font-size:.76rem;
}

/* sidebar */
.sidebar-brand {
    padding:5px 3px 18px;
}

.sidebar-title {
    font-family:'Space Grotesk';
    font-size:1.1rem;
    font-weight:700;
}

.sidebar-caption {
    color:#738199;
    font-size:.7rem;
}

.sidebar-section {
    color:#74839b;
    font-size:.64rem;
    font-weight:800;
    letter-spacing:.13em;
    margin:18px 0 8px;
}

/* streamlit widgets */
.stButton > button {
    border-radius:12px;
    border:1px solid #30415d;
    background:#111a2a;
    color:#eaf1fb;
    font-weight:700;
}

.stButton > button:hover {
    border-color:var(--cyan);
    color:var(--cyan);
}

div[data-baseweb="select"] > div {
    background:#0d1422;
    border-color:#28364f;
}

.stDownloadButton > button {
    border-radius:12px;
    background:#10192a;
    border:1px solid #2d405d;
    color:#dce8f8;
}

hr {
    border-color:#1b2537;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# OPENVINO ENGINE
# ------------------------------------------------------------
@st.cache_resource
def build_openvino_engine():
    core = ov.Core()

    x = ov.opset13.parameter(
        [1, 6],
        ov.Type.f32,
        name="scene_features"
    )

    weights = ov.opset13.constant(
        np.array(
            [[1.1], [0.9], [1.2], [1.0], [0.8], [1.0]],
            dtype=np.float32
        )
    )

    bias = ov.opset13.constant(
        np.array([[-2.7]], dtype=np.float32)
    )

    y = ov.opset13.matmul(x, weights, False, False)
    y = ov.opset13.add(y, bias)
    y = ov.opset13.sigmoid(y)

    model = ov.Model([y], [x], "edgegate_risk")
    compiled = core.compile_model(model, "CPU")
    request = compiled.create_infer_request()

    return core, request


def run_edge_inference(x):
    _, request = build_openvino_engine()

    features = np.array(
        [[
            x["conf"],
            min(x["age"] / 3.0, 1.0),
            min(x["clearance"] / .7, 1.0),
            float(x["obstacle"]),
            float(x["keepout"]),
            x["drift"],
        ]],
        dtype=np.float32
    )

    start = time.perf_counter()

    output = request.infer({
        "scene_features": features
    })

    latency = (time.perf_counter() - start) * 1000
    risk = float(next(iter(output.values())).reshape(-1)[0])

    return risk, latency


# ------------------------------------------------------------
# SAFETY SCENARIOS
# ------------------------------------------------------------
SCENARIOS = {
    "Nominal / Fresh Scene": {
        "conf": 0.94,
        "age": 0.18,
        "clearance": 0.62,
        "obstacle": False,
        "keepout": False,
        "drift": 0.04,
        "operator": False,
    },
    "Stale Scene / Drift": {
        "conf": 0.78,
        "age": 2.70,
        "clearance": 0.62,
        "obstacle": False,
        "keepout": False,
        "drift": 0.46,
        "operator": False,
    },
    "Dynamic Obstacle": {
        "conf": 0.92,
        "age": 0.34,
        "clearance": 0.18,
        "obstacle": True,
        "keepout": False,
        "drift": 0.07,
        "operator": False,
    },
    "Keep-out Violation": {
        "conf": 0.95,
        "age": 0.22,
        "clearance": 0.54,
        "obstacle": False,
        "keepout": True,
        "drift": 0.03,
        "operator": False,
    },
    "Operator Emergency Stop": {
        "conf": 0.91,
        "age": 0.16,
        "clearance": 0.51,
        "obstacle": False,
        "keepout": False,
        "drift": 0.02,
        "operator": True,
    },
}


def decide(x):
    reasons = []

    if x["operator"]:
        return "REJECT", ["Operator emergency stop asserted"]

    if x["keepout"]:
        reasons.append("planned path intersects keep-out zone")

    if x["obstacle"] or x["clearance"] < 0.25:
        reasons.append("dynamic obstacle / insufficient clearance")

    if x["age"] > 2:
        reasons.append("scene observation is stale")

    if x["drift"] > 0.30:
        reasons.append("scene drift exceeds threshold")

    if x["conf"] < 0.82:
        reasons.append("perception confidence below threshold")

    if reasons:
        if len(reasons) <= 2 and not x["keepout"]:
            return "ROLLBACK", reasons
        return "REJECT", reasons

    return "PROMOTE", ["all runtime gates satisfied"]


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown("""
<div class="topbar">
    <div class="brand">
        <div class="brand-mark">◈</div>
        <div>
            <div class="brand-name">EDGEGATE</div>
            <div class="brand-sub">SHUNYA CODE · PHYSICAL AI INFRASTRUCTURE</div>
        </div>
    </div>
    <div class="status-pill">● EDGE RUNTIME ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-title">EdgeGate Control</div>
    <div class="sidebar-caption">Evidence-gated action authorization</div>
</div>
""", unsafe_allow_html=True)

scenario = st.sidebar.selectbox(
    "Replay a safety scenario",
    list(SCENARIOS.keys())
)

x = SCENARIOS[scenario]

st.sidebar.markdown('<div class="sidebar-section">RUNTIME POLICY</div>', unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="policy-card">
    <div class="policy-row">
        <span class="policy-name">Freshness</span>
        <span class="policy-value">≤ 2.00 s</span>
    </div>
    <div class="policy-row">
        <span class="policy-name">Confidence</span>
        <span class="policy-value">≥ 0.82</span>
    </div>
    <div class="policy-row">
        <span class="policy-name">Clearance</span>
        <span class="policy-value">≥ 0.25 m</span>
    </div>
    <div class="policy-row">
        <span class="policy-name">Drift</span>
        <span class="policy-value">≤ 0.30</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">EDGE STACK</div>', unsafe_allow_html=True)
st.sidebar.caption("Intel OpenVINO · CPU")
st.sidebar.caption("Python · Streamlit")
st.sidebar.caption("Deterministic evidence ledger")

st.sidebar.markdown('<div class="sidebar-section">DECISION MODEL</div>', unsafe_allow_html=True)
st.sidebar.caption("Perception proposes.")
st.sidebar.caption("EdgeGate evaluates.")
st.sidebar.caption("Evidence authorizes.")

# ------------------------------------------------------------
# DECISION
# ------------------------------------------------------------
verdict, reasons = decide(x)
risk, inference_ms = run_edge_inference(x)

evidence_payload = {
    "scenario": scenario,
    "telemetry": x,
    "verdict": verdict,
    "reasons": reasons,
    "openvino_risk": round(risk, 4),
    "inference_ms": round(inference_ms, 3),
}

evidence_hash = hashlib.sha256(
    json.dumps(
        evidence_payload,
        sort_keys=True
    ).encode()
).hexdigest()[:16]

st.markdown(f"""
<div class="hero">
    <div class="hero-grid"></div>
    <div class="hero-content">
        <div class="eyebrow">RUNTIME AUTHORIZATION · PHYSICAL AI</div>
        <div class="hero-title">Edge<span>Gate</span></div>
        <div class="hero-desc">
            A safety boundary between <strong>perception</strong> and
            <strong>physical action</strong>. EdgeGate refuses to trust
            confidence alone — it checks freshness, geometry, drift,
            obstacles, keep-out zones and operator control before an
            action can proceed.
        </div>
        <div class="hero-tags">
            <span class="tag">LOCAL-FIRST</span>
            <span class="tag">OPENVINO EDGE</span>
            <span class="tag">EVIDENCE-BACKED</span>
            <span class="tag">FAIL-SAFE</span>
            <span class="tag">AUDITABLE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# LIVE TELEMETRY
# ------------------------------------------------------------
metric_data = [
    ("PERCEPTION", f"{x['conf']*100:.0f}%", "model confidence"),
    ("SCENE AGE", f"{x['age']:.2f}s", "observation age"),
    ("CLEARANCE", f"{x['clearance']:.2f}m", "path clearance"),
    ("DRIFT", f"{x['drift']*100:.0f}%", "scene divergence"),
    ("EDGE LATENCY", f"{inference_ms:.1f}ms", "OpenVINO / CPU"),
]

cols = st.columns(5)

for col, (label, value, note) in zip(cols, metric_data):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# MAIN DECISION PANEL
# ------------------------------------------------------------
st.markdown('<div class="section-title">Authorization Decision</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Six independent runtime gates are evaluated before action authorization.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.15, .85], gap="large")

with left:
    decision_class = {
        "PROMOTE": "good",
        "ROLLBACK": "warn",
        "REJECT": "bad",
    }[verdict]

    icon = {
        "PROMOTE": "✓",
        "ROLLBACK": "↩",
        "REJECT": "×",
    }[verdict]

    explanation = {
        "PROMOTE": "All safety gates are satisfied. The proposed action may proceed.",
        "ROLLBACK": "The current action should be withdrawn while the scene is re-evaluated.",
        "REJECT": "The proposed action is blocked because the evidence violates safety policy.",
    }[verdict]

    st.markdown(f"""
    <div class="decision {decision_class}">
        <div class="decision-label">RUNTIME AUTHORIZATION</div>
        <h1>{icon} {verdict}</h1>
        <div class="decision-text">{explanation}</div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title" style="margin-top:0">Why the Gate Fired</div>', unsafe_allow_html=True)

    for reason in reasons:
        st.markdown(
            f'<div class="reason">• {reason}</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="evidence" style="margin-top:13px">
            <div class="metric-label">EVIDENCE ID</div>
            <div class="hash">{evidence_hash}</div>
            <div class="metric-note">SHA-256 hash of the decision packet</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# GATE EVALUATION
# ------------------------------------------------------------
st.markdown('<div class="section-title">Gate Evaluation</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">The action is evaluated against explicit, inspectable policy rather than an opaque confidence score.</div>',
    unsafe_allow_html=True
)

rows = [
    [
        "Perception confidence",
        f"{x['conf']:.2f}",
        "≥ 0.82",
        "PASS" if x["conf"] >= .82 else "FAIL"
    ],
    [
        "Scene freshness",
        f"{x['age']:.2f}s",
        "≤ 2.00s",
        "PASS" if x["age"] <= 2 else "FAIL"
    ],
    [
        "Path clearance",
        f"{x['clearance']:.2f}m",
        "≥ 0.25m",
        "PASS" if x["clearance"] >= .25 and not x["obstacle"] else "FAIL"
    ],
    [
        "Scene drift",
        f"{x['drift']:.2f}",
        "≤ 0.30",
        "PASS" if x["drift"] <= .30 else "FAIL"
    ],
    [
        "Keep-out zone",
        "CLEAR" if not x["keepout"] else "VIOLATED",
        "CLEAR",
        "PASS" if not x["keepout"] else "FAIL"
    ],
    [
        "Operator override",
        "NONE" if not x["operator"] else "STOP",
        "NONE",
        "PASS" if not x["operator"] else "FAIL"
    ],
]

df = pd.DataFrame(
    rows,
    columns=["Gate", "Observed", "Policy", "Result"]
)

st.dataframe(
    df,
    hide_index=True,
    use_container_width=True,
    height=270,
)

# ------------------------------------------------------------
# PIPELINE
# ------------------------------------------------------------
st.markdown('<div class="section-title">Runtime Pipeline</div>', unsafe_allow_html=True)

pipeline = [
    ("01", "PERCEIVE", "Capture model perception and scene telemetry."),
    ("02", "VERIFY", "Check confidence and temporal freshness."),
    ("03", "GEOMETRY", "Evaluate clearance, obstacles and keep-out zones."),
    ("04", "REASON", "Apply deterministic runtime safety policy."),
    ("05", "AUTHORIZE", "Emit PROMOTE, ROLLBACK or REJECT."),
    ("06", "AUDIT", "Create a hash-linked evidence packet."),
]

pcols = st.columns(6)

for col, (num, name, desc) in zip(pcols, pipeline):
    col.markdown(f"""
    <div class="arch-card">
        <div class="arch-number">{num}</div>
        <div class="arch-name">{name}</div>
        <div class="arch-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# SCENARIO REPLAY
# ------------------------------------------------------------
st.markdown('<div class="section-title">Safety Scenario Matrix</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">One interface, multiple failure modes — useful for a live judge demonstration.</div>',
    unsafe_allow_html=True
)

scenario_cols = st.columns(5)

for col, scenario_name in zip(scenario_cols, SCENARIOS):
    v, r = decide(SCENARIOS[scenario_name])

    label = {
        "PROMOTE": "SAFE TO ACT",
        "ROLLBACK": "RE-EVALUATE",
        "REJECT": "BLOCKED",
    }[v]

    col.markdown(f"""
    <div class="arch-card">
        <div class="arch-number">{v}</div>
        <div class="arch-name">{scenario_name}</div>
        <div class="arch-desc">{label}<br>{r[0]}</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# EVIDENCE PACKET
# ------------------------------------------------------------
st.markdown('<div class="section-title">Evidence Ledger</div>', unsafe_allow_html=True)

evidence = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "team": "Shunya Code",
    "system": "EdgeGate",
    "scenario": scenario,
    "verdict": verdict,
    "reasons": reasons,
    "runtime": "OpenVINO / CPU",
    "openvino_risk": round(risk, 4),
    "inference_ms": round(inference_ms, 3),
    "evidence_id": evidence_hash,
}

ev_left, ev_right = st.columns([1.4, .6])

with ev_left:
    st.code(
        json.dumps(evidence, indent=2),
        language="json"
    )

with ev_right:
    st.markdown("""
    <div class="evidence">
        <div class="metric-label">AUDITABLE OUTPUT</div>
        <div style="font-family:'Space Grotesk';font-size:1.25rem;font-weight:700;margin-top:8px">
            Decision → Evidence
        </div>
        <div class="arch-desc">
            Every decision produces a deterministic,
            downloadable evidence packet containing
            telemetry, policy result and runtime metadata.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        "Download evidence packet",
        json.dumps(evidence, indent=2),
        f"edgegate-{evidence_hash}.json",
        "application/json",
        use_container_width=True,
    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;color:#62718a;font-size:.68rem">
    <span>EDGEGATE · SHUNYA CODE · PHYSICAL AI INFRASTRUCTURE</span>
    <span>Perception proposes. EdgeGate decides.</span>
</div>
""", unsafe_allow_html=True)
