import json

print("Welcome to the test maker\n")

test = []

loop = 1
while True:
    problem = input(f"Please enter the problem for question #{loop}: ")
    answer = input(f"Please enter the answer for question #{loop}: ")
    choices = input(
        "If the question is multiple choice, enter the choices seperated by commas. If not, leave blank: "
    ).split(",")

    test.append([problem, answer, (choices if len(choices) > 1 else None)])

    _exit = input("Would you like to add another question (Y/n): ")
    if _exit.lower() == "n":
        break

    loop += 1

with open("test.json", "w") as f:
    json.dump(test, f)
