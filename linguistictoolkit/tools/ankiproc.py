import pyperclip

def masker(singleword,isabc):
    singleword = singleword.strip(' ')
    if singleword == '':
        return ''
    output = ''
    if len(singleword)<2:
        output += '*'
    else:
        output += singleword[0]
    for ch in singleword[1:]:
        if isabc(ch):
            output += '*'
        else:
            output += ch
    return output

def wordmasker(words,isabc):
    masks = ''
    word = words + ' '
    singleword = ''
    for ch in word:
        if isabc(ch):
            singleword += ch
        else:
            masks += masker(singleword,isabc)
            singleword = ''
            masks += ch
    masks = masks.strip()
    return masks

def getabc(text):
    return ''.join(sorted(set(text)))
