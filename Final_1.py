import curses


def calculator(sub_expression: list):

    if sub_expression[0] == "(":
        sub_expression.pop(0)

    if sub_expression[-1] == ")":
        sub_expression.pop(-1)

    while len(sub_expression) > 1:

        idx = 0

        if sub_expression.count("^") > 0:
            while sub_expression.count("^") > 0:

                if sub_expression[idx] == "^":
                    sub_expression[idx-1:idx+2] = [sub_expression[idx-1] ** sub_expression[idx+1]]

                else:
                    idx = idx + 1

        elif sub_expression.count("-") > 0:
            while sub_expression.count("-") > 0:

                if sub_expression[idx] == "-":

                    if idx == 0:
                        sub_expression[idx:idx+2] = [-1 * sub_expression[idx+1]]

                    else:
                        sub_expression[idx:idx+2] = ["+", -1 * sub_expression[idx + 1]]

                else:
                    idx = idx + 1

        elif sub_expression.count("*")+sub_expression.count("/")+sub_expression.count("%") > 0:
            while sub_expression.count("*")+sub_expression.count("/")+sub_expression.count("%") > 0:

                if sub_expression[idx] == "*":
                    sub_expression[idx-1:idx+2] = [sub_expression[idx-1] * sub_expression[idx+1]]

                elif sub_expression[idx] == "/":
                    sub_expression[idx - 1:idx + 2] = [sub_expression[idx - 1] / sub_expression[idx + 1]]

                elif sub_expression[idx] == "%":
                    sub_expression[idx - 1:idx + 2] = [sub_expression[idx - 1] % sub_expression[idx + 1]]

                else:
                    idx = idx + 1

        elif (type(sub_expression[idx]) == float) and (type(sub_expression[idx + 1]) == float):
            sub_expression[idx: idx+2] = [sub_expression[idx] * sub_expression[idx+1]]

        elif sub_expression.count("+") > 0:
            while sub_expression.count("+") > 0:

                if sub_expression[idx] == "+":
                    sub_expression[idx-1:idx+2] = [sub_expression[idx-1] + sub_expression[idx+1]]

                else:
                    idx = idx + 1

    return sub_expression


def analyser(math_expression):

    # Defining some local variables
    operators = ["-", "+", "^", "*", "/", "%"]
    parentheses = ["(", ")"]
    consecutive_occurrence = 0
    lvl_dict = {
        "0": [0, len(math_expression) - 1]
    }
    first_char = True

    # CLEANING 1: Remove spaces and duplicate items.
    while math_expression.count(" ") > 0:

        math_expression = math_expression.replace(" ", "")

    if len(math_expression) == 0:
        result = ("[AWAIT]", "Awaiting for user input.")
        return math_expression, result

    for operator in operators:

        while math_expression.count(2*operator) > 0:

            math_expression = math_expression.replace(2*operator, operator)

    if math_expression[-1] in operators:
        result = ("[ERROR]", "Last character cannot be an operation!")
        return math_expression, result

    math_expression_cleaned = math_expression

    # make a list from input.
    for operator in operators:

        math_expression = math_expression.replace(operator, f" {operator} ")

    for p in parentheses:

        math_expression = math_expression.replace(p, f" {p} ")

    math_expression = math_expression.split()

    for i in range(len(math_expression)):

        try:

            math_expression[i] = float(math_expression[i])

            if consecutive_occurrence > 0:
                consecutive_occurrence = consecutive_occurrence - 1

            first_char = False

        except ValueError:

            if math_expression[i] == parentheses[0]:
                first_char = True

            elif math_expression[i] == parentheses[1]:
                continue

            elif math_expression[i] == operators[0]:

                first_char = True

            elif math_expression[i] in operators[1:]:

                consecutive_occurrence = consecutive_occurrence + 1

                if first_char:
                    result = ("[ERROR]", "First character cannot be an operation!")
                    return math_expression_cleaned, result

                if consecutive_occurrence > 1:
                    result = ("[ERROR]", "Consecutive operations detected!")
                    return math_expression_cleaned, result

            elif (math_expression[i] not in operators) and (math_expression[i] not in parentheses):
                result = ("[ERROR]", "I don't understand.")
                return math_expression_cleaned, result

    while len(lvl_dict) > 0:

        lvl_value = 0
        lvl_dict.update({"0": [0, len(math_expression) - 1]})

        if math_expression == parentheses:
            result = ("[AWAIT]", "Calculator needs more info to calculate.")
            return math_expression_cleaned, result

        if math_expression.count(parentheses[0]) != math_expression.count(parentheses[1]):
            result = ("[ERROR]", "Parentheses are imbalance")
            return math_expression_cleaned, result

        for i in range(0, len(math_expression)):

            if math_expression[i] == parentheses[0]:
                lvl_value = lvl_value + 1
                lvl_dict.update({str(lvl_value): [i]})

            elif math_expression[i] == parentheses[1]:

                tmp = lvl_dict.get(str(lvl_value))
                tmp.append(i)
                lvl_dict.update({str(lvl_value): tmp})
                lvl_value = lvl_value - 1
                if lvl_value < 0:
                    result = ("[ERROR]", "Parentheses are imbalance")
                    return math_expression_cleaned, result
                del tmp

        if len(lvl_dict) == 2:
            if lvl_dict["0"] == lvl_dict["1"]:
                lvl_dict.popitem()

        # noinspection PyTypeChecker
        lvl_dict = dict(sorted(lvl_dict.items(), key=lambda item: int(item[0])))
        depth = len(lvl_dict.items()) - 1
        az = ((list(lvl_dict.items())[depth])[-1])[0]
        ta = ((list(lvl_dict.items())[depth])[-1])[-1]

        try:
            math_expression[az:int(ta) + 1] = calculator(math_expression[az:int(ta) + 1])
        except ZeroDivisionError:
            result = ("[ERROR]", "You tried divide items by zero!")
            return math_expression_cleaned, result

        lvl_dict.popitem()

    result = ("[ANS]", str(math_expression[0]))
    return math_expression_cleaned, result


def main(screen):

    # Default screen settings
    screen.clear()
    curses.curs_set(0)

    # Variables
    math_expression = str()
    scroll = 0
    input_mode = "Calculator"
    curses.init_pair(1, 135, 0)
    curses.init_pair(2, 4, 0)
    curses.init_pair(3, 8, 0)
    curses.init_pair(4, 2, 0)
    f_magenta = curses.color_pair(1)
    f_red = curses.color_pair(2)
    f_grey = curses.color_pair(3)
    f_green = curses.color_pair(4)

    # Layout and design:
    # math expression window
    screen.addstr(0, 0, "╔═════▷ Mathematical Expression ◁═══════════════════════╗")
    screen.addstr(1, 0, "║                                                       ║")
    screen.addstr(2, 0, "║                                                       ║")
    screen.addstr(3, 0, "║                                                       ║")
    screen.addstr(4, 0, "╚═══════════════════════════════════════════════════════╝")
    math_expression_window = curses.newwin(1, 54, 2, 2)

    # result window
    screen.addstr(5, 0, "╔═════▷ Result ◁════════════════════════════════════════╗")
    screen.addstr(6, 0, "║                                                       ║")
    screen.addstr(7, 0, "╚═══════════════════════════════════════════════════════╝")
    result_window = curses.newwin(1, 54, 6, 2)

    # Guid
    screen.addstr(8, 0, "╔═════▷ Guid ◁══════════════════════════════════════════╗")
    screen.addstr(9, 0, "║This program is optimized for windows operating system.║")
    screen.addstr(10, 0, "║Simply type numbers, parentheses to change calculation ║")
    screen.addstr(11, 0, "║priority, backspace to remove the last character and  -║")
    screen.addstr(12, 0, "║ESC to exit program. supported operations: * / % + - ^ ║")
    screen.addstr(13, 0, "║ArrowUp and Down to navigate history panel.            ║")
    screen.addstr(14, 0, "╚═══════════════════════════════════════════════════════╝")

    # history padding
    screen.addstr(0, 58, "╔═════▷ History ◁═══════════════════════════════════════╗")
    screen.addstr(1, 58, "║                                                       ║")
    screen.addstr(2, 58, "║                                                       ║")
    screen.addstr(3, 58, "║                                                       ║")
    screen.addstr(4, 58, "║                                                       ║")
    screen.addstr(5, 58, "║                                                       ║")
    screen.addstr(6, 58, "║                                                       ║")
    screen.addstr(7, 58, "║                                                       ║")
    screen.addstr(8, 58, "║                                                       ║")
    screen.addstr(9, 58, "║                                                       ║")
    screen.addstr(10, 58, "║                                                       ║")
    screen.addstr(11, 58, "║                                                       ║")
    screen.addstr(12, 58, "║                                                       ║")
    screen.addstr(13, 58, "║                                                       ║")
    screen.addstr(14, 58, "╚═══════════════════════════════════════════════════════╝")
    history_pad = curses.newpad(1000, 54)
    screen.refresh()

    # divider
    divider = str(53*".")

    while input_mode == "Calculator":

        math_expression_window.clear()
        result_window.clear()

        history_pad.clear()
        history.seek(0)
        history_pad.addstr(history.read())
        history_pad.refresh(scroll, 0, 1, 59, 13, 113)

        curses.flushinp()
        inp = screen.getch()

        if inp == 8:

            if len(math_expression) > 0:

                math_expression = math_expression[0:len(math_expression)-1]

                math_expression, result = analyser(math_expression)

            else:

                result = ("[ERROR]", "Nothing to erase.")

        elif inp == 259:  # ArrowUp

            if scroll != 0:

                scroll = scroll - 1

            continue

        elif inp == 258:  # ArrowDown

            history.seek(0)
            if scroll < len(history.readlines()):

                scroll = scroll + 1

            continue

        elif (inp == 10) or (inp == 459):  # Enter/Return

            history_pad.clear()
            math_expression, result = analyser(math_expression)

            if result[0] == "[ANS]":

                history.write(f"{math_expression}\n{result[1]}\n{divider}\n")

            else:

                result_window.addstr(0, 0, "[ERROR] ", f_red)
                result_window.addstr("Only valid answers can be saved in history.")
                result_window.refresh()

            continue

        elif inp == 27:

            result = ("[END]", "May the god be with you.")

        elif len(chr(inp))+len(math_expression) > 53:

            result = ("[ERROR]", "Your input is too long!")

        else:

            math_expression = math_expression + chr(inp)
            math_expression, result = analyser(math_expression)

        # Result handler
        if result[0] == "[ERROR]":
            result_window.addstr(0, 0, "[ERROR] ", f_red)
            result_window.addstr(result[1])

        elif result[0] == "[ANS]":
            result_window.addstr(0, 0, "[ANS] ", f_green)
            result_window.addstr(result[1])

        elif result[0] == "[AWAIT]":
            result_window.addstr(0, 0, "[AWAIT] ", f_grey)
            result_window.addstr(result[1])

        elif result[0] == "[END]":
            result_window.addstr(0, 0, "[END] ", f_magenta)
            result_window.addstr(result[1])
            result_window.refresh()
            curses.napms(5000)
            quit()

        math_expression_window.addstr(0, 0, math_expression)
        math_expression_window.refresh()
        result_window.refresh()

    curses.napms(3000)


history = open("history.txt", "r+")
curses.wrapper(main)
history.close()
