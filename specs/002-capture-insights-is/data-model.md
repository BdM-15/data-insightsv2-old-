# Data Model: Capture Insights Core Capture Loop

## Entities

### MarketSlice
- filters: object (agency[], naics_psc[], set_aside[], date_range, vehicle[])
- created_at: datetime
 - source_location: string [NEEDS CLARIFICATION] (PostgreSQL DSN/schema/views for cleansed data)

### Signals
- obligations_over_time: array(period, amount)
- top_competitors: array(entity_id, name, amount, share)
- competition_levels: array(metric, value)
- expiring_contracts: array(contract_id, incumbent_entity_id, end_date, window_bucket)

### CapabilityBaseline
- tag: string
- class: enum(core|differentiator|emerging)
- evidence_award_ids: array[string]
- notes: string?
- revision_hash: string
- revised_at: datetime

### CaptureProfile
- filters: object
- sources: array[source_ref]
- win_themes: array[{title, rationale, sources[]}]
- generated_at: datetime
- model_info: {name, version, params}

### SessionSnapshot
- filters: object
- horizon: {preset: enum(0-6|6-12|12-24)|custom: {start,end}}
- selected_entities: object
- stance_revision_hash: string
- generation_metadata: object
- export_timestamp: datetime

## Relationships
- CaptureProfile references MarketSlice and CapabilityBaseline
- Signals derive from MarketSlice (1:1 per evaluation)
- Expiring contracts link to incumbents (entity_id)

## Validation Rules
- class must be one of core|differentiator|emerging
- horizon preset must be in {0-6,6-12,12-24}; custom requires valid dates
- evidence_award_ids must match known award IDs if present

