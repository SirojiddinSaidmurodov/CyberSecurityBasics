import os.path

latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
russian_alphabet = "абвгдеёжзийклмнопрстуфхцшщчъыьэюя"

alphabets = {0: latin_alphabet}

def get_setting(question, variants, error):
    """
        Function for setting the parameters of another functions
        :type error: str
        :type variants: int
        :type question: str
        :param question: your question with va riants of answers
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


def cipher(text, key, alphabet, is_Encrypt):
    key = -key if not is_Encrypt else key
    ciphered_text = ""
    for letter in text:
        upper = letter.isupper()
        letter = letter.lower()
        index = alphabet.find(letter)
        if index >= 0:
            letter = alphabet[(key + index) % len(alphabet)]
        if upper:
            ciphered_text += letter.upper()
        else:
            ciphered_text += letter
    return ciphered_text


def check_keys(text, alphabet):
    text = text[:50]
    for key in range(1, len(alphabet)):
        print(" {i:2d}".format(i=key) + "  >>  " + cipher(text, key, alphabet, False))


def application():
    alphabet = get_setting("Choose an alphabet:\n1 - Latin\n2 - Cyrillic\n", 2, "Wrong alphabet, try again\n")
    alphabet = latin_alphabet if alphabet == 1 else russian_alphabet
    encrypt = get_setting(
        "Enter the number:\n1 - if you want to encrypt something\n"
        "2 - if you want to decrypt something\n3 - you want to hack\n",
        3, "Wrong variant, try again!\n")
    input_type = get_setting("Choose the type of your input text:\n1 - text from command line\n2 - file\n", 2,
                             "Wrong type, try again!\n")
    if input_type == 2:
        while True:
            path = input("Enter the path to your text file:\n")
            if os.path.exists(path) and os.path.isfile(path):
                file = open(path, 'r', encoding='utf-8')
                break
            else:
                print("Wrong path, try again")
        text = "".join(line for line in file.readlines())

        file.close()
    else:
        text = input("Enter your text to command line:\n")


    output = get_setting("Choose the output type:\n1 - commandline\n2 - file\n", 2, "Wrong variant, try again!")

    if encrypt == 1:
        key = int(input("Enter the key:\n"))
        key = key % len(alphabet)
        if output == 1:
            print(cipher(text, key, alphabet, True))
        else:
            file = open("output.txt", 'w', encoding='utf-8')
            file.writelines(cipher(text, key, alphabet, True))
            file.close()
    elif encrypt == 3:
        check_keys(text, alphabet)
        key = int(input("Enter key:\n"))
        if output == 1:
            print(cipher(text, key, alphabet, False))
        else:
            file = open("output.txt", 'w', encoding='utf-8')
            file.writelines(cipher(text, key, alphabet, False))
            file.close()
    else:
        decipher_key = int(input("Enter the key for deciphering the text:\n"))
        decipher_key %= len(alphabet)
        print(cipher(text, decipher_key, alphabet, False))


application()
