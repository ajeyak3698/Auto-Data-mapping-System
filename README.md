# Auto-Data-mapping-System

Auto-Data-mapping-System (ADMS) is an opinionated, Jupyter-first toolkit for accelerating the work of data engineers, analysts, and ML practitioners who need to discover, align, and transform messy source datasets into clean, production-ready target schemas. This repository combines Python modules and interactive notebooks to make data mapping repeatable, explainable, and easy to iterate.

---

## Why ADMS exists

Mapping data from one schema to another is a common but often tedious task: column matching, type conversions, value normalization, and edge-case handling all make mapping brittle and time-consuming. ADMS provides a structured, semi-automated approach that reduces manual effort while keeping human-in-the-loop control through interactive notebooks and configurable rules.

## Highlights / Features

- Smart profiling: automatic inference of column types, missingness, unique values, and example values.
- Column matching suggestions using heuristics and similarity scoring.
- Transformation generation: suggested Python/pandas transformations for common cases (date parsing, normalization, type casting, categorical mapping).
- Rule-based overrides: specify mapping rules in JSON/YAML to enforce business logic.
- Notebook-driven exploration: step-by-step notebooks for profiling, mapping, testing and exporting results.
- Auditability and reproducibility: export mapping specifications and transformation scripts for review and productionization.

## Repository layout (what to look at first)

- `src/` — core Python modules (data profiling, matching engine, transformation generators).
- `notebooks/` — interactive Jupyter notebooks demonstrating end-to-end workflows, experiments, and troubleshooting.
- `examples/` — sample datasets and example mapping specifications (if present).
- `tests/` — unit and integration tests (run with pytest).
- `README.md` — this file.

If any of these directories are missing in your clone, explore the repository root to see where notebooks and modules are placed — the project is intentionally lightweight and notebook-driven.

## Quickstart

Prerequisites: Python 3.10+ recommended, Git, and optionally JupyterLab/Jupyter Notebook.

1. Clone the repo:

```bash
git clone https://github.com/ajeyak3698/Auto-Data-mapping-System.git
cd Auto-Data-mapping-System
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.\.venv\Scripts\activate  # Windows
```

3. Install dependencies (if `requirements.txt` exists):

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt`, you can still run notebooks by installing Jupyter and pandas: `pip install jupyterlab pandas numpy matplotlib`

4. Launch JupyterLab and open the notebooks folder:

```bash
jupyter lab
```

Open notebooks in `notebooks/` and run the cells to reproduce the demos and experiments.

## Typical workflow (conceptual)

1. Ingest: load source dataset(s) (CSV, Parquet, database export) into a pandas DataFrame.
2. Profile: run the profiling notebook to collect column statistics, sample values and inferred types.
3. Suggest: run the column-matching step to get suggested mappings between source and target schemas.
4. Refine: apply rule overrides (JSON/YAML) and edit suggested transformations interactively.
5. Validate: run small-batch transformations and unit tests to confirm correctness.
6. Export: save mapping spec and generated transformation script for deployment.

## Mapping rule example

Here is a minimal example of a mapping specification you can use to override or pin mapping decisions (YAML or JSON accepted):

```yaml
source: sample_customers.csv
target_schema:
  - name: customer_id
    type: integer
    source_candidates: ["id", "customerId", "cust_id"]
  - name: signup_date
    type: datetime
    source_candidates: ["signup", "created_at"]
    transform: "pd.to_datetime(value, errors='coerce')"
  - name: country
    type: category
    map_values:
      UK: ["United Kingdom", "U.K."]
      US: ["United States", "USA"]
```

Save this file as `mappings/my_mapping.yaml` and point the notebook or script to it to enforce the mapping.

## Example (pseudo-code)

Below is a short illustrative example; your concrete API and module names may differ — consult the `src/` modules and notebooks for the real entry points.

```python
# high-level usage flow (pseudocode)
from pathlib import Path
import pandas as pd

# 1. load
src_df = pd.read_csv('examples/raw/customers.csv')

# 2. profile
# profiler = src.profiler.Profiler()
# report = profiler.profile(src_df)

# 3. suggest mappings
# suggester = src.matcher.Matcher()
# candidate_mappings = suggester.suggest(src_df, target_schema)
# 4. apply rules and generate transform
# transformer = src.transformer.Transformer.from_spec('mappings/my_mapping.yaml')
# transformed = transformer.apply(src_df)
```

## Testing

If a `tests/` directory exists, run the test suite with pytest:

```bash
pip install -r requirements-dev.txt  # if present
pytest -q
```

## How to contribute

We welcome contributions! A few ways to help:

- Open issues describing feature requests, bugs or UX improvements.
- Add examples or new notebooks that show real mapping scenarios.
- Improve the profiling, matching heuristics or transformation templates.
- Add tests for edge cases (null-heavy columns, ambiguous column names, locale-specific formats).

Please follow these lightweight guidelines when opening PRs: keep changes focused, include reproducible examples in notebooks, and add or update tests when you add behavior.

## Roadmap & Ideas

- Integrate ML-based column matching (learned name and value similarity).
- Add connectors to databases and streaming sources.
- Output guarded transformation functions for safe production deployment.
- UI for visual mapping review and approval.

## Troubleshooting tips

- If cells error due to missing packages, install them into the active environment.
- If mapping suggestions look off, add manual rules in a mapping spec and re-run the pipeline.
- For large datasets, profile and test on a sampled subset before applying transforms to the whole dataset.
