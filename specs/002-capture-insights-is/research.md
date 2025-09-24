# Phase 0 Research: Capture Insights Core Capture Loop

## Data Source Dependency (External ETL)

- Decision: Treat cleansed USASpending primes/subawards as an external dependency provided by a separate ETL/cleansing project.
- Rationale: Keeps this project focused on analysis and UI; aligns with user directive to separate concerns.
- Unknowns [NEEDS CLARIFICATION]: PostgreSQL connection/DSN, database, schema, and table/view names for the cleansed data.

## Schema Mapping

- Decision: Expose logical views: prime_awards, subawards_enriched, mv_expiring_contracts.
- Rationale: Decouple app logic from raw schema; aligns with constitution.
- Alternatives: Hardwire to raw tables (tight coupling, brittle migrations).

## Session Snapshot Schema

- Decision: JSON with fields: filters, horizon (preset/custom), selected_entities, stance_revision_hash, generation_metadata, export_timestamp.
- Rationale: Minimal, portable, no secrets; supports reload later.
- Alternatives: DB-backed sessions (overhead for single-user MVP).

## Capability Baseline Import

- Decision: CSV columns: tag, class (core|differentiator|emerging), evidence_award_ids (optional; semicolon-delimited), notes (optional). Validate and report errors.
- Rationale: Simple, user-editable; supports reuse.
- Alternatives: Complex schema (adds friction), UI-only editing (hard to seed).

## Expiring/Recompete Heuristic

- Decision: Presets 0–6, 6–12, 12–24 months; default 6–24; incumbent = top recipient by obligations on base/vehicle; show provenance.
- Rationale: Matches PRD cadence and user goals.
- Alternatives: ML classifier (overkill now).

## Performance Baselines

- Decision: Index common filters; pre-aggregate obligations by period; exact pgvector first.
- Rationale: Meet <5s dashboard without extra complexity.
- Alternatives: External vector store (premature).

## LLM Drafting

- Decision: Local model (Llama 3.2 8B q4_K_M), temp~0.2 for exports; JSON-mode structured outputs for win themes.
- Rationale: Deterministic, fast-enough on target hardware.
- Alternatives: Larger models (latency/VRAM), cloud (violates constitution).
