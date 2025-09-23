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

### Backend & Database

PostgreSQL with pgvector. Tables for awards, subawards, recipients, entities, relationships, embeddings, and summaries. Indexes for common filters (date/agency/NAICS/PSC/recipient) + vector indexes for semantic search.

**Required Tables**: `s3_processed.usaspending_prime_awards_dedup`, `s3_processed.usaspending_subawards_enriched`, `mv_expiring_contracts` (materialized view)

**Performance Standards**: Dashboard queries <5s, semantic vector operations <2s, materialized view refresh <30min

### AI/Agents Framework

**Default Models**: Llama 3.2 8B Instruct (q4_K_M quantization)
**Alternative Models**: Mistral 7B, Qwen2.5 7B  
**Embeddings**: all-minilm or nomic-embed
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

## Governance

### Constitution Authority

This constitution supersedes all other development practices and technical decisions. All features, APIs, and integrations must align with stated principles. Complexity must be justified against core requirements.

### Amendment Process

Constitution amendments require documented justification, technical impact assessment, and migration plan. All changes must maintain non-negotiable principles (local-only, open-source, uv dependency management).

### Compliance Verification

All development work must verify compliance with:

- Local-first architecture (no cloud dependencies)
- Open-source licensing requirements
- Shipley capture methodology alignment
- Performance and security standards

### Quality Gates

Regular reviews ensure adherence to constitution principles. Any deviation requires explicit documentation and remediation timeline. Use structured logging and metrics to validate ongoing compliance.

**Version**: 1.0.0 | **Ratified**: 2025-09-23 | **Last Amended**: 2025-09-23
