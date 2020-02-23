import os.path
from matplotlib import pyplot

latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
russian_alphabet = "абвгдеёжзийклмнопрстуфхцшщчъыьэюя"


def get_setting(question: str, variants: int, error: str):
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


def analysis(text: str, alphabet: str, is_learning: bool) -> list:
    """

    :param is_learning: True if saving to file needed
    :type is_learning: bool
    :param text: input text for analysing
    :type text: str
    :param alphabet: alphabet of input text
    :type alphabet: str
    :return list of tuples, which consists letter and its frequency, sort by their frequency
    """
    chars = 0
    frequencies = {}
    for char in text:
        char = char.lower()
        if char in alphabet:
            chars += 1
            if char in frequencies.keys():
                frequencies[char] += 1
            else:
                frequencies[char] = 1
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


def input_text():
    """

    :return: text read from file
    :rtype: str
    """
    while True:
        path = input("Enter the path to your encrypted text file:\n")
        if os.path.exists(path) & os.path.isfile(path):
            file = open(path, 'r', encoding='utf-8')
            break
        else:
            print("Wrong path, try again")
    encrypted_text = ""
    for line in file.readlines():
        encrypted_text += line
    file.close()
    return encrypted_text


def set_analise(alphabet):
    """

    :param alphabet: alphabet of plain text
    :type alphabet: str
    :return: list of tuples (letter, frequency)
    :rtype: list
    """
    need_analysis = True if get_setting("Do you want to analise the plain text?\n1 - yes\n2 - no\n", 2,
                                        "Wrong answer, try again") == 1 else False
    if need_analysis:
        while True:
            plain_path = input("Enter the path to your plain text file:\n")
            if os.path.exists(plain_path) & os.path.isfile(plain_path):
                plain_file = open(plain_path, 'r', encoding='utf-8')
                text = ''
                for line in plain_file.readlines():
                    text += line
                plain_file.close()
                break
            else:
                print("Wrong path, try again")

        general_results = analysis(text, alphabet, True)
    else:
        results_file = open('results.txt', 'r', encoding='utf-8')
        general_results = []
        for lines in results_file.readlines():
            temp = lines.split(' ')
            general_results.append((temp[0], temp[1]))
    return general_results


def make_key(key, value, is_List: bool) -> dict:
    """
    Return the dict (letter,letter) as key
    :param is_List:
    :type is_List: bool
    :param key: letters
    :type key: str
    :param value: letters
    :type value: str
    :return: key
    :rtype: dict
    """
    output_key = {}
    if is_List:
        for i in range(len(key)):
            output_key[key[i]] = value[i]
    else:
        for i in range(len(key)):
            key_letter, frequency = key[i]
            value_letter, freq = value[i]
            output_key[key_letter] = value_letter
    return output_key


def substitution(text: str, key: dict, is_Encrypt: bool) -> str:
    """
    Substitution ciphering function. Key is a dict (plain, encrypted) letters
    :type text: str
    :param text: text for encrypting or decrypting
    :param key: dict
    :param is_Encrypt: bool
    :return: str
    """
    encrypted_text = ""
    if is_Encrypt:
        key = {y: x for x, y in key.items()}

    for letter in text:
        upper = True if letter.isupper() else False

        letter = letter.lower()
        letter = key.get(letter, letter)
        if upper:
            encrypted_text += letter.upper()
        else:
            encrypted_text += letter
    return encrypted_text


def analise_key(text: str, key, alphabet: str, general_res):
    """
    Function for computing the accuracy of keys depending on the length of text
    :param alphabet:
    :type alphabet:
    :param key: original key
    :type key: dict
    :type text: str
    """
    iterations = len(text) % 1000
    accuracy_list = []
    for i in range(iterations):
        temp_text = text[:i * 1000]
        if i + 1 == iterations:
            temp_text = text
        temp_results = analysis(temp_text, alphabet, False)
        temp_key = make_key(temp_results, general_res, False)
        accuracy = 0
        for letter in alphabet:
            if temp_key.get(letter) == key.get(letter):
                accuracy += 1
        accuracy_list.append(accuracy)
    pyplot.plot(accuracy_list)
    pyplot.show()


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet

    encrypted_text = input_text()
    general_results = set_analise(alphabet)

    #  encrypted text analysis
    encrypted_results = analysis(encrypted_text, alphabet, False)  # encrypted text analysis
    encrypted_key = make_key(encrypted_results, general_results, False)  # key for deciphering
    print(substitution(encrypted_text, encrypted_key, False))
    # key_file = open('Key.txt', 'r', encoding='utf-8')
    # temp_key = ''
    # temp_val = ''
    # for line in key_file.readlines():
    #     temp_key += line[1]
    #     temp_val += line[0]
    # print(encrypted_key)
    # print(make_key(temp_key, temp_val, True))
    # analise_key(encrypted_text, make_key(temp_key, temp_val, True), alphabet, general_results)


# print(analysis("data_rus.txt", russian_alphabet, True))


application()
