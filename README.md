# Health Camp Coverage Analyzer 🏥

An interactive, production-grade Python dashboard built with **Streamlit** and **Plotly** for public health organizations, medical NGOs, and healthcare administrators.

## Features

- **📊 Executive Overview**: High-level KPIs, geospatial map of health camp locations, district population coverage gaps, and monthly patient screening & referral trends.
- **🩺 Clinical & Demographics**: Age/gender cohort breakdown, patient risk stratification (low risk, moderate risk, urgent referral), and disease prevalence comparison across camp types.
- **🚑 Logistics & Cost Efficiency**: Doctor, nurse, and CHW deployment ratios per organizer, cost per patient screened, and quadrant scatter plot analyzing budget allocation efficiency.
- **📋 Camp Directory & Data Explorer**: Searchable, filterable ledger with custom HTML table formatting, status badges, and one-click CSV dataset export.
- **🔮 Coverage Scenario Simulator**: Interactive what-if planning tool to project screening coverage gains by adjusting medical staff and budget allocations.
- **🎨 Theme Support**: Dark/Light mode toggle with responsive UI styling.

## Directory Structure

```
health_camp_coverage_analyzer/
├── .venv/
├── data/
│   └── health_camps.csv
├── generate_data.py
├── app.py
├── requirements.txt
└── README.md
```

## Quick Start

1. **Activate Virtual Environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Generate Synthetic Data** (Automated on first run, or run manually):
   ```powershell
   python generate_data.py
   ```

3. **Run Dashboard**:
   ```powershell
   streamlit run app.py
   ```
