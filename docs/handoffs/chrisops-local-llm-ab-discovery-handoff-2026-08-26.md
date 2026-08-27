# ChrisOps Local LLM A/B Discovery Handoff

## Objective

Identify the best realistic local model/runtime candidate to test against the
existing `chrisops-grounded-qwen3-8b` control on the Intel Arc Pro A60 in
`ai-lab`.

This is a read-only discovery result. No model, runtime, service, firewall,
Open WebUI object, RAG setting, repository deployment, or production state was
changed. No inference request was submitted during discovery.

The recommendation is optimized for:

1. factual quality when supplied with fixed RAG evidence;
2. infrastructure and system-administration reasoning;
3. correct separation of current, historical, configured, and unknown state;
4. evidence fidelity and explicit treatment of missing facts;
5. resistance to distractors and incomplete retrieval;
6. operational instruction following;
7. acceptable latency and throughput; and
8. realistic operation on the existing 12 GB-class A60.

## Authoritative Sources

- Gitea `aeons/homelab-ops` is authoritative for infrastructure intent,
  desired state, Ansible automation, deployment configuration, and
  infrastructure procedures.
- Gitea `aeons/chrisops` is authoritative for ChrisOps product source, runtime
  state, APIs, collectors, contracts, tests, and application behavior.
- Gitea `aeons/chrisops-assistant` is authoritative for assistant reasoning,
  provider contracts, evaluation, and model-integration behavior.
- Current bounded command output from `ai-lab` is authoritative for directly
  observed runtime state.
- Model authors and runtime maintainers are authoritative for model cards,
  supported architectures, generation semantics, and published artifacts.
- GitHub mirrors are one-way disaster-recovery copies.
- Open WebUI Knowledge is a derived RAG index, not an authority.

Primary upstream sources used:

- [Qwen3.5-9B model card](https://huggingface.co/Qwen/Qwen3.5-9B)
- [Official OpenVINO Qwen3.5-9B INT4 artifact](https://huggingface.co/OpenVINO/Qwen3.5-9B-int4-ov)
- [OpenVINO 2026 release notes](https://docs.openvino.ai/2026/about-openvino/release-notes-openvino.html)
- [OpenVINO GenAI supported-model notes](https://github.com/openvinotoolkit/openvino.genai/blob/master/site/docs/supported-models/index.mdx)
- [OpenVINO GenAI Qwen3.5 `VLMPipeline` issue 4222](https://github.com/openvinotoolkit/openvino.genai/issues/4222)
- [Granite 4.2 8B model card](https://huggingface.co/ibm-granite/granite-4.2-8b)
- [Official Granite 4.2 8B GGUF artifacts](https://huggingface.co/ibm-granite/granite-4.2-8b-GGUF)
- [llama.cpp SYCL backend documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/SYCL.md)
- [Ministral 3 8B Instruct model card](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512)
- [Official Ministral 3 8B GGUF artifacts](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-GGUF)
- [Phi-4 model card](https://huggingface.co/microsoft/phi-4)
- [Official OpenVINO Phi-4 INT4 artifact](https://huggingface.co/OpenVINO/phi-4-int4-ov)
- [Qwen3-14B model card](https://huggingface.co/Qwen/Qwen3-14B)
- [Official OpenVINO Qwen3-14B INT4 artifact](https://huggingface.co/OpenVINO/Qwen3-14B-int4-ov)
- [vLLM Intel XPU installation documentation](https://github.com/vllm-project/vllm/blob/main/docs/getting_started/installation/gpu.md)
- [Archived IPEX-LLM repository](https://github.com/intel/ipex-llm)

## Execution Context

| Item | Value |
|---|---|
| Workstation | Arrakis; PowerShell |
| Infrastructure repository | `D:\Aeons\Git\homelab-ops` |
| Evaluation repository | `D:\Aeons\Git\chrisops-assistant` |
| Inspected host | `ai-lab` / `192.168.20.70` |
| Remote account and shell | `aeons`; Bash |
| Runtime working directory | `/home/aeons/ai-lab/src/ov-api` |
| Model root | `/home/aeons/ai-lab/models` |
| OpenVINO environment | `/home/aeons/ai-lab/venvs/openvino` |
| Existing API | `http://192.168.20.70:8000/v1` |
| Discovery date | 2026-08-26 |

## Current Repository State

| Repository | Ownership | Branch | HEAD | Working tree | Gitea readback |
|---|---|---|---|---|---|
| `aeons/homelab-ops` | Infrastructure and deployment | `main` | `cc4485239c3817606de0370c56923e6f86f8bb7e` | Intentionally dirty before discovery; eight unrelated modified/untracked paths | Not refreshed in this packet |
| `aeons/chrisops-assistant` | Reasoning and evaluation | `main` | `d8c0bb4fecdbc8e474b8bdd67c0615d0c0a28f0b` | Pre-existing `.gitignore` modification plus this handoff | Remote lookup blocked because the sandbox did not resolve the configured `gitea-arrakis` alias |

The pre-existing changes were preserved. This handoff is not committed.

The deployed `/home/aeons/ai-lab/src/ov-api/server_multi.py` and the
`homelab-ops` `HEAD` version normalize to the same Git blob:
`14c60eddafbf0e3303dbb63597073322bc52a0d2`.

## Discovery Boundaries

Permitted and performed:

- bounded SSH metadata inspection;
- service status and read-only health/model-list API calls;
- small Hugging Face metadata/config/file-list queries;
- upstream documentation research;
- repository inspection and this handoff.

Not performed:

- generation or model-quality calls;
- model downloads or conversions;
- package installation or upgrade;
- service start, stop, restart, or enablement;
- Open WebUI API or database mutation;
- driver, firewall, container, RAG, or systemd changes;
- repository commit, push, deployment, or production activation.

## Current Known-Good Control

The control remained untouched:

| Item | Current value |
|---|---|
| Open WebUI object | `chrisops-grounded-qwen3-8b` |
| Display name | `ChrisOps Grounded (Qwen3-8B)` |
| Base model | `qwen3-8b-openvino-gpu` |
| Model artifact | `/home/aeons/ai-lab/models/Qwen3-8B-int4-ov` |
| Runtime | OpenVINO `2026.2.1`; OpenVINO GenAI `2026.2.1.0` |
| Device and precision | Intel Arc Pro A60; INT4; `GPU` |
| Thinking | Disabled |
| Temperature / output cap | `0.3` / 512 tokens |
| RAG | Vector-only Top-K 5; no reranker |
| Knowledge collection | `ChrisOps Homelab` |
| Frozen corpus commit | `cc4485239c3817606de0370c56923e6f86f8bb7e` |

Live read-only API results:

- `/health`: `ok`, model `qwen3-8b-openvino-gpu`, device `GPU`, native chat
  enabled, thinking default false, model load 10.007 seconds.
- `/status`: idle, queue depth zero, no current request, 17 completed requests,
  zero failed requests, no last error.
- `/v1/models`: exactly one served model, `qwen3-8b-openvino-gpu`.
- `openvino-api.service`: active/running, PID 1372, zero systemd restarts.
- The two-second DRM engine-counter sample was unchanged, establishing no GPU
  compute/copy/render activity during that interval.

## Verified A60 Host Constraints

### Hardware and operating system

| Constraint | Fresh observation |
|---|---|
| GPU | Intel DG2 Arc Pro A60, PCI `8086:56b3`, subsystem `8086:1010`, guest PCI `0000:01:00.0` |
| Kernel binding | `i915`; `xe` also available as a module |
| Render device | `/dev/dri/renderD128` |
| OpenCL-reported global memory | 12,160,962,560 bytes = 11.33 GiB |
| OpenCL max single allocation | 4,294,959,104 bytes, approximately 4 GiB |
| GPU host-memory model | Discrete; OpenCL reports host/device unified memory false |
| CPU | Eight assigned vCPUs from AMD Ryzen 9 7900X host CPU |
| Guest RAM | 32,861,072 kB total; 30,370,492 kB available at inspection |
| Swap | None documented; not changed or re-evaluated here |
| OS | Ubuntu 24.04.4 LTS |
| Kernel | `6.8.0-138-generic` |
| Root/model filesystem | ext4, 290 GB total, 238 GB available |

The A60 is marketed as a 12 GB card, but feasibility calculations in this
handoff use the observed 11.33 GiB OpenCL allocation domain, not a rounded
marketing number.

### Intel compute stack

| Layer | Observed state |
|---|---|
| OpenVINO device enumeration | `CPU`, `GPU`; GPU name `Intel(R) Graphics [0x56b3] (dGPU)` |
| OpenCL | Available through Intel OpenCL Graphics; device `0x56b3` |
| Intel compute runtime package | `intel-opencl-icd 23.43.27642.40-1ubuntu3` |
| Level Zero loader | `libze_loader.so.1`; package `libze1 1.16.1-1build1` |
| Level Zero GPU runtime | `libze_intel_gpu.so.1`; package `libze-intel-gpu1 23.43.27642.40-1ubuntu3` |
| oneAPI/SYCL toolchain | Not present; no `/opt/intel/oneapi` toolchain and no `sycl-ls` |
| `intel_gpu_top` | Installed but unusable for this passthrough/kernel combination: engine discovery fails |
| Per-process DRM accounting | Engine counters available; VRAM byte accounting absent from PID fdinfo |

Exact live VRAM consumption could not be read without privileged debugfs
access. Non-interactive sudo was unavailable. The truthful idle statement is:
the OpenVINO service had one loaded model and no request or engine activity,
but exact allocated/free VRAM was unavailable from the permitted interfaces.
OpenVINO exposed `GPU_MEMORY_STATISTICS`, but a separate inspection process
reported zero for its own fresh context; that is not system-wide usage and was
not misreported as free VRAM for the already-running service.

### Installed inference components

| Component | Observed state |
|---|---|
| OpenVINO | `2026.2.1` |
| OpenVINO GenAI | `2026.2.1.0` |
| OpenVINO Tokenizers | `2026.2.1.0` |
| Python | 3.12.3 in `/home/aeons/ai-lab/venvs/openvino` |
| Transformers | Not installed in the inference environment |
| Optimum Intel | Not installed |
| PyTorch / Intel Extension for PyTorch | Not installed in the inference environment |
| llama.cpp | No `llama-server` or `llama-cli` installed |
| oneAPI/SYCL | Not installed |
| vLLM | Not installed |
| IPEX-LLM | Not installed; upstream project was archived in January 2026 |
| Ollama | Client `0.32.5` installed; service loaded but inactive/dead; no live model list available |
| Docker inference workloads | Only `open-webui` running; no alternate inference container |

### Existing model storage

| Artifact | Disk size |
|---|---:|
| `Qwen3-8B-int4-ov` | 4.6 GB |
| `Qwen2.5-7B-Instruct-int4-ov` | 4.2 GB |
| `TinyLlama-1.1B-Chat-v1.0-int4-ov` | 611 MB |

The 238 GB free filesystem has ample artifact capacity. VRAM and runtime
compatibility, not disk, are the controlling constraints.

## Current API and Model-Loading Architecture

The deployed API uses `openvino_genai.LLMPipeline` and loads one configured
model synchronously at module import/service start. `OV_MODEL` selects one of
two static configuration entries (`qwen25` or `qwen3`). Requests for any other
model ID return a `model_not_loaded` error.

Consequences:

- Multiple artifact directories already coexist on disk.
- The current service cannot keep multiple registered API model IDs while
  dynamically loading only the selected one.
- It does not expose load, unload, swap, or eviction operations.
- It serializes generation with a process lock.
- Multiple Open WebUI model objects can be registered, but a separate endpoint
  or an explicit service swap is required for a second runtime model.
- Simultaneously loading both Qwen3-8B and Qwen3.5-9B is not credible within
  11.33 GiB once runtime buffers and KV cache are included. Sequential service
  ownership is required.

### OpenAI-compatible requirements for Open WebUI

A clean second integration should provide:

- stable `GET /v1/models` model identity;
- OpenAI-style `POST /v1/chat/completions` with `model`, `messages`, generation
  controls, non-streaming JSON, and streaming SSE;
- explicit 4xx errors for invalid parameters/model identity;
- a chat template that implements the model author's reasoning switch;
- either separate `reasoning_content` or reliable removal of `<think>` content
  from the final answer shown/scored;
- reachability from the Open WebUI container through the Docker host/bridge,
  not `127.0.0.1` inside the container;
- no broader LAN/tailnet exposure; and
- model lifecycle telemetry that distinguishes load time from request TTFT.

## Runtime Assessment

### 1. OpenVINO

OpenVINO remains the preferred runtime for the first candidate.

Strengths:

- already deployed and proven on the exact A60;
- current versions explicitly added Qwen3.5 support;
- Intel publishes an official `OpenVINO/Qwen3.5-9B-int4-ov` artifact compatible
  with OpenVINO 2026.2.0 or later;
- the artifact is 6.13 GB on disk and uses INT4 asymmetric group-128 weights;
- OpenVINO GenAI provides the lowest-change path for Intel GPU residency; and
- model-quality comparison does not require a new GPU programming stack.

Risks:

- Qwen3.5 is a vision-language conditional-generation architecture and needs
  `VLMPipeline`, not the current `LLMPipeline` wrapper.
- The upstream 2026.2.1 issue tracker records a `VLMPipeline` rejection of
  `model_type=qwen3_5`; Intel's artifact card simultaneously states 2026.2+
  compatibility but demonstrates nightly packages. This contradiction must be
  resolved by a bounded text-only smoke test before Open WebUI registration.
- The current wrapper does not implement Qwen3.5's reasoning/template options.
- No quality or performance result has yet been observed on this A60.

Recommendation: use a separate, pinned candidate environment and service. Do
not upgrade or edit the working Qwen control environment.

### 2. llama.cpp with SYCL/Level Zero

llama.cpp is the preferred alternate runtime when a candidate lacks a clean
OpenVINO path.

Strengths:

- official SYCL backend targets Intel Arc and Level Zero;
- OpenAI-compatible `llama-server` is mature and supports partial CPU offload;
- official Granite and Mistral GGUF repositories provide Q4/Q5/Q6 artifacts;
- Granite 4.2's own GGUF page directly documents `llama-server` use; and
- Q4_K_M provides a well-understood quality/size compromise.

Costs and risks:

- no llama.cpp or oneAPI/SYCL toolchain is installed;
- installation adds a new compiler/runtime path and more variables than the
  first A/B needs;
- the available Level Zero runtime is necessary but not sufficient for a SYCL
  build;
- A60 performance is credible by Arc-family support, but not measured on this
  host; and
- Vulkan/Ollama may be convenient but is not preferred as the evidence-bearing
  baseline because the local Ollama service is inactive and its A60 backend has
  not been verified.

Recommendation: keep llama.cpp/SYCL as the deliberate second runtime track,
starting with Granite 4.2-8B if Qwen3.5 does not clearly win.

### 3. Other Intel-capable runtimes

#### vLLM XPU

Current vLLM documentation includes an Intel XPU backend and forthcoming/
release Docker images. It is technically credible, especially for throughput
and OpenAI compatibility. It is not the right first runtime here:

- it is not installed;
- the A60 is a single client Arc device rather than a high-throughput XPU
  serving node;
- Intel quantization support is still evolving; and
- a heavyweight serving stack would confound a single-user model-quality test.

Use vLLM XPU only if later work needs a model/template feature not available in
OpenVINO or llama.cpp, or if measured concurrent throughput becomes important.

#### IPEX-LLM

Reject for new work. Intel archived the upstream repository on 2026-01-28. It
can explain historical Arc/Ollama configurations but is not a maintainable new
evaluation dependency.

#### Ollama

Ollama is installed but inactive. It can consume GGUF models and expose an
OpenAI-compatible surface, but its exact A60 acceleration path is unverified.
Treat it as a convenience wrapper for a later exploratory probe, not the
canonical performance runtime.

## Candidate Research

### Qwen3.5-9B

- Dense 9B language model with a vision encoder; 9.653B published parameters in
  the Hugging Face metadata.
- Hybrid layout: 32 layers with three linear-attention layers followed by one
  full-attention layer per block.
- Native context: 262,144 tokens, extensible farther; initial A60 testing must
  be capped far below that.
- Thinking is on by default. Non-thinking requires chat-template
  `enable_thinking=false`; `/nothink` is not the supported switch.
- Tool/agent support is a first-class training/evaluation target.
- Apache 2.0.
- Official OpenVINO INT4 artifact: 6.13 GB.
- Published language results include MMLU-Pro 82.5, IFEval 91.5, IFBench 64.5,
  BFCL-v4 66.1, and TAU2-Bench 79.1. These are author-reported and not a direct
  ChrisOps comparison.
- Expected A60 footprint at an 8K initial context: approximately 7-9 GiB
  including artifact, recurrent/attention state, runtime buffers, and margin.
  This is an engineering estimate, not an observed allocation.
- Full GPU residency is realistic at 8K; CPU offload should not be required.
- Major unknown: stable text-only `VLMPipeline` operation on the installed
  2026.2.1 packages and correct reasoning separation.

### Granite 4.2 family

IBM released dense Granite 4.2 models at 3B, 8B, and 30B parameters under
Apache 2.0. All have 131,072-token native context and thinking, non-thinking,
and low-effort modes. Granite's model card specifies `temperature=1.0`,
`top_p=0.95`, and sampling for all modes.

Official GGUF availability is unusually strong: IBM publishes Q2_K through
Q8_0 plus BF16 for each size.

#### Granite 4.2-3B

- Official Q4_K_M: 2.244 GB; Q6_K: 3.006 GB.
- Easy full residency with long headroom.
- Author-reported 3B results are strong for its size, but there is no credible
  reason yet to expect a 3B model to beat the existing Qwen3-8B on nuanced
  infrastructure evidence and distractor resistance.
- Reject as an A/B priority. It is a latency/efficiency candidate, not a likely
  quality winner.

#### Granite 4.2-8B

- 8.792B parameters; 40 layers, 32 attention heads, 8 KV heads.
- Official Q4_K_M GGUF: 5.348 GB; Q5_K_M: 6.254 GB; Q6_K: 7.216 GB.
- Estimated Q4_K_M A60 footprint at 8K context: approximately 7-8.5 GiB. Full
  GPU residency is realistic.
- IBM reports strong instruction following, reasoning, code, terminal, and
  agentic results, including IFBench 79.33 and Terminal-Bench 2.1 20.56.
- llama.cpp recognizes the official artifact and chat template.
- Optimum Intel 1.27 reports Granite-4 export support, so an OpenVINO conversion
  is plausible. No official Granite 4.2 OpenVINO artifact was found, and the
  installed host lacks Optimum Intel/Transformers; conversion is therefore
  unverified rather than cleanly supported.
- For the first controlled Granite comparison use non-thinking mode. Low-effort
  is the next diagnostic if non-thinking is close. Full thinking changes
  latency, token budget, and answer style too much for the first isolated test.

#### Granite 4.2-30B

- 29.277B parameters; 64 layers.
- Official Q2_K is 10.859 GB and Q4_K_M is 17.721 GB.
- Even Q2_K consumes almost the entire observed 11.33 GiB before KV cache and
  runtime buffers. Useful Q4/Q5 quantizations require substantial CPU offload.
- The guest has enough RAM to start a partially offloaded model, but PCIe/CPU
  traffic would likely make it a slow, runtime-confounded comparison.
- Reject for this A60. Technical start-up is not sufficient evidence of useful
  interactive operation.

### Ministral 3 8B Instruct 2512

- 8.4B language model plus approximately 0.4B vision encoder; 34 language
  layers; 262K published context.
- Apache 2.0; tool calling requires Mistral's tokenizer/config and parser.
- Official FP8 artifact is intended to fit a 12 GB device, but leaves little
  cache margin. Official Q4_K_M GGUF is 5.2 GB and is the credible A60 choice.
- Mistral reports near-parity or modest gains over Qwen3-8B base on several
  knowledge/reasoning measures, not a decisive expected ChrisOps win.
- Recommended runtime: llama.cpp/SYCL, Q4_K_M, text-only (omit the multimodal
  projection) at 8K initial context.
- Major unknown: whether its required Mistral system prompt/template can be
  made semantically equivalent to the ChrisOps control without changing model
  behavior.

### Phi-4 14B

- Dense 14.66B model, 40 layers, 16K context, MIT license.
- Official OpenVINO INT4 artifact: approximately 8.13 GB.
- Strong reasoning and instruction alignment, but it is an older static model,
  primarily English, and not specifically optimized for RAG/tool workflows.
- Estimated full-GPU footprint at only 4K context is approximately 10-11.3 GiB;
  8K is likely marginal once KV cache and buffers are included.
- Recommended runtime: OpenVINO `LLMPipeline`, INT4, 4K initial context.
- Major unknown: whether reasoning gains translate into evidence fidelity and
  operational state separation rather than math/academic performance.

### Qwen3-14B

- Dense 14.8B model, 40 layers, 8 KV heads, 32K native context, Apache 2.0.
- Official OpenVINO INT4 artifact: 9.73 GB.
- Same family and chat semantics as the control, so it is a clean model-scale
  question and should improve some reasoning tasks.
- The artifact alone occupies about 9.06 GiB. At 4K, FP16 KV cache is roughly
  0.63 GiB before runtime buffers. Full residency is marginal; partial offload
  or a very short context may be required.
- Recommended runtime: OpenVINO, INT4, 4K only for a later feasibility probe.
- Major risk: insufficient VRAM margin and latency without enough expected
  quality gain over the newer Qwen3.5-9B.

### Gemma and other reviewed exclusions

- Gemma 4 12B is current and Apache 2.0, but the 23.9 GB BF16 artifact, new
  unified multimodal architecture, and OpenVINO export/version requirements do
  not provide a clean A60 test today. No credible official quantized Intel path
  was found that outranks the shortlist.
- Gemma 3 12B is more mature but does not have GPU verification in the cited
  OpenVINO compatibility matrix and offers no clear advantage over Qwen3.5 for
  this workload.
- Qwen3.8-27B and other 20B-30B-class current models are outside credible full
  residency. Partial offload would confound latency and runtime comparisons.
- GPT-OSS-20B is technically possible with aggressive quantization, but its
  size and prior observed slowness make it a later out-of-band comparison, not
  a first A60 candidate.
- No Llama-family 8B candidate was found with a stronger combined case than
  Qwen3.5, Granite 4.2, or Ministral 3 for this evidence-grounded workload.

## Feasibility Estimation Method

The estimates intentionally reserve room beyond the weight file:

- OpenVINO/GGUF artifact or weight allocation;
- KV cache or recurrent/linear-attention state at the stated context target;
- tokenizer, graph, temporary, and command buffers;
- runtime fragmentation and driver allocations; and
- output growth to the 512-token initial cap.

They do not claim exact allocation. Exact A60 VRAM usage must be captured in the
implementation phase with a working privileged Intel telemetry path or a
runtime-native metric.

## Proposed Evaluation Artifacts

The implementation phase should create an evaluation package in
`chrisops-assistant`, separate from production telemetry:

- immutable question-set manifest and version;
- fixed retrieval snapshots containing ordered chunk IDs, source paths,
  source commit, chunk hashes, exact chunk text, and rendered context hash;
- model/runtime/config manifest for every run;
- raw answer files with stable run IDs;
- privacy-safe performance records without prompt/answer content;
- blinded answer bundles with randomized labels; and
- scorer rubric, independent scores, adjudication, and final comparison.

The frozen corpus commit is necessary but not sufficient. Vector retrieval can
still vary with embedding/runtime/index state. The exact retrieved chunks must
be captured once and replayed verbatim for the model-quality lane.

## Scoring Rubric

Blind human scoring should weight the requested priorities rather than generic
chat quality:

| Dimension | Weight | Failure examples |
|---|---:|---|
| Factual correctness against supplied evidence | 30% | Wrong fact; contradicts evidence |
| State classification | 20% | Treats historical/configured state as current |
| Evidence fidelity and unsupported-claim restraint | 20% | Invents missing host, status, command result, or cause |
| Technical reasoning | 15% | Invalid diagnosis, unsafe dependency chain, missed constraint |
| Distractor/incomplete-context robustness | 10% | Uses irrelevant chunk; hides uncertainty |
| Procedure usefulness and instruction following | 5% | Omits gate/rollback/order; violates requested format |

Each answer should also receive independent binary flags for fabricated fact,
unsafe operational instruction, authority-boundary violation, and failure to
say that evidence is insufficient. A single severe unsafe/fabricated answer
must remain visible and cannot be averaged away.

## Validation Completed

- Pinned homelab Agent Kit validation: pass for `chrisops-agent-kit 1.0.3`.
- Repository root, branch, HEAD, status, remotes, and recent history inspected.
- Live host hardware, OS, kernel, RAM, disk, PCI, OpenCL, Level Zero, package,
  service, endpoint, model-storage, and wrapper architecture inspected.
- Live/repository wrapper Git blob match confirmed.
- Two-second idle DRM engine sample: no counter movement.
- Small upstream metadata queries confirmed exact model architectures,
  parameter counts, context limits, licenses, and official quantization files.
- No generation, model load, or mutable acceptance was run.

## Production State Versus Repository State

- Repository implementation: current `homelab-ops` wrapper supports Qwen2.5
  and Qwen3 through one `LLMPipeline` and one active model.
- Deployed implementation: matches the repository Git blob after line-ending
  normalization.
- Production model: Qwen3-8B INT4 remains loaded and healthy on GPU.
- Open WebUI control: existing grounded object and retrieval settings were not
  inspected through a mutable/authenticated API and were not changed.
- Candidate models/runtimes: researched and documented only; none installed,
  downloaded, registered, activated, or accepted.

## Unresolved Issues and Unverified Assumptions

- Qwen3.5-9B has not been loaded on this host.
- OpenVINO 2026.2.1 `VLMPipeline` text-only operation against the official
  Qwen3.5 artifact is unresolved because upstream compatibility statements and
  issue evidence conflict.
- Exact loaded Qwen VRAM and free VRAM were unavailable without privileged
  debugfs/runtime telemetry.
- No candidate tokens/second, TTFT, prompt throughput, load time, or answer
  quality is known on this A60.
- llama.cpp SYCL performance on this exact A60/kernel/driver is unverified.
- The current Ollama binary's effective Intel GPU backend is unverified.
- Candidate quantization quality loss has not been measured against BF16.
- Open WebUI's ability to expose and replay exact retrieved chunks through its
  current version must be verified before using its profile lane as a strict
  retrieval-controlled result.

## Safety, Rollback, and Access Considerations

- Do not modify `openvino-api.service`, its venv, Qwen artifact, or the existing
  Open WebUI control object for candidate enablement.
- Do not try simultaneous residency of control and candidate.
- Bind any candidate API only to a container-reachable local interface, ideally
  Docker bridge `172.17.0.1`, or apply the same fail-closed firewall pattern as
  the control if a broader bind is unavoidable.
- Use separate artifact, venv, source, unit, port, logs, and model ID.
- Stop candidate service before restoring the Qwen service. Validate the Qwen
  `/health`, `/status`, and `/v1/models` identity after every swap.
- A failed candidate smoke test must stop before Open WebUI registration.
- Preserve answer content outside privacy-safe operational telemetry. The
  existing `chrisops.inference-run.v1` contract must not acquire prompts,
  responses, reasoning, raw errors, credentials, or endpoints.

## Do Not Redo or Reopen

- Do not treat Granite 4.2 as the default merely because it initiated the
  investigation.
- Do not attempt Granite 4.2-30B on the A60 for the controlled first round.
- Do not add Granite 4.2-3B to the quality shortlist without new task-specific
  evidence that a 3B model can beat the Qwen3-8B control.
- Do not adopt IPEX-LLM for new work.
- Do not upgrade the working OpenVINO environment to enable a candidate.
- Do not claim a fair RAG comparison from the same corpus alone; replay the same
  exact retrieval payload.
- Do not interpret successful model load as model-quality acceptance.

## Recommended First Candidate

**Qwen3.5-9B, official OpenVINO INT4 artifact, in a separate candidate
service.**

It has the best probability of materially improving ChrisOps because:

- it is newer than the control and has strong author-reported instruction,
  agent, knowledge, and long-context results;
- 9B remains inside the A60's useful full-residency class;
- Intel publishes a 6.13 GB INT4 artifact for the installed OpenVINO generation;
- it avoids adding llama.cpp/SYCL before model quality is known; and
- its non-thinking mode can approximate the current control while retaining a
  later reasoning-mode experiment.

Confidence is **medium-high on candidate quality and hardware fit**, and
**medium on first-load runtime compatibility** because the current service is
`LLMPipeline`-only and upstream Qwen3.5 `VLMPipeline` evidence is inconsistent.

Granite 4.2-8B is not first because its strongest verified local path is an
official GGUF through a llama.cpp/SYCL stack that is absent from `ai-lab`.
Granite remains the best second model because it fits, has excellent published
instruction-following/terminal evidence, and gives a genuinely different
training family rather than another Qwen scale point.

## Ranked Shortlist

| Rank | Model | Precision / runtime | A60 feasibility | Expected advantage over Qwen3-8B | Major risk | Confidence |
|---:|---|---|---|---|---|---|
| 1 | Qwen3.5-9B | Official INT4 OpenVINO IR; separate OpenVINO GenAI service | High at 8K; estimated 7-9 GiB; full residency expected | Material improvement in instruction following, evidence synthesis, agents, and reasoning | `VLMPipeline`/template compatibility on 2026.2.1 is unresolved | Medium-high |
| 2 | Granite 4.2-8B | Official Q4_K_M GGUF; llama.cpp SYCL/Level Zero | High at 8K; estimated 7-8.5 GiB | Strong instruction/terminal/coding behavior and independent model-family signal | Brand-new model; new SYCL stack; no observed A60 performance | Medium |
| 3 | Ministral 3 8B Instruct 2512 | Official Q4_K_M GGUF; llama.cpp SYCL | High at 8K; estimated 7-9 GiB | Possible modest reasoning/instruction improvement and strong edge focus | Published gains over Qwen3-8B are not decisive; template/system-prompt differences | Medium |
| 4 | Phi-4 14B | Official OpenVINO INT4 IR | Marginal at 4K; estimated 10-11.3 GiB | Strong dense reasoning and instruction alignment | Tight VRAM, 16K context, older/non-agentic focus | Medium-low |
| 5 | Qwen3-14B | Official OpenVINO INT4 IR | Marginal at 4K; likely partial offload or low headroom | More parameters with familiar Qwen semantics | 9.73 GB artifact leaves insufficient practical cache/buffer margin | Medium-low |

Test order if Qwen3.5 does not clearly win:

1. Granite 4.2-8B Q4_K_M via llama.cpp/SYCL.
2. Ministral 3 8B Instruct Q4_K_M via the same llama.cpp build.
3. Stop unless results justify the marginal Phi-4 or Qwen3-14B feasibility
   probes.

## Runtime Recommendation

For Qwen3.5-9B initial testing:

| Setting | Recommendation |
|---|---|
| Artifact | `OpenVINO/Qwen3.5-9B-int4-ov`, pinned to an exact Hugging Face revision |
| Precision | INT4 asymmetric, group size 128, official Intel conversion |
| Runtime | Separate OpenVINO GenAI candidate environment; try exact `2026.2.1` first |
| Pipeline | `VLMPipeline`, text-only requests |
| Context target | 8,192 total tokens initially; do not advertise native 262K |
| Output cap | 512 tokens for the controlled lane |
| Reasoning | Disabled for the first controlled comparison |
| Matched generation lane | Temperature 0.3; same output cap and semantic system prompt as control |
| Model-native lane | Non-thinking; temperature 0.7, top-p 0.8, top-k 20, min-p 0, presence penalty 1.5, repetition penalty 1.0 |
| API | Separate OpenAI-compatible service and stable model ID, not an edit to port 8000 |
| Listener | Prefer Docker bridge `172.17.0.1` on a new port so Open WebUI can reach it without LAN exposure |
| Lifecycle | Load on demand through explicit service swap; never simultaneous with Qwen |
| Disk | Approximately 6.13 GB artifact plus roughly 1-2 GB isolated environment/cache allowance |
| VRAM | Estimated 7-9 GiB at 8K; must be measured |
| RAM | 2-6 GiB host-side runtime/staging allowance expected; 30.4 GB was available during discovery |

The matched lane isolates model identity but may understate Qwen3.5 because
0.3 is not the author-recommended non-thinking temperature. The model-native
lane answers the operational question: whether a properly configured candidate
is actually better. Report both; do not merge their scores.

Do not start with thinking mode. If non-thinking Qwen3.5 is close but not a
clear win, add a separately scored thinking lane at temperature 1.0, top-p
0.95, top-k 20, presence penalty 1.5, and a larger output budget. That lane is
not directly comparable on latency or output length.

## A60 Fit and Risks

- The observed device allocation domain is 11.33 GiB, so practical model
  planning must reserve at least 2 GiB beyond 5-7 GB quantized weights.
- Qwen3.5-9B INT4, Granite 4.2-8B Q4_K_M, and Ministral 3 8B Q4_K_M are the
  credible full-residency tier.
- Phi-4 INT4 is a tight-fit 4K experiment, not an 8K default.
- Qwen3-14B INT4 and Granite 4.2-30B require unacceptable margin reduction or
  CPU offload for a clean interactive comparison.
- Multiple artifacts can coexist on disk, but the present service cannot
  dynamically register/swap them and simultaneous model residency is unsafe.
- OpenCL's 4 GiB maximum allocation is not automatically a model-size ceiling;
  runtimes partition allocations. It remains a runtime compatibility detail to
  observe during first load.
- Exact idle VRAM was unavailable. Implementation acceptance must add a
  truthful measurement path before reporting memory headroom.
- Qwen3.5/OpenVINO is the smallest software delta, but the current wrapper's
  `LLMPipeline` architecture cannot simply add it to `MODEL_CONFIGS`.
- llama.cpp/SYCL is credible on Arc but introduces oneAPI packages, build
  identity, and backend tuning. Keep that work isolated until needed.

## Fair A/B Test Design

### Architecture

```text
Frozen corpus commit cc448523...
          |
          v
One-time retrieval snapshot builder
  - exact ordered chunks
  - source/chunk hashes
  - exact rendered evidence
          |
          +-----------------------+
          |                       |
          v                       v
Qwen3-8B control endpoint   Candidate endpoint
(active alone on A60)       (active alone on A60)
          |                       |
          +-----------+-----------+
                      v
        Content-separated evaluation package
          - raw answers by opaque run ID
          - privacy-safe performance telemetry
          - blinded/randomized answer bundles
          - human scoring and adjudication
```

### Test lanes

1. **Raw fixed-evidence lane**
   - bypass Open WebUI retrieval;
   - replay identical evidence text and question to both base endpoints;
   - preserve the same semantic system instruction;
   - primary source for answer-quality decisions.

2. **Matched grounded-profile lane**
   - create a candidate grounded profile attached to the same frozen
     collection only after raw API acceptance;
   - use the same Top-K 5, vector-only, no-reranker settings;
   - capture and compare retrieved chunk IDs/text on every run;
   - exclude any pair whose retrieval payload differs from the strict score,
     while retaining it as integration evidence.

3. **Model-native configuration lane**
   - same fixed evidence and questions;
   - use each author's recommended non-thinking generation parameters;
   - score separately from the matched-parameter lane.

4. **Reasoning follow-up lane**
   - only after the non-thinking result;
   - permit model-specific thinking semantics and larger output budget;
   - compare quality separately and report added latency/tokens.

### Sequential benchmarking

- Warm/load one model at a time.
- Run the full question set in randomized question order.
- Stop/unload the active candidate and restore/validate Qwen before control
  runs, or alternate in coarse blocks if thermal drift is material.
- Record model load time separately.
- Use at least three repeated runs for stochastic configurations and preserve
  per-run scores rather than only averages.
- Record ambient ordering/block so warm-cache and temperature effects can be
  detected.

### Telemetry

Record per run where available:

- opaque run ID and evaluation manifest version;
- model ID, artifact revision/hash, quantization, runtime/version, device;
- context/output caps, reasoning mode, sampling controls, and seed;
- prompt-token and completion-token counts in the model's own tokenizer;
- queue time, model-load time, TTFT, total duration, prompt throughput,
  generation tokens/second, and finish reason;
- peak/steady VRAM and host RSS when trustworthy metrics exist; and
- success/failure category without raw error text in operational telemetry.

Keep prompts, retrieved chunks, answers, and reasoning traces in the isolated
evaluation package. Do not put them in `chrisops.inference-run.v1`.

### Blind scoring

- Replace model/run identities with randomized labels.
- Randomize answer order per question.
- Score against the fixed evidence and explicit rubric, not against a preferred
  prose style.
- Use at least two independent scorers for decision questions, followed by
  adjudication on material disagreement.
- Reveal model identity only after scores and critical-failure flags are locked.
- Decide on paired question-level wins and severe-error counts, not benchmark
  prestige or aggregate speed alone.

### Variables that cannot be identical

| Variable | Why it differs | Accounting method |
|---|---|---|
| Tokenizer and token count | Model vocabularies/rendering differ | Fix exact evidence text; record each token count and rendered-prompt hash |
| Chat template | Required special tokens/reasoning switches differ | Keep semantic roles/content fixed; archive rendered template output |
| Runtime | Qwen3.5 uses OpenVINO `VLMPipeline`; later Granite uses llama.cpp | Separate quality from performance conclusions; record runtime explicitly |
| Quantization | Official artifacts use different schemes/calibration | Treat artifact as part of deployable candidate; do not infer BF16 quality |
| Recommended sampling | Authors prescribe different values | Maintain distinct matched and model-native lanes |
| Reasoning mode | Thinking formats and token budgets differ | Non-thinking first; separate reasoning lane |
| KV/cache implementation | Runtime and architecture differ | Fix context target; measure memory/TTFT rather than assuming equivalence |
| Open WebUI retrieval | Vector search may vary despite same corpus/settings | Strict score uses replayed chunks; integration lane records/excludes mismatches |
| System prompt extensions | Some models require vendor system guidance | Use common semantic core; document additions and score separately if unavoidable |
| Stochastic output | Sampling and seed support differ | Repeat runs, record seeds where honored, report variance |

## Exact Next Implementation Step

Create one reversible, candidate-only Qwen3.5 slice without editing the Qwen
control:

1. Pin and download `OpenVINO/Qwen3.5-9B-int4-ov` to a new model directory and
   verify its revision and file hashes.
2. Create a separate pinned Python environment and a minimal candidate wrapper
   using `openvino_genai.VLMPipeline`, with a new model ID and OpenAI-compatible
   `/health`, `/status`, `/v1/models`, and `/v1/chat/completions` surface.
3. Add a separate systemd unit bound only to Docker bridge `172.17.0.1` on a new
   port. Give it an explicit conflict with `openvino-api.service` so both models
   cannot occupy the A60 simultaneously. Do not edit the existing unit, venv,
   artifact, port, or Open WebUI object.
4. With Open WebUI still unchanged, stop the Qwen service, start the candidate,
   and run one non-thinking text-only smoke request at 8K context capacity.
   Measure load time, TTFT, output, host RSS, and trustworthy VRAM if available.
5. If OpenVINO 2026.2.1 hits the known Qwen3.5 `VLMPipeline` incompatibility,
   stop and document it; do not upgrade the control environment. A later packet
   may authorize an isolated newer candidate runtime.
6. Stop the candidate, restart Qwen, and verify the original health/status/model
   identity. Only after both directions pass should a separate candidate Open
   WebUI connection/profile be proposed.

That is the smallest coherent change that can run Qwen3.5 beside the preserved
control while enforcing sequential GPU residency and providing a complete
rollback: remove/disable the candidate unit, venv, wrapper, and artifact, then
start the unchanged Qwen service.
