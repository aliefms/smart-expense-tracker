"""Command-line entry point for the Smart Expense Tracker."""


def main() -> None:
    """Display the current application status."""
    print("Smart Expense Tracker")
    print("Development environment is ready.")
    print("Current pipeline target:")
    print("Receipt Image -> PaddleOCR -> Ollama -> JSON -> PostgreSQL")


if __name__ == "__main__":
    main()