
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
        cols = ('name','syllable','remark','notes')
        inhalt = ['%04d'%num,]
        for col in cols:
            try:
                inhalt.append(i[col].replace('\t',' ').strip())
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


def getsd(word):
    sdtype = ''
    for char in word:
        if char in '0123456789':
            sdtype += char
        else:
            sdtype += '-'
    while '--' in sdtype:
        sdtype = sdtype.replace('--','-')
    sdtype = sdtype.strip('-')
    return sdtype

def sdtodiacritics(word,diacriticstable):
    word += ' '
    newword = ''
    sd = ''
    for char in word:
        if char in '0123456789':
            sd += char
        else:
            if sd == '':
                newword += char
            else:
                try:
                    newword += diacriticstable[sd]
                    newword += ' '
                except KeyError:
                    newword += sd
                newword += char
                sd = ''
    newword = newword[:-1]
    return newword
                
