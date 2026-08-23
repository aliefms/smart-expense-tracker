"""Generate synthetic receipt images and matching ground-truth JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = PROJECT_ROOT / "data" / "receipts" / "samples"
GROUND_TRUTH_DIR = PROJECT_ROOT / "data" / "receipts" / "ground_truth"

IMAGE_WIDTH = 900
FONT_SIZE = 30
LINE_SPACING = 17
MARGIN = 60


RECEIPTS: list[dict[str, Any]] = [
    {
        "filename": "receipt_001_clear.png",
        "difficulty": "easy",
        "lines": [
            "TOKO MAJU",
            "JL. MERDEKA NO. 10",
            "2026-08-24 10:15",
            "----------------------------------------",
            "AIR MINERAL   2 x 5000      10000",
            "NASI GORENG   1 x 35000     35000",
            "----------------------------------------",
            "SUBTOTAL                      45000",
            "PAJAK                          4950",
            "TOTAL                         49950",
            "TERIMA KASIH",
        ],
        "expected": {
            "merchant_name": "Toko Maju",
            "transaction_date": "2026-08-24",
            "currency": "IDR",
            "subtotal": 45000,
            "tax": 4950,
            "discount": 0,
            "total": 49950,
            "items": [
                {
                    "name": "Air Mineral",
                    "quantity": 2,
                    "unit_price": 5000,
                    "line_total": 10000,
                },
                {
                    "name": "Nasi Goreng",
                    "quantity": 1,
                    "unit_price": 35000,
                    "line_total": 35000,
                },
            ],
        },
    },
    {
        "filename": "receipt_002_multi_item.png",
        "difficulty": "medium",
        "lines": [
            "MINIMARKET HEMAT",
            "JL. MELATI NO. 25",
            "2026-08-23 19:42",
            "----------------------------------------",
            "SUSU UHT      2 x 8500      17000",
            "ROTI TAWAR    1 x 18000     18000",
            "TELUR AYAM    1 x 28000     28000",
            "SABUN MANDI   3 x 4500      13500",
            "----------------------------------------",
            "SUBTOTAL                      76500",
            "DISKON                         6500",
            "PAJAK                          7700",
            "TOTAL                         77700",
            "TERIMA KASIH",
        ],
        "expected": {
            "merchant_name": "Minimarket Hemat",
            "transaction_date": "2026-08-23",
            "currency": "IDR",
            "subtotal": 76500,
            "tax": 7700,
            "discount": 6500,
            "total": 77700,
            "items": [
                {
                    "name": "Susu UHT",
                    "quantity": 2,
                    "unit_price": 8500,
                    "line_total": 17000,
                },
                {
                    "name": "Roti Tawar",
                    "quantity": 1,
                    "unit_price": 18000,
                    "line_total": 18000,
                },
                {
                    "name": "Telur Ayam",
                    "quantity": 1,
                    "unit_price": 28000,
                    "line_total": 28000,
                },
                {
                    "name": "Sabun Mandi",
                    "quantity": 3,
                    "unit_price": 4500,
                    "line_total": 13500,
                },
            ],
        },
    },
    {
        "filename": "receipt_003_low_quality.png",
        "difficulty": "difficult",
        "lines": [
            "KEDAI NUSANTARA",
            "JL. KENANGA NO. 7",
            "24/08/2026 08:05",
            "----------------------------------------",
            "KOPI SUSU     2 x 18000     36000",
            "MIE GORENG    1 x 22000     22000",
            "----------------------------------------",
            "SUBTOTAL                      58000",
            "PAJAK                          2900",
            "TOTAL                         60900",
            "TERIMA KASIH",
        ],
        "expected": {
            "merchant_name": "Kedai Nusantara",
            "transaction_date": "2026-08-24",
            "currency": "IDR",
            "subtotal": 58000,
            "tax": 2900,
            "discount": 0,
            "total": 60900,
            "items": [
                {
                    "name": "Kopi Susu",
                    "quantity": 2,
                    "unit_price": 18000,
                    "line_total": 36000,
                },
                {
                    "name": "Mie Goreng",
                    "quantity": 1,
                    "unit_price": 22000,
                    "line_total": 22000,
                },
            ],
        },
    },
]


def load_receipt_font() -> ImageFont.FreeTypeFont:
    """Load a readable monospace Windows font."""

    font_candidates = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/cour.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]

    for font_path in font_candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), FONT_SIZE)

    raise FileNotFoundError(
        "No supported Windows font was found. "
        "Expected Consolas, Courier New, or Arial."
    )


def create_receipt_image(
    lines: list[str],
    output_path: Path,
    difficult: bool = False,
) -> None:
    """Render receipt text into a PNG image."""

    font = load_receipt_font()
    line_height = FONT_SIZE + LINE_SPACING
    image_height = (MARGIN * 2) + (len(lines) * line_height)

    background = (255, 255, 250)
    text_color = (25, 25, 25)

    image = Image.new(
        mode="RGB",
        size=(IMAGE_WIDTH, image_height),
        color=background,
    )
    drawing = ImageDraw.Draw(image)

    current_y = MARGIN

    for line in lines:
        drawing.text(
            xy=(MARGIN, current_y),
            text=line,
            fill=text_color,
            font=font,
        )
        current_y += line_height

    if difficult:
        image = ImageEnhance.Contrast(image).enhance(0.58)
        image = image.rotate(
            angle=1.4,
            resample=Image.Resampling.BICUBIC,
            expand=False,
            fillcolor=(235, 232, 220),
        )
        image = image.filter(ImageFilter.GaussianBlur(radius=0.75))

    image.save(output_path, format="PNG")


def write_ground_truth(
    expected_data: dict[str, Any],
    output_path: Path,
) -> None:
    """Write the expected receipt data as formatted JSON."""

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(
            expected_data,
            json_file,
            ensure_ascii=False,
            indent=2,
        )
        json_file.write("\n")


def write_manifest() -> None:
    """Write dataset metadata without duplicating ground-truth values."""

    manifest = {
        "dataset_name": "Smart Expense Tracker Synthetic Receipts",
        "description": (
            "Controlled receipt images for OCR and AI parsing development."
        ),
        "receipts": [
            {
                "image": receipt["filename"],
                "ground_truth": receipt["filename"].replace(".png", ".json"),
                "difficulty": receipt["difficulty"],
            }
            for receipt in RECEIPTS
        ],
    }

    manifest_path = PROJECT_ROOT / "data" / "receipts" / "manifest.json"

    with manifest_path.open("w", encoding="utf-8") as manifest_file:
        json.dump(
            manifest,
            manifest_file,
            ensure_ascii=False,
            indent=2,
        )
        manifest_file.write("\n")


def main() -> None:
    """Generate every synthetic receipt and its expected JSON."""

    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    GROUND_TRUTH_DIR.mkdir(parents=True, exist_ok=True)

    for receipt in RECEIPTS:
        image_path = SAMPLES_DIR / receipt["filename"]
        json_path = GROUND_TRUTH_DIR / receipt["filename"].replace(
            ".png",
            ".json",
        )

        create_receipt_image(
            lines=receipt["lines"],
            output_path=image_path,
            difficult=receipt["difficulty"] == "difficult",
        )

        write_ground_truth(
            expected_data=receipt["expected"],
            output_path=json_path,
        )

        print(f"[OK] Generated image: {image_path.name}")
        print(f"[OK] Generated JSON:  {json_path.name}")

    write_manifest()
    print("[OK] Generated manifest.json")
    print(f"[DONE] Generated {len(RECEIPTS)} receipt test cases.")


if __name__ == "__main__":
    main()