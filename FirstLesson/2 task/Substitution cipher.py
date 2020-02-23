from random import randint
import os

latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
russian_alphabet = "абвгдеёжзийклмнопрстуфхцшщчъыьэюя"


# TODO: make file input and output, take it from caesar cipher

# function to fet the answers for the questions
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


def key_generator(alphabet: str):
    """
    Function for generating random cipher key.
    Key is a dict (plain, encrypted) letters
    :param alphabet: str of alphabet
    :return: dict randomly generated key
    """
    temp = [i for i in alphabet]
    key = []
    for letter in alphabet:
        key.append((letter, temp.pop(randint(0, len(temp) - 1))))
    key = dict(key)
    return key


def key_reader():
    """
    Function for reading the key from file
    :return: key
    """
    file = open("Key.txt", 'r', encoding='utf-8')
    key = {}
    for line in file.readlines():
        key[line[0]] = line[1]
    file.close()
    return key


def key_saver(key):
    """
    Function for saving the key to file
    :return: void
    """
    file = open("Key.txt", 'w', encoding='utf-8')
    for letter in key.keys():
        file.write(str(letter) + str(key.get(letter)) + "\n")
    file.close()


def substitution(text: str, key, is_Encrypt):
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


def input_text():
    input_type = get_setting("Choose the type of your input text:\n1 - text from command line\n2 - file\n", 2,
                             "Wrong type, try again!\n")
    if input_type == 2:
        while True:
            path = input("Enter the path to your text file:\n")
            if os.path.exists(path) & os.path.isfile(path):
                input_file = open(path, 'r', encoding='utf-8')
                break
            else:
                print("Wrong path, try again")
        text = ""
        for line in input_file.readlines():
            text += line
        input_file.close()
    else:
        text = str(input("Enter your text to command line:\n"))
    return text


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet
    encrypt = get_setting("I want to...\n"
                          "1 - encrypt the text\n"
                          "2 - decrypt the text\n", 2, "Wrong variant, choose the valid one\n")
    text = input_text()
    output = get_setting("Choose the output type:\n1 - commandline\n2 - file\n", 2, "Wrong variant, try again!")

    if encrypt == 1:
        is_encrypting = True
        file = get_setting("I want to encrypt the text with:\n"
                           "1 - old saved key\n"
                           "2 - new generated key\n", 2, "Wrong variant, try again!\n")
        if file == 1:
            key = key_reader()
        else:
            key = key_generator(alphabet)
            key_saver(key)
    else:
        is_encrypting = False
        key = key_reader()
    if output == 1:
        print(substitution(text, key, is_encrypting))
    else:
        output_file = open("../3 task/Ciphered.txt", 'w', encoding='utf-8')
        output_file.writelines(substitution(text, key, is_encrypting))
        output_file.close()


application()
