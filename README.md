# 🎮 Tic-Tac-Toe with Django

A simple **Tic-Tac-Toe game** built with Python and Django. The game offers two playing modes: play against a bot or challenge a friend in a local two-player game. Players can choose their preferred mark and enjoy different levels of difficulty when playing against the bot.

---

# Features

- **Two Game Modes:** Play against a bot or a friend on the same device.
- **Four Bot Difficulty Levels:** Choose from four difficulty levels to match your skills.
- **Choose Your Mark:** Select whether to play as X or O.
- **Alternating Starting Player:** In local two-player mode, the player who makes the first move changes each time a new game starts.
- **Interactive Game Board:** Click on the board to make your move.
- **Win Detection:** The game detects when a player wins.
- **Draw Detection:** The game recognizes when the board is full and no player has won.
- **Game Status:** Displays the current game status and indicates the winner or a draw.

---

# Game Modes

## 1. Play Against the Bot 🤖

Play Tic-Tac-Toe against a computer-controlled opponent.

- Choose one of four bot difficulty levels.
- Select your player mark (X or O).
- Make your moves and try to win against the bot.
- Test your skills by choosing different difficulty levels.

## 2. Play with a Friend 👥

Play against another person on the same device.

- Two players take turns on the same game board.
- The game automatically switches between Player X and Player O.
- The starting player alternates with each new game, giving both players a fair chance to move first.

---

# How to Play

1. Open the application.
2. Choose a game mode: play against the bot or a friend.
3. If you choose bot mode, select the difficulty level and your mark.
4. Start the game.
5. Click on an empty square to make your move.
6. Try to get three marks in a row horizontally, vertically, or diagonally.
7. The game ends when a player wins or the board is full.

---

# Technologies Used

- **Python** — Programming language.
- **Django** — Web framework.
- **HTML** — Page structure.
- **CSS** — Styling and layout.
- **JavaScript** — Interactive game functionality, if used in the project.

---

# How to Run the Project

## 1. Clone the Repository

```bash
git clone <repository_url>
cd <project_name>
```

## 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Start the Development Server

```bash
python manage.py runserver
```

## 5. Open the Application

Open your browser and visit:

http://127.0.0.1:8000/

---

# Project Goal

This project was developed to practice building web applications with Django, implementing game logic, creating different game modes, and working with bot difficulty levels.

---

# Author

**Ainagul**
