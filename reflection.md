# Reflection

## 1. Which issues were easiest and hardest to fix?
Easiest: docstrings, renaming `setExpiry` to `set_expiry`, and splitting the long line.
Hardest: the date format bug. Pylint never flagged it, and I only found it by
running the program and noticing that the expired permit still looked valid.
It took changing both `set_expiry` and `is_expired`.

## 2. Did the tools report anything wrong or unhelpful?
None of the tools gave a clearly wrong result, but some reports were less useful
than others:
- Pylint reported 9 missing-docstring messages out of 21 total. For a small
  script these are style issues, and they made the report look worse than the
  real problems justified.
- The tools disagree on line length. Pylint allows 100 characters by default and
  Flake8 allows 79, so a line can pass one tool and fail the other.
- The same bare `except` was reported twice, as W0702 by Pylint and E722 by
  Flake8. That makes the problem look bigger than it is.
- Bandit's warning about `random` is easy to dismiss for a campus project, but
  permit numbers should not be predictable, so it was worth fixing.

## 3. What did the tools miss?
Pylint, Flake8 and Bandit did not catch:
- the date format mismatch that made expired permits count as valid
- `register_permit` accepting an empty plate, None and an invalid zone ("Z")

Only running the code and reading the output showed these.

## 4. How would static analysis fit into your workflow?
Run the three tools before every commit, or automatically on each push (for
example with GitHub Actions), so problems are caught early. Keep tests alongside
them, because the tools cannot find logic bugs.

## Results
- Pylint: 6.32/10 before, 10.00/10 after
- Bandit: the `random` warning is gone after switching to `secrets`
- Flake8: clean after the fixes
