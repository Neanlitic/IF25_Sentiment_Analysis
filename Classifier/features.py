# http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip : labelled tweets data set
# https://www.w3.org/community/sentiment/wiki/Datasets : emoticon Lexicon dictionary among others
# https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107 : english positive and negative words
# http://positivewordsresearch.com/liste-des-mots-positifs/ : french positive words
# http://richesse-et-finance.com/liste-mots-cles-negatifs/ : french negative words

from re import match

from Data.clean_data import clean_end_line
from Ressources.resource import get_path_resource


def load_positive_words(language='en'):
    """
    Load in a list all the positive words contained in a text file. One word per line
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return: list of words
    """
    if language == 'fr':
        path = get_path_resource('positive_word_fr.txt')
    elif language == 'en':
        path = get_path_resource('positive_word_en.txt')

    with open(path, 'rb') as file_positive_word:
        positive_word = [clean_end_line(x) for x in file_positive_word.readlines()]
    return positive_word


def load_negative_words(language='en'):
    """
        Load in a list all the negative words contained in a text file. One word per line
        :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
        :return: list of words
        """
    if language == 'fr':
        path = get_path_resource('negative_word_fr.txt')
    elif language == 'en':
        path = get_path_resource('negative_word_en.txt')

    with open(path, 'rb') as file_negative_word:
        negative_word = [clean_end_line(x) for x in file_negative_word.readlines()]
    return negative_word


def load_emoticons():
    """
    Load in two separate lists the positive and negative emoticons.
    The file is composed of 'emoticons'sep'0|1' per line.
    Due to the character used in emoticons we have to read them in binary mode.
    :return: 2 lists of positive and negative emoticons
    """
    positive_emoticon_dict, negative_emoticon_dict = list(), list()
    with open(get_path_resource('EmoticonSentimentLexicon.txt'), 'rb') as emoticons_file:
        for line in emoticons_file.readlines():
            key, value = line.split(b'sep')
            if value == b'1':
                positive_emoticon_dict.append(key)
            else:
                negative_emoticon_dict.append(key)
    return positive_emoticon_dict, negative_emoticon_dict


def _count_generic(list_element, list_words, weight=1):
    """
    Generic function to count the number of element from list_element in list_words.
    Since we are going to call this function in thread we use a struct -> dict to store the result of the counting.
    We can also apply a weight on the counting (emoticons have somehow bigger impact on the sentiment).
    :param list_element: list of elements we need to confront to list_words
    :param list_words: list of words that we are trying to count in list_element
    :param weight: importance coefficient to use
    :return: None, this function will be used in a thread (hence the dict)
    """
    count = 0
    for element in list_element:
        if element in list_words:
            count += 1 * weight
    return count


def _negation_presence(list_element, language='en'):
    """
    Method to be called within a thread to detect whether there is a negation or not among the elements of the tweets
    contained in the list of elements.
    :param list_element: list of relevant element in the tweet
    :param language: Choose the language from 'fr' that stands for french and 'en' that stands for english
        'fr' | 'en'
    :return: None, this function will be used in a thread (hence the dict)
    """
    if language == 'fr':
        for element in list_element:
            if match(rb'ne|n\'.*', element):
                return 1
    elif language == 'en':
        for element in list_element:
            if match(rb'.*n\'t', element) or match(rb'neither|not|nor', element):
                return 1
    return 0


def characteristic_vector(list_element_tweet, Ressource=None, language='en'):
    """
    Creation of the characteristic vector to further use in a classifier.
    The characteristics to be counted :
        - Number of positive words
        - Number of negative words
        - Number of positive emoticons
        - Number of negative emoticons
        - Presence of negation
    :param list_element_tweet: list of key elements of a tweet
    :param language: language used to write the tweet
        'fr' | 'en'
    :return: list / vector
    """
    if Ressource:
        positive_words = Ressource.positive_words
        negative_words = Ressource.negative_words
        positive_emoticons = Ressource.positive_emoticons
        negative_emoticons = Ressource.negative_emoticons
    else:
        positive_words = load_positive_words()
        negative_words = load_negative_words()
        positive_emoticons, negative_emoticons = load_emoticons()

    return [_count_generic(list_element_tweet, positive_words), _count_generic(list_element_tweet, negative_words),
            _count_generic(list_element_tweet, positive_emoticons, 2),
            _count_generic(list_element_tweet, negative_emoticons, 2), _negation_presence(list_element_tweet)]
