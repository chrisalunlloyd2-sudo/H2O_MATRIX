# H2O_MATRIX

> H2O_MATRIX — part of the Viper RAID-0 workstation system.

*Auto-generated 2026-06-29 09:02 from source — branch `main`, 37 Python modules, 31 other files.*

## Architecture

```
  .director_payload.md
  .gitignore
  900_STEPS_SINGULARITY.md
  Blueprint.md
  CHANGELOG.md
  CLIDE_SPEC.md
  ENTERPRISE_INIT.p
  GEMINI.md
  LOGOS_PURPOSE.md
  MATRIX_GEN8_MASTER_PLAN.md
  MIGRATION_PLAN.md
  PROJECT_LOG.md
  H2OIDE/
  agy-cli-go/
    agy-go
    go.mod
    main.go
  genetic_flow/
    .aider.conf.json
    .env
    .gitignore
    __init__.py
    install_genetic_flow.sh
    runtime_loop.py
    cluster/
      __init__.py
      sync_hook.py
      topology_mapper.py
    core_brain/
      __init__.py
      router.py
      target_feature.py
      test_harness.py
      tui_layout.py
      watchdog.py
      binary/
        binary_code_bod.txt
      binary_engine/
        __init__.py
        decompiler.py
    master_logic/
      gemini_agent.py
    memory_daemon/
      gemini_client.py
      gemini_daemon.py
    memory_pipeline/
      __init__.py
      audio_engine.py
      headless_orchestrator.py
      rag_interceptor.py
    pyramid/
      __init__.py
      code_sprite.py
    symbolic_brain/
      __init__.py
      engine.py
      extractor.py
      parser.py
      rules.sql
      symbolic_inference.py
      weight_backprop.py
    tracking_db/
      __init__.py
      writer.py
  src/
    main.py
    matrix_operations.py
  tmp_extract/
    VIPER_SHIPMENT_STAGING/
      VIPER_FORMATTING_SPEC.md
      JRM/
```

## Dependencies

External packages imported by this project:

`asyncpg`, `core_brain`, `dis`, `dotenv`, `genetic_flow`, `kqml_protocol`, `numpy`, `openai`, `rag_pipeline`, `requests`, `rich`

## How to run

Executable entry points (have a `__main__` block):

- `python genetic_flow/cluster/sync_hook.py`
- `python genetic_flow/cluster/topology_mapper.py`
- `python genetic_flow/master_logic/gemini_agent.py`
- `python genetic_flow/memory_daemon/gemini_client.py`
- `python genetic_flow/memory_daemon/gemini_daemon.py`
- `python genetic_flow/memory_pipeline/audio_engine.py`
- `python genetic_flow/memory_pipeline/headless_orchestrator.py`
- `python genetic_flow/memory_pipeline/rag_interceptor.py`
- `python genetic_flow/pyramid/code_sprite.py`
- `python genetic_flow/runtime_loop.py`
- `python genetic_flow/symbolic_brain/extractor.py`
- `python genetic_flow/symbolic_brain/parser.py`

## Modules

### `genetic_flow/cluster/sync_hook.py`

- `sync_bayesian_weights()` — Bridge ledger.db quantum_parameters into the genetic flow loop.
- `export_optimization_stats()` — Export genetic progress back to the main IDE ledger.

### `genetic_flow/cluster/topology_mapper.py`

- `initialize_cluster_table()`
- `update_heartbeat(node_id)` — Updates the heartbeat for a specific cluster node.
- `get_cluster_topology()` — Returns a string representation of the cluster topology for the TUI.

### `genetic_flow/core_brain/binary_engine/decompiler.py`

- **class `BinaryDecompilationEngine`** — Airgapped processor that translates Python logic into binary opcode math.
  - methods: `decompile_and_score`

### `genetic_flow/core_brain/router.py`

- **class `LocalAgentRouter`** — [PERFORMATIVE: ROUTE] Native 32-bit llama-cli Wrapper with KQML/Vector Handoff.
  - methods: `get_management_rules`, `run_generation`, `clean_code`
- `extract_clean_code(raw_stream)`

### `genetic_flow/core_brain/target_feature.py`

- `algorithm(n)`

### `genetic_flow/core_brain/test_harness.py`

- **class `StatisticalEvaluator`** — [PERFORMATIVE: EVALUATE] Evaluates microsecond trends via IQR variance algorithms (Pure Python).
  - methods: `evaluate_performance`
- `evaluate()`

### `genetic_flow/core_brain/tui_layout.py`

- `get_last_insight()`
- `generate_dashboard(gen, fitness, code_str, stuck_count, max_stuck, sprite_status)`

### `genetic_flow/core_brain/watchdog.py`

- **class `Watchdog`**
  - methods: `check_stagnation`, `get_hyperparameter_adjustment`, `trigger_cloud_escalation`

### `genetic_flow/master_logic/gemini_agent.py`

- `get_embedding(text)`
- `fetch_memory_context(goal)`
- `run_cmd(cmd)`
- `fix_step(step_data, error_output, sys_constraints, decompiler, max_retries)`
- `main(goal)`

### `genetic_flow/memory_daemon/gemini_client.py`

- `send_to_daemon(command, exit_code)`

### `genetic_flow/memory_daemon/gemini_daemon.py`

- `process_and_store(payload)` — The heavy lifting she does silently after your terminal is already free.
- `handle_connection(reader, writer)` — Instantly accepts data from your shell hook and releases it.
- `main()`

### `genetic_flow/memory_pipeline/audio_engine.py`

- **class `AudioManifestationEngine`** — [PHASE 5.2/5.3] Headless TTS & Async Streaming Engine.
  - methods: `speak`, `run_audio_feedback`

### `genetic_flow/memory_pipeline/headless_orchestrator.py`

- **class `HeadlessOrchestrator`**
  - methods: `handle_input`

### `genetic_flow/memory_pipeline/rag_interceptor.py`

- **class `SimpleEmbedder`** — Computes fixed-dimension semantic vector via hashing.
  - methods: `embed`
- **class `RAGInterceptor`**
  - methods: `pre_flight_query`, `log_event`

### `genetic_flow/pyramid/code_sprite.py`

- **class `CodeSprite`** — Autonomous Dependency Sprite: Scans for imports and manifests environment.
  - methods: `_get_installed_packages`, `scan_and_fix`

### `genetic_flow/runtime_loop.py`

- `main_loop(max_gen)`

### `genetic_flow/symbolic_brain/engine.py`

- **class `SymbolicContextEngine`** — [PERFORMATIVE: TOKENIZE] Compiles dynamic AST tree; extracts parent/child shapes.
  - methods: `get_structural_signature`, `_walk_signature`, `generate_context_hash`, `update_relational_matrix`
- **class `ProductionRuleMatcher`** — [PERFORMATIVE: MATCH] Inductive Logic Loop matching pattern variations.
  - methods: `match_rule`
- **class `MutationInjector`** — [PERFORMATIVE: INJECT] Executes physical AST block mutations.
  - methods: `apply_mutation`
- **class `WeightBackpropagator`** — [PERFORMATIVE: UPDATE] Symbolic Backprop Step.
  - methods: `backprop`

### `genetic_flow/symbolic_brain/extractor.py`

- **class `SymbolicExtractor`** — Extracts symbolic rules from successful mutations in the ledger.
  - methods: `analyze_patterns`

### `genetic_flow/symbolic_brain/parser.py`

- **class `SymbolicParser`** — [PERFORMATIVE: TOKENIZE] Compiles live files into structured AST nodes.
  - methods: `get_signature_hash`, `_get_structural_string`, `map_token_relations`

### `genetic_flow/symbolic_brain/symbolic_inference.py`

- **class `SymbolicInference`** — [PERFORMATIVE: INFER] Selects target execution transformation rules.
  - methods: `infer_optimization_directive`

### `genetic_flow/symbolic_brain/weight_backprop.py`

- **class `WeightBackprop`** — [PERFORMATIVE: UPDATE] Calculates code fitness improvements and updates rule weights.
  - methods: `update_rule_weights`

### `genetic_flow/tracking_db/writer.py`

- `get_git_hash()`
- `store_mutation(chash, gen, score, code, task, ast_depth, stagnation, latency_delta)`

### `genetic_optimizer.py`

- `fitness(response_text, duration)`

### `initialize_enterprise_project.py`

- `get_token()`
- `generate_ascii_tree(path)` — Simple ASCII tree generator.
- `initialize()`

### `scientific_executor.py`

- `log_scientific_step(step_num, step_desc, observation, hypothesis, experiment, result)`
- `get_next_step()`
- `mark_step_complete(step_num)`
- `run_with_limits(command)`
- `execute_step(step_num, step_desc)`

### `scientific_orchestrator.py`

- **class `ScientificOrchestrator`**
  - methods: `log_scientific_step`, `get_next_step`, `mark_step_complete`, `run_with_limits`, `orchestrate`

### `src/main.py`

- `main()`

## Public API index

| Module | Function | Signature |
|--------|----------|-----------|
| `gemini_agent` | `fetch_memory_context` | `fetch_memory_context(goal)` |
| `gemini_agent` | `fix_step` | `fix_step(step_data, error_output, sys_constraints, decompiler, max_retries)` |
| `gemini_agent` | `get_embedding` | `get_embedding(text)` |
| `gemini_agent` | `main` | `main(goal)` |
| `gemini_agent` | `run_cmd` | `run_cmd(cmd)` |
| `gemini_client` | `send_to_daemon` | `send_to_daemon(command, exit_code)` |
| `gemini_daemon` | `handle_connection` | `handle_connection(reader, writer)` |
| `gemini_daemon` | `main` | `main()` |
| `gemini_daemon` | `process_and_store` | `process_and_store(payload)` |
| `genetic_optimizer` | `fitness` | `fitness(response_text, duration)` |
| `initialize_enterprise_project` | `generate_ascii_tree` | `generate_ascii_tree(path)` |
| `initialize_enterprise_project` | `get_token` | `get_token()` |
| `initialize_enterprise_project` | `initialize` | `initialize()` |
| `main` | `main` | `main()` |
| `router` | `extract_clean_code` | `extract_clean_code(raw_stream)` |
| `runtime_loop` | `main_loop` | `main_loop(max_gen)` |
| `scientific_executor` | `execute_step` | `execute_step(step_num, step_desc)` |
| `scientific_executor` | `get_next_step` | `get_next_step()` |
| `scientific_executor` | `log_scientific_step` | `log_scientific_step(step_num, step_desc, observation, hypothesis, experiment, result)` |
| `scientific_executor` | `mark_step_complete` | `mark_step_complete(step_num)` |
| `scientific_executor` | `run_with_limits` | `run_with_limits(command)` |
| `sync_hook` | `export_optimization_stats` | `export_optimization_stats()` |
| `sync_hook` | `sync_bayesian_weights` | `sync_bayesian_weights()` |
| `target_feature` | `algorithm` | `algorithm(n)` |
| `test_harness` | `evaluate` | `evaluate()` |
| `topology_mapper` | `get_cluster_topology` | `get_cluster_topology()` |
| `topology_mapper` | `initialize_cluster_table` | `initialize_cluster_table()` |
| `topology_mapper` | `update_heartbeat` | `update_heartbeat(node_id)` |
| `tui_layout` | `generate_dashboard` | `generate_dashboard(gen, fitness, code_str, stuck_count, max_stuck, sprite_status)` |
| `tui_layout` | `get_last_insight` | `get_last_insight()` |
| `writer` | `get_git_hash` | `get_git_hash()` |
| `writer` | `store_mutation` | `store_mutation(chash, gen, score, code, task, ast_depth, stagnation, latency_delta)` |

## Status

- Branch: `main`
- Last commit: 2026-06-27 19:30:18 -0600
- File types: .md ×19, .sh ×4, .json ×2, .p ×1, .rs ×1, .mod ×1, .go ×1, .txt ×1

### Recent commits
```
cc928da [Moe autonomous] H2O_MATRIX 2026-06-27 19:30
a093041 [Moe autonomous] H2O_MATRIX 2026-06-26 23:35
a688d66 [Moe autonomous] H2O_MATRIX 2026-06-20 13:23
82ac6f3 [Moe autonomous] H2O_MATRIX 2026-06-20 02:52
102d078 Initial commit
f41f663 Enterprise: H2O Matrix Unified Manifestation
89b3f68 Enterprise: Automated Project Sync
47b628f Enterprise: Project SOP Manifestation
```

---
*README generated by `readme_generator.py` (Viper). Deterministic — derived from source, not LLM prose.*