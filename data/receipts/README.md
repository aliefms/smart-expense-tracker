# Receipt Test Dataset

This directory contains receipt inputs used to develop and verify the Smart
Expense Tracker.

## Directories

- `samples/`: Synthetic or privacy-safe receipt images that may be committed
- `ground_truth/`: Correct expected JSON for each synthetic receipt
- `private/`: Real personal receipts that must never be committed

## Test Cases

| Image | Difficulty | Purpose |
|---|---|---|
| `receipt_001_clear.png` | Easy | Clear OCR baseline |
| `receipt_002_multi_item.png` | Medium | Multiple items, tax, and discount |
| `receipt_003_low_quality.png` | Difficult | Low contrast, rotation, and blur |

## Naming Convention

```text
receipt_NNN_description.png
receipt_NNN_description.json