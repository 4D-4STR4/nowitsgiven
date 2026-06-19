# Market & Stock Research

A workspace for market and equity research — notes, data, and deep-dive dossiers.

> **Note on hosting:** This folder is staged inside the `nowitsgiven` repo because the
> GitHub integration for this session is scoped to a single repo and cannot create a
> new standalone repository. It is designed to be split out into its own dedicated
> `market-research` repo later via:
> ```
> git subtree split -P market-research -b market-research
> ```

## Structure
```
market-research/
├── ONDS/            # Deep-dive dossier: Ondas Inc. (NASDAQ: ONDS)
│   └── sections/    # Modular research sections (financials, TAM, competition, etc.)
├── data/            # Raw / processed datasets
├── notebooks/       # Analysis notebooks
└── scripts/         # Data-fetching / utility scripts
```

## Research index
| Ticker | Company | Status | Folder |
|--------|---------|--------|--------|
| ONDS | Ondas Inc. | Complete | [`ONDS/`](./ONDS/) |

## Automation
The ONDS dossier can auto-refresh on a schedule and open a PR with updates.
See [`AUTOMATION.md`](./AUTOMATION.md) for what it does and the one-time setup.

## Disclaimer
All content here is for informational and educational purposes only. It is **not financial advice**.
Research is AI-assisted and may contain errors or become outdated. Always do your own due diligence.
