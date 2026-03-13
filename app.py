import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, get_guess_closeness

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# Live status metrics
attempts_used = st.session_state.attempts
attempts_left = attempt_limit - attempts_used
m1, m2, m3 = st.columns(3)
m1.metric("Range", f"{low} – {high}")
m2.metric("Attempts Left", attempts_left)
m3.metric("Score", st.session_state.score)

# Attempts progress bar
st.progress(attempts_used / attempt_limit if attempt_limit else 0, text="Attempts used")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.checkbox("Show Developer Debug Info", key="show_debug"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()


def _hot_cold_label(closeness: float) -> str:
    """Return an emoji hot/cold label for a closeness value in [0, 1]."""
    if closeness >= 0.90:
        return "🔥 ON FIRE"
    if closeness >= 0.70:
        return "♨️ Hot"
    if closeness >= 0.45:
        return "🌡️ Warm"
    if closeness >= 0.20:
        return "❄️ Cold"
    return "🧊 Freezing"


def _show_summary_table(history: list, secret: int, low: int, high: int) -> None:
    """Render a session summary table after the game ends."""
    st.subheader("📋 Session Summary")
    rows = []
    running_score = 0
    for i, g in enumerate(history, start=1):
        if not isinstance(g, int):
            continue
        outcome, _ = check_guess(g, secret)
        closeness = get_guess_closeness(g, secret, low, high)
        delta = update_score(0, outcome, i) - 0
        running_score += delta
        direction_emoji = {"Win": "🟢 Win", "Too High": "🔴 Too High", "Too Low": "🔵 Too Low"}.get(outcome, outcome)
        rows.append({
            "Attempt": i,
            "Guess": g,
            "Result": direction_emoji,
            "Closeness": f"{closeness * 100:.0f}%",
            "Temperature": _hot_cold_label(closeness),
            "Score Δ": f"{delta:+d}",
        })
    if rows:
        st.table(rows)


if st.session_state.status != "playing":
    valid_history = [g for g in st.session_state.history if isinstance(g, int)]
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    if valid_history:
        _show_summary_table(valid_history, st.session_state.secret, low, high)
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    elif guess_int < low or guess_int > high:
        st.error(f"Please enter a number between {low} and {high}.")
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        closeness = get_guess_closeness(guess_int, secret, low, high)

        if show_hint:
            if outcome == "Too High":
                st.error(f"🔴 {message}")
            elif outcome == "Too Low":
                st.info(f"🔵 {message}")

            hot_cold = _hot_cold_label(closeness)
            st.markdown(f"### {hot_cold} &nbsp; `{closeness * 100:.0f}%` close")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"🎉 You won! The secret was **{st.session_state.secret}**. "
                f"Final score: **{st.session_state.score}**"
            )
            valid_history = [g for g in st.session_state.history if isinstance(g, int)]
            _show_summary_table(valid_history, st.session_state.secret, low, high)
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"💀 Out of attempts! "
                    f"The secret was **{st.session_state.secret}**. "
                    f"Score: **{st.session_state.score}**"
                )
                valid_history = [g for g in st.session_state.history if isinstance(g, int)]
                _show_summary_table(valid_history, st.session_state.secret, low, high)

# --- Guess History Sidebar ---
valid_history = [g for g in st.session_state.get("history", []) if isinstance(g, int)]

if valid_history:
    st.sidebar.divider()
    st.sidebar.subheader("Guess History")
    game_over = st.session_state.get("status", "playing") in ("won", "lost")

    for g in valid_history:
        outcome, _ = check_guess(g, st.session_state.get("secret", 0))
        if outcome == "Win":
            direction = "🟢"
        elif outcome == "Too High":
            direction = "🔴"
        else:
            direction = "🔵"
        closeness = get_guess_closeness(g, st.session_state.get("secret", 0), low, high)
        st.sidebar.write(f"{direction} Guess: {g}")
        st.sidebar.progress(closeness)

    if game_over:
        st.sidebar.caption(f"Secret was: {st.session_state.secret}")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
