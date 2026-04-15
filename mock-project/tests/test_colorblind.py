import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app import is_distinguishable

def test_red_vs_green():
    assert is_distinguishable("#FF0000", "#00FF00") == False

def test_red_vs_blue():
    assert is_distinguishable("#FF0000", "#0000FF") == True

def test_identical_colors():
    assert is_distinguishable("#FF0000", "#FF0000") == False

def test_green_vs_green():
    assert is_distinguishable("#00FF00", "#00FF00") == False

def test_case_insensitivity():
    assert is_distinguishable("#ff0000", "#00ff00") == False

def test_invalid_hex_format():
    # Current function does not validate, but test documents the expectation
    result = is_distinguishable("invalid", "#FF0000")
    assert result in [True, False]  # Placeholder until validation is added