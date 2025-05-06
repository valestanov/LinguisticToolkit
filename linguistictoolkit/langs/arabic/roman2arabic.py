import pyperclip
roabc = 'abcdfhijklmnqrstuwyzāīūġħšḍḏxḳṣṭṯẓ'
connectword = ['wa','sa','fa','ka','bi','li','al','qa','ha']
hideyword = ['cala','qila','mata','lada','mabna','ḳaḍa','ħatta','quxra','layla','mustašfa','qiħda','bala','ntaha','intaha']
nohideyword = ['cindamā']
rotoardic = {'a': 'َ', 'i': 'ِ', 'u': 'ُ', 'b': 'ب', 't': 'ت', 'ṯ': 'ث', 'j': 'ج', 'ħ': 'ح', 'x': 'خ', 'd': 'د', 'ḏ': 'ذ', 'r': 'ر', 'z': 'ز', 's': 'س', 'š': 'ش', 'ṣ': 'ص', 'ḍ': 'ض', 'ṭ': 'ط', 'ẓ': 'ظ', 'c': 'ع', 'ġ': 'غ', 'f': 'ف', 'ḳ': 'ق', 'k': 'ك', 'l': 'ل', 'm': 'م', 'n': 'ن', 'h': 'ه', 'w': 'و', 'y': 'ي'}
#rotoardic = {'a': '', 'i': '', 'u': '', 'b': 'ب', 't': 'ت', 'ṯ': 'ث', 'j': 'ج', 'ħ': 'ح', 'x': 'خ', 'd': 'د', 'ḏ': 'ذ', 'r': 'ر', 'z': 'ز', 's': 'س', 'š': 'ش', 'ṣ': 'ص', 'ḍ': 'ض', 'ṭ': 'ط', 'ẓ': 'ظ', 'c': 'ع', 'ġ': 'غ', 'f': 'ف', 'ḳ': 'ق', 'k': 'ك', 'l': 'ل', 'm': 'م', 'n': 'ن', 'h': 'ه', 'w': 'و', 'y': 'ي'}
puncdic = {',': '،', '?': '؟', '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤', '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'}
def rompreedit(word):
    #真主名讳
    if len(word)>=5 and len(word)<=6 and word[:5] == 'allah':
        word = 'al-lah' + word[5:]
    elif len(word)>=4 and len(word)<=5 and word[:4] == 'llah':
        word = 'l-lah' + word[4:]
    #冠词
    if len(word)>4 and (word[0] == 'a' and word[2] == '-'):
        if word[1] == 'l' and word[3] != 'l':
            word = 'al\u200d ' + word[3:]            
        for i in ['t', 'ṯ', 'd', 'ḏ', 'r', 'z', 's', 'š', 'ṣ', 'ḍ', 'ṭ', 'ẓ', 'l', 'n']:
            if word[:4] == ('a'+i+'-'+i):
                word = 'al\u200a\u200d '+i+i+word[4:]
    elif len(word)>3 and (word[1] == '-'):
        if word[0] == 'l' and word[2] != 'l':
            word = 'al\u200d ' + word[2:]
        else:
            for i in ['t', 'ṯ', 'd', 'ḏ', 'r', 'z', 's', 'š', 'ṣ', 'ḍ', 'ṭ', 'ẓ', 'l', 'n']:
                if word[:3] == (i+'-'+i):
                    word = 'al\u200a\u200d '+i+i+word[3:]
    #连接词
    if word in connectword:
        word += '\u200d'
    word = word.replace('-','\u200d ')
    word = word.split(' ')
    return word

def gethamza(left,right,pos):
    ugroup = ['u','ū']
    igroup = ['i','ī']
    agroup = ['a','ā','ً']
    endgroup = ['ٌ', 'ٍ']
    subendgroup = ['a','i','u']
    #词尾hamza
    if right in endgroup or pos==0:
            if left == 'u':
                return 'ؤ'
            elif left == 'i':
                return 'ئ'            
            elif left == 'a':
                return 'أ'
            else:
                return 'ء'
    else:
        if left in igroup or right in igroup:
            return 'ئ'
        elif left in ugroup or right in ugroup:
            return 'ؤ'
        elif right in agroup:
            if left in ugroup or left == 'ā' or left == 'w':
                return 'ء'
            elif left in igroup or left == 'y':
                return 'ئ'
            else:
                return 'أ'
        else:
            if left in agroup:
                return 'أ'
            else:
                return 'ء'
        

def romtoar(word,full=1):
    #隐藏y
    if word in hideyword:
        word += 'ى'
    elif word in nohideyword:
        word = word[:-1] + 'a' + 'ا'
    elif word[:-1]+word[-1].replace('ā','a') in hideyword:
        word = word[:-1] + 'a' + 'ى'
    #aa末尾的隐藏y
    if len(word)>4 and word[-2] not in ('n','m','h') and word[-1] == 'ā':
        word = word[:-1] + 'a' + 'ى'
    #鼻音尾
    if len(word)>4 and word[-2:] in ['an','un','in']:
        word = word[:-2] + ['ًا', 'ٌ', 'ٍ'][['an','un','in'].index(word[-2:])]
    #长uw变位：
    if len(word)>4 and word[-1] == 'ū':
        word = word + 'ا'
    #非hamza元音开头
    if word[0] in 'aiu':
        word = 'ا' + word
    #阴性:
    if len(word)>=5:
        if word[-3:-1]=='at' and word[-1] in ['ٌ', 'ٍ','a','i','u'] :
            word = word[:-2] + 'ة' + word[-1]
        elif word[-4:-2]=='at' and word[-2:] == 'ًا':
            word = word[:-3] + 'ة' + word[-2]
#        elif word[-2:]=='at':
#            word = word[:-1] + 'ة'
    #hamza底座
    if len(word)>=2 and word[:2] in ['qā']:
        word = 'آ' + word[2:]    
    if len(word)>=2 and word[:2] in ['qa','qu','qū']:
        word = 'أ' + word[1:]
    elif len(word)>=2 and word[:2] in ['qi','qī']:
        word = 'إ' + word[1:]
    word = word.replace('q','ء')
    if len(word)>=2:
        word = list(word)
        hamzalist = [pos for (pos,j) in enumerate(word) if j == 'ء']
        for pos in hamzalist:
            if pos < len(word)-2 or (pos == len(word)-2 and word[pos+1] not in ['ً', 'ٌ', 'ٍ','a','i','u']):
                thehamza = gethamza(word[pos-1],word[pos+1],1)
                word = word[:pos]+[thehamza+'ْ']+ word[pos+1:]
            elif pos == len(word)-2:
                thehamza = gethamza(word[pos-1],word[pos+1],0)
                word = word[:pos]+[thehamza]+ word[pos+1:]
            else:
                thehamza = gethamza(word[pos-1],'ٌ',0)
                word = word[:pos]+[thehamza]
        word = ''.join(word)
        if word[-4:] == 'ءًْا':
            word = word[:-1]
    else:
        word = word.replace('ء','أ')
    #长音
    word = word.replace('ā','aا')
    word = word.replace('ī','iy')
    word = word.replace('ū','uw')    
    #叠音
    for i in 'bcdfhjklmnrstwyzġħšḍḏxḳṣṭṯẓ':
        word = word.replace(i+i,i+'ّ')
    #静音
    for i in ('ءأإئؤة' + 'bcdfhjklmnrstwyzġħšḍḏxḳṣṭṯẓ'):
        word = word.replace(i,i+'ْ')
    for i in rotoardic:
        word = word.replace(i, rotoardic[i])
    #上标清理
    word = word.replace('ِيْ','ِي')
    word = word.replace('ُوْ','ُو')
    while 'ْْ' in word:
        word = word.replace('ْْ','ْ')
    word = word.replace('ّْ','ّْ')
    #a前的连续辅音：
    if len(word)>4 and word[1] == 'ْ' and word[3] == 'ْ':
        word = 'ا' + word
    for i in ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ']:
        word = word.replace('ْ'+i,i)
        word = word.replace(i+'ْ',i)
    if full == 3:
        for i in ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ']:
            word = word.replace(i,'')
    elif full == 2:
        for i in ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ']:
            word = word.replace(i,'')
    elif full == 1:
        for i in ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ']:
            word = word[:-1].replace(i,'') + word[-1]
    elif full == 0:
        word = word
    return word

def texttoar(text,full=1):
    text = text.lower()
    text += ' '
    newtext = []
    word = ''
    for char in text:
        if char in roabc + '-':
            word += char
        else:
            if word != '':
                newtext.extend(rompreedit(word))
            newtext.append(char)
            word = ''
    text = ''.join(newtext)
    text = text.replace('li\u200d al\u200d', 'lil\u200d')
    text = text.replace('li\u200d al\u200a\u200d', 'lil\u200a\u200d')
    newtext = []
    for char in text:
        if char in roabc:
            word += char
        else:
            if word != '':
                newtext.append(romtoar(word,full=full))
            newtext.append(char)
            word = ''
    text = ''.join(newtext)
    text = text.replace('ْ\u200a','')
    text = text.replace('\u200a','')
    text = text.replace('\u200d ','')
    text = text.replace('\u200d','')
    text = text.replace('الْله','الله')
    text = text.replace('اللّه','الله')
    for i in puncdic:
        text = text.replace(i,puncdic[i])
    return text
