# Worked example (fictional): "Nimbus Books" bookkeeping app

All names and numbers here are invented for illustration. The CSV files in this folder hold the same fictional data so you can run the helper yourself.

## Situation

Nimbus Books launched an Android app in March 2026. Customers report that assistants still say it is iPhone-only.

## Truth sheet (excerpt)

```yaml
facts:
  platforms: { value: "iOS, Android, web", as_of: "2026-03-12", public_url: "https://example.com/download" }
  price:     { value: "Free for 1 user; Team 12 USD/month", as_of: "2026-06-01", public_url: "https://example.com/pricing" }
  owner:     { value: "Independent, founded 2021 in Lisbon", as_of: "2026-10-01", public_url: none }
retired_facts:
  - { fact: "iOS only", true_until: "2026-03" }
  - { fact: "9 USD/month", true_until: "2026-06" }
```

`owner` has no public page: that is already a finding.

## Baseline batch (2026-09-01)

12 core questions x 2 modes (search on/off) x 3 repeats = 72 answers.

```text
$ python3 scripts/standing.py tally examples/answers-before.csv --brand "Nimbus Books"
answers read: 72   brand mentioned: 22   rate  30.6%  (95% range  21.1% -  42.0%)
...
by family
  category             3/18   16.7%
  comparison           1/18    5.6%
  direct              18/18  100.0%
  problem              0/18    0.0%  <- never mentioned
```

Reading: the assistant knows the product when asked by name, but almost never suggests it on its own.

## Claims

```text
$ python3 scripts/standing.py claims examples/claims-before.csv
claims: 7   correct=2, stale=3, invented=1, conflated=1
wrong claims by fact (fix these first)
  platforms   2x  sources: own FAQ page /faq; comparison article 2025
  price       1x  sources: app directory listing
  owner       1x  sources: model memory (namesake company)
  bank_sync   1x  sources: no source found
```

## Repairs (in order)

1. Edit `/faq` (it still said "Android coming soon"); add "Updated March 2026: now on Android" to the homepage and pricing page.
2. Publish a plain About page with owner and founding year, to separate Nimbus Books from the unrelated Nimbus Cloud.
3. Update the app directory listing price.
4. Email the author of the 2025 comparison article with the store link.
5. Bank sync: the product does not offer it. Add a clear "What Nimbus Books does not do" line on the features page, because invented features thrive where limits are never stated.
6. Problem questions: write one honest guide, "How freelancers can track expenses offline on Android", with real steps and limits.

## Re-measure (2026-10-15)

```text
$ python3 scripts/standing.py compare examples/answers-before.csv examples/answers-after.csv
before: 22/72  30.6%
after : 26/72  36.1%
z = +0.71  ->  no detectable change
```

The report says plainly: claim accuracy improved (fewer stale platform claims), but the mention rate has not moved beyond noise yet. Next re-measure is set for six weeks later with five repeats on the problem questions.
