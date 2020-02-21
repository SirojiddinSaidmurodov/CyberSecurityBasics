import os.path

latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
russian_alphabet = "абвгдеёжзийклмнопрстуфхцшщчъыьэюя"


def get_setting(question, variants, error):
    """
    Function for setting the parameters of another functions
    :type error: str
    :type variants: int
    :type question: str
    :param question: your question with variants of answers
    :param variants: number of your variants of answer
    :param error: what to print when entered variant is not valid
    :return: chosen variant
    """
    while True:
        try:
            result = int(input(question))
        except ValueError:
            result = -1
        if variants + 1 > result > 0:
            return result
        else:
            print(error)


def analysis(file, alphabet, is_learning):
    text = open(file, 'r', encoding='utf-8')
    chars = 0
    frequencies = {}
    for line in text.readlines():
        for char in line:
            if char in alphabet:
                chars += 1
                if char in frequencies.keys():
                    frequencies[char] += 1
                else:
                    frequencies[char] = 1
    text.close()

    results = open("results.txt", 'w', encoding='utf-8')
    temp = []
    for key, value in frequencies.items():
        temp.append((key, value / chars * 100))  # counting the frequencies in percents
    temp.sort(key=lambda tup: tup[1], reverse=True)  # sorting list using second item of
    if is_learning:
        for (key, value) in temp:
            results.write(str(key) + " " + str(value)+"\n")
    results.close()
    return temp


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet
    input_type = get_setting("Choose the type of your input text:\n1 - text from command line\n2 - file\n", 2,
                             "Wrong type, try again!\n")
    if input_type == 2:
        while True:
            path = input("Enter the path to your text file:\n")
            if os.path.exists(path) & os.path.isfile(path):
                file = open(path, 'r')
                break
            else:
                print("Wrong path, try again")
        text = ""
        for line in file.readlines():
            text += line
        file.close()
    else:
        text = str(input("Enter your text to command line:\n"))


print(analysis("data_rus.txt", russian_alphabet, True))
