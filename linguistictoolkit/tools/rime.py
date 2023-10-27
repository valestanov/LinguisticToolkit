import pyperclip
import math

def torime(textlines):
    textlines = textlines.replace('\r','').split('\n')
    for n,line in enumerate(textlines):
        line = line.split('\t')
        if len(line) >= 4:
            line = line[:3] + [''.join(line[3:])]
        else:
            while len(line) < 4:
                line.append('')
        line = [i.strip() for i in line]
        line = '%s[%s]{%s}【%s】' % tuple(line)
        line = line.replace('[]','').replace('{}','').replace('【】','')
        textlines[n] = line
    return '\n'.join(textlines)

supnumdic = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
puncdic = {'，': ', ', '。': '. ', '？': '? ', '、': ', ', '；': '; ', '：': ': ', '！': '! ', '——': ' — ', '（': ' (', '）': ') '}
punclist = [i for i in puncdic] + [puncdic[i].strip() for i in puncdic]
log = ''

def supnumber(text):
    for i in supnumdic:
        text = text.replace(i,supnumdic[i])
    return text

def nodupspace(text):
    while '  ' in text:
        text = text.replace('  ',' ')
    return text

def gettext(textlines,lborder='',rborder=''):
    textlines = textlines.replace('\r','').split('\n')
    if lborder == 1:
        lborder = ''
        rborder = ''
    elif lborder == 2:
        lborder = '['
        rborder = ']'
    elif lborder == 3:
        lborder = '{'
        rborder = '}'
    elif lborder == 4:
        lborder = '【'
        rborder = '】'
    for n, line in enumerate(textlines):
        line = nodupspace(line)
        for i in puncdic:
            line = line.replace(' ' + i,i)
        if lborder != '' and rborder != '':
            newline = ''
            inborder = False
            inotherborder = False
            for char in line:
                if char == lborder:
                    inborder = True
                elif char == rborder:
                    inborder = False
                elif char in '[{【':
                    inotherborder = True
                elif char in ']}】':
                    inotherborder = False
                else:
                    if inborder:
                        newline += char
                    else:
                        if (not inotherborder) and char in punclist:
                            if char in puncdic:
                                newline += puncdic[char]
                            elif char in punclist:
                                newline += char
                        else:
                            newline += ' '
            newline = nodupspace(newline).strip()
            for i in puncdic:
                newline = newline.replace(' ' + puncdic[i].strip(),puncdic[i].strip())
            textlines[n] = newline
        else:
            newline = ''
            inborder = True
            for char in line:
                if char in '[{【':
                    inborder = False
                elif char in ']}】':
                    inborder = True
                else:
                    if inborder:
                        newline += char
            newline = nodupspace(newline).strip()
            textlines[n] = newline
    return '\n'.join(textlines)

def rimetodic(rimetext):
    rimetext = rimetext.replace('\r','').strip('\ufeff\n').split('\n')
    rimetext = [i.strip() for i in rimetext if i.strip() != '']
    innerdic = {}
    for entry in rimetext:
        c = gettext(entry,1)
        if c not in innerdic:
            innerdic[c] = []
        innerdic[c].append(entry)
    return innerdic

def texttrans(text,dic,lborder = '\ue000',rborder = '\ue001'):
    innerdic = {}
    maxlength = 6
    allword = set(text)
    maxlength = max(int(math.log10(len(allword))),6)
    maxtext = '%0' + str(maxlength) + 'd'
    for n,i in enumerate(sorted(dic.items(),key=lambda x:len(x[0]),reverse=True)):
        no = lborder + (maxtext % n) + rborder
        innerdic[no] = dic[i[0]]
        text = text.replace(i[0],no)
    for no in innerdic:
        if isinstance(innerdic[no],list):
            text = text.replace(no,''.join(['%s%s%s' % (lborder,i,rborder) for i in innerdic[no]]))
        else:
            text = text.replace(no,lborder+innerdic[no]+rborder)
    return text

def texttowords(text,lborder='\ue000',rborder = '\ue001'):
    text = text.replace('\r','').strip('\ufeff\n')
    newtext = ''
    log = ''
    flag = False
    for i in text:
        if i == lborder:
            flag = True
        elif i == rborder:
            flag = False
        if not flag:
            if i in punclist + [' ']:
                newtext += (lborder+i+rborder)
                continue
        newtext += i
    text = newtext
    wlist = []
    sentlist = text.split('\n')
    try:
        for sent in sentlist:
            sent = sent.replace(rborder,lborder)
            sentinhalt = sent.replace(lborder,'')
            sent = sent.split(lborder)
            sentwords = []
            for word in sent:
                if word not in sentwords and word not in punclist + ['', ' ']:
                    sentwords.append(word)
            print('句子：\n%s' % gettext(sentinhalt,1))
            for i in sentwords:
                print(gettext(i,1),gettext(i,2),gettext(i,3),gettext(i,4),sep='\t')
            wordappend = input('需要添补的词，请用逗号隔开：\n').replace('，',',').split(',')
            sentwords.extend([i.strip() for i in wordappend if i.strip() != ''])
            for i in sentwords:
                if i not in [j[0] for j in wlist]:
                    wlist.append([i,gettext(i,1),gettext(i,2),gettext(i,3),gettext(i,4),'w'])
            wlist.append([sentinhalt,gettext(sentinhalt,1),gettext(sentinhalt,2),gettext(sentinhalt,3),gettext(sentinhalt,4),'s'])
            log = '\n'.join(['\t'.join(i) for i in wlist])
    except:
        return log
    return '\n'.join(['\t'.join(i) for i in wlist])

def inabc(text):
    return lambda x:x in text

def wordsplitter(text,func):
    textsplit = []
    word = ''
    flag = True
    for char in text:
        if func(char):
            flag = True
            word += char
        else:
            flag = False
            textsplit.append(word)
            word = ''
            textsplit.append(char)
    if flag:
        textsplit.append(word)
    return textsplit

def textsplittrans(text,dic,splitfunc,splitter = '\ue002',lborder = '\ue000',rborder = '\ue001'):
    innerdic = {}
    wordvecdic = {}
    newdic = {}
    maxlength = 6
    for i in dic:
        spliti = splitfunc(i.lower())
        newdic[splitter.join(spliti)] = dic[i]
    text = splitfunc(text.lower())
    allword = splitter.join([i for i in newdic]) + splitter.join(text)
    allword = list(set(allword.split(splitter)))
    maxlength = max(int(math.log10(len(allword))),6)
    maxtext = '%0' + str(maxlength) + 'd'
    for n,word in enumerate(allword):
        wordvecdic[word] = '%s%s%s' % (splitter, maxtext % n, splitter)
    newtext = ''
    for word in text:
        if word in wordvecdic:
            newtext += wordvecdic[word]
        else:
            newtext += word
    for word in list(newdic.keys()):
        newword = ''
        for syl in word.split(splitter):
            if syl in wordvecdic:
                newword += wordvecdic[syl]
            else:
                newtext += syl
        newdic[newword] = newdic[word]
    text = newtext
    for n,i in enumerate(sorted(newdic.items(),key=lambda x:len(x[0]),reverse=True)):
        no = lborder + (maxtext % n) + rborder
        innerdic[no] = newdic[i[0]]
        text = text.replace(i[0],no)
    for no in innerdic:
        if isinstance(innerdic[no],list):
            text = text.replace(no,''.join(['%s%s%s' % (lborder,i,rborder) for i in innerdic[no]]))
        else:
            text = text.replace(no,lborder+innerdic[no]+rborder)
    for word in wordvecdic:
        text = text.replace(wordvecdic[word],word)
    return text
            
        
    
