import enum


class EnglishTokenName(enum.Enum):

    # TODO: Implement math extraction (i.e. extract "2x" from "The answer is $2x$.")
    # MATH = enum.auto()  # Note that math preserves whitespace (i.e. a math token may keep the text "2x+5 = 10")

    POSSESSIVE_SUFFIX = enum.auto()  # i.e. "'" in "The chips' clock speeds" or "'s" in "The computer's software"

    NUMBER = enum.auto()
    WORD = enum.auto()

    PUNCTUATION = enum.auto()  # i.e. !, ?, :, ;, ",", ..., or .
    OPENING_PUNCTUATION = enum.auto()  # i.e. (, [, {, ', or "
    CLOSING_PUNCTUATION = enum.auto()  # i.e. ), ], }, ', or "

    SYMBOL = enum.auto()  # i.e. $, %, or #

    NONE = enum.auto()
