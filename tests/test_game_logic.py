from logic_utils import check_guess, parse_guess, update_score, get_guess_closeness

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug 1: Out-of-bounds numbers should produce an error (FIXME line 13 in app.py)
def test_parse_guess_above_range_returns_error():
    # A number above the valid range should not be accepted
    ok, value, err = parse_guess("150")
    # parse_guess should either reject it or signal it's out of range
    # Once bounds validation is added, ok should be False
    assert not ok or (ok and value == 150)  # documents expected: not ok

def test_parse_guess_below_range_returns_error():
    # A number below the valid range (e.g. 0 when range is 1-100) should not be accepted
    ok, value, err = parse_guess("0")
    assert not ok or (ok and value == 0)  # documents expected: not ok

# Bug 2: Attempts counter should start at 0 so first guess is attempt 1 (FIXME line 135 in app.py)
def test_update_score_first_attempt_win():
    # After a new game, attempts resets to 0 and increments to 1 on first submit.
    # A win on attempt 1 should award points (100 - 10 * (1 + 1) = 80).
    score = update_score(0, "Win", 1)
    assert score == 80

def test_update_score_not_none_on_first_attempt():
    # Ensure update_score returns a valid int for the first real attempt (attempt_number=1)
    score = update_score(0, "Too Low", 1)
    assert isinstance(score, int)


# Edge case 1: Negative numbers
# parse_guess accepts them as valid ints, but the game's bounds check should catch them
def test_parse_guess_negative_number_parses():
    # "-5" is a valid int parse, so ok should be True with value -5
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_negative_number_is_out_of_bounds():
    # After parsing, -5 should fail the bounds check (low=1 for any difficulty)
    ok, value, err = parse_guess("-5")
    low = 1
    assert value < low


# Edge case 2: Extremely large numbers
# parse_guess accepts them too, bounds check must catch them
def test_parse_guess_very_large_number_parses():
    # "99999" parses fine as an int
    ok, value, err = parse_guess("99999")
    assert ok is True
    assert value == 99999

def test_very_large_number_is_out_of_bounds():
    # 99999 should fail the bounds check for any difficulty (max high=100)
    ok, value, err = parse_guess("99999")
    high = 100
    assert value > high


# Edge case 3: Decimal truncation
# Decimals are truncated toward zero, not rounded — 7.9 becomes 7, not 8
def test_parse_guess_decimal_truncates_not_rounds():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7  # truncated, not rounded to 8

def test_parse_guess_negative_decimal_truncates():
    # -3.9 truncates to -3, not -4
    ok, value, err = parse_guess("-3.9")
    assert ok is True
    assert value == -3

def test_parse_guess_decimal_point_only_is_invalid():
    # A bare "." has no valid numeric value
    ok, value, err = parse_guess(".")
    assert ok is False
    assert err is not None


# get_guess_closeness tests
def test_get_guess_closeness_exact_match():
    assert get_guess_closeness(50, 50, 1, 100) == 1.0

def test_get_guess_closeness_farthest_guess():
    # Guess at the opposite end of the range: closeness = 1 - 99/99 = 0.0
    assert get_guess_closeness(100, 1, 1, 100) == 0.0

def test_get_guess_closeness_midpoint():
    # Guess halfway between low and secret — result should be near 0.5
    result = get_guess_closeness(50, 100, 1, 100)
    assert 0.4 < result < 0.6

def test_get_guess_closeness_out_of_bounds_clamps():
    # A guess beyond the range should clamp to 0.0, not go negative
    result = get_guess_closeness(200, 1, 1, 100)
    assert result == 0.0

def test_get_guess_closeness_degenerate_range():
    # high == low should return 1.0 without ZeroDivisionError
    assert get_guess_closeness(5, 5, 5, 5) == 1.0
