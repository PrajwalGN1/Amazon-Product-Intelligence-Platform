"""Unit tests for preprocessing helpers."""

import unittest

from src.preprocessing import parse_count, parse_currency, parse_percentage, split_category


class TestPreprocessing(unittest.TestCase):
    """Validate parsing helpers used by the ETL pipeline."""

    def test_parse_currency_handles_rupee_and_commas(self) -> None:
        self.assertEqual(parse_currency("Rs.1,099"), 1099.0)

    def test_parse_percentage_returns_decimal(self) -> None:
        self.assertEqual(parse_percentage("64%"), 0.64)

    def test_parse_count_handles_missing(self) -> None:
        self.assertEqual(parse_count("24,269"), 24269.0)

    def test_split_category_path(self) -> None:
        self.assertEqual(split_category("A|B|C"), ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()

