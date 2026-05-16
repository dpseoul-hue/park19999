# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This App Does

A Korean tax office field-visit schedule form (일정표) for the Seoul National Tax Service. It lets field officers record arrival, consultation, and departure times for each taxpayer visit, plus a remark (e.g. 부재중/absent, 면담완료/interview complete). The page is designed to be printed on A4 paper.

## Running the App

```bash
pip install flask
python app.py
```

The dev server runs at `http://127.0.0.1:5000` with `debug=True`.

## Architecture

The entire app is three files:

- **`app.py`** — Flask app with two routes:
  - `GET /` — renders `templates/index.html` passing the full `data.json` payload
  - `POST /api/update/<idx>` — updates a single visit record by index; accepts a JSON body with any subset of `{arrive, consult, depart, remark}`
- **`data.json`** — the sole data store (no database). Top-level keys: `title`, `date`, `team`, `officials` (list), `visits` (list of visit objects). Mutated in-place by `save_data()`.
- **`templates/index.html`** — Jinja2 template that renders the full table and embeds all interactivity inline via `<script>`. Two interaction patterns:
  - **Time cells** (`arrive`, `consult`, `depart`): click-to-edit — a `<input>` is injected on click, removed on blur/Enter, and auto-saved.
  - **Remark cell**: a `<select>` with preset Korean values plus a `직접입력` (custom) option that reveals a text `<input>`. Both call `saveField()` on change.
  - `saveField(idx, field, value)` POSTs to `/api/update/${idx}` immediately — there is no explicit save button.
- **`static/style.css`** — styles for both screen and print. `.no-print` / `.print-only` classes toggle visibility at `@media print`. The `.page` div is sized at 210mm × 297mm (A4).

## Data Shape

Each entry in `data.visits` has:
```json
{
  "order": 1,
  "name": "...",
  "note_name": "...",
  "address": "...",
  "arrive": "",
  "consult": "",
  "depart": "",
  "remark": ""
}
```

`order`, `name`, `note_name`, and `address` are static (edited directly in `data.json`). `arrive`, `consult`, `depart`, and `remark` are the live editable fields persisted via the API.

## Print Behaviour

The toolbar (print button) and all form controls are hidden in print via `.no-print`. The `.remark-text` `<span>` (which mirrors the selected remark value) is shown only in print via `.print-only`. Ensure any new editable UI follows this same pattern.
