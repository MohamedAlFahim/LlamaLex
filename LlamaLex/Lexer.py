import typing

import LlamaLex.Filters as EnglishFilters
from LlamaLex.TokenNames import EnglishTokenName

TOKEN_TYPE_HINT = typing.Tuple[str, EnglishTokenName]


class EnglishLexer:
    tokens: typing.List[TOKEN_TYPE_HINT] = []
    token_text: str = ''
    token_name: EnglishTokenName = EnglishTokenName.NONE

    input_text: str = ''
    position: int = 0

    opened_double_quote: bool = False
    opened_single_quote: bool = False
    potentially_opened_math: bool = False  # Note that "$100" can make potentially_opened_math True.

    disabled_filters: typing.List[str] = []  # By default, all filters are enabled.
    # Add a filter override if you want to use your own regular expression to match a token name.
    filter_overrides: typing.Dict[str, typing.Callable] = {}

    @classmethod
    def reset(cls):
        cls.tokens = []
        cls.token_text = ''
        cls.token_name = EnglishTokenName.NONE
        cls.input_text = ''
        cls.position = 0
        cls.opened_double_quote = False
        cls.opened_single_quote = False
        cls.potentially_opened_math = False
        cls.disabled_filters = []
        cls.filter_overrides = {}

    @classmethod
    def append_token(cls):
        if (cls.token_text in '([') and (cls.token_name is EnglishTokenName.PUNCTUATION):
            cls.token_name = EnglishTokenName.OPENING_PUNCTUATION
        elif (cls.token_text in ')]') and (cls.token_name is EnglishTokenName.PUNCTUATION):
            cls.token_name = EnglishTokenName.CLOSING_PUNCTUATION
        elif cls.token_text == '"' and (cls.token_name is EnglishTokenName.PUNCTUATION):
            cls.opened_double_quote = not cls.opened_double_quote
            cls.token_name = EnglishTokenName.OPENING_PUNCTUATION if cls.opened_double_quote else \
                EnglishTokenName.CLOSING_PUNCTUATION
        elif cls.token_text == "'" and cls.opened_single_quote:
            cls.opened_single_quote = False
            cls.token_name = EnglishTokenName.CLOSING_PUNCTUATION

        if (cls.token_name is EnglishTokenName.POSSESSIVE_SUFFIX) and (cls.token_text == "'") and \
                (cls.tokens[-1][1] is EnglishTokenName.OPENING_PUNCTUATION):
            cls.token_name = EnglishTokenName.OPENING_PUNCTUATION if (not cls.opened_single_quote) else \
                EnglishTokenName.CLOSING_PUNCTUATION
            cls.opened_single_quote = not cls.opened_single_quote

        cls.tokens.append((cls.token_text, cls.token_name))
        cls.token_text = ''
        cls.token_name = EnglishTokenName.NONE

    @classmethod
    def lex(cls, input_text: str, disable_filters: typing.List[str] = [],
            filter_overrides: typing.Dict[str, typing.Callable] = {}) -> typing.List[TOKEN_TYPE_HINT]:
        cls.disabled_filters = disable_filters
        cls.filter_overrides = filter_overrides
        cls.input_text = input_text + ' '
        while cls.position != len(cls.input_text):
            current_character = cls.input_text[cls.position]

            if cls.token_text.startswith('$'):
                cls.potentially_opened_math = True
            if (current_character != ' ') or cls.potentially_opened_math:
                cls.token_text += current_character
            else:
                cls.handle_space()

            cls.position += 1

        result = cls.tokens
        cls.reset()
        return result

    @classmethod
    def handle_space(cls):
        if cls.token_text.startswith("'"):  # i.e. 'Hello
            cls.handle_filter_function_result(("'", cls.token_text[1:], EnglishTokenName.OPENING_PUNCTUATION),
                                              open_single_quote=True)
        cls.decompose_and_analyze_current_token_text()
        cls.token_text = ''

    @classmethod
    def handle_filter_function_result(cls, filter_function_result, open_single_quote: bool = False):
        filtered_out_token_text, remaining_token_text, token_name = filter_function_result

        cls.token_text = filtered_out_token_text
        cls.token_name = token_name
        cls.append_token()

        if open_single_quote:
            cls.opened_single_quote = True

        cls.token_text = remaining_token_text
        cls.decompose_and_analyze_current_token_text()

    @classmethod
    def decompose_and_analyze_current_token_text(cls):
        # The idea is to recursively decompose the token text using filters, and add those pieces as tokens.
        # Note that some filters have higher priorities than other filters.

        current_token_text = cls.token_text
        if current_token_text == '':
            return

        names_of_allowed_filter_functions = [item for item in EnglishFilters.filter_functions if
                                             (item not in cls.disabled_filters)]
        allowed_filter_functions = [
            (EnglishFilters.filter_functions[each_name] if (each_name not in cls.filter_overrides) else
             cls.filter_overrides[each_name])
            for each_name in names_of_allowed_filter_functions
        ]
        for each_filter_function in allowed_filter_functions:
            filter_function_result = each_filter_function(current_token_text)
            if filter_function_result is not None:
                cls.handle_filter_function_result(filter_function_result)
                break
