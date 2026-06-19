# Automated Dossier Refresh

The ONDS dossier can refresh itself on a schedule via a GitHub Action:
[`.github/workflows/refresh-onds-dossier.yml`](../.github/workflows/refresh-onds-dossier.yml).

## What it does
- Runs **on demand only** — you trigger it from **Actions → "Refresh ONDS Dossier" → Run workflow**. There is intentionally **no cron schedule**, so it's not an unattended autonomous loop; every run is human-initiated.
- Uses the Claude Code GitHub Action to re-research the latest verified figures (price, newest quarter, backlog, guidance, new SEC filings / press releases, new catalysts).
- Updates `market-research/ONDS/DOSSIER.md` (and any sections whose figures materially changed), preserving structure and citations.
- **Opens a pull request** with a summary of what changed — it never pushes to a protected branch directly, so you review before merging.

> Want it scheduled later? Add a `schedule:` trigger with a `cron` line to the workflow (e.g. `0 13 * * 1` for weekly).

## One-time setup (required)
1. **Add the API key secret:** repo **Settings → Secrets and variables → Actions → New repository secret**, name it `ANTHROPIC_API_KEY` (get one at https://console.anthropic.com/).
2. **Allow PR creation:** **Settings → Actions → General → Workflow permissions** → enable *"Allow GitHub Actions to create and approve pull requests."*
3. Trigger it from **Actions → "Refresh ONDS Dossier" → Run workflow** whenever you want a refresh.

## Notes
- The workflow enforces a zero-hallucination rule: every changed figure must trace to a cited source, and unverifiable changes are left as-is with an `UNVERIFIED` note.
- It distinguishes audited SEC figures from company-provided (press-release / non-GAAP) figures.
- Cost is roughly one Claude Code research run per trigger; tune `--max-turns` / cadence to manage spend.
- This is informational research automation only — **not financial advice.**
