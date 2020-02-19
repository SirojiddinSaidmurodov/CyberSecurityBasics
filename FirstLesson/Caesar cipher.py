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
        result = int(input(question))
        if variants + 1 > result > 0:
            return result
        else:
            print(error)


def cipher(text, key, alphabet, is_Encrypt):
    key = -key if not is_Encrypt else key
    text = text.lower()
    cipheredtext = ""
    for letter in text:
        index = alphabet.find(letter)
        if index >= 0:
            cipheredtext += alphabet[(key + index) % len(alphabet)]
        else:
            cipheredtext += letter
    return cipheredtext


def check_keys(text, alphabet):
    if len(text) > 20:
        text = text[:20]
    for key in range(1, len(alphabet)):
        print(str(key) + "::  " + cipher(text, key, alphabet, False))


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet
    encrypt = get_setting(
        "Enter the number:\n1 - if you want to encrypt something\n2 - if you want to decrypt something\n",
        2, "Wrong variant, try again!\n")
    encrypt = True if encrypt == 1 else False
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
    if encrypt:
        key = int(input("Enter the key:\n"))
        key = key % len(alphabet)
        print(cipher(text, key, alphabet, True))
    else:
        check_keys(text, alphabet)
        key = int(input("Enter key:\n"))
        print(cipher(text, key, alphabet, False))


while True:
    application()
