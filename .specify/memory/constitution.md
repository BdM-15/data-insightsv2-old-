# Capture Insights Constitution

<!-- Local BD/Capture Workbench for Federal Contracting -->

## Core Principles

### I. Local-First Architecture (NON-NEGOTIABLE)

All-local LLMs via Ollama; no cloud AI services. Local, private, Shipley-aligned capture workbench for federal contracting. All processing, storage, and AI inference remains on local hardware. Target hardware: Windows, 64GB RAM, NVIDIA RTX 4060 (8GB VRAM). From market intel to win themes and gate artifacts, with traceable sources.

### II. Open Source Tooling Only (NON-NEGOTIABLE)

Open-source/free tooling only. Use uv for Python, dependency management, and lockfiles. Prefer Apache/MIT/BSD licenses; verify model/dataset licenses for internal commercial use. No proprietary dependencies or cloud services.

### III. Configuration Management (NON-NEGOTIABLE)

All secrets only in .env; access via config.py. Explicit, logged API calls with reason, params, and durations. Validate critical config at startup; fail fast with remediation hints. Local structured logging; counters around fetch, LLM calls, embeddings, and DB operations.

### IV. Performance Standards

Fast dashboards (<5s per filter), evidence-based narratives. Deterministic drafting for exports: temp ~0.2, fixed seed, JSON mode for schemas. Context discipline; change-hash gated re-embedding. Local structured logging with performance metrics.

### V. Provenance & Traceability

Provenance on every computed metric and narrative. Explicit, logged API calls with reason, params, and durations. Tool schemas mirrored between PydanticAI/LangChain and MCP servers. Export with filters, timestamps, and model/version information.

## Technical Architecture

### Frontend Requirements

Streamlit multipage app (filters, insights, relationships, export). Use chat elements for AI-assisted drafting. Dashboard performance requirement: <5s per filter. Export capabilities for Markdown/Docx with sources and footnotes.

### Visualization & Chart Types

Standardize visualizations to ensure consistency and speed while keeping scope lean. Split into core vs optional so teams can ship iteratively.

Core (ship first):

- Bar/Column: top agencies, NAICS/PSC, contractors by count/obligation
- Line/Area: quarterly trends, simple forecasts (24–36 months)
- Tables with cross-filtering: expiring recompetes, opportunity pipelines

Advanced (optional, behind feature flag VIS_ADVANCED_CHARTS):

- Scatter/Bubble: obligation vs award_count, competition vs obligation (size by avg value)
- Treemap: competitive landscape (parent → recipient → sub-agency)
- Heatmaps/Choropleth: competitor–agency, NAICS–agency density, geography
- Timeline: expiring contracts by timeframe (0–6, 6–12, 12–24 months)
- Network graphs: prime–sub relationships, IDV–task order linkages
- Sankey diagrams: contract flow (agency → prime → sub), funding sources, award lifecycle transitions

All charts should support cross-filtering and export as PNG/PDF. Use Plotly where interactive. Target redraws p95 <2s; degrade gracefully on large selections (sampling, aggregation).

### Backend & Database

PostgreSQL with pgvector. Logical tables for awards, subawards, recipients, entities, relationships, embeddings, and summaries. Index for common filters (date/agency/NAICS/PSC/recipient) + vector indexes for semantic search.

Baseline logical tables (map via views/aliases to your schema):

- `prime_awards`
- `subawards_enriched`
- `mv_expiring_contracts`

Note: If using existing schemas (e.g., `s3_processed.usaspending_prime_awards_dedup`), provide SQL views to expose the above logical names to the app to avoid hard coupling to one warehouse layout.

Scope Clarification: This project does not perform data cleansing/ETL for USASpending. A separate project provides cleansed, ready-to-query tables/views in PostgreSQL. This app must be configurable to point at that external location (connection/DSN, database, schema, view/table names) and treat it as read-only.

Performance targets (pragmatic): dashboard queries p95 <5s, vector ops p95 <2s, MV refresh <30min. Prefer materialized views for heavy aggregations.

### AI/Agents Framework

**Baseline Local Models**: Prefer 7–13B instruct class (e.g., Llama 3.2 8B Instruct q4_K_M). Model is swappable via config; avoid hardcoding.
**Alternatives**: Mistral 7B, Qwen2.5 7B
**Embeddings**: all-minilm or nomic-embed (configurable)
**Ollama Endpoints**: chat (/api/chat) and embeddings (/api/embed); JSON mode and structured outputs supported
**PydanticAI**: structured, type-safe tools and outputs; dependency injection; streaming; optional durable execution
**LangChain + LangGraph**: lightweight chains and graph control for step-wise flows (fetch → summarize → compare → draft)
**MCP Python SDK**: local tools/servers for web intel, document creation, visualization, and analysis; strict parameterization and logging
**VS Code AI Toolkit**: local agent development, prompt iteration, optional model conversion

### Data Sources & API Constraints

**USASpending** (no auth): endpoints for search, awards, transactions, subawards, spending by NAICS/PSC/agency/time; last_updated tracking
**SAM.gov Opportunities v2** (api_key required): date range mandatory; filters for NAICS/PSC/set-aside/organization; pagination and response limits
**SAM.gov Entity Management v4** (api_key required, roles vary): public/FOUO/sensitive data; extract API for JSON/CSV; rate limits; D&B data usage disclaimer
**GSA Pricing Intelligence** (CALC+/Quick Rate): use published interfaces/downloads; some datasets restricted; do not scrape
**BLS API v2** (registration encouraged): timeseries JSON, GET/POST, inflation and wage indices, unemployment
**ILOSTAT** (SDMX): integrate via documented SDMX endpoints where permitted; use local caching
**Web search** (DuckDuckGo): strictly bounded queries and snippet length; always capture sources

**Additional Sources**: SBA Mentor-Protégé Agreements, NATO NSPA XML Feed, Federal Procurement Data System (FPDS), Data.gov Contract-Awarded Labor Category API (CALC)

## Security & Compliance

### Data Protection

Local-first; no data sent to cloud LLMs. All processing remains on local infrastructure. Explicit consent required for any external API calls with full logging of data transmitted.

### API Security

Explicit, logged API calls with reason, params, and durations. Rate limiting compliance for all external APIs. API keys stored only in .env files with config.py access patterns.

### License Compliance

Prefer Apache/MIT/BSD licenses; verify model/dataset licenses for internal commercial use. Document all dependencies and their license requirements. Regular license audits for compliance.

## Shipley Capture Framework

### Qualification & Bid Decisions

Focus on qualification (bid/no-bid), competitor analysis, customer hot buttons, win themes. Implement Shipley decision gate reviews with documented criteria. Gate-ready artifacts: qualification worksheet, competitor snapshot, teaming rationale, IGCE sanity checks, risk mitigations.

**Four-Milestone Framework**:

- **Milestone 0**: Opportunity Identification (70-80% automated)
- **Milestone 1**: Opportunity Assessment (50-60% automated)
- **Milestone 2**: Bid/No-Bid Decision (30-40% automated)
- **Milestone 3**: Proposal Strategy Validation (20-30% automated)

### Competitive Intelligence

Bidder Comparison Charts with customer-perceived strengths/weaknesses. Integrated Solution Worksheets linking customer issues to requirements and solutions. Competitor analysis covering market approach, pricing patterns, customer relationships, and past performance.

**Required Analytics**: Number of offers received analysis, competitive density mapping, pWin calculations based on historical bidder counts

### Win Strategy Development

Leverage strengths, mitigate weaknesses, exploit competitor weaknesses, neutralize competitor strengths. Value propositions for economic buyers, users, and technical buyers. Price-to-win analysis within customer budget constraints.

**BLS OEWS Integration**: Bureau of Labor Statistics wage data for labor rate benchmarking and pricing justification across 800+ occupations with percentile breakdowns

### Capture Deliverables

Stance editor, expiring/recompete list, competitor snapshot, teaming graph, win themes. Export "Capture Profile" with sources and footnotes. All artifacts aligned with Shipley methodology and federal contracting best practices.

## Development Standards

### Installation & Operations

uv pin Python 3.12; uv sync; streamlit run. Validate critical config at startup; fail fast with remediation hints. Local structured logging; counters around fetch, LLM calls, embeddings, and DB operations.

### LLM Usage Policies

Deterministic drafting for exports: temp ~0.2, fixed seed, JSON mode for schemas. Context discipline; change-hash gated re-embedding. Tool schemas mirrored between PydanticAI/LangChain and MCP servers. Reproducible artifacts with explicit model versions and parameters.

Simplicity & Anti-Overfitting Guardrails:

- Prefer simple prompts and few-shot patterns before complex agent graphs.
- Ship minimal viable tools; add new tools only if they unlock a use case measured by users.
- Avoid training on narrow agency/vendor idiosyncrasies; enforce stratified sampling across time, agencies, values.
- Keep evaluation tasks representative of real workflows (classification, mapping, validation) vs. synthetic trivia.

### Code Quality

Type hints required for all functions. Structured logging with standardized format. Error handling with user-friendly messages and technical logging. Unit tests for core business logic.

## Success Criteria & Deliverables

### Primary Deliverables

1. **Stance Editor**: Interactive tool for developing and refining capture positions with AI assistance
2. **Expiring/Recompete List**: Automated tracking of contract opportunities with renewal timelines
3. **Competitor Snapshot**: Comprehensive profiles with strengths, weaknesses, and positioning analysis
4. **Teaming Graph**: Visualization of prime/subcontractor relationships and teaming opportunities
5. **Win Themes Generator**: AI-assisted development of customer-focused value propositions
6. **Capture Profile Export**: Complete capture package with sources, footnotes, and Shipley artifacts

### Performance Metrics

- Dashboard response time: <5 seconds per filter operation
- Data freshness: API updates within 24 hours of source availability
- Model inference: Local processing with <2 second response for standard queries
- Export generation: Complete capture profiles within 30 seconds

### Quality Standards

- All computed metrics include provenance and source citations
- AI-generated content marked with model version and parameters
- Shipley methodology compliance verified through structured reviews
- Export formats compatible with standard federal proposal development workflows

## Training Reference Standards

### Authoritative Sources for LLM Fine-Tuning

**USASpending API References**: All dataset generation and fine-tuning must use official USASpending glossary and data dictionary definitions for field names, terminology, and relationships. Cache locally in `data/reference/usaspending/` with date-stamped filenames.

**Shipley-Aligned Training Reference**: Mandatory use of `SHIPLEY_LLM_CURATED_REFERENCE.md` for capture and proposal methodology training. This curated reference provides paraphrased Shipley principles without copyright violations.

**Terminology Consistency**: LLM training examples must align with USASpending field definitions (e.g., "base_and_all_options_value" vs. "total_obligation") and Shipley capture terminology (e.g., "discriminators" vs. "differentiators").

### Training Data Requirements

**Seed Examples**: Use structured JSONL format with system/user/assistant message patterns. Include contract classification, competitive analysis, evaluation criteria mapping, risk assessment, and pricing justification examples.

**Business Rules Integration**: Training examples must reflect actual database constraints, contract types, set-aside categories, and competitive dynamics from USASpending data patterns.

**Reference Validation**: All training content must be traceable to authoritative sources with explicit citations and version control for reference materials.

## Governance

### Constitution Authority

This constitution supersedes all other development practices and technical decisions. All features, APIs, and integrations must align with stated principles. Complexity must be explicitly justified against core requirements and user impact. Prefer config toggles/feature flags over hard wiring choices.

### Amendment Process

Constitution amendments require documented justification, technical impact assessment, and migration plan. All changes must maintain non-negotiable principles (local-only, open-source, uv dependency management).

### Compliance Verification

All development work must verify compliance with:

- Local-first architecture (no cloud dependencies)
- Open-source licensing requirements
- Shipley capture methodology alignment
- Performance and security standards

### Quality Gates

Regular reviews ensure adherence to constitution principles. Any deviation requires explicit documentation and remediation timeline. Use structured logging and metrics to validate ongoing compliance. Track advanced features under flags with clear exit criteria to graduate to core.

**Version**: 1.0.0 | **Ratified**: 2025-09-23 | **Last Amended**: 2025-09-23
