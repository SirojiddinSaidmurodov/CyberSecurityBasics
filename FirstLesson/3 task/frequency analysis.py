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
    temp = []
    for key, value in frequencies.items():
        temp.append((key, value / chars * 100))  # counting the frequencies in percents
    temp.sort(key=lambda tup: tup[1], reverse=True)  # sorting list using second item of
    if is_learning:
        results = open("results.txt", 'w', encoding='utf-8')
        for (key, value) in temp:
            results.write(str(key) + " " + str(value) + "\n")
        results.close()
    return temp


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet
    while True:
        path = input("Enter the path to your encrypted text file:\n")
        if os.path.exists(path) & os.path.isfile(path):
            file = open(path, 'r')
            break
        else:
            print("Wrong path, try again")
    encrypted_text = ""
    for line in file.readlines():
        encrypted_text += line
    file.close()
    need_analysis = True if get_setting("Do you want to analise the plain text?\n1 - yes\n2 - no\n", 2,
                                        "Wrong answer, try again") == 1 else False

    if need_analysis:
        while True:
            plain_path = input("Enter the path to your plain text file:\n")
            if os.path.exists(plain_path) & os.path.isfile(plain_path):
                plain_file = open(plain_path, 'r')
                break
            else:
                print("Wrong path, try again")
        general_results = analysis(plain_file, alphabet, True)
    else:
        results_file = open('results.txt', 'r', encoding='utf-8')
        general_results = []
        for lines in results_file.readlines():
            temp = lines.split(' ')
            general_results.append((temp[0], temp[1]))

    #  encrypted text analysis

    encrypted_results = analysis(encrypted_text, alphabet, False)

    # print(analysis("data_rus.txt", russian_alphabet, True))
