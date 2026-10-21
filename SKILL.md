---
name: answer-standing
description: Measure and repair how AI assistants (ChatGPT, Claude, Gemini, Perplexity, Copilot, DeepSeek, Doubao, Kimi and others) answer questions about a product, company, person or project. Use when someone asks "does ChatGPT recommend us?", "AI keeps getting our price wrong", "why do assistants suggest our competitor?", "track our AI visibility", or wants a before/after check that a GEO/AEO change actually worked. Produces a truth sheet, a question deck, a repeated-sampling log, graded claims traced to their sources, a source-first repair plan and an honest standing report with uncertainty ranges.
---

# Answer Standing

## What this is

People now ask an assistant before they ask a search engine. "Which note app works offline?" "Is Acme cheaper than Brightly?" The answer they get is a short paragraph that names two or three products and states a few facts about each. If your product is missing from that paragraph, framed as a warning, or described with last year's price, you lose people you never see.

**Answer Standing** is a disciplined way to find out where a subject actually stands in AI answers and to fix what is wrong at the place it comes from. It treats the assistant as a witness, not an oracle: you ask the same questions several times, write down exactly what it says, check every statement about the subject against a sheet of verified facts, trace each wrong statement to the page or listing it most likely came from, repair that source, and measure again with the same protocol.

It solves three common problems:

1. **Anecdote instead of measurement.** One screenshot of one answer proves nothing. Answers vary from run to run, by mode (search on or off), by language and by region. This skill samples repeatedly and reports rates with a range, so nobody celebrates noise.
2. **Visibility without accuracy.** Being mentioned is worthless if the assistant says you have no free plan when you do. This skill grades every claim, not only mentions.
3. **Fixing the symptom.** You cannot edit an AI's answer. You can edit, or ask someone to edit, the pages it reads. This skill always ends in a concrete fix on a concrete source, and a date to re-measure.

## When to use it

- A founder, marketer or maintainer wants to know if assistants recommend them for the questions buyers really ask.
- An assistant repeatedly states something false or outdated: price, availability, ownership, a discontinued feature, a scandal that belongs to a namesake.
- A team shipped GEO/AEO work (new pages, structured data, listings) and needs to know whether anything changed.
- Before a launch or rename, to record a baseline.
- A person (author, researcher, public figure) wants to check how they are described.

Do **not** use it to manipulate answers: no fake reviews, no undisclosed paid placements, no mass-produced look-alike articles, no editing third-party pages you are not allowed to edit. Those tactics are dishonest and tend to backfire once detected.

## The working folder

Everything lives in one folder (default `standing/`) so the next run can reuse it:

| File | What it holds |
| --- | --- |
| `truth-sheet.yaml` | verified facts, each with an "as of" date and the public URL that states it |
| `questions.csv` | the question deck, tagged by family, with a core subset |
| `answers/<batch>/` | the raw answer text, one file per answer, never edited |
| `answers.csv` | one row per answer read: mention, position, framing, all products named |
| `claims.csv` | each statement about the subject, its verdict, the matching fact, likely source, fix |
| `repairs.md` | the repair plan, ordered |
| `report-<date>.md` | the one-page standing report |

Run `python3 scripts/standing.py init standing/` to create blank templates. The script needs only Python 3.

## Steps

### 1. Pin down the subject and the arena

Ask at most three questions, and skip any you can answer from context:

- What exactly is the subject (name, URL, the category it competes in)?
- Which assistants matter, and in which language and region? Default to the one or two the audience really uses, not all of them.
- Who is the buyer or reader, and what problem brings them to the question?

Write down namesakes and confusable products now. Half of all "wrong" answers turn out to be about someone else with a similar name.

### 2. Build the truth sheet

Collect the facts an answer could get right or wrong: what it is, who it is for, price and plans, platforms, availability by region, owner, founding date, key limits. For each fact record the value, an `as_of` date, and the public URL where anyone can read it.

Two rules:

- **A fact with no public source is a finding.** If the free plan is only described inside the app, assistants cannot know it. Mark `public_url: none` and put "publish this" on the repair list.
- **Keep retired facts.** Old prices and dropped features are exactly what stale answers repeat; listing them lets you recognise a "stale" verdict instantly.

Check that your own pages agree with each other. Contradictions between the pricing page, the docs and an app store listing are the most common self-inflicted cause of wrong answers.

### 3. Write the question deck

Write 16 to 30 questions in the words real people use (search forums, support tickets, sales calls, community threads). Cover four families:

| Family | Example | What it tests |
| --- | --- | --- |
| category | "best offline note app for a small team" | are you on the shortlist at all |
| comparison | "Acme vs Brightly for invoicing" | how you are framed against a rival |
| direct | "how much does Acme cost?" | accuracy of facts about you |
| problem | "how do I share notes without the internet?" | do you come up when the user does not know the category name |

Mark 8 to 12 as `core`. Core questions are the ones you will re-ask every time, word for word. Never reword a core question between batches; a new wording is a new question.

### 4. Sample with a fixed protocol

For each core question and each chosen assistant, collect **at least 3 answers** (5 is better for the questions that matter most). Use a fresh conversation each time, signed out or with memory and custom instructions off, and note:

- `date`, `engine` (assistant and model if visible), `mode` (search/browse on or off), and language/region.
- Save the full answer text verbatim to `answers/<batch>/<question>-<engine>-<repeat>.md`, including any cited links.

If an API is available, automated sampling is fine, but keep API answers in their own batch: API and consumer app answers often differ. If you cannot reach an assistant yourself, give the user the exact questions and ask them to paste the answers back.

A batch should be collected within a few days; spread over weeks it measures drift, not standing.

### 5. Read every answer the same way

For each answer fill one row of `answers.csv`:

- `mentioned`: was the subject named (y/n)?
- `position`: if several products were named, at which place was the subject named (1 = first)?
- `framing`: `rec` (recommended or praised), `neutral`, or `warn` (cautioned against, criticised).
- `names`: every product named, separated by `;`. This feeds share of voice.

Then pull each statement about the subject into `claims.csv` as one short, checkable sentence ("free plan limited to 3 users"). Ignore opinions you cannot check.

### 6. Grade the claims

Compare each claim with the truth sheet and give one verdict:

| Verdict | Meaning | Typical cause |
| --- | --- | --- |
| correct | matches a current fact | |
| stale | was true once, matches a retired fact | old pages, old listings, model memory |
| wrong | contradicts a current fact | inconsistent own pages, third-party error |
| invented | no basis anywhere | the assistant filled a gap; usually the fact is not public |
| conflated | belongs to a namesake or a competitor | similar names, merged entities |
| unverifiable | cannot be checked against the sheet | add the fact to the sheet or drop the claim |

Put the matching truth-sheet key in `truth_key` so errors can be grouped by fact.

### 7. Trace each wrong claim to a source

For every non-correct claim, look for where it came from, in this order:

1. Links the answer itself cited.
2. Your own pages, old blog posts, cached docs, changelogs that still state the old fact.
3. Listings you control: app stores, marketplaces, directories, social bios, package registries.
4. Third parties: review sites, comparison articles, forum threads, encyclopedic pages, news.
5. Search the exact wrong phrase; the original wording often survives somewhere.

If nothing turns up and the answer cited nothing, record `source: model memory`. That is the slowest error to fix; the lever is to make the correct fact abundant, consistent and dated on pages the assistant can read.

### 8. Plan repairs, sources first

Order `repairs.md` by how many wrong answers a fix addresses and how directly you control the source:

1. **Your own site.** Correct every page that states the fact; make the current value easy to read in plain HTML (not only in images or scripts); add a dated note such as "Updated October 2026: the Team plan now includes 10 users"; make sure AI and search crawlers are not blocked from those pages.
2. **Structured, plain facts.** A short, factual "facts" or "about" page and accurate structured data help machines read the facts; they are not a ranking trick.
3. **Listings you control.** Update every profile and store listing so it says the same thing as the site.
4. **Third parties.** Ask for corrections politely with the evidence link. Where you post yourself (forums, Q&A), disclose who you are.
5. **Fill gaps with genuinely useful content.** For a problem question where you never appear, write one honest page that answers it with real specifics (numbers, steps, limits), not a promotional piece.

For every repair note the URL, the change, the owner and the date done.

### 9. Wait, then re-measure the same way

Allow time for pages to be recrawled and indexed: days for search-backed modes, often weeks or longer for answers from model memory. Then collect a new batch with the **same core questions, same engines, same mode, same number of repeats**. Run:

```bash
python3 scripts/standing.py compare standing/answers-before.csv standing/answers-after.csv
```

It reports both rates with 95% ranges and a two-proportion test. Only call a change "real" when the test says so. "Maybe" means collect more repeats, not write a victory post.

### 10. Write the standing report

One page, in the user's language:

- Subject, engines, mode, dates, number of questions and answers read.
- Mention rate with range, first-named rate, framing mix, share of voice versus the top rivals.
- Claim accuracy with range and the three most damaging wrong claims, each with its traced source and repair status.
- What changed since the last batch, and whether the change is real or noise.
- Next re-measure date.

## Example

> **User:** ChatGPT keeps telling people our bookkeeping app has no Android version. We launched one in March.
>
> **Agent:** builds a truth sheet (`platforms: iOS, Android, web; as_of 2026-03-12; public_url /download`) and notes the retired fact "iOS only (until 2026-03)". Writes 12 core questions including "bookkeeping app for Android for freelancers". Collects 3 answers per question from ChatGPT with search off and on (72 answers). Tally: mentioned in 21/72 (29%, range 20-41%); in direct questions, 9 of 14 platform claims are stale. Tracing finds the app's own FAQ page still says "Android coming soon" and two comparison articles from 2025 say iOS only. Repairs: fix the FAQ the same day, add a dated "Now on Android" line to the homepage and pricing page, update the product directory listing, email both article authors with the store link. Six weeks later the same 72 answers show stale platform claims dropping from 9/14 to 2/15; `compare` reports the mention rate change (29% to 38%) as "maybe", so the report says so honestly.

More worked examples are in `examples/`.

## Tips

- Search-on and search-off answers are different products; never mix them in one rate.
- Three repeats is a floor, not a target. With 20 answers a 30% rate has a range of roughly 15-52%.
- Read the cited links even when the answer is right; they show which sources the assistant trusts in your category.
- A rival that is named first everywhere usually has one strong, plain, up-to-date comparison or "best of" page that you lack. Study what that page states, then write your own honest version.
- Never promise a result. No one controls what an assistant says; you control the evidence it can find.
- Keep the raw answers forever. They are the only proof of what was said on a given date.
