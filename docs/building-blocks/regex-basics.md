# Building Block: Regex Basics for Parsing

## Goal

Extract reliable values from messy text using small, targeted patterns.

## Beginner Strategy

1. Normalize text first (case, spacing, line breaks as needed).
2. Match one field at a time with simple patterns.
3. Prefer section-limited matching over global matching.
4. Keep fallback behavior when a match fails.

## Intermediate Pattern Design

- Use named groups when extracting multi-part values to make code self-describing.
- Keep one regex per business concept instead of one giant pattern.
- Compile frequently reused patterns once if performance becomes noticeable.
- Add a narrow pre-check (`if "net pay" in line_lower`) before running expensive patterns.

## Example Progression

Start simple:

```python
r"net\s*pay\s*[:\-]?\s*([\d,]+\.\d{2})"
```

Then improve readability and resilience:

```python
r"(?P<label>net\s*pay)\s*[:\-]?\s*(?P<amount>[\d,]+(?:\.\d{2})?)"
```

Keep amount parsing separate from pattern matching so error handling stays explicit.

## Useful Pattern Habits

- Anchor with nearby keywords, not only numbers.
- Keep patterns readable; split complex parsing into multiple checks.
- Test patterns on real sample lines before scaling.

## Debugging Checklist

1. Print the exact raw line before matching.
2. Print normalized line.
3. Confirm section state (for section-based parsing).
4. Verify all expected capture groups are present.
5. Record unmatched but important lines in parse notes for follow-up.

## When Regex Is Not The Best Tool

- Input format is fully structured (use CSV/JSON parsing instead).
- Rules become unreadable (use a parser state machine).

## Maintainability Guardrail

If a regex cannot be explained in one short sentence, split it into smaller steps.
