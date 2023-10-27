def lbltoaegisub(lbl):
    lbl = lbl.replace('\r','').split('\n')
    lbl = [i for i in lbl if len(i.split('\t'))>1]
    newlbl = []
    for i in lbl:
        i = i.split('\t')
        beg = float(i[0])
        end = float(i[1])
        bgm,bgs = divmod(beg,60)
        bgh,bgm = divmod(bgm,60)
        enm,ens = divmod(end,60)
        enh,enm = divmod(enm,60)
        t = 'Dialogue: 0,%d:%0d:%02.2f,%d:%0d:%02.2f,Default,,0,0,0,,' % (bgh,bgm,bgs,enh,enm,ens)
        newlbl.append(t)
    return '\n'.join(newlbl)

def aegisubtolbl(lbl):
    lbl = lbl.replace('\r','').split('\n')
    lbl = [i for i in lbl if len(i.split(','))>8]
    newlbl = []
    for i in lbl:
        i = i.split(',')
        beg = i[1].split(':')
        end = i[2].split(':')
        bgm = int(beg[0])*3600 + int(beg[1])*60 + float(beg[2])
        enm = int(end[0])*3600 + int(end[1])*60 + float(end[2])
        txt = '\,'.join(i[9:])
        t = '%f\t%f\t%s' % (bgm,enm,txt)
        newlbl.append(t)
    return '\n'.join(newlbl)
