# EdgeGate

## Title

**EdgeGate — Evidence-Gated Runtime for Physical AI**

## Tagline

**AI proposes. Evidence decides.**

## One-Line Idea

EdgeGate is a lightweight edge runtime layer that evaluates candidate Physical-AI actions against perception, temporal, geometry, policy, and execution-safety evidence before authorizing execution.

---

## Problem

Modern Physical-AI systems can generate sophisticated actions from vision, language, and multimodal models, but a strong model proposal does not automatically mean that an action is safe to execute.

In a physical environment, the scene can change after perception, objects can move, sensor information can become stale, clearances can shrink, and multiple actions can conflict. A model may therefore propose an action that was reasonable when generated but is no longer valid when execution is about to happen.

EdgeGate addresses this runtime gap.

Instead of treating an AI-generated action as automatically executable, EdgeGate places an evidence-gated authorization layer between the AI proposal and the physical execution layer.

The central principle is:

> AI proposes. Evidence decides.

---

## Solution

EdgeGate receives a candidate Physical-AI action together with synthetic scene telemetry and evaluates whether the available evidence is sufficient for authorization.

The runtime evaluates deterministic safety gates including:

- Scene grounding
- Perception confidence
- Scene freshness / temporal consistency
- Geometry and clearance
- Policy compliance
- Execution safety

The result is an explicit runtime decision:

- **PROMOTE** — evidence satisfies the required gates and the action can proceed in the prototype.
- **ROLLBACK** — the action should be withdrawn because the runtime state is no longer consistent with the proposed action.
- **REJECT** — evidence is insufficient or a safety constraint fails, so the action is not authorized.

Every decision can be represented as an evidence packet so that the decision is explainable and reproducible rather than being a black-box yes/no response.

---

## What EdgeGate Solves

EdgeGate is designed to address a practical Physical-AI deployment problem:

**How do we prevent a valid-looking AI action from being executed when the physical state has changed or the evidence supporting that action is no longer sufficient?**

Examples demonstrated by the prototype include:

1. Scene drift / stale state
2. Dynamic obstacle / keep-out violation
3. Evidence or confidence failure
4. Unsafe candidate action
5. Bimanual/shared-object conflicts in the safety simulation

The prototype fails closed when required evidence is not available.

---

## Core Workflow

```text
AI / VLA Candidate Action
          |
          v
      PERCEIVE
          |
          v
       VALIDATE
          |
          v
       GEOMETRY
          |
          v
         POLICY
          |
          v
       AUTHORIZE
          |
          v
         AUDIT
          |
          v
   PROMOTE / ROLLBACK / REJECT
```

The runtime therefore separates:

**what the AI proposes**

from

**what the environment provides evidence for**

and finally

**what the runtime authorizes**.

---

## Architecture

```text
+-----------------------------+
|   Physical-AI / VLA Model   |
|     Candidate Action        |
+--------------+--------------+
               |
               v
+-----------------------------+
|       EdgeGate Runtime      |
|                             |
|  Scene Grounding            |
|  Temporal Consistency       |
|  Geometry / Clearance       |
|  Policy Compliance          |
|  Execution Safety           |
+--------------+--------------+
               |
               v
+-----------------------------+
|     Decision Authority      |
|                             |
| PROMOTE | ROLLBACK | REJECT |
+--------------+--------------+
               |
               v
+-----------------------------+
|       Evidence Ledger       |
|  Decision + Reasons + Data  |
+--------------+--------------+
               |
               v
+-----------------------------+
|     Physical Execution      |
|       Authorization         |
+-----------------------------+
```

---

## Edge Inference Path

EdgeGate includes an OpenVINO capability/inference probe for the local edge environment.

The verified local probe demonstrated:

```text
OpenVINO: 2026.4.0
Available device: CPU
Compiled target: CPU
Measured inference: ~15.859 ms
Probe status: PASS
```

The measurement is a local prototype measurement and is presented as such. It is not claimed as a universal benchmark for all Intel hardware.

OpenVINO provides the edge inference path used by the prototype.

---

## Technology Stack

### Application

- Python
- Streamlit

### Edge AI

- OpenVINO
- CPU edge inference
- OpenVINO Runtime / Core device discovery

### Runtime Logic

- Deterministic evidence gates
- Scene-state validation
- Geometry / clearance checks
- Temporal freshness checks
- Policy decision engine
- Evidence ledger

### Development

- Ubuntu / WSL
- Python virtual environment
- Git
- GitHub

### Deployment

- Streamlit Community Cloud

---

## Why EdgeGate Is Different

Many Physical-AI systems focus on generating an action.

EdgeGate focuses on the question that comes immediately after generation:

**Should this action still be authorized right now?**

This creates a complementary architecture:

```text
Multimodal AI
     |
     | proposes
     v
+------------+
|  EdgeGate  |
|   Runtime  |
+------------+
     |
     | authorizes only when evidence passes
     v
Physical Execution
```

EdgeGate does not claim to replace a VLA or robotics policy model. It provides a runtime evidence and authorization layer around candidate actions.

---

## Demonstration

The intended demonstration is deliberately short and deterministic.

### Scenario A — Safe Action

Run the safe scenario.

Expected flow:

```text
Scene grounded       PASS
Geometry             PASS
Temporal consistency PASS
Policy               PASS
Execution safety     PASS

FINAL DECISION
PROMOTE
```

The UI explains why the action was authorized and exposes the supporting evidence.

### Scenario B — Failure Injection

Inject a runtime failure such as stale scene information, a dynamic obstacle, insufficient clearance, or an incompatible bimanual/shared-object condition.

Expected flow:

```text
Required evidence fails

FINAL DECISION
REJECT
```

The key behavior is that EdgeGate does not silently continue when the evidence no longer supports execution.

### Scenario C — Rollback

When an already proposed action becomes inconsistent with the updated runtime state, the prototype can demonstrate:

```text
Previous proposal
       |
       v
Runtime state changed
       |
       v
Evidence invalidated
       |
       v
ROLLBACK
```

---

## Output

For every evaluated scenario, EdgeGate produces a decision and human-readable reasons.

Example conceptual output:

```text
DECISION: REJECT

Failed gates:
- Temporal consistency
- Dynamic obstacle / clearance

Reason:
The candidate action was generated from an earlier scene state,
but the current evidence no longer supports safe authorization.

Action:
DO NOT EXECUTE

Evidence:
Recorded for replay and audit.
```

For a successful case:

```text
DECISION: PROMOTE

All required evidence gates passed.

Action:
AUTHORIZED FOR PROTOTYPE EXECUTION

Evidence:
Recorded for reproducibility.
```

---

## Evidence Ledger

EdgeGate records structured decision evidence containing information such as:

- Evidence ID
- Scenario
- Candidate action
- Decision
- Confidence
- Scene age
- Clearance
- Drift
- Gate results
- Decision reasons

The prototype also provides an evidence-packet download capability.

This makes the runtime decision inspectable instead of presenting only a final status indicator.

---

## Replay Safety

The prototype includes deterministic replay scenarios for demonstrating how the policy behaves under changing runtime conditions.

The safety matrix can be used to compare scenarios such as:

```text
Safe scene             -> PROMOTE
Scene drift             -> ROLLBACK / REJECT
Dynamic obstacle       -> REJECT
Unsafe geometry        -> REJECT
Evidence failure       -> REJECT
```

The exact result is determined by the policy logic implemented in the application.

---

## UI

The Streamlit interface is designed as a Physical-AI runtime control room.

The main interface exposes:

- Current runtime status
- Candidate perception proposal
- Decision status
- Evidence gates
- Decision pipeline
- OpenVINO edge inference information
- Evidence ledger
- Replay safety matrix
- Evidence packet download

The goal is to make the release decision visible immediately:

```text
PROMOTE
ROLLBACK
REJECT
```

---

## Simplifying the Concept

The complete EdgeGate idea can be reduced to one sentence:

> **A Physical-AI model can propose an action, but EdgeGate requires current evidence before that action is authorized.**

Or even more simply:

```text
MODEL PROPOSES
      +
CURRENT EVIDENCE
      |
      v
EDGEGATE
      |
      v
AUTHORIZE / BLOCK
```

---

## Benefits

### Safety-oriented runtime behavior

Actions can be blocked when required runtime evidence fails.

### Edge-first execution

OpenVINO provides a local inference path instead of requiring every inference step to depend on a remote service.

### Explainability

The system exposes the gates and reasons behind a decision.

### Reproducibility

Deterministic scenarios make runtime behavior easy to demonstrate and replay.

### Auditability

Evidence packets provide a structured record of why a candidate action was promoted, rolled back, or rejected.

### Modularity

EdgeGate can sit between different AI/robotics policy systems and the execution layer without requiring the policy model itself to be replaced.

---

## Published Project URLs

### Live Demo

https://edgegate-c6ahozdyvpdei5nzxcim55.streamlit.app/

### GitHub

https://github.com/Ajayrathod04/Edgegate

### Project / Hackathon

https://lablab.ai/ai-hackathons/ai-infra-summit-hackathon

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Ajayrathod04/Edgegate.git
cd Edgegate
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the application dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run EdgeGate:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Running the OpenVINO Probe

Activate the environment:

```bash
source .venv/bin/activate
```

Install edge dependencies:

```bash
python3 -m pip install -r requirements-edge.txt
```

Run:

```bash
python3 edge/openvino_probe.py
```

The probe reports the OpenVINO version, available devices, target device, inference timing, risk score, and status.

---

## Repository Structure

```text
Edgegate/
├── app.py
├── app.backup.185325.py
├── core/
│   └── __init__.py
├── edge/
│   ├── __init__.py
│   └── openvino_probe.py
├── openvino_probe.json
├── requirements.txt
├── requirements-edge.txt
├── .streamlit/
│   └── config.toml
├── .gitignore
├── LICENSE
└── README.md
```

---

## Hackathon Positioning

EdgeGate is positioned as an infrastructure/runtime component for Physical AI.

Rather than competing only on model generation, it addresses the deployment boundary where an AI proposal becomes a physical action.

The architecture is intentionally model-agnostic:

```text
Vision / Language / VLA / AI Policy
                |
                v
       Candidate Action
                |
                v
          EDGEGATE
                |
        +-------+-------+
        | Evidence      |
        | Runtime       |
        | Policy        |
        +-------+-------+
                |
                v
       Execution Decision
                |
       +--------+--------+
       |        |        |
    PROMOTE  ROLLBACK  REJECT
```

---

## Limitations

This is a hackathon prototype.

- Scene telemetry used by the deterministic demonstrations is synthetic.
- The prototype does not directly control a physical robot.
- The OpenVINO measurement is an environment-specific local measurement.
- The prototype is not a safety certification or production robotics safety system.
- Physical deployment would require additional hardware validation, sensor validation, control integration, testing, and appropriate safety certification.

---

## Future Work

Potential extensions include:

- Integration with real robot controllers
- Real camera and depth-sensor feeds
- Core Ultra / NPU benchmarking on supported hardware
- Integration with VLA policy models
- Robot simulation environments
- Formal policy specifications
- Cryptographically signed evidence packets
- Distributed evidence verification
- Hardware-aware runtime scheduling
- Continuous post-execution verification

---

## Team

**Team Shunya Code**

Built for the AI Infra Summit Hackathon.

---

## License

MIT License
