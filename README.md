# All "dle" Game Solver

This project was originaly a basic Python-based **Loldle.net** solver. I made it more generic to solve other games of the same author **Onepiecedle.net**, **Pokedle.net**, ...
The game requires players to guess a Game or Annime character daily based on multiple properties. Each guess receives feedback indicating whether each property is **correct (T)**, **incorrect (F)**, **partially correct (P)**, or for ranges, **lower (L) / greater (G)**.

## Features

- Algorithm that determine the best guess by maximizing the number of eliminated possibilities.
- Dynamically filters remaining candidates based on game feedback.
- Allows users to iteratively enter feedback until the correct character is found.

## Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/abonvalle/alldle-solver.git
cd alldle-solver
```

### 2️⃣ Create & Activate a Virtual Environment

```sh
python3 -m venv .alldle_env
source ./venv/bin/activate
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

## Running the Solver

To start the program, run:

```sh
python3 app.py
```

The script will ask you the game you're playing, suggest the best initial guess and prompt you to enter feedback after each guess.

you can play faster with :

```sh
python3 app.py -g Loldle -s Singed -f -q
```

See the [CLI Arguments](#cli_Arguments) section below for a full description.

## How to Play

1. Run the script and use the suggested first guess.
2. Enter the feedback for each property:
   - **T** → Correct.
   - **F** → Incorrect.
   - **P** → Partially correct (e.g., Color = Red, but actual character has Red & Blue).
   - **L** → Number is **lower** than guessed.
   - **G** → Number is **greater** than guessed.
3. The script will suggest the next best guess.
4. Repeat until the correct character is found!

## Example Run

```sh
Playing Loldle
Best initial guess: Zilean
Enter feedback: FFPTFFG
Candidates left after filtering: 9
Next best guess: Vi
GRGGGRG
The character is: Fiora
```

## CLI Arguments

The ALLDLE Solver script uses the argparse module to handle command-line arguments, allowing users to customize their gameplay experience. Below is a detailed description of each argument:

`--game` or `-g`

- Type: `str`
- Default: `None` (You can select the game before guessing)
- Description: Specifies the name of the game to start the app with.
- Usage Example:

```sh
python3 app.py --game Loldle
```

---

`--start_with` or `-s`

- Type: `str`
- Default: `None` (You can select the character later)
- Description: Defines the first word guess to begin the game.
- Usage Example:

```sh
python3 app.py -g Loldle --start_with Singed
```

---

`--fast_game` or `-f`

- Type: `flag` (No value required, `store_true`)
- Description: Activates the fast game mode, where the solver automatically picks the best possible guess without user intervention.
- Usage Example:

```sh
python3 app.py --fast_game
```

---

- `--quiet` or `-q`
- Type: `flag` (No value required, `store_true`)
- Description: Runs the script in quiet mode, suppressing verbose output.
- Usage Example:

```sh
python3 app.py --quiet
```

---

## About

This tool is designed to assist players in the **Classic modes** of the following sites:

- [Loldle.net](https://loldle.net/classic)
- [Pokedle.net](https://pokedle.net/classic)
- [Onepiecedle.net](https://onepiecedle.net/classic)
- [Narutodle.net](https://narutodle.net/classic)
- [Smashdle.net](https://smashdle.net/classic)
- [Dotadle.net](https://dotadle.net/classic)

> **Disclaimer**: This is an independent project and is not affiliated with any of the websites mentioned above, nor with any game or anime.

## License

This project is licensed under the **MIT License**.

---

### 🚀 Happy Guessing! 🎮
