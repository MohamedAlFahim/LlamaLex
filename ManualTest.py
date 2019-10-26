from LlamaLex.Lexer import EnglishLexer

for each in EnglishLexer.lex('-2000.0 equals -2000 equals -2e3 equals -2x10^3.'):
    print(each)
print(' ')
for each in EnglishLexer.lex('Carefully scanning the code, Mr. Programmer looked for potential bugs.'):
    print(each)
print(' ')
for each in EnglishLexer.lex('"What is the perfect programming language?," wondered Jim. '
                             'Of course, there was no answer...'):
    print(each)
print(' ')
for each in EnglishLexer.lex('"Why isn\'t this code working?!," yelled Jim. It was because of GPU drivers!...'):
    print(each)
print(' ')
for each in EnglishLexer.lex("Jim's code from 2001 works even in 2019. "
                             "Nevertheless, the Hawaiian Islands' top programmers pointed out a few performance issues."
                             " \"The program now runs 22.3% slower\", Mr. Programmer commented."):
    print(each)
print(' ')
for each in EnglishLexer.lex('His email is person123@email.com, and not person@some.domain.'):
    print(each)
print(' ')
for each in EnglishLexer.lex("Here is 'some text in single-quotes'."):
    print(each)
print(' ')
for each in EnglishLexer.lex("C.P.U.s are unfortunately not keeping up with Moore's law. Also, shrinking current "
                             "transistors below 7 nm is not possible due to quantum tunnelling (remember that "
                             "transistors must act like switches to function correctly)."):
    print(each)
print(' ')
for each in EnglishLexer.lex('Semicolons must not be overused; it is easier said than done. The semicolon is no match '
                             'for the ultimate punctuation mark: the colon.'):
    print(each)
print(' ')
for each in EnglishLexer.lex('Use [square brackets].'):
    print(each)
print(' ')
for each in EnglishLexer.lex("The chips' clock speeds were way slower than they should have been."):
    print(each)
print(' ')
for each in EnglishLexer.lex("The computer's GPU drivers were not working properly. The 'Why' was not answered."):
    print(each)
print(' ')
for each in EnglishLexer.lex("That's not a solution. That will bring more problems. "
                             "Shouldn't solution C be used instead?"):
    print(each)
print(' ')
for each in EnglishLexer.lex('User123 joined the server. In addition, User_123 joined the server.'):
    print(each)
print(' ')
