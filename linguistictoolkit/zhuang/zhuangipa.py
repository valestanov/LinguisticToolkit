import sys
import os

def initialisedic():
    folder = sys.path[0]
    smipafile = os.path.join(folder,'smipa.txt')
    ymipafile = os.path.join(folder,'ymipa.txt')
    sdipafile = os.path.join(folder,'sdipa.txt')
    global smipadic
    global ymipadic
    global sdipadic
    smipadic = dicparser(smipafile)
    ymipadic = dicparser(ymipafile)
    sdipadic = dicparser(sdipafile)
    global smlengthdic
    smlengthdic = {}
    for sm in smipadic:
        if len(sm) not in smlengthdic:
            smlengthdic[len(sm)]=[sm]
        else:
            smlengthdic[len(sm)].append(sm)
    global changym
    changym = []
    for ym in ymipadic:
        if 'ː' in ymipadic[ym]:
            changym.append(ym)
    global rsym
    rsym = []
    for ym in ymipadic:
        if ('p' in ym) or ('t' in ym) or ('k' in ym) or ('b' in ym) or ('d' in ym) or ('g' in ym):
            rsym.append(ym)
            
def dicparser(file):
    origindic = ''
    thedic = {}
    with open(file,'r',encoding='utf-8') as f:
        origindic = f.readlines()
    for phonemepair in origindic:
        pairlist = phonemepair.strip('\ufeff\n').strip('\t').split('\t')
        phoneme = pairlist[0].strip()
        ipa = pairlist[1].strip()
        thedic[phoneme] = ipa
    return thedic

class NoPhoneme(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

def scsyltoipa(scsyl):
    syl = scsyl
    sm = ''
    ym = ''
    sd = ''
    smipa = ''
    ymipa = ''
    sdipa = ''
    sdinterndic = {'z':2,'j':3,'x':4,'q':5,'h':6,'p':7,'t':7,'k':7,'b':9,'d':9,'g':9}
    try:
        #声调识别
        sd = 1 #未标调的默认即平声
        if syl[-1:] in sdinterndic: sd = sdinterndic[syl[-1]]
        if sd in [2,3,4,5,6]:
            syl = syl[:-1]
        #声母识别
        if syl[:3] in smlengthdic[3]:
            sm = syl[:3]
            ym = syl[3:]
        elif syl[:2] in smlengthdic[2]:
            sm = syl[:2]
            ym = syl[2:]
        elif syl[:1] in smlengthdic[1]:
            sm = syl[:1]
            ym = syl[1:]
        else:
            sm = '∅'
            ym = syl
        if ym in rsym:
            if sd == 7 and ym in changym: sd = 8 #长声调清入
        if sm in smipadic:
            smipa = smipadic[sm]
        else:
            raise NoPhoneme("声母有误：%s, %s, %s, %s" % (sm,ym,sd,syl))
        if ym in ymipadic:
            ymipa = ymipadic[ym]
        else:
            raise NoPhoneme("韵母有误：%s, %s, %s, %s" % (sm,ym,sd,syl))
        sd = str(sd) #转换成文本型，以免数字与文本类型不匹配无法识别
        if sd in sdipadic:
            sdipa = sdipadic[sd]
        else:
            raise NoPhoneme("声调有误：%s, %s, %s, %s" % (sm,ym,sd,syl))
        ipa = smipa + ymipa + sdipa
        return ipa
    except NoPhoneme as e:
        if syl != '': print(e)
        return scsyl

def sctoipa(text):
    scabc = 'abcdefghijklmnopqrstuvwxyz'
    word = ''
    ipatext = ''
    text = text.lower()
    text += ' '
    for i in text:
        if i in scabc:
            word += i
        else:
            ipatext += scsyltoipa(word)
            ipatext += i
            word = ''
    ipatext = ipatext[:-1]
    return ipatext

def filetoipa():
    folder = sys.path[0]
    inputfile = os.path.join(folder,'Inputfile.txt')
    outputfile = os.path.join(folder,'Outputfile.txt')
    with open(inputfile,'r',encoding='utf-8') as ipfile:
        sctext = ipfile.read()
    ipatext = sctoipa(sctext)
    with open(outputfile,'w',encoding='utf-8') as opfile:
        opfile.write(ipatext)
    return

if __name__ == "__main__":
    print ('Initializing......')
    initialisedic()
    print ('Initialized!\n')
    inputsc = ' '
    while inputsc != '':
        inputsc = input('请输入需要转换为IPA的壮文，可以整句整段输入。直接回车退出：\n')
        print(sctoipa(inputsc))


            
        
            
        

