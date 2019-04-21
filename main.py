import model

print("doing something with the model, plz wait. . .\n\n\n")

model = model.Model("sample_model.txt", "questions.txt")

print("=====\nWelcome to Akinator-like\nType Y for Yes and N for No \n=====\n\n")

is_playing = True

while is_playing:
    word = model.highest_word_value

    while True:
        val = input(model.questions[word] + "\n").lower()

        if val == "n" or val == "y":
            suggested, max_object = model.calculate_probability(word, True if val == "y" else False)

            if suggested is not None:
                word = suggested
            elif suggested is None and max_object is None:
                print("=====\nsorry, cannot find the right answer\n=====\n")
                break
            else:
                print("=====\nthe answer is " + max_object + "\n=====\n")
                break
        else:
            print("=====\nWrong input man, let me ask you one more time\n====\n")

    while True:
        val = input("Hey, wanna play again?\n").lower()
        if val == "y":
            model.reset_dynamic_calculation()
            break
        elif val == "n":
            is_playing = False
            break
        else:
            print("=====\nWrong input man, let me ask you one more time\n====\n")
