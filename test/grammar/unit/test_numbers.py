import sys
import pytest
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[3]))

from textmate_grammar.handler import ContentHandler
from textmate_grammar.language import LanguageParser
from textmate_grammar.grammars import matlab
from unit import MSG_NO_MATCH


logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("textmate_grammar").setLevel(logging.INFO)
parser = LanguageParser(matlab.GRAMMAR)
parser.initialize_repository()


@pytest.mark.parametrize("check", ["1", ".1", "1.1", ".1e1", "1.1e1", "1e1", "1i", "1j", "1e2j"])
def test_decimal(check):
    """Test numbers decimal"""
    parsed, elements, _ = parser.parse(ContentHandler(check), find_one=False)
    assert parsed, MSG_NO_MATCH
    assert elements[0].token == "constant.numeric.decimal.matlab", MSG_NO_MATCH
    if "i" in check or "j" in check:
        assert elements[0].captures[0].token == "storage.type.number.imaginary.matlab", MSG_NO_MATCH


@pytest.mark.parametrize(
    "check", ["0xF", "0XF", "0xFs8", "0xFs16", "0xFs32", "0xFs64", "0xFu8", "0xFu16", "0xFu32", "0xFu64"]
)
def test_hex(check):
    """Test numbers hex"""
    parsed, elements, _ = parser.parse(ContentHandler(check), find_one=False)
    assert parsed, MSG_NO_MATCH
    assert elements[0].token == "constant.numeric.hex.matlab", MSG_NO_MATCH
    if "s" in check or "u" in check:
        assert elements[0].captures[0].token == "storage.type.number.hex.matlab", MSG_NO_MATCH


@pytest.mark.parametrize(
    "check", ["0b1", "0B1", "0b1s8", "0b1s16", "0b1s32", "0b1s64", "0b1u8", "0b1u16", "0b1u32", "0b1u64"]
)
def test_binary(check):
    """Test numbers binary"""
    parsed, elements, _ = parser.parse(ContentHandler(check), find_one=False)
    elements[0].flatten()
    assert parsed, MSG_NO_MATCH
    assert elements[0].token == "constant.numeric.binary.matlab", MSG_NO_MATCH
    if "s" in check or "u" in check:
        assert elements[0].captures[0].token == "storage.type.number.binary.matlab", MSG_NO_MATCH
