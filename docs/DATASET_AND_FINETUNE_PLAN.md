# Data Insights LLM Fine-Tuning & Dataset Development Plan

## Objective

Develop a comprehensive training dataset for fine-tuning local LLMs (Ollama Llama 3.2, Mistral, Qwen) to understand federal contracting data structures, terminology, and business rules. The goal is to train models that can accurately distinguish between contracts, modifications, task orders, IDVs, and various contract vehicles while providing expert-level capture management insights aligned with Shipley methodology.

## Critical Contract Knowledge for LLM Training

### 1. Contract vs. Modification Distinction (CRITICAL)

- **Base Contract**: `modification_number = '0'` - Original contract award
- **Modification**: `modification_number != '0'` - Changes to existing contract (funding, scope, time)
- **P-Modifications**: Pattern `P\d+` (e.g., P00001) - Administrative modifications
- **Key Rule**: A database record is NOT a contract unless `modification_number = '0'`
- **Training Focus**: LLMs must never confuse transaction records with actual contracts

### 2. Contract Vehicle Taxonomy

**Primary Award Types** (from database analysis):

- `DELIVERY ORDER` (41.6M records) - Task orders under IDVs
- `PURCHASE ORDER` (9.4M records) - Simple purchases
- `BPA CALL` (6.6M records) - Calls against Blanket Purchase Agreements
- `DEFINITIVE CONTRACT` (1.8M records) - Standard contracts
- `DO` (2.3M records) - Delivery Orders (text format)
- `DCA`, `BPA`, `PO` - Various contract vehicles

**IDV Relationships**:

- `parent_award_id_piid` links task orders to their parent IDV
- `award_id_piid` is the specific task order number
- Example: Parent IDV `W912P916D0022` → Task Order `W912P919F0277`

### 3. Small Business Set-Aside Categories

**Major Set-Aside Types** (by volume):

- `SMALL BUSINESS SET ASIDE - TOTAL` (3.8M records, $338B)
- `8(A) SOLE SOURCE` (534K records, $105B)
- `SERVICE DISABLED VETERAN OWNED SMALL BUSINESS SET-ASIDE` (381K records, $65B)
- `8A COMPETED` (249K records, $66B)
- `HUBZONE SET-ASIDE` (88K records, $13B)
- `WOMEN OWNED SMALL BUSINESS` (45K records, $5B)

## Training Dataset Structure (Target: 1000+ Examples)

### Dataset 1: Contract Type Recognition (300 examples)

**Base Contracts** (75 examples):

```json
{
  "input": "What type of record is award_id_piid 'W50S6U24C0002' with modification_number '0'?",
  "output": "This is a BASE CONTRACT (original award). The modification_number='0' indicates this is the initial contract award, not a modification. Award details: DEFINITIVE CONTRACT for $482,389 to AC LOPEZ CONSTRUCTION INC for pavement maintenance at San Diego ANGS.",
  "metadata": {
    "record_type": "BASE_CONTRACT",
    "award_type": "DEFINITIVE CONTRACT",
    "modification_number": "0",
    "obligation": 482389.0
  }
}
```

**Modifications** (75 examples):

**Authoritative Definitions via USAspending API**:

- Get Glossary (endpoint): Returns JSON glossary terms and definitions to align model vocabulary with public definitions.
- Get Data Dictionary (endpoint): Returns JSON describing data elements, ensuring field-level consistency during training.
  - Use both to auto-generate “definition-context” snippets appended to training prompts when fields like `extent_competed`, `type_of_set_aside`, `award_type`, `idv_type`, and `type_of_contract_pricing` are present.
  - Cache locally and version with a timestamp and source URL for provenance.

```json
{
  "input": "Explain the relationship between records with contract_award_unique_key 'CONT_AWD_000001_2036_TPDOIT13D0001_2036' and modification_numbers '0', '1', '2', '3'.",
  "output": "This shows a contract lifecycle: mod '0' is the BASE CONTRACT (original award for $182,975 to XA SYSTEMS LLC), while mods '1', '2', '3' are MODIFICATIONS (administrative actions with $0 obligations). The base contract is the actual award; modifications are actions against that existing contract.",
  "metadata": {
    "contract_lifecycle": true,
    "base_contract_mod": "0",
    "modification_mods": ["1", "2", "3"]
  }
}
```

**IDV/Task Orders** (75 examples):

```json
{
  "input": "Explain the relationship between parent_award_id_piid 'NNG15SD20B' and award_id_piid '15M10419FA4100025'.",
  "output": "This is an IDV to Task Order relationship. The parent award 'NNG15SD20B' is the vehicle; '15M10419FA4100025' is a task/delivery order placed against it. Pursuit strategy should consider on-ramp options or teaming with vehicle holders.",
  "metadata": {
    "relationship_type": "IDV_TASK_ORDER",
    "parent_idv": "NNG15SD20B",
    "task_order": "15M10419FA4100025"
  }
}
```

## Authoritative References (Updated)

- `docs/CAPTUREINTEL.md` — Canonical schemas, Shipley milestone mapping, competitive intelligence, and dashboard specification. Use to seed schema-aware prompts and milestone-aligned examples.
- `docs/SQL_VISUALIZATION_QUERIES.md` — Canonical SQL powering charts; use query intent and dimensions/metrics to craft realistic Q&A pairs and teach the model factual anchors and aggregations.
- `docs/SHIPLEY_LLM_CURATED_REFERENCE.md` — Paraphrased Shipley-aligned training guidance (gates, checklists, competitive analysis, pricing, evaluation factors) for safe fine-tuning.
- USAspending API (read-only reference augmentation during dataset generation):
  - Glossary endpoint: JSON terms/definitions for vocabulary alignment.
  - Data Dictionary endpoint: JSON element definitions to standardize field semantics.
    Note: Cache responses under `data/reference/usaspending/` with date-stamped filenames and include the exact URL and retrieved-at timestamp in training metadata for provenance.
- SAM.gov v2/v4 APIs — Opportunity and entity contexts for M0–M3 capture examples.
- BLS OEWS v2 + CALC API — Pricing intelligence references for Shipley M2/M3 examples.

Notes:

- Store all fetched API JSON locally under `data/reference/` with date-stamped filenames; reference the exact version in training metadata for reproducibility.
- When a field appears with ambiguous values (e.g., `extent_competed` variants), normalize using the Data Dictionary definitions prior to training example generation.

**Set-Asides** (75 examples):

```json
{
  "input": "What does type_of_set_aside 'SERVICE DISABLED VETERAN OWNED SMALL BUSINESS SET-ASIDE' mean?",
  "output": "This is a SDVOSB set-aside, meaning the contract was restricted to competition among Service-Disabled Veteran-Owned Small Businesses only. This is one of the major small business contracting programs, representing $65B in obligations across 381K records in the database.",
  "metadata": {
    "set_aside_type": "SDVOSB",
    "program_purpose": "small_business",
    "market_size": "$65B"
  }
}
```

### Dataset 2: Database Schema Understanding (200 examples)

**Table Relationships**:

- `s3_processed.usaspending_prime_awards` - Main contracts table
- `s3_processed.usaspending_subawards_enriched` - Subcontracts with prime award details
- `s3_processed.mv_expiring_contracts` - Materialized view of contracts ending soon
- `s3_processed.mv_contract_net_obligations` - Contract-level obligation rollups

**Key Fields Training**:

- `contract_transaction_unique_key` vs `contract_award_unique_key`
- `federal_action_obligation` vs `potential_total_value_of_award`
- `extent_competed` categories and competition levels
- `action_type` meanings (CLOSE OUT, SUPPLEMENTAL AGREEMENT, etc.)

### Dataset 3: Business Intelligence Queries (300 examples)

**Competitor Analysis**:

```json
{
  "input": "Who are the top competitors in NAICS 541519 (Other Computer Related Services)?",
  "output": "Based on federal_action_obligation in NAICS 541519: 1) SCIENCE APPLICATIONS INTERNATIONAL CORPORATION ($750M+ contracts), 2) THUNDERCAT TECHNOLOGY LLC ($8M contract), 3) CDW GOVERNMENT LLC ($121K contract). Query: SELECT recipient_name, SUM(federal_action_obligation) FROM usaspending_prime_awards WHERE naics_code='541519' AND modification_number='0' GROUP BY recipient_name ORDER BY sum DESC;",
  "metadata": {
    "query_type": "competitor_analysis",
    "naics_code": "541519",
    "business_rule": "use_modification_0_for_contract_values"
  }
}
```

**Market Opportunity**:

```json
{
  "input": "Show me expiring contracts over $1M in the next 6 months.",
  "output": "Use mv_expiring_contracts materialized view: SELECT * FROM s3_processed.mv_expiring_contracts WHERE days_to_expiration <= 180 AND federal_action_obligation > 1000000 ORDER BY days_to_expiration, federal_action_obligation DESC; This identifies recompete opportunities with sufficient time for capture planning.",
  "metadata": {
    "query_type": "opportunity_identification",
    "shipley_milestone": "M0_opportunity_identification",
    "time_horizon": "6_months"
  }
}
```

### Dataset 4: Shipley Methodology Integration (200 examples)

**Milestone Mapping**:

- **M0** (Opportunity ID): Automated queries for new opportunities, expiring contracts
- **M1** (Assessment): Competitive landscape analysis, historical bidder patterns
- **M2** (Bid/No-Bid): Win probability based on past performance, competition density
- **M3** (Strategy): Price benchmarking, teaming partner identification

**Capture Intelligence**:

```json
{
  "input": "Analyze the competitive landscape for Army contracts in NAICS 541519.",
  "output": "Army (DEPT OF DEFENSE) NAICS 541519 analysis: 15 unique contractors, avg contract $2.1M, 73% competed, dominated by SAIC ($750M), followed by mid-tier players. Competition level: HIGH (avg 4.2 bidders). Shipley Assessment: Strong incumbent presence suggests need for differentiated solution and strategic teaming. Recommend M1 deep-dive on SAIC's approach and customer relationships.",
  "metadata": {
    "analysis_type": "competitive_landscape",
    "agency": "DEPT_OF_DEFENSE",
    "naics": "541519",
    "shipley_gate": "M1_assessment"
  }
}
```

## Training Methodology

### 1. Data Extraction Process

- **Stratified Sampling**: 25% base contracts, 25% modifications, 25% IDV/task orders, 25% set-asides
- **Value Distribution**: Mix of small ($10K-$100K), medium ($100K-$10M), large ($10M+) contracts
- **Agency Diversity**: Include DoD, VA, GSA, Treasury, State, NASA, and civilian agencies
- **Time Range**: FY2020-2024 to capture recent patterns and policy changes

### 2. Fine-Tuning Parameters

- **Base Model**: Llama 3.2 8B Instruct (q4_K_M quantization)
- **Training Format**: JSONL with input/output pairs + metadata
- **Context Length**: 4096 tokens (database schema + query + response)
- **Instruction Format**: Alpaca/ChatML compatible
- **Validation Split**: 80/20 train/validation

### 3. Evaluation Metrics

- **Contract Type Classification**: >95% accuracy on contract vs modification
- **SQL Generation**: Syntactically correct queries for 90% of business questions
- **Business Rule Compliance**: 100% adherence to "modification_number='0' for contracts"
- **Shipley Alignment**: Milestone-appropriate recommendations and analysis depth

## Dataset Generation Commands

### Extract Contract Samples:

```sql
-- Base contracts across different award types
SELECT 'BASE_CONTRACT', * FROM s3_processed.usaspending_prime_awards
WHERE modification_number = '0' AND federal_action_obligation > 100000
ORDER BY RANDOM() LIMIT 250;

-- Modifications showing contract lifecycle
SELECT 'MODIFICATION', * FROM s3_processed.usaspending_prime_awards
WHERE modification_number != '0' AND contract_award_unique_key IN (
  SELECT contract_award_unique_key FROM s3_processed.usaspending_prime_awards
  WHERE modification_number = '0' ORDER BY RANDOM() LIMIT 100
) ORDER BY contract_award_unique_key, modification_number;

-- IDV/Task order relationships
SELECT 'IDV_RELATIONSHIP', * FROM s3_processed.usaspending_prime_awards
WHERE parent_award_id_piid IS NOT NULL AND award_type IN ('DELIVERY ORDER', 'BPA CALL')
ORDER BY parent_award_id_piid, award_id_piid LIMIT 250;

-- Set-aside examples across categories
SELECT 'SET_ASIDE', * FROM s3_processed.usaspending_prime_awards
WHERE type_of_set_aside NOT IN ('NO SET ASIDE USED', '')
  AND type_of_set_aside IS NOT NULL
ORDER BY type_of_set_aside, RANDOM() LIMIT 250;
```

## Platform Compatibility

### Google Colab Integration:

- Dataset stored as `contracts_training_dataset.jsonl`
- Notebook with Ollama setup and fine-tuning pipeline
- Model evaluation scripts with business rule validation

### Unsloth.ai Configuration:

- Pre-configured training templates for Llama 3.2
- Quantization-aware training for 8-bit inference
- Custom evaluation metrics for contract domain

### Export Formats:

- **JSONL**: Primary training format
- **CSV**: Tabular data for analysis
- **Parquet**: Optimized for large-scale processing
- **HuggingFace Datasets**: Community sharing and validation

## References

- `docs/AGENTIC_LLM_PLAN.md`: LLM architecture, prompt, and fine-tuning strategy
- `docs/CAPTUREINTEL.md`: Shipley process mapping and capture intelligence
- `docs/PLANNING.md`: Project vision and milestone planning
- `docs/TASKS.md`: Dataset, prompt, and testing tasks
- `src/backend/data/models/data_models.py`: Data schemas and validation models
- `agent_test_cases.md`: Example queries and agent test cases
- Dashboard code in `src/frontend/visualizations/` and `src/frontend/ai/`

---

**This document is the starting point for all dataset and fine-tuning work. Update as you progress.**
