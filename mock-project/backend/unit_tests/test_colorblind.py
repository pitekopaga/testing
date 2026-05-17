import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import get_pattern, PATTERNS

class TestGetPattern:
    def test_single_digit_pattern(self):
        """Test that single digit returns correct pattern"""
        pattern = get_pattern(5)
        assert len(pattern) == 5  # 5 rows
        assert len(pattern[0]) == 5  # 5 columns
        assert pattern == PATTERNS[5]
    
    def test_two_digit_pattern_has_gap(self):
        """Test that two-digit numbers have a column gap between digits"""
        pattern = get_pattern(74)
        assert len(pattern) == 5  # 5 rows
        # Two-digit pattern: 5 + 1 (gap) + 5 = 11 columns
        assert len(pattern[0]) == 11
        # Middle column (index 5) should be all zeros (the gap)
        for row in pattern:
            assert row[5] == 0
    
    def test_pattern_returns_valid_for_unknown(self):
        """Test that unknown number returns pattern for 0"""
        pattern = get_pattern(99)
        assert pattern is not None
        assert len(pattern) == 5

class TestPatternsStructure:
    def test_all_digits_have_consistent_size(self):
        """Test that all digit patterns are 5x5 grids"""
        for digit, pattern in PATTERNS.items():
            assert len(pattern) == 5, f"Digit {digit} has wrong row count"
            for row in pattern:
                assert len(row) == 5, f"Digit {digit} has wrong column count"
                for cell in row:
                    assert cell in [0, 1], f"Digit {digit} has invalid cell value"
    
    def test_patterns_are_not_empty(self):
        """Test that no pattern is all zeros"""
        for digit, pattern in PATTERNS.items():
            total = sum(sum(row) for row in pattern)
            assert total > 0, f"Digit {digit} pattern is all zeros"
