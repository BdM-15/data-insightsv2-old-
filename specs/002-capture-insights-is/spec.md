# Feature Specification: Capture Insights Core Capture Loop

**Feature Branch**: `002-capture-insights-is`  
**Created**: 2025-09-23  
**Status**: Draft  
**Input**: User description: "Capture Insights is a local, private tool that helps you move quickly from raw federal contract data to clear decisions about whether and how to pursue an opportunity. It pulls processed historical award data (prime and subaward) into simple dashboards, lets you explore competitors and upcoming recompetes, builds and maintains a reusable baseline of your company capabilities, and uses local AI to draft win themes and narrative blocks. Everything runs on your own machine. No outside AI services. No hidden network calls. The heart of the product is the 'capture loop' which is Pick and filter a slice of the market, See core spend, timing, and competitor signals fast, Spot expiring or likely-to-recompete contracts, Compare your capability baseline to requirements, incumbents, and other competitors, Generate data‑backed win themes and action ideas, Export a clean Markdown capture profile with sources. The product stays lean on purpose: fewer screens, faster answers, lower mental load. Problem Statement, Early capture work today usually means jumping between spreadsheets, clunky downloads, and manual notes. That wastes time, buries context, and makes it hard to repeat what worked. Data is often too summarized to be useful or too raw to be quick. There is no simple, private workstation tool that: (a) shows the right market and competitor slices fast, (b) keeps a living baseline of what your company can actually do, and (c) helps draft trustworthy narrative content with clear source references."

## Clarifications

### Session

- Data freshness: Default warning threshold = 7 days; show last refresh timestamp prominently (derived from PRD “Fast Feels Better” and local, on-demand refresh posture).
- Expiring/recompete horizons: Presets = 0–6, 6–12, 12–24 months; default = 6–24 months; allow custom range.
- Session persistence: MUST support exporting a local JSON Session Snapshot (filters, horizon, selected entities, stance revision hash, generation metadata). SHOULD support loading a prior snapshot (can be deferred).
- Baseline import: SHOULD support CSV import with columns: tag, class (core|differentiator|emerging), evidence_award_ids (optional; semicolon-delimited), notes (optional). YAML import may follow.

### Data Source

- [NEEDS CLARIFICATION] Cleansed USASpending data source location (PostgreSQL connection/DSN, database, schema, and table/view names) will be provided by a separate ETL/cleansing project. This project does not perform cleansing.
- Assumption: Read-only access to provided schema/views; app maps them to logical names (prime_awards, subawards_enriched, mv_expiring_contracts) via configuration.

## Execution Flow (main)

```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines

- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "login system" without auth method), mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
4. **Common underspecified areas**:
   - User types and permissions
   - Data retention/deletion policies
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs

---

## User Scenarios & Testing (mandatory)

### Primary User Story

As a capture manager, I want a fast, private workstation that lets me filter the federal market, see spend/timing/competitor signals, spot expiring or likely-to-recompete contracts, compare our capability baseline against incumbents and requirements, generate data-backed win themes and action ideas, and export a clean capture profile with sources—so that I can decide whether and how to pursue opportunities quickly and confidently.

### Acceptance Scenarios

1. Given processed award data are available, When the user filters by agency, NAICS, time window, and set-aside, Then the system shows core spend, timing, and competitor signals within a single dashboard view.
2. Given the user has applied filters, When the user selects "Expiring/Recompetes," Then the system lists contracts expiring within the chosen horizon and highlights incumbent(s) and likely recompete indicators.
3. Given a capability baseline exists, When the user opens "Compare," Then the system presents a gap/fit view comparing baseline capabilities to requirements and incumbent patterns.
4. Given filtered context and comparison are ready, When the user clicks "Generate Themes," Then the system produces draft win themes and narrative blocks with explicit references to data points.
5. Given a session is complete, When the user selects "Export Capture Profile," Then the system exports a Markdown report that includes sources, filters used, and generated narrative.
6. Given the user wants to preserve their work, When the user selects "Export Session Snapshot," Then the system saves a single local file capturing filters, horizon preset, selected entities, stance revision hash, and generation metadata.
7. Given a capability baseline file exists, When the user selects "Import Baseline" and provides a valid CSV, Then the system loads capability tags and classes, flags any invalid rows, and updates the baseline for comparison.

### Edge Cases

- What happens when the selected filters produce too few or zero records? The system should indicate no results and suggest broader filters or adjacent NAICS/PSC.
- How does the system handle stale or partially loaded data? The system should clearly show last-updated timestamps and warn if freshness thresholds are exceeded.
- How does the system behave without a defined capability baseline? Provide a guided starter to build/import a minimal baseline before comparison.
- What if expiring contract data conflicts with recent modifications? The system should prioritize authoritative fields and show provenance for reconciliation.

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: System MUST allow users to filter market data by agency, NAICS/PSC, date range, contract vehicle/IDV, and set-aside.
- **FR-002**: System MUST present core signals for the filtered slice: total obligations over time, top competitors, award timing, and competition levels.
- **FR-003**: System MUST provide an expiring/likely-to-recompete list within a chosen horizon (e.g., 0–6, 6–12, 12–24 months) with incumbent identification.
- **FR-004**: System MUST maintain a reusable company capability baseline and allow comparison against requirements, incumbents, and competitors.
- **FR-005**: System MUST generate draft win themes and narrative blocks that reference underlying data and cite sources.
- **FR-006**: System MUST export a Markdown capture profile including filters applied, sources, and generated content.
- **FR-007**: System MUST operate entirely locally with no external AI services or hidden network calls.
- **FR-008**: System MUST display data freshness timestamps and warn when freshness thresholds are exceeded.
- **FR-009**: System MUST provide clear empty-state guidance when filters return no results.
- **FR-010**: System MUST keep the experience lean: minimize screens, consolidate insights, and reduce cognitive load.

Clarified items (from PRD assumptions):

- **FR-011**: System MUST warn when processed awards/subawards data are older than 7 days (default freshness threshold) and show the last refresh timestamp prominently.
- **FR-012**: System MUST offer expiring/recompete horizon presets of 0–6, 6–12, and 12–24 months, with a default selection of 6–24 months and an option for a custom range.
- **FR-013**: System MUST support exporting a local Session Snapshot file (.json) containing filters, active horizon preset or custom range, selected entities (e.g., target agency/NAICS), stance revision hash, and generation metadata; System SHOULD support loading a previously exported snapshot (reload may be deferred to a later iteration).
- **FR-014**: System SHOULD support importing a capability baseline from a local CSV file. Minimum CSV columns: `tag`, `class` (one of core|differentiator|emerging), `evidence_award_ids` (semicolon-separated optional), `notes` (optional). YAML import may be added later.
- **FR-015**: System MUST allow configuration of an external, cleansed data source (PostgreSQL) including connection parameters and logical view/table names for prime awards, subawards, and expiring contracts. System WILL NOT perform data cleansing or ETL.

### Key Entities (include if feature involves data)

- **Market Slice**: The filtered subset of awards/subawards (attributes: filters, time range, agencies, NAICS/PSC, set-aside, vehicle).
- **Signals**: Derived metrics for the market slice (attributes: obligations over time, top recipients, competition levels, expiring contracts).
- **Capability Baseline**: Company capabilities and evidence (attributes: domains, past performance references, certifications, labor categories).
- **Capture Profile**: Exportable narrative output (attributes: applied filters, referenced sources, win themes, recommendations, timestamp).
- **Session Snapshot**: A portable file representing the current working context (attributes: filters, horizon preset/custom range, selected entities, stance revision hash, generation metadata, export timestamp).

---

## Review & Acceptance Checklist

### Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed
