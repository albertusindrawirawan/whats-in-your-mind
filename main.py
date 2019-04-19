import model

print("doing something with the model, plz wait. . .\n\n\n")

model = model.Model("sample_model.txt")

print("Welcome to Akinator-like\nType Y for Yes and N for No \n\n")

is_playing = True

while is_playing:
    word = model.highest_word_value

    while True:
        val = input("is it " + word + "?\n").lower()

        if val == "n" or val == "y":
            suggested, max_object = model.calculate_probability(word, True if val == "y" else False)

            if suggested is not "":
                word = suggested
            else:
                print(max_object)
                break
        else:
            print("Wrong input man\n\n")

    while True:
        val = input("Hey, wanna play again?\n").lower()
        if val == "y":
            model.reset_dynamic_calculation()
            break
        elif val == "n":
            is_playing = False
            break
        else:
            print("Wrong input man\n\n")
