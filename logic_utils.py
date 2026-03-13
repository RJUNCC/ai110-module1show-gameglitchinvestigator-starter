"""Game logic utilities for the Glitchy Guesser number-guessing game.

All functions in this module are pure (no Streamlit imports or side effects)
so they can be unit-tested independently of the UI layer.
"""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive guess range.
        Defaults to (1, 100) for unrecognised difficulty strings.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw text input into an integer guess.

    Accepts whole numbers and decimals (decimals are truncated toward zero,
    e.g. "7.9" → 7). Rejects None, empty strings, and non-numeric input.

    Args:
        raw: The raw string entered by the player.

    Returns:
        A three-tuple ``(ok, value, error)``:
        - ``ok`` (bool): True when parsing succeeded.
        - ``value`` (int | None): The parsed integer, or None on failure.
        - ``error`` (str | None): A user-facing error message, or None on success.
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a guess to the secret number and return an outcome with a hint message.

    Args:
        guess: The player's guessed integer.
        secret: The secret integer the player is trying to find.

    Returns:
        A two-tuple ``(outcome, message)``:
        - ``outcome``: ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        - ``message``: A short, emoji-decorated hint string for display.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go HIGHER!"
        return "Too Low", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return an updated score based on the guess outcome.

    Scoring rules:
    - **Win**: awards ``max(10, 100 - 10 * (attempt_number + 1))`` points,
      so earlier wins are worth more.
    - **Too High** on an even attempt: +5 points; on an odd attempt: -5 points.
    - **Too Low**: -5 points.
    - Any other outcome: score is unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: One of ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        attempt_number: The 1-based attempt count for the current guess.

    Returns:
        The updated integer score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def get_guess_closeness(guess: int, secret: int, low: int, high: int) -> float:
    """Return a normalised closeness score in the range [0.0, 1.0].

    A score of 1.0 indicates an exact match; 0.0 indicates the guess is as far
    from the secret as the full range allows. Out-of-range guesses are clamped
    to 0.0 rather than going negative.

    Args:
        guess: The player's guessed integer.
        secret: The secret integer the player is trying to find.
        low: The lower bound of the valid guess range (inclusive).
        high: The upper bound of the valid guess range (inclusive).

    Returns:
        A float in [0.0, 1.0] representing how close the guess is to the secret.
    """
    if high == low:
        return 1.0
    raw = 1.0 - abs(guess - secret) / (high - low)
    return max(0.0, min(1.0, raw))
