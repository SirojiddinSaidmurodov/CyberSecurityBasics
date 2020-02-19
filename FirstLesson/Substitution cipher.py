from random import randint

latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
russian_alphabet = "абвгдеёжзийклмнопрстуфхцшщчъыьэюя"


# function to fet the answers for the questions
def get_setting(question, variants, error):
    while True:
        result = int(input(question))
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
    file = open("Key.txt", 'r')
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
    file = open("Key.txt", 'w')
    for letter in key.keys():
        file.write(str(letter) + str(key.get(letter)) + "\n")
    file.close()


def substitution(input_text: str, key, is_Encrypt):
    """
    Substitution ciphering function. Key is a dict (plain, encrypted) letters
    :type input_text: str
    :param input_text: text for encrypting or decrypting
    :param key: dict
    :param is_Encrypt: bool
    :return: str
    """
    encrypted_text = ""
    if is_Encrypt:
        key = {y: x for x, y in key.items()}
    for i in range(len(input_text)):
        encrypted_text += key.get(input_text[i], input_text[i])
    return encrypted_text


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet
    encrypt = get_setting("I want to...\n"
                          "1 - encrypt the text\n"
                          "2 - decrypt the text\n", 2, "Wrong variant, choose the valid one\n")
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
    text = input("Enter the text:\n")
    print(substitution(text, key, is_encrypting))


while True:
    application()
