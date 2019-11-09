import re
import typing

from LlamaLex.TokenNames import EnglishTokenName

PERIOD = r'\.'
QUESTION_MARK = r'\?'
DOLLAR_SIGN = r'\$'
HYPHEN_MINUS = r'\-'
CARET = r'\^'
OPENING_SQUARE_BRACKET = r'\['
CLOSING_SQUARE_BRACKET = r'\]'

DIGIT = r'\d'
WORD_CHARACTER = r'\w'
NOT_WORD_CHARACTER = r'\W'
ANY_CHARACTER = r'.'

SINGLE_QUOTE = "'"
LEFT_NUMBER_CURLY_BRACKET = '{'
RIGHT_NUMBER_CURLY_BRACKET = '}'


def filter_out_token_text_from_start(pattern: str, text: str, group_number: int = 0, ignore_case: bool = False) -> \
        typing.Optional[typing.Tuple[str, str]]:

    regex_match_result = re.match(r'^' + pattern, text, flags=(re.IGNORECASE if ignore_case else 0))

    if regex_match_result is None:
        return None

    index_for_splitting = len(regex_match_result.group(group_number))
    return text[0:index_for_splitting], text[index_for_splitting:]


def function_that_filters_out_token_text_from_start(pattern: str, token_name: EnglishTokenName, group_number: int = 0,
                                                    ignore_case: bool = False):

    def inner_function(text: str) -> typing.Optional[typing.Tuple[str, str, EnglishTokenName]]:
        filter_result = filter_out_token_text_from_start(pattern=pattern, text=text, group_number=group_number,
                                                         ignore_case=ignore_case)
        if filter_result is not None:
            return filter_result[0], filter_result[1], token_name

    return inner_function


# filter functions higher up have higher priority, as dictionaries in Python 3.7 are ordered
filter_functions: typing.Dict[str, typing.Callable] = {
    'symbol': function_that_filters_out_token_text_from_start(
        r'[\$#%]', EnglishTokenName.SYMBOL),
    'contraction': function_that_filters_out_token_text_from_start(
        r"(it's|that's|let's|he's|she's|what's|who's)", EnglishTokenName.WORD, ignore_case=True),
    'possessive_suffix': function_that_filters_out_token_text_from_start(
        r"'s?", EnglishTokenName.POSSESSIVE_SUFFIX),
    'ellipses': function_that_filters_out_token_text_from_start(
        f'{PERIOD}{PERIOD}{PERIOD}', EnglishTokenName.PUNCTUATION),
    'exclamation_mark': function_that_filters_out_token_text_from_start(
        r'!+', EnglishTokenName.PUNCTUATION),
    'question_mark': function_that_filters_out_token_text_from_start(
        f'{QUESTION_MARK}+', EnglishTokenName.PUNCTUATION),
    'email': function_that_filters_out_token_text_from_start(
        r'[a-z0-9_]+@[a-z0-9]+(.[a-z0-9]+)+', EnglishTokenName.WORD, ignore_case=True),
    'scientific_notation': function_that_filters_out_token_text_from_start(
        f'{HYPHEN_MINUS}?[1-9]({PERIOD}{DIGIT}*)?(e|x10{CARET})[+{HYPHEN_MINUS}]?{DIGIT}+', EnglishTokenName.NUMBER,
        ignore_case=True),
    'simple_number': function_that_filters_out_token_text_from_start(
        f'{HYPHEN_MINUS}?{DIGIT}+({PERIOD}{DIGIT}+)?', EnglishTokenName.NUMBER),
    'acronym_with_periods': function_that_filters_out_token_text_from_start(
        f'([A-Z]{PERIOD})' + r'{2,}s?', EnglishTokenName.WORD),
    'abbreviation_with_period': function_that_filters_out_token_text_from_start(
        f'(st|dr|mr){PERIOD}', EnglishTokenName.WORD, ignore_case=True),
    'other': function_that_filters_out_token_text_from_start(
        f'([^:;&*,.?!"(){OPENING_SQUARE_BRACKET}{CLOSING_SQUARE_BRACKET}{SINGLE_QUOTE}]+'
        f'{SINGLE_QUOTE}[a-z]{LEFT_NUMBER_CURLY_BRACKET}2,{RIGHT_NUMBER_CURLY_BRACKET}|'
        f'[^:;&*,.?!"(){OPENING_SQUARE_BRACKET}{CLOSING_SQUARE_BRACKET}{SINGLE_QUOTE}]+'
        f'{SINGLE_QUOTE}[a-rt-z]|'
        f'[^:;&*,.?!"(){OPENING_SQUARE_BRACKET}{CLOSING_SQUARE_BRACKET}{SINGLE_QUOTE}]+)', EnglishTokenName.WORD),
    'double_quote': function_that_filters_out_token_text_from_start(
        r'"', EnglishTokenName.PUNCTUATION),
    'round_brackets': function_that_filters_out_token_text_from_start(
        r'[()]', EnglishTokenName.PUNCTUATION),
    'square_brackets': function_that_filters_out_token_text_from_start(
        r'[\[\]]', EnglishTokenName.PUNCTUATION),
    'other_punctuation': function_that_filters_out_token_text_from_start(
        r'[:;&*,]', EnglishTokenName.PUNCTUATION),
    'period': function_that_filters_out_token_text_from_start(
        f'{PERIOD}', EnglishTokenName.PUNCTUATION)
}
