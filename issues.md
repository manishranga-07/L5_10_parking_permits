| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Insecure random for permit numbers | Security (Bandit B311) | 11 | `random.randint` is predictable, so permit numbers can be guessed | Use `secrets.randbelow` |
| Wrong date format makes expired permits look valid | Bug | 25-31, 51-52 | `setExpiry` accepts any string. `is_expired` fails to parse it, and the bare except returns False | Validate the date in `set_expiry`, and return True when the date is missing or invalid |
| No input validation in register_permit | Bug | 9-17 | Accepts empty plate, None and zone "Z", and `ZONES` is never used | Reject a missing plate or a zone not in `ZONES` |
| Mutable default argument | Bug (Pylint W0102) | 9 | `zone_records=[]` is shared between calls | Use `None` and create the list inside |
| Bare except clauses | Error handling (W0702, E722) | 16, 22, 29, 43 | Hides real errors, and `revoke_permit` silently ignores failures | Catch specific exceptions, or use `permits.pop(plate, None)` |
| open() without `with` or encoding | Resource handling (R1732, W1514) | 42, 47 | File handles are never closed explicitly and the encoding is unspecified | Use `with open(..., encoding="utf-8")` |
| Global statement | Design (W0603) | 40 | Rebinds a global variable inside a function | Use `permits.clear()` and `permits.update(data)` |
| Missing docstrings | Style (C0114, C0116) | 1, 9, 19, 25, 32, 39, 46, 51, 54 | The module and 8 functions have no docstrings | Add a one-line docstring to each |
| Naming and line length | Style (C0103, C0301) | 51, 13 | `setExpiry` is not snake_case, and one line is 110 characters | Rename to `set_expiry` and split the dict across lines |
