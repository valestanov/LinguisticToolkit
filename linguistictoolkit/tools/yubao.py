
#
#语保F12最大的那个Json响应的后处理程序

import json
import os

def tableproc(table):
    optable = {}
    for i in ['sounder','type']:
        if i not in optable:
            optable[i] = ''
    if 'items' not in optable:
        optable['items'] = []
    sounder = table['sounder']
    tabletype = table['type']
    tableitems = itemsproc(table['items'])
    return (sounder,tabletype,tableitems)

def itemsproc(items):
    opitems = []
    for num,i in enumerate(items,start=1):
        cols = ('name','syllable','remark','note')
        inhalt = ['%04d'%num,]
        for col in cols:
            try:
                inhalt.append(i[col].replace('\t',' ').replace('\n',' ').strip())
            except KeyError:
                inhalt.append('')
        opitems.append(inhalt)
    return opitems

def YubaoJsonProc(ipfile,opfile):
    #From JSON on Yubao Site to readable word list
    try:
        with open(ipfile,'r',encoding='utf-8') as ipf:
            metadata = json.load(ipf)
        data = metadata['data']
    except:
        print('文件有误')
    for table in data['resourceList']:
        tabledata = tableproc(table)
        with open(opfile,'a',encoding='utf-8') as opf:
            head = '%s-%s' % (tabledata[0],tabledata[1])
            opf.writelines('%s\n====================\n' % head)
            for item in tabledata[2]:
                opf.writelines(head + '-' + '\t'.join(item) + '\n')
            print('%s 输出完成' % head)
    print('全表输出完成')


def getsd(word, sdfh='0123456789'):
    sdtype = ''
    for char in word:
        if char in sdfh:
            sdtype += char
        else:
            sdtype += '-'
    while '--' in sdtype:
        sdtype = sdtype.replace('--','-')
    sdtype = sdtype.strip('-')
    return sdtype

def commonsdfh(description):
    sdfhlist = {'normal': '0123456789',
                'diac': '⁰¹²³⁴⁵⁶⁷⁸⁹',
                'ru': '0123456789ʔ',
                'diacru': '⁰¹²³⁴⁵⁶⁷⁸⁹ʔ'}
    try:
        return sdfhlist[description]
    except KeyError:
        return sdfhlist['normal']

def sdtodiacritics(word,diacriticstable,sdfh='0123456789'):
    word += ' '
    newword = ''
    sd = ''
    for char in word:
        if char in sdfh:
            sd += char
        else:
            if sd == '':
                newword += char
            else:
                try:
                    newword += diacriticstable[sd]
                    newword += '-'
                except KeyError:
                    newword += sd
                newword += char
                sd = ''
    newword = newword.replace('- ',' ')
    newword = newword[:-1]
    return newword

def autosddic(sdlist):
    numdict = {'0':'⁰', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶', '7':'⁷', '8':'⁸', '9':'⁹',}
    sddic = {}
    for sd in sdlist:
        sdout = ''
        for char in sd:
            try:
                sdout += numdict[char]
            except KeyError:
                sdout += char
        sddic[sd] = sdout
    return sddic

def getsdgroup(wordlist,sdfh='0123456789'):
    sdlist = [getsd(w,sdfh) for w in wordlist]
    sdgroup = sorted(list(set(sdlist)))
    allsd = sorted(list(set([sd.strip() for sd in '-'.join(sdgroup).split('-')])))
    sdlen = {}
    for sd in sdgroup:
        charlen = sd.count('-') + 1
        if charlen not in sdlen:
            sdlen[charlen] = []
        sdlen[charlen].append(sd)
    for charlen in sdlen:
        sdlen[charlen] = sorted(sdlen[charlen])
    bisyl = []
    for i in range(3):
        try:
            bisyl.append(sdlen[i])
        except KeyError:
            continue
    return allsd, bisyl, sdlen
    
