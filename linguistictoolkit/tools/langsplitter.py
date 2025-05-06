import unicodedata
from linguistictoolkit.tools.textsplitter import Lemma, SentenceSplitter
from typing import Callable, List, Optional

def is_punct(char):
    char_category = unicodedata.category(char)
    return (char_category[0] in 'PSZ' or char_category in ('Cc'))

def split_text_by_char(text: str, lang: Optional[str] = None, islang: Optional[Callable[[str], bool]] = None) -> SentenceSplitter:
    """
    根据字符拆分文本，将符合条件的字符单独作为一个词素。

    参数：
    text (str): 要拆分的文本。
    lang (str, optional): 语言代码，默认值为 None。
    islang (function, optional): 判断字符是否属于某语言的函数，默认值为 None。

    返回值：
    list: 拆分后的词素列表。
    """
    if islang is None:
        islang = lambda x: True

    wordlist: List[Lemma] = []
    current_token = ''
    in_lang = False

    def submit_current_lemma(token):
        if token != '':
            if in_lang:
                wordlist.append(Lemma(token, is_lang=True, properties={'lang': lang} if lang else {}))
            else:
                wordlist.append(Lemma(token, is_lang=False))
            

    for char in text:
        if is_punct(char):
            submit_current_lemma(current_token)
            current_token = ''
            wordlist.append(Lemma(char, is_lang=False, in_dict=True))
        elif islang(char) and unicodedata.category(char) == 'Lo':
            submit_current_lemma(current_token)
            current_token = ''
            in_lang = True
            wordlist.append(Lemma(char, is_lang=True, properties={'lang': lang} if lang else {}))
        else:
            current_token += char

    submit_current_lemma(current_token)
    current_token = ''
    #return wordlist
    return SentenceSplitter(wordlist)

def split_text_by_word(text: str, lang: Optional[str] = None, islang: Optional[Callable[[str], bool]] = None) -> SentenceSplitter:
    """
    根据单词拆分文本，将符合条件的单词作为一个词素。

    参数：
    text (str): 要拆分的文本。
    lang (str, optional): 语言代码，默认值为 None。
    islang (function, optional): 判断字符是否属于某语言的函数，默认值为 None。

    返回值：
    list: 拆分后的词素列表。
    """
    if islang is None:
        islang = lambda x: unicodedata.category(x)[0] not in 'PSZ' or unicodedata.category(x) not in ('Cc')

    wordlist: List[Lemma] = []
    current_token = ''
    in_lang = False
    def submit_current_lemma(token):
        if token != '':
            if in_lang:
                wordlist.append(Lemma(token, is_lang=True, properties={'lang': lang} if lang else {}))
            else:
                wordlist.append(Lemma(token, is_lang=False))

    for char in text:
        if in_lang ^ islang(char):  # 使用异或运算符检测语言切换
            submit_current_lemma(current_token)
            current_token = ''
        if is_punct(char):
            submit_current_lemma(current_token)
            current_token = ''
            if char not in "' -་":
                wordlist.append(Lemma(char, is_lang=False, in_dict=True))
            else:
                wordlist.append(Lemma(char, is_lang=False))
        elif islang(char):
            in_lang = True
            current_token += char
        else:
            in_lang = False
            current_token += char

    submit_current_lemma(current_token)
    #return wordlist
    return SentenceSplitter(wordlist)

def split_text_sea_lang(text: str, lang: Optional[str] = None, islang: Optional[Callable[[str], bool]] = None) -> SentenceSplitter:
    extend_to_right = 'ເແໂໃໄเแโใไ္្'
    equal_to_letter = 'ៗ'
    check_no_submit = '်'

    if islang is None:
        islang = lambda x: unicodedata.category(x)[0] not in 'PSZ' or unicodedata.category(x) not in ('Cc')

    wordlist: List[Lemma] = []
    current_token = ''
    is_extendable = False
    in_lang = False
    def submit_current_lemma(token):
        if token != '':
            if in_lang:
                wordlist.append(Lemma(token, is_lang=True, properties={'lang': lang} if lang else {}))
            else:
                wordlist.append(Lemma(token, is_lang=False))
    
    
    for pos, char in enumerate(text):
        if in_lang ^ islang(char):  # 使用异或运算符检测语言切换
            submit_current_lemma(current_token)
            current_token = ''
        if is_punct(char):
            submit_current_lemma(current_token)
            current_token = ''
            wordlist.append(Lemma(char, is_lang=False, in_dict=True))
        elif islang(char):
            letter_to_submit = unicodedata.category(char) == 'Lo'
            if char in equal_to_letter:
                letter_to_submit = True
            if unicodedata.category(char) == 'Nd':
                letter_to_submit = True
            if is_extendable:
                letter_to_submit = False
            if pos != len(text) - 1:
                if text[pos+1] in check_no_submit:
                    letter_to_submit = False
            if letter_to_submit:
                submit_current_lemma(current_token)
                current_token = ''
            in_lang = True
            current_token += char
            is_extendable = char in extend_to_right
        else:
            in_lang = False
            current_token += char

    submit_current_lemma(current_token)
    return SentenceSplitter(wordlist)
    #return wordlist
