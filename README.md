# Unique LLM Bench

A personal LLM evaluation bench built on [promptfoo](https://promptfoo.dev), using hand-curated question sets with exact-match answers. Tests are run manually via GitHub Actions against models served through [OpenRouter](https://openrouter.ai).

---

## How it works

Question sets live in `question-sets/`. When you're ready to run an eval, copy or move whichever files you want tested into the repo root. The GitHub Actions workflow picks up any `.yaml` file at the root level and runs them all.

```
unique-llm-bench/
├── .github/
│   └── workflows/
│       └── promptfoo.yml       # Manual trigger workflow
├── question-sets/              # Storage — ignored by the workflow
│   └── mtg_promptfoo_qa.yaml
├── promptfoo.config.base.yaml  # Shared provider/model definitions
└── my-active-test.yaml         # Files at root get picked up and run
```

---

## Running an eval

1. Move the question set(s) you want to test from `question-sets/` into the repo root
2. Commit and push (or just trigger from the current branch)
3. Go to **Actions → Promptfoo Eval → Run workflow**
4. When the run completes:
   - The **share link** (hosted on app.promptfoo.dev) appears in the Actions log
   - `results.html`, `results.json`, and `results.csv` are available as a downloadable artifact from the run summary page
5. Move your test files back to `question-sets/` when done

---

## Question sets

| File | Description | Answer format |
|------|-------------|---------------|
| `mtg_promptfoo_qa.yaml` | Magic: The Gathering knowledge + card oracle text | Exact match / JSON |

### Answer formats

**Knowledge questions** expect a plain string exact match, e.g.:

```
Commander, Legacy, Modern, Pauper, Pioneer, Standard, Vintage
```

**Card text questions** ask the model to output a JSON object for 3 cards at a time:

```json
{
  "Sol Ring": {
    "mana_cost": "{1}",
    "type_line": "Artifact",
    "oracle_text": "{T}: Add {C}{C}.",
    "rarity": "Uncommon"
  }
}
```

> **Note on fuzzy matching:** Some cards (e.g. Cyclonic Rift) have multiple accepted answer variants. Those questions include a note recommending a `contains` or partial-match assertion rather than strict equals — see the comments in the YAML.

---

## Adding a new question set

1. Create a new `.yaml` file in `question-sets/`
2. Follow the structure in `mtg_promptfoo_qa.yaml` — each question needs at minimum an `id`, `question`, and `answer`
3. Add a row to the table above

For exact-match card text questions, always verify oracle text against [Scryfall](https://scryfall.com) before committing — printed card text and oracle text often differ, and even well-known cards get errata over time.

---

## Providers

Models are accessed via OpenRouter. Add or swap models in `promptfoo.config.base.yaml` or directly in a question set's `providers` block. The OpenRouter model slug format is:

```
openrouter:<author>/<model-slug>
```

Browse available models at [openrouter.ai/models](https://openrouter.ai/models).

---

## Secrets

| Secret | Where to add | Used for |
|--------|-------------|----------|
| `OPENROUTER_API_KEY` | Repo Settings → Secrets → Actions | All model calls |

---

## Outputs

Each run produces three output formats, all uploaded as a GitHub Actions artifact (retained for 30 days):

| File | Use |
|------|-----|
| `results.html` | Visual report — open in browser |
| `results.json` | Full structured results for scripting |
| `results.csv` | Quick review in a spreadsheet |

A public share link is also printed to the Actions log via `promptfoo share`.

---

## Tech stack

- [promptfoo](https://promptfoo.dev) — eval runner
- [OpenRouter](https://openrouter.ai) — model API gateway
- [GitHub Actions](https://docs.github.com/en/actions) — CI runner (manual trigger only)
