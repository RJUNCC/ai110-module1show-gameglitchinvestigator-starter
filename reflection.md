# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Answers:
- You get a text box saying to put a number between 1 and 100. There are three buttons: Submit guess, New game, and if we want hints or not, which just tell us to go lower or higher.
- Two concrete bugs:
  - Putting a number outside the boundaries doesn't produce an error, the hint just tells us to go lower or higher, which doesn't make any sense. I put a number below the boundaries, and it said go lower.
  - When you get the correct answer and press "New Game", you can't play the new game, it just basically freezes, and I noticed that the attempts go to 0. I was expecting each game to have a number of attempts but it just seems like the attempts are incrementing down for each game, instead of each individual attempt, which should be independent of each game. 
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Answers:
- The first thing I noticed was that if I put in a number out of range so <1 or >1 with hints on would produce wrong hints and that the buttons would break after playing one game. I also noticed that the attempts thing just looked wrong, it would start at 1 in the debugging section of the streamlit app. Claude suggested to fix the attempts first so that it initalizes to 0 and to fix the out-of-bounds validation, which will show an error as a "hint" if the guess is outside the valid range. Then, I also saw that the score was weird, it felt random. The AI also suggested to check logic_utils.py for parse_guess, which handles None/empty input, decimals, and non-numeric strings, check_guess, which returns the right hint, and update_score, which awards points on win (but decreases by attempts), and penalizes/rewards on high/low guesses. The hints didnt work at first when I verified them by just testing the streamlit app. Claude decided when secret was higher than guess should be higher and vice versa, so we had to fix that, and we did fix it; it works now. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

Answers:
- I tested the streamlit app again with the updated code, and see if it worked the way I wanted to. The manual tests were to test the UI and the pytest were just to check the tests. Claude refactored the pytests a little bit since there were three failing but there were four passing. 
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
