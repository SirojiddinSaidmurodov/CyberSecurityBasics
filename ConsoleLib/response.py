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
