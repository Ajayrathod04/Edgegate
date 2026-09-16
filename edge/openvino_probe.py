import json
import time
import numpy as np
import openvino as ov

core = ov.Core()

x = ov.opset13.parameter(
    [1, 6],
    ov.Type.f32,
    name="scene_features"
)

w = ov.opset13.constant(
    np.array(
        [[1.1], [0.9], [1.2], [1.0], [0.8], [1.0]],
        dtype=np.float32
    )
)

b = ov.opset13.constant(
    np.array([[-2.7]], dtype=np.float32)
)

y = ov.opset13.matmul(x, w, False, False)
y = ov.opset13.add(y, b)
y = ov.opset13.sigmoid(y)

model = ov.Model([y], [x], "edgegate_risk")

compiled = core.compile_model(model, "CPU")
request = compiled.create_infer_request()

sample = np.array(
    [[0.94, 0.18, 0.62, 0.0, 0.0, 0.04]],
    dtype=np.float32
)

start = time.perf_counter()

output = request.infer({
    "scene_features": sample
})

latency_ms = (time.perf_counter() - start) * 1000

risk = float(
    next(iter(output.values())).reshape(-1)[0]
)

result = {
    "openvino": ov.__version__,
    "devices": core.available_devices,
    "cpu_available": "CPU" in core.available_devices,
    "compiled_target": "CPU",
    "inference_ms": round(latency_ms, 3),
    "risk_score": round(risk, 4),
    "status": "PASS" if "CPU" in core.available_devices else "FAIL",
}

print(json.dumps(result, indent=2))
