# Enhanced Ping Pong Game 🏓

A classic Arcade Ping Pong game built with Python and Pygame, now updated with an interactive difficulty menu, dynamic gameplay mechanics, and speed limits to prevent glitches.

---

## 🚀 New Features in this Version

- **Interactive Main Menu:** Choose your challenge before starting the game using numerical keys (`1`, `2`, or `3`).
- **3 Difficulty Levels:**
  - **Easy:** Standard speeds for a casual match.
  - **Medium (Dynamic):** Every time the ball hits a paddle, the ball and paddle speeds increase by **15%**, making the game progressively intense!
  - **Hard:** Starts at a very high velocity for experienced players.
- **Speed Capping (Anti-Tunneling Bug):** Implemented a velocity threshold (`MAX_BALL_SPEED` & `MAX_PADDLE_SPEED`) so the ball never moves too fast to glitch through paddles or boundaries.
- **In-Game Timer & Scoreboard:** Tracks match duration and real-time scores. First to **5 points** wins!

---

## 🎮 Controls

### Menu Navigation
- `1` - Select Easy Difficulty
- `2` - Select Medium Difficulty
- `3` - Select Hard Difficulty
- `SPACE` - Start the Game / Return to Menu after a game ends

### Gameplay
| Action | Player 1 (Left) | Player 2 (Right) |
| :--- | :--- | :--- |
| **Move Up** | `W` | `UP Arrow` |
| **Move Down**| `S` | `DOWN Arrow` |

---

## 🛠️ Prerequisites & Installation

Make sure you have Python and Pygame installed on your system.

1. **Install Pygame:**
   ```bash
   pip install pygame

2. **Run the Game:**
   Place your code and the `ball.png` asset in the same directory, then run:
   ```bash
   python main.py
   ```

---

## ⚙️ Technical Highlights

- **Precise Collision Logic:** Fixed ball-trapping issues on paddles by using absolute values (`abs()`) for directional changes instead of simple inversion multipliers.
- **Velocity Regulators:** Integrated clean Pythonic syntax for keeping ball components (`X` and `Y`) separate and checking safety speed caps independently on every frame.