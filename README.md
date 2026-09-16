# EdgeGate — Evidence-Gated Physical AI Runtime

**Team Shunya Code**

EdgeGate is a fail-safe runtime authorization layer
for Physical AI.

Instead of allowing a vision/VLA model to directly
trigger an action, EdgeGate evaluates:

- perception confidence
- scene freshness
- scene drift
- dynamic-obstacle clearance
- keep-out zones
- operator override

before emitting:

**PROMOTE / ROLLBACK / REJECT**

## Core insight

A high-confidence model can still be unsafe when its
observation is stale or the physical environment has
changed.

EdgeGate makes the action decision a separate,
inspectable infrastructure layer.

## Pipeline

Perception
→ Temporal/Geometry Checks
→ Runtime Policy Gate
→ Action Authorization
→ Evidence Ledger

## OpenVINO

edge/openvino_probe.py compiles and executes a
deterministic graph on Intel OpenVINO CPU and records
device availability and inference latency.

## Run

source .venv/bin/activate

python edge/openvino_probe.py

streamlit run app.py

## License

MIT
