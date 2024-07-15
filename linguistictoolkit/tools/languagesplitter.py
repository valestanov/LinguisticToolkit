import unicodedata
from textsplitter import Lemma, SentenceSplitter
from typing import Callable, List, Optional

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
    
    for char in text:
        if islang(char) and unicodedata.category(char) == 'Lo':
            if current_token != '':
                wordlist.append(Lemma(current_token))
                current_token = ''
            wordlist.append(Lemma(char, properties={'lang': lang} if lang else {}))
        else:
            current_token += char

    if current_token != '':
        wordlist.append(Lemma(current_token))
    return wordlist
    #return SentenceSplitter(wordlist)

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
        islang = lambda x: unicodedata.category(x)[0] not in 'PSZ'

    wordlist: List[Lemma] = []
    current_token = ''
    current_lang = None
    flag = False
    for char in text:
        if flag ^ islang(char):  # 使用异或运算符检测语言切换
            if current_token != '':
                wordlist.append(Lemma(current_token, properties={'lang': current_lang} if current_lang else {}))
                current_token = ''
        if islang(char):
            flag = True
            current_token += char
            current_lang = lang
        else:
            flag = False
            current_token += char
            current_lang = None
    if current_token != '':
        wordlist.append(Lemma(current_token, properties={'lang': current_lang} if current_lang else {}))
    return wordlist
    #return SentenceSplitter(wordlist)

def split_text_sea_lang(text: str, lang: Optional[str] = None, islang: Optional[Callable[[str], bool]] = None):
    extend_to_right = 'ເແໂໃໄเแโใไ္្'
    if islang is None:
        islang = lambda x: unicodedata.category(x)[0] not in 'PSZ'

    wordlist: List[Lemma] = []
    current_token = ''
    is_extendable = False
    is_in_lang = False
    current_lang = None
    
    for char in text:
        if is_in_lang ^ islang(char):  # 使用异或运算符检测语言切换
            if current_token != '':
                wordlist.append(Lemma(current_token, properties={'lang': current_lang} if current_lang else {}))
                current_token = ''
        if islang(char):
            is_in_lang = True
            current_lang = lang
            if unicodedata.category(char) == 'Lo' and is_extendable == False:
                if current_token != '':
                    wordlist.append(Lemma(current_token, properties={'lang': current_lang} if lang else {}))
                    current_token = ''
            current_token += char
            is_extendable = char in extend_to_right
        else:
            is_in_lang = False
            current_token += char
            current_lang = None

    if current_token != '':
        wordlist.append(Lemma(current_token, properties={'lang': current_lang} if current_lang else {}))

    return wordlist
