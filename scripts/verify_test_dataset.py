"""Validate the synthetic receipt test dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RECEIPTS_DIR = PROJECT_ROOT / "data" / "receipts"
SAMPLES_DIR = RECEIPTS_DIR / "samples"
GROUND_TRUTH_DIR = RECEIPTS_DIR / "ground_truth"
MANIFEST_PATH = RECEIPTS_DIR / "manifest.json"

REQUIRED_RECEIPT_FIELDS = {
    "merchant_name",
    "transaction_date",
    "currency",
    "subtotal",
    "tax",
    "discount",
    "total",
    "items",
}

REQUIRED_ITEM_FIELDS = {
    "name",
    "quantity",
    "unit_price",
    "line_total",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load and return a JSON object."""

    with path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a JSON object")

    return data


def validate_image(path: Path) -> None:
    """Check that an image exists, opens correctly, and has useful dimensions."""

    if not path.exists():
        raise FileNotFoundError(f"Image is missing: {path}")

    try:
        with Image.open(path) as image:
            image.verify()

        with Image.open(path) as image:
            width, height = image.size
            image_format = image.format

    except UnidentifiedImageError as error:
        raise ValueError(f"Invalid image: {path}") from error

    if width < 500 or height < 500:
        raise ValueError(
            f"{path.name} is too small: {width}x{height}"
        )

    print(
        f"[OK] Image: {path.name} "
        f"({image_format}, {width}x{height})"
    )


def validate_ground_truth(path: Path) -> None:
    """Check one ground-truth JSON file."""

    if not path.exists():
        raise FileNotFoundError(f"Ground truth is missing: {path}")

    receipt = load_json(path)

    missing_fields = REQUIRED_RECEIPT_FIELDS - receipt.keys()

    if missing_fields:
        raise ValueError(
            f"{path.name} is missing fields: {sorted(missing_fields)}"
        )

    if not isinstance(receipt["items"], list):
        raise TypeError(f"{path.name}: items must be a list")

    for item_number, item in enumerate(receipt["items"], start=1):
        if not isinstance(item, dict):
            raise TypeError(
                f"{path.name}: item {item_number} must be an object"
            )

        missing_item_fields = REQUIRED_ITEM_FIELDS - item.keys()

        if missing_item_fields:
            raise ValueError(
                f"{path.name}: item {item_number} is missing "
                f"{sorted(missing_item_fields)}"
            )

    if receipt["total"] is not None and not isinstance(
        receipt["total"],
        (int, float),
    ):
        raise TypeError(
            f"{path.name}: total must be a number or null"
        )

    print(
        f"[OK] JSON:  {path.name} "
        f"({len(receipt['items'])} items)"
    )


def main() -> None:
    """Validate every dataset entry listed in the manifest."""

    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "manifest.json is missing. Run the generator first."
        )

    manifest = load_json(MANIFEST_PATH)
    receipt_entries = manifest.get("receipts")

    if not isinstance(receipt_entries, list) or not receipt_entries:
        raise ValueError(
            "manifest.json must contain a non-empty receipts list"
        )

    for entry in receipt_entries:
        image_path = SAMPLES_DIR / entry["image"]
        ground_truth_path = GROUND_TRUTH_DIR / entry["ground_truth"]

        print(
            f"\n[CHECK] {entry['image']} "
            f"(difficulty: {entry['difficulty']})"
        )

        validate_image(image_path)
        validate_ground_truth(ground_truth_path)

    print(
        f"\n[DONE] Dataset verification passed: "
        f"{len(receipt_entries)} receipt cases."
    )


if __name__ == "__main__":
    main()