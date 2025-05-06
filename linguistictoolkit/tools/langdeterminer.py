import unicodedata

def islang_by_name(lang_name):
    lang_name = lang_name.strip().lower()
    lang_dict = {
        "chinese": is_cn,
        "english": is_en,
        "russian": is_ru,
        "korean": is_ko,
        "japanese": is_ja,
        "greek": is_gr,
        "thai": is_th,
        "burmese": is_my,
        "vietnamese": is_vi,
        "cambodian": is_km,
        "khmer": is_km,
        "lao": is_lo,
        "sinhala": is_si,
        "sanskrit": is_sa,
        "hindi": is_sa,
        "devanagari": is_sa,
        "tibetan": is_bo,
    }
    if lang_name in lang_dict:
        return lang_dict[lang_name]
    else:
        return None

def is_punct(char):
    char_category = unicodedata.category(char)
    return (char_category[0] in 'PSZ' or char_category in ('Cc'))

def is_cn(char):
    if '\u4e00' <= char <= '\u9fef' or char == '〇': #基本区
        return True
    elif '\u3400' <= char <= '\u4dbf': #扩展A区
        return True
    elif '\U00020000' <= char <= '\U0002EBEF': #扩展B-F区
        return True
    elif '\U00030000' <= char <= '\U0003134F': #扩展G区
        return True
    else:
        return False

def is_en(char):
    return 'a' <= char.lower() <= 'z'

def is_ru(char):
    return char.lower() in 'абвгдеёжзийклмнопxрстуфхцчшщъыьэюя'

def is_ko(char):
    if '\uac00' <= char <= '\ud7a3':
        return True
    elif '\u1100' <= char <= '\u11ff': #朝鲜文字母区
        return True
    else:
        return False
    
def is_ja(char):
    if is_cn(char):
        return True
    elif '\u3040' <= char <= '\u30ff':
        return True #假名
    else:
        return False
    
def is_gr(char):
    if '\u0370' <= char <= '\u03ff':
        return True #基本希腊字母
    elif '\u1f00' <= char <= '\u1fff':
        return True #扩展希腊字母
    else:
        return False
    
def is_th(char):
    if '\u0e01' <= char <= '\u0e5c':
        return True
    else:
        return False
    
def is_my(char):
    if '\u1000' <= char <= '\u109f':
        return True
    else:
        return False

def is_lo(char):
    if '\u0e80' <= char <= '\u0edf':
        return True
    else:
        return False
    
def is_km(char):
    if '\u1780' <= char <= '\u17ff':
        return True
    else:
        return False
        
def is_si(char):
    if '\u0d80' <= char <= '\u0dff':
        return True
    else:
        return False
    
def is_am(char):
    if '\u1200' <= char <= '\u137f':
        return True
    elif '\u1380' <= char <= '\u139f':
        return True #埃塞俄比亚语言补充区
    elif '\u2d80' <= char <= '\u2ddf':
        return True #埃塞俄比亚语言扩展区
    elif '\uab00' <= char <= '\uab2f':
        return True #埃塞俄比亚语言扩展A区
    else:
        return False

def is_sa(char):
    if '\u0900' <= char <= '\u097f':
        return True #天城文区
    else:
        return False

def is_vi(char):
    if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ':
        return True
    else:
        return False

def is_bo(char):
    if '\u0f00' <= char <= '\u0fdf':
        return True
    else:
        return False