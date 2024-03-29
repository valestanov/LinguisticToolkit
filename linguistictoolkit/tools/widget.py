enabc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
enabc = enabc + enabc.lower()

def langsplit(line,islang):
    linelist = [islang(char) for char in line]
    if True in linelist:
        return line[:linelist.index(True)],line[linelist.index(True):]
    else:
        return line,''
