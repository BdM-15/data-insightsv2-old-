# Quickstart: Validate Capture Loop Flow

1. Configure data source (external ETL):
   - Provide PostgreSQL connection/DSN, database, schema, and view/table names for cleansed USASpending data [NEEDS CLARIFICATION]
   - Note: ETL/cleansing and refresh are out of scope for this project
2. Market slice:
   - Apply filters (agency, NAICS/PSC, set-aside, 6–24 month horizon)
   - Confirm dashboard renders core signals under 5 seconds
3. Expiring list:
   - View expiring contracts; verify incumbent identification and buckets (0–6, 6–12, 12–24)
4. Compare:
   - Load/import capability baseline CSV
   - Open “Compare” to view fit/gap
5. Generate themes:
   - Click “Generate Themes”; verify citations reference signals and comparisons
6. Export:
   - Export Capture Profile (Markdown) including filters, timestamps, model/version
   - Export Session Snapshot (JSON)

Success = Each step completes without errors and within target performance windows.
