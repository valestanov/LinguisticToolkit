enabc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
enabc = enabc + enabc.lower()
iscn = lambda x:x>='一'

def langsplit(line,islang):
    linelist = [islang(char) or char=='\t' for char in line]
    if True in linelist:
        pos = linelist.index(True)
        left = line[:pos].strip()
        right = line[pos:].replace('\t','').strip()
        while '  ' in left:
            left = left.replace('  ',' ')
        while '  ' in right:
            right = right.replace('  ',' ')
        return left,right
    else:
        return line,''

def textsplit(text,islang):
    text = text.replace('\ufeff','').replace('\r','').split('\n')
    textsplit = [langsplit(line,islang) for line in text]
    textsplit = ['\t'.join(line) for line in text]
    return '\n'.join(textsplit)
