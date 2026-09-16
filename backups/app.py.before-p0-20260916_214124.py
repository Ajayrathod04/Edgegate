import json, hashlib, time
from datetime import datetime, timezone
import streamlit as st

st.set_page_config(page_title="EdgeGate | Shunya Code", page_icon="◈", layout="wide")

SCENARIOS = {
    "Nominal / Fresh Scene": dict(action="Navigate to target", confidence=.96, age=.4, clearance=.82, drift=.08, obstacle=False, keepout=False, estop=False),
    "Stale Scene / Drift": dict(action="Navigate to target", confidence=.94, age=3.8, clearance=.71, drift=.47, obstacle=False, keepout=False, estop=False),
    "Dynamic Obstacle": dict(action="Move through corridor", confidence=.97, age=.5, clearance=.19, drift=.09, obstacle=True, keepout=False, estop=False),
    "Keep-out Zone Violation": dict(action="Enter restricted zone", confidence=.98, age=.3, clearance=.76, drift=.06, obstacle=False, keepout=True, estop=False),
    "Operator Emergency Stop": dict(action="Continue motion", confidence=.99, age=.2, clearance=.91, drift=.04, obstacle=False, keepout=False, estop=True),
    "Bimanual / Shared-Object Conflict": dict(action="Dual-arm handoff", confidence=.97, age=.4, clearance=.48, drift=.07, obstacle=False, keepout=False, estop=False, shared_conflict=True),
}

def decide(x):
    gates = {
        "Confidence ≥ 0.82": x["confidence"] >= .82,
        "Freshness ≤ 2.0s": x["age"] <= 2,
        "Clearance ≥ 0.25m": x["clearance"] >= .25,
        "Drift ≤ 0.30": x["drift"] <= .30,
        "Dynamic obstacle clear": not x["obstacle"],
        "Keep-out zone clear": not x["keepout"],
        "Emergency stop inactive": not x["estop"],
        "Shared-object conflict clear": not x.get("shared_conflict", False),
    }
    reasons=[]
    if x["estop"]: reasons.append("Operator emergency stop is active.")
    if x["obstacle"]: reasons.append("Dynamic obstacle detected in planned path.")
    if x["keepout"]: reasons.append("Trajectory intersects keep-out zone.")
    if x.get("shared_conflict", False): reasons.append("Bimanual/shared-object conflict detected; coordinated action is blocked.")
    if x["age"] > 2: reasons.append(f"Scene is stale: {x['age']:.1f}s > 2.0s.")
    if x["drift"] > .30: reasons.append(f"Scene drift is {x['drift']:.2f} > 0.30.")
    if x["clearance"] < .25: reasons.append(f"Clearance is {x['clearance']:.2f}m < 0.25m.")
    if x["confidence"] < .82: reasons.append("Perception confidence is below policy.")
    hard = x["estop"] or x["obstacle"] or x["keepout"] or x.get("shared_conflict", False)
    soft = x["age"] > 2 or x["drift"] > .30 or x["clearance"] < .25 or x["confidence"] < .82
    decision = "REJECT" if hard else ("ROLLBACK" if soft else "PROMOTE")
    if not reasons: reasons=["All runtime gates passed."]
    return decision, gates, reasons

@st.cache_resource
def openvino_status():
    try:
        import openvino as ov
        import numpy as np
        core=ov.Core()
        devices=core.available_devices
        x=ov.opset13.parameter([1,2],ov.Type.f32)
        y=ov.opset13.multiply(x,ov.opset13.constant(np.array([[1.0,1.0]],dtype=np.float32)))
        model=ov.Model([y],[x],"edgegate_probe")
        compiled=core.compile_model(model,"CPU")
        req=compiled.create_infer_request()
        t=time.perf_counter()
        req.infer({"Parameter_1":np.array([[.5,.5]],dtype=np.float32)})
        ms=(time.perf_counter()-t)*1000
        return True, ov.__version__, devices, ms
    except Exception as e:
        return False, str(e), [], 0

ok, ov_version, devices, latency = openvino_status()

st.markdown("""
<style>
.stApp{background:#070a10;color:#edf4ff}
.block-container{max-width:1500px;padding-top:1.5rem}
[data-testid="stSidebar"]{background:#080c13}
.hero{padding:30px;border:1px solid #26384d;border-radius:24px;background:#0d1520;box-shadow:0 20px 60px #0008}
.kicker{color:#62e6ff;font-size:.72rem;font-weight:800;letter-spacing:.2em}
h1{letter-spacing:-.05em}
.sub{color:#9eafc4;font-size:1.05rem;max-width:900px}
.card{background:#0d141e;border:1px solid #213044;border-radius:18px;padding:20px;height:100%}
.metric{font-size:1.55rem;font-weight:800}
.label{color:#8294ab;font-size:.68rem;letter-spacing:.12em}
.decision{padding:35px;border-radius:22px;text-align:center;border:1px solid #2c4056;background:#101923}
.promote{border-color:#35c98b}.rollback{border-color:#e8ae55}.reject{border-color:#ef6670}
.decision h1{font-size:3.3rem;margin:8px 0}
.good{color:#61e6a8}.warn{color:#f4c36b}.bad{color:#ff737d}
.pill{display:inline-block;border:1px solid #29435a;border-radius:99px;padding:6px 11px;margin:4px;color:#a9bfd3;font-size:.68rem}
 .stage{padding:14px;border:1px solid #213044;border-radius:14px;background:#0b1119;text-align:center}
.flow{display:flex;align-items:stretch;gap:10px;margin:18px 0 22px}
.flowbox{flex:1;padding:18px 14px;border:1px solid #26384d;border-radius:16px;background:linear-gradient(180deg,#101b28,#0b1119);text-align:center}
.flowbox .num{font-size:.65rem;letter-spacing:.16em;color:#62e6ff;font-weight:800}
.flowbox .title{font-size:1rem;font-weight:800;margin-top:7px}
.flowbox .desc{font-size:.72rem;color:#8294ab;margin-top:5px}
.flowarrow{display:flex;align-items:center;color:#62e6ff;font-size:1.4rem;font-weight:900}
.proof{padding:17px;border:1px solid #26384d;border-radius:16px;background:#0c141e}
.proof .value{font-size:1.7rem;font-weight:900}
.proof .label{margin-top:4px}
.verdict{padding:16px 18px;border-radius:16px;border:1px solid #35c98b;background:#0b1714}
@media(max-width:900px){.flow{flex-direction:column}.flowarrow{justify-content:center;transform:rotate(90deg)}}
</style>
""", unsafe_allow_html=True)

scenario=st.sidebar.selectbox(
    "REPLAY SAFETY SCENARIO",
    list(SCENARIOS),
    index=list(SCENARIOS).index("Bimanual / Shared-Object Conflict")
)
x=SCENARIOS[scenario]
decision,gates,reasons=decide(x)

evidence={
    "evidence_id": "",
    "timestamp":datetime.now(timezone.utc).isoformat(),
    "scenario":scenario,
    "proposed_action":x["action"],
    "policy_version":"EDGEGATE-1.0",
    "gates":gates,
    "reasons":reasons,
    "decision":decision,
    "runtime":"OpenVINO / CPU" if ok else "OpenVINO unavailable",
    "openvino_version":ov_version,
    "device":devices,
    "inference_ms":round(latency,3),
}
evidence["evidence_id"]=hashlib.sha256(json.dumps(evidence,sort_keys=True).encode()).hexdigest()[:16]

st.markdown("""
<div class="hero">
<div class="kicker">SHUNYA CODE · PHYSICAL AI INFRASTRUCTURE</div>
<h1 style="font-size:3.4rem;margin:8px 0">EdgeGate</h1>
<div class="sub">Evidence-Gated Runtime Authorization for Physical AI.<br>
Perception proposes. <b>EdgeGate decides.</b></div>
<br>
<span class="pill">LOCAL-FIRST</span><span class="pill">OPENVINO EDGE</span>
<span class="pill">DETERMINISTIC POLICY</span><span class="pill">AUDITABLE</span>
</div>
""",unsafe_allow_html=True)

st.write("")
a,b,c,d,e=st.columns(5)
for col,label,value in [
    (a,"PERCEPTION",f"{x['confidence']*100:.0f}%"),
    (b,"SCENE AGE",f"{x['age']:.1f}s"),
    (c,"CLEARANCE",f"{x['clearance']:.2f}m"),
    (d,"DRIFT",f"{x['drift']*100:.0f}%"),
    (e,"EDGE LATENCY",f"{latency:.1f}ms" if ok else "N/A")]:
    col.markdown(f'<div class="card"><div class="label">{label}</div><div class="metric">{value}</div></div>',unsafe_allow_html=True)

st.markdown(
    f'<div class="card" style="padding:12px 16px;margin-bottom:14px">'
    f'<span class="good">● OPENVINO READY</span>&nbsp;&nbsp; '
    f'<b>{ov_version}</b>&nbsp;&nbsp; '
    f'DEVICE: <b>{"CPU" if ok else "UNAVAILABLE"}</b>&nbsp;&nbsp; '
    f'EDGE INFERENCE: <b>{latency:.2f} ms</b>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="
padding:16px 20px;
margin:12px 0 18px 0;
border:1px solid #26384d;
border-radius:16px;
background:linear-gradient(90deg,#0d1722,#101d2b);
">
<div style="font-size:0.68rem;letter-spacing:.16em;color:#62e6ff;font-weight:800">
PHYSICAL AI RUNTIME
</div>
<div style="font-size:1.45rem;font-weight:900;margin-top:5px">
AI proposes. Evidence decides.
</div>
<div style="font-size:.82rem;color:#91a3b8;margin-top:6px">
Physical-AI proposal → OpenVINO edge path → evidence verification → runtime authorization
</div>
</div>
""", unsafe_allow_html=True)

st.write("")
left,right=st.columns([1.25,1])

with left:
    cls={"PROMOTE":"promote","ROLLBACK":"rollback","REJECT":"reject"}[decision]
    txt={"PROMOTE":"good","ROLLBACK":"warn","REJECT":"bad"}[decision]
    icon={"PROMOTE":"✓","ROLLBACK":"↩","REJECT":"×"}[decision]
    st.markdown(f"""
    <div class="decision {cls}">
    <div class="label">RUNTIME AUTHORIZATION</div>
    <h1 class="{txt}">{icon} {decision}</h1>
    <div class="sub" style="margin:auto">The action is authorized only after independent runtime evidence passes policy.</div>
    </div>
    """,unsafe_allow_html=True)

    st.write("")
    st.markdown("### Runtime Gate Matrix")
    for name,p in gates.items():
        icon="PASS" if p else "BLOCK"
        color="good" if p else "bad"
        st.markdown(f'<div class="card" style="margin:7px 0;padding:13px"><b>{name}</b><span class="{color}" style="float:right;font-weight:800">{icon}</span></div>',unsafe_allow_html=True)

with right:
    st.markdown('<div class="card"><div class="label">PERCEPTION PROPOSAL</div><h2>'+x["action"]+'</h2><p class="sub">'+scenario+'</p><hr>',unsafe_allow_html=True)
    for k,v in [("Confidence",f"{x['confidence']:.2f}"),("Scene age",f"{x['age']:.2f}s"),("Clearance",f"{x['clearance']:.2f}m"),("Drift",f"{x['drift']:.2f}")]:
        st.write(f"**{k}**  `{v}`")
    st.markdown("</div>",unsafe_allow_html=True)

st.write("")
st.markdown("### Why EdgeGate decided this way")
for r in reasons:
    st.write(("✓ " if decision=="PROMOTE" else "• ")+r)

st.markdown("### Decision Pipeline")
p=st.columns(6)
for col,label in zip(p,["PERCEIVE","VALIDATE","GEOMETRY","POLICY","AUTHORIZE","AUDIT"]):
    col.markdown(f'<div class="stage"><b>{label}</b></div>',unsafe_allow_html=True)

st.write("")
l,r=st.columns([1,1])
with l:
    st.markdown("### Evidence Ledger")
    st.code(json.dumps(evidence,indent=2),language="json")
with r:
    st.markdown("### Replay Safety Matrix")
    for name,data in SCENARIOS.items():
        v,_,rr=decide(data)
        st.write(f"**{name}** → `{v}`")
    st.download_button("Download Evidence Packet",json.dumps(evidence,indent=2),f"edgegate-{evidence['evidence_id']}.json","application/json",use_container_width=True)

st.divider()
st.caption("Hackathon prototype. Synthetic scene telemetry is used for deterministic policy demonstration; OpenVINO provides the local CPU edge inference path. This prototype does not directly control a physical robot or represent a safety certification.")
