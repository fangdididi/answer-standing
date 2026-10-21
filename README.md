**English** | [简体中文](README.zh-CN.md)

# Answer Standing

**Find out how AI assistants really describe your product, prove it with numbers, and fix wrong answers at their source.**

When someone asks ChatGPT, Claude, Gemini, Perplexity, Copilot, DeepSeek, Doubao or Kimi "what's the best tool for X?", the answer names a few products and states a few facts. Answer Standing is an agent skill that measures whether your product (or company, project, or your own name) is in those answers, whether what is said is true, where the wrong statements come from, and whether your fixes actually changed anything.

It treats the assistant as a witness: ask the same questions several times, record every answer verbatim, grade each statement against verified facts, trace errors to pages and listings, repair those sources, then re-measure with the same protocol and an honest statistical test.

## Why it exists

- **One screenshot is not a measurement.** Answers vary by run, mode, language and region. The skill samples repeatedly and reports rates with 95% ranges.
- **Being mentioned is not enough.** A mention with the wrong price or a namesake's scandal can hurt more than silence. Every claim gets a verdict.
- **You can't edit an answer, only its sources.** Every wrong claim ends in a concrete fix on a concrete URL and a date to re-check.
- **No wishful thinking.** A built-in comparison tells you whether a change is real, maybe, or just noise.

## Features

- Truth sheet with `as_of` dates, public URLs, namesakes and retired facts
- Four-family question deck (category, comparison, direct, problem) with a frozen core set
- Fixed sampling protocol: fresh sessions, mode tracking, 3+ repeats, raw answers archived
- Per-answer reading: mention, position, framing (recommended / neutral / warned), share of voice
- Six claim verdicts: correct, stale, wrong, invented, conflated, unverifiable
- Source tracing ladder from cited links to "model memory"
- Source-first repair plan with honesty guardrails (no fake reviews, no undisclosed posting)
- `standing.py` helper (Python 3, no dependencies): `init`, `tally`, `claims`, `compare`
- One-page standing report template

## Installation

The skill is the folder containing `SKILL.md` (English) and `SKILL.zh-CN.md` (Chinese). Copy the whole folder so the `scripts/` and `templates/` come with it.

**Claude Code**

```bash
git clone https://github.com/fangdididi/answer-standing.git ~/.claude/skills/answer-standing
```

**Codex / agents that read `~/.agents/skills`**

```bash
git clone https://github.com/fangdididi/answer-standing.git ~/.agents/skills/answer-standing
```

**Cursor** (project rules / skills folder)

```bash
git clone https://github.com/fangdididi/answer-standing.git .cursor/skills/answer-standing
```

**Any other agent**: paste the contents of `SKILL.md` into its instructions, or ask it to install the skill from this repository URL.

## Usage

Start a conversation with something like:

- "Check how ChatGPT and Perplexity talk about our app, acme.example."
- "AI assistants keep saying we have no free plan. Find out why and fix it."
- "We updated our pricing pages a month ago. Did AI answers change?"
- "Which competitor do assistants recommend instead of us, and why?"

The agent will ask up to three questions, build the working folder `standing/`, and walk through the ten steps. You can also run the helper directly:

```bash
python3 scripts/standing.py init standing/
python3 scripts/standing.py tally standing/answers.csv --brand "Acme"
python3 scripts/standing.py claims standing/claims.csv
python3 scripts/standing.py compare standing/answers-before.csv standing/answers-after.csv
```

## Example output

```text
answers read: 72   brand mentioned: 22   rate  30.6%  (95% range  21.1% -  42.0%)
by family
  category      3/18   16.7%
  comparison    1/18    5.6%
  direct       18/18  100.0%
  problem       0/18    0.0%  <- never mentioned

claims: 7   correct=2, stale=3, invented=1, conflated=1
wrong claims by fact (fix these first)
  platforms   2x  sources: own FAQ page /faq; comparison article 2025

before: 22/72  30.6%
after : 26/72  36.1%
z = +0.71  ->  no detectable change
```

See [`examples/example-en.md`](examples/example-en.md) (a product) and [`examples/example-zh.md`](examples/example-zh.md) (a person). All example data is fictional.

## File structure

```text
answer-standing/
├── SKILL.md               # skill instructions (English)
├── SKILL.zh-CN.md         # skill instructions (Chinese)
├── README.md
├── README.zh-CN.md
├── LICENSE
├── scripts/
│   └── standing.py        # init / tally / claims / compare
├── templates/
│   ├── truth-sheet.yaml
│   ├── questions.csv
│   ├── answers.csv
│   └── claims.csv
└── examples/
    ├── example-en.md
    ├── example-zh.md
    ├── answers-before.csv
    ├── answers-after.csv
    └── claims-before.csv
```

## Principles

- Only verified facts; unknown stays unknown.
- No promised outcomes; results are reported with their uncertainty.
- No manipulation: no fake reviews, astroturfing, or mass look-alike content.

## License

MIT © fangdididi
