# description:

Here is a basic calculator written in python.

# Requirements:

- This calculator has been optimized for the Windows operating system. So you need Windows operating system to achieve the best results.

- Python 3.10+

- "windows-curses" library.
```
py -m pip windows-curses
```

# Features:

- Supported mathematical operations and hotkeys:
```
-"+": Addition.
-"-": Submission.
-"*": Multiplication.
-"/": Division.
-"^": Power. Use "^(1/n)" to find the "n" -th root.
-"%": Remaining of division.
-"(" and ")": Use parentheses to re-order calculation priority.
-"Enter" or "Return": Save a valid mathematical expression and its answer to the history panel.
-"backspace": to remove the last character from the mathematical expression.
-"ArrowUp" and "ArrowDown": Navigate the history panel.
```

- Real-time UI with an error handler and auto-correction.

- Not using redundant libraries or "eval" command.

- History panel.

- Obeying PEP-8 in source code.

# known bugs and limitations:

- This program creates a "history.txt" file and deletes previous entries (if there were any); Although you can change this behavior by using "r+" instead of "w+" in the file handling section of the code.

- There is a history limitation of 1000 lines of history and 53 columns.

- There is a calculation bug for calculating fractions that are incompatible with the binary system. (e.g. 0.1+0.2)

# Plans:

- Debug the mentioned issues.

- Making the code look more professional.

# How does it work?

- So here is the problem. My mother tongue is Persian and English is not my primarily used language. I know how my code works but I can't explain it in English. You can either wait until I master the mentioned language or help me to translate documents from Persian to English.
