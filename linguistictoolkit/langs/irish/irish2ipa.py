import pyperclip
import os

folder = os.path.dirname(os.path.abspath(__file__))
predef = os.path.join(folder,'IrishIPADict.txt')
predefdic = {}
checkflag = False

def initialize():
    if __name__ == "__main__":
        os.startfile(predef)
        input('确定自定义词典？')
    with open(predef,'r',encoding='utf-8') as f:
        tmp = f.read()
    tmp = tmp.strip('\ufeff \n').split('\n')
    tmp = [t.strip('\n').split('\t') for t in tmp]
    predefdic = dict([(t[0].strip().lower(),(t[1].strip(),t[2].strip())) for t in tmp])
    if __name__ == "__main__":
        print('词典初始化完成。')
    return predefdic

def checkdic():
    os.startfile(predef)
    input('确定自定义词典？')
    predefdic = initialize()

predefdic = initialize()

def irishtext(text,opt=1):
    gaabc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÚáéíóú'
    word = ''
    ipatext = ''
    text += ' '
    for i in text:
        if i in gaabc:
            word += i
        else:
            ipa = irishipa(word,opt)
            if opt == 2:
                if len(word)>=1:
                    if word[0] == word[0].upper():
                        if len(ipa)>1:
                            ipa = ipa[0].upper() + ipa[1:]
                        else:
                            ipa = ipa[0].upper()
            ipatext += ipa
            ipatext += i
            word = ''
    ipatext = ipatext[:-1]
    return ipatext

def irishipa(word,opt=1,accent=1):
    if word == '':
        return ''
    if word.lower() in predefdic:
        if opt == 1:
            return predefdic[word.lower()][0]
        elif opt == 2:
            return predefdic[word.lower()][1]
    try:
        originalword = word
        vowellist = ['Á','EÁ','ÁI','EÁI','É','ÉA','ÉI','AE','AEI','Í','UÍ','OÍ','AO','AOI','ÍO','UÍO','AÍO','Ó','ÓI','EO','EOI','Ú','ÚI','IÚI','IÚ','A','AI','EA','EAI','E','EI','I','UI','IO','O','OI','U','IU','IA','IAI','UA','UAI']
        word = word.upper()
        word += ' '
        #word = word.replace('OMH','Ú断')
        #word = word.replace('UMH','Ú断')
        #word = word.replace('UBH','Ú断')
        #word = word.replace('ABH','Ъ奥Ъ')
        #word = word.replace('AMH','Ъ奥Ъ')
        #word = word.replace('ODH','Ъ奥Ъ')
        #word = word.replace('OGH','Ъ奥Ъ')
        #word = word.replace('ADH','Ъ艾Ъ')
        #word = word.replace('AGH','Ъ艾Ъ')
        #word = word.replace('AIDH','Ъ艾Ь')
        #word = word.replace('AIGH','Ъ艾Ь')
        #word = word.replace('EIDH','Ь艾Ь')
        #word = word.replace('EIGH','Ь艾Ь')
        #word = word.replace('OIGH','Ъ艾Ь')
        word = word.replace('BH','博')
        word = word.replace('CH','赫')
        word = word.replace('DH','德')
        word = word.replace('FH','法')
        word = word.replace('GH','格')
        word = word.replace('LL','勒')
        word = word.replace('MH','姆')
        word = word.replace('NN','尼')
        word = word.replace('PH','佩')
        word = word.replace('RR','热')
        word = word.replace('SH','瑟')
        word = word.replace('TH','特')
        syls = []
        syl = ''
        vowelflag = ''
        for n,i in enumerate(word):
            if vowelflag != isvowel(i) or vowelflag == 'c' or (vowelflag == 'v' and syl+i not in vowellist):
                if n == len(word)-1 or syl+i+word[n+1] not in vowellist:
                    if syl != '':
                        syls.append(gaphoneme(syl,vowelflag))
                        syl = ''
            syl += i
            vowelflag = isvowel(i)

        syls[0].begin = True
        syls[-1].end = True
        
        gaphonv = [g for g in syls if g.cv == 'v']
        if len(gaphonv)>0:
            gaphonv[accent-1].accent = True

        for n,gaphon in enumerate(syls):
            gaphon.prephon = syls[n-1] if not gaphon.begin else None
            gaphon.nextphon = syls[n+1] if not gaphon.end else None
            gaphon.preabc = syls[n-1].firstabc if not gaphon.begin else ''
            gaphon.nextabc = syls[n+1].lastabc if not gaphon.end else ''
            gaphon.sylvcount = len([g for g in syls if g.cv=='v'])
            if len([g for g in syls[n-1::-1] if g.cv == 'v']):
                gaphon.prev = [g for g in syls[n-1::-1] if g.cv == 'v'][0]
            if len([g for g in syls[n+1:] if g.cv == 'v']):
                gaphon.nextv = [g for g in syls[n+1:] if g.cv == 'v'][0]
            if len([g for g in syls[n-1::-1] if g.cv == 'c']):
                gaphon.prec = [g for g in syls[n-1::-1] if g.cv == 'c'][0]      
            if len([g for g in syls[n+1:] if g.cv == 'c']):
                gaphon.nextc = [g for g in syls[n+1:] if g.cv == 'c'][0]

        try:
            for gaphon in syls:
                gaphon.broadslender()    
            while len([i for i in syls if i.bs=='wait' or i.bs == 'vor']):
                for gaphon in syls:
                    gaphon.broadslender()
                    
            for gaphon in syls:
                gaphon.ipaget()
            for gaphon in syls:
                gaphon.ipaget()
            for gaphon in syls:
                gaphon.sandhi()
            for gaphon in syls:
                gaphon.sandhi()
            for gaphon in syls:
                gaphon.relink()
            for gaphon in syls:
                gaphon.sandhi()
            for gaphon in syls:
                gaphon.relink()
            for gaphon in syls:
                gaphon.cyrilic()
        except (KeyboardInterrupt, SystemExit) as e:
            raise e
        except Exception as e:
            #raise IrishIPAError
            raise e

        if checkflag:
            raise IrishIPAError
        
        if opt == 1:
            ipa = ''.join([i.ipa for i in syls])
        elif opt == 2:
            ipa = ''.join([i.cyril for i in syls])
        if max(ipa)>='一':
            raise IrishIPAError
        for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ':
            if i in ipa:
                raise IrishIPAError
        #ipa = meihua(ipa)
        return ipa
    except (KeyboardInterrupt, SystemExit) as e:
        raise e
    except IrishIPAError as e:
        try:
            print('Error: ',[i.name for i in syls],[i.bs for i in syls],[i.ipa for i in syls],[i.cyril for i in syls])
            raise e
            return originalword
        except:
            print(e)
            return originalword

class IrishIPAError(Exception):
    pass

def meihua(ipa):
    #meihuadic = {'ː':'̄' , 'i':'ˠɪ', 'ʲˠɪ' : 'ʲi', 'kʲ' : 'c' , 'gʲ' : 'ɟ' , 'xʲ' : 'ç' , 'sʲ' : 'ʃ'}
    meihuadic = {'ː':'̄' , 'i':'ˠɪ', 'ʲˠɪ' : 'ʲi', 'sʲ' : 'ʃ','ʲ':'̃'}
    for i in meihuadic:
        ipa = ipa.replace(i,meihuadic[i])
    return ipa

def isvowel(abc):
    if abc in 'AOUÁÓÚEIÉÍ艾爱奥ЬЪ':
        return 'v'
    elif abc == ' ':
        return 0
    else:
        return 'c'

class gaphoneme():
    def __init__(self,name,cv):
        self.name = name.upper()
        self.cv = cv.lower()
        self.firstabc = name[0]
        self.lastabc = name[-1]
        self.ipa = name.upper()
        self.accent = False
        self.bs = ''
        self.preabc = ''
        self.nextabc = ''
        self.prephon = None
        self.nextphon = None
        self.prev = None
        self.nextv = None
        self.prec = None
        self.nextc = None
        self.nextnextc = None
        self.begin = False
        self.end = False
        self.sylvcount = 0
        self.cyril = name.upper()
        
    def broadslender(self):
        if self.cv == 'c':
            if (self.prephon != None and self.prephon.cv == 'v') or (self.nextphon != None and self.nextphon.cv == 'v'):
                if self.prephon != None and self.prephon.cv == 'v':
                    if self.prephon.name == 'AE':
                        self.bs = 'br'
                        return
                    elif self.prephon.lastabc in 'EIÉÍЬ':
                        self.bs = 'sl'
                        return
                    elif self.prephon.lastabc in 'AOUÁÓÚЪ':
                        self.bs = 'br'
                if self.nextphon != None and self.nextphon.cv == 'v':
                    if self.nextphon.firstabc in 'EIÉÍЬ':
                        self.bs = 'sl'
                    elif self.nextphon.firstabc in 'AOUÁÓÚЪ':
                        self.bs = 'br'
                        return
            else:
                if self.bs == '':
                    self.bs = 'wait'
            if self.bs == 'wait':
                if self.nextphon == None:
                    self.bs = 'vor'
                else:
                    if self.nextphon.bs != '':
                        self.bs = self.nextphon.bs
            elif self.bs == 'vor':
                if self.prephon == None:
                    self.bs = ''
                else:
                    if self.prephon.bs != 'wait':
                        self.bs = self.prephon.bs

    def ipaget(self):
        if self.name in ('Á','EÁ','ÁI','EÁI'):
            self.ipa = 'ɑː'
        elif self.name in ('É','ÉA','ÉI','AE','AEI'):
            self.ipa = 'eː'
        elif self.name in ('Í','UÍ','OÍ','AO','AOI'):
            self.ipa = 'iː'
        elif self.name in ('ÍO','UÍO','AÍO'):
            if self.nextphon != None and self.nextphon.name in ('R','L','赫'):
                self.ipa = 'iːə'
            else:
                self.ipa = 'iː'
        elif self.name in ('Ó','ÓI'):
            if self.prephon != None and self.prephon.name in ('N','尼','M','姆'):
                self.ipa = 'uː'
            elif self.nextphon != None and self.nextphon.name in ('N','尼','M','姆'):
                self.ipa = 'uː'
            else:
                self.ipa = 'oː'
        elif self.name in ('EO','EOI'):
            if self.prephon != None and self.prephon.name in ('N','尼','M','姆'):
                self.ipa = 'uː'
            elif self.nextphon != None and self.nextphon.name in ('N','尼','M','姆'):
                self.ipa = 'uː'
            elif self.nextphon != None and self.nextphon.name in ('赫'):
                self.ipa = 'o'
            else:
                self.ipa = 'oː'
        elif self.name in ('Ú','ÚI','IÚI','IÚ'):
            self.ipa = 'uː'
        elif self.name == 'A':
            if not self.accent:
                self.ipa = 'ə'
            else:
                if self.nextphon != None and self.nextphon.nextphon != None and self.nextphon.cv=='c' and self.nextphon.nextphon.name in ('Á','EÁ','ÁI','EÁI'):
                    self.ipa = 'u'
                else:
                    self.ipa = 'aː'
        elif self.name == 'AI':
            if not self.accent:
                self.ipa = 'ə'
            else:
                if self.begin:
                    self.ipa = 'æː'
                elif (self.prephon != None and self.prephon.name in ('T','D','S','R','H')) and (self.nextphon != None and self.nextphon.bs == 'sl'):
                    self.ipa = 'æː'
                elif self.nextphon != None and self.nextphon.nextphon != None and self.nextphon.cv=='c' and self.nextphon.nextphon.name in ('Á','EÁ','ÁI','EÁI'):
                    self.ipa = 'u'
                else:
                    self.ipa = 'aː'
        elif self.name in ('EA','EAI'):
            if not self.accent:
                self.ipa = 'ə'
            else:
                if self.prephon != None and self.prephon.prephon != None and self.prephon.prephon.name == 'S' and self.prephon.name == 'R':
                    self.ipa = 'aː'
                elif self.nextphon != None and self.nextphon.nextphon != None and self.nextphon.name in ('R','S','N','T','D') and self.nextphon.nextphon.name in ('Á','EÁ','ÁI','EÁI'):
                    self.ipa = 'i'
                else:
                    self.ipa = 'æː'
        elif self.name in ('E', 'EI'):
            if not self.accent:
                self.ipa = 'ə'
            else:
                if self.nextphon != None and self.nextphon.name in ('N','尼','M','姆'):
                    self.ipa = 'i'
                else:
                    self.ipa = 'e'
        elif self.name == 'I':
            if not self.accent:
                self.ipa = 'ə'
            else:
                self.ipa = 'i'
        elif self.name == 'UI':
            if self.prephon != None and self.nextphon != None and self.prephon.bs == 'br' and self.nextphon.name in ('格''特') and self.sylvcount == 1:
                self.ipa = 'u'
            else:
                self.ipa = 'i'
        elif self.name == 'IO':
            if (not self.begin) and self.nextphon != None and (self.nextphon.name in ('R','S','N','T','D') or (self.nextphon.name == '特' and self.nextphon.end)):
                self.ipa = 'i'
            else:
                self.ipa = 'u'
        elif self.name == 'O':
            if not self.accent:
                self.ipa = 'ə'
            else:
                if self.nextphon != None and self.nextphon.name in ('N','尼','M','姆'):
                    self.ipa = 'u'
                else:
                    self.ipa = 'o'
        elif self.name == 'OI':
            if (self.nextphon != None and self.nextphon.name in ('N','M','姆','尼')) and (self.nextphon.nextphon == None or self.nextphon.nextphon.name not in ('N','L','尼','勒')):
                self.ipa = 'i'
            elif (self.nextphon != None and self.nextphon.nextphon != None) and self.nextphon.name == 'R' and self.nextphon.nextphon.name in ('T','N','D','L','尼','勒'):
                self.ipa = 'o'
            elif (self.nextphon != None and self.nextphon.nextphon != None) and self.nextphon.name == '赫' and self.nextphon.nextphon.name == 'T':
                self.ipa = 'o'
            elif (self.prephon != None and self.nextphon != None) and self.prephon.bs == 'br' and self.nextphon.name in ('格','赫') and self.nextphon.end and self.sylvcount == 1:
                self.ipa = 'o'
            else:
                self.ipa = 'e'
        elif self.name in ('U','IU'):
            if self.nextphon != None and self.nextphon.name in ('赫','R','L','热','勒'):
                self.ipa = 'o'
            else:
                self.ipa = 'u'
        elif self.name in ('IA','IAI'):
            self.ipa = 'iːə'
        elif self.name in ('UA','UAI'):
            self.ipa = 'uːə'
        elif self.name in ('EЪ奥Ъ','Ъ奥ЪA','EЪ奥ЪA','Ъ奥Ъ'):
            if self.accent and not self.end:
                self.ipa = 'au'
        elif self.name in ('EЪ艾Ъ','Ъ艾ЪA','EЪ艾ЪA','Ъ艾Ъ','Ъ艾Ь','Ъ艾ЬE','Ь艾Ь','Ь艾ЬE'):
            if self.accent and not self.end:
                self.ipa = 'ai'
        #辅音部分！
        elif self.name == 'B':
            if self.bs == 'br':
                if self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 'p'
                else:
                    self.ipa = 'b'
            elif self.bs == 'sl':
                self.ipa = 'bʲ'
        elif self.name == '博':
            if self.bs == 'sl':
                if self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 'fʲ'
                else:
                    self.ipa = 'wʲ'
            elif self.bs == 'br':
                if self.nextphon != None and self.nextphon.name in ('特'):
                    self.ipa = 'f'
                elif not self.begin and self.nextphon != None and self.nextphon.name in ('F'):
                    self.ipa = 'f'
                elif self.prephon != None and self.prephon.name in ('U','IU','Ú','ÚI','IÚI','IÚ'):
                    self.ipa = '长u'
                elif self.prephon != None and self.prephon.name in ('A','EA') and not self.end and self.prephon.accent:
                    self.ipa = '奥u'
                elif self.sylvcount == 1 and self.end and self.prephon != None and self.prephon.cv == 'v' and ('ː' not in self.prephon.ipa or self.prephon.ipa in ('aː' , 'æː')):
                    self.ipa = ''
                elif self.prephon != None and self.prephon.name in ('R'):
                    self.ipa = 'uː'
                else:
                    self.ipa = 'w'
        elif self.name == 'C':
            if self.bs == 'br':
                self.ipa = 'k'
            elif self.bs == 'sl':
                self.ipa = 'kʲ'
        elif self.name == '赫':
            if self.bs == 'br':
                self.ipa = 'x'
            elif self.bs == 'sl':
                if self.begin:
                    self.ipa = 'xʲ'
                elif (self.prephon != None and self.nextphon != None) and self.prephon.name == 'UAI' and self.nextphon.name == 'E' and self.prephon.accent:
                    self.ipa = 'iː'
                else:
                    self.ipa = '和'
        elif self.name == 'D':
            if self.bs == 'br':
                if self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 't'
                else:
                    self.ipa = 'd'
            elif self.bs == 'sl':
                if self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 'tʲ'
                else:
                    self.ipa = 'dʲ'
        elif self.name == '德':
            if self.bs == 'sl':
                if self.begin:
                    self.ipa = 'ɣʲ'
                elif self.prephon != None and self.prephon.name in ('AI','EI') and not self.end and self.prephon.accent:
                    self.ipa = '艾i'
                elif self.end:
                    self.ipa = ''
                else:
                    self.ipa = 'ɣʲ'
            elif self.bs == 'br':
                if self.begin:
                    self.ipa = 'ɣ'
                elif self.prephon != None and self.prephon.name in ('A','EA') and not self.end and self.prephon.accent:
                    self.ipa = '艾i'
                elif self.prephon != None and self.prephon.name in ('O')  and not self.end and self.prephon.accent:
                    self.ipa = '奥u'
                elif (self.prephon != None and self.nextphon != None and self.nextphon.nextphon != None) and self.prephon.name == 'UA' and self.nextphon.name == 'A' and self.nextphon.nextphon.name == '德' and self.prephon.accent:
                    self.ipa = 'uː'
                elif self.end:
                    self.ipa = ''
                else:
                    self.ipa = 'h'
        elif self.name == 'F':
            if self.bs == 'br':
                self.ipa = 'f'
            elif self.bs == 'sl':
                self.ipa = 'fʲ'
        elif self.name == '法':
            self.ipa = ''
            if self.nextphon != None and self.prephon != None:
                self.nextphon.prephon = self.prephon
                self.prephon.nextphon = self.nextphon
        elif self.name == 'G':
            if self.bs == 'br':
                if self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 'k'
                else:
                    self.ipa = 'g'
            elif self.bs == 'sl':
                if self.prephon != None and self.prephon.name in ('N') and self.end and self.prephon.prephon != None and self.prephon.prephon.cv == 'v' and not self.prephon.prephon.accent:
                    self.ipa = ''
                elif self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 'kʲ'
                elif self.end and self.prephon != None and 'ː' not in self.prephon.ipa:
                    self.ipa = 'kʲ'
                else:
                    self.ipa = 'gʲ'
        elif self.name == '格':
            if self.bs == 'sl':
                if self.begin:
                    self.ipa = 'ɣʲ'
                elif self.prephon != None and self.prephon.name in ('AI','EI','OI') and not self.end and self.prephon.accent:
                    self.ipa = '艾i'
                elif self.end:
                    self.ipa = ''
                else:
                    self.ipa = 'ɣʲ'
            elif self.bs == 'br':
                if self.begin:
                    self.ipa = 'ɣ'
                elif self.prephon != None and self.prephon.name in ('A','EA') and not self.end and self.prephon.accent:
                    self.ipa = '艾i'
                elif self.prephon != None and self.prephon.name in ('O')  and not self.end and self.prephon.accent:
                    self.ipa = '奥u'
                else:
                    self.ipa = 'ɣ'
        elif self.name == 'H':
            self.ipa = 'h'
        elif self.name == 'L':
            if self.bs == 'br':
                self.ipa = 'ʟ'
            elif self.bs == 'sl':
                if self.begin:
                    self.ipa = 'ʟʲ'
                elif self.prephon != None and self.prephon.name == 'R':
                    self.ipa = 'ʟʲ'  
                elif self.nextphon != None and self.nextphon.name == 'T':
                    self.ipa = 'ʟʲ'
                else:
                    self.ipa = 'lʲ'
            if self.nextphon != None and self.nextphon.name in ('B','博','F','M','G','赫') and self.prev != None and ('ː' not in self.prev.ipa or self.prev.ipa in ('aː' , 'æː')) and self.prev.accent:
                self.ipa += 'ə'
        elif self.name == '勒':
            if self.bs == 'br':
                self.ipa = 'ʟ'
            elif self.bs == 'sl':
                self.ipa = 'ʟʲ'
            if self.nextphon != None and self.nextphon.name in ('B','博','F','M','G','赫') and self.prev != None and ('ː' not in self.prev.ipa or self.prev.ipa in ('aː' , 'æː')) and self.prev.accent:
                self.ipa += 'ə'
#至爱尔兰语教材第217页Fh，2023年6月7日03:19:34。
        elif self.name == 'M':
            if self.bs == 'br':
                self.ipa = 'm'
            elif self.bs == 'sl':
                self.ipa = 'mʲ'
        elif self.name == '姆':
            if self.bs == 'br':
                if self.nextphon != None and self.nextphon.name in ('F','特'):
                    self.ipa = 'f'
                elif self.end and self.prephon != None and self.prephon.cv == 'v' and ('ː' not in self.prephon.ipa or self.prephon.ipa in ('aː' , 'æː')):
                    self.ipa = ''
                elif self.prephon != None and self.prephon.name in ('A','EA') and not self.end and self.prephon.accent:
                    self.ipa = '奥u'
                elif self.prephon != None and self.prephon.name in ('O','IO','U','IU','Ú','ÚI','IÚI','IÚ')  and not self.end and self.prephon.accent:
                    self.ipa = '长u'
                else:
                    self.ipa = 'w'
            elif self.bs == 'sl':
                if self.end and self.prephon != None and self.prephon.cv == 'v' and ('ː' not in self.prephon.ipa or self.prephon.ipa in ('aː' , 'æː')):
                    self.ipa = ''
                else:
                    self.ipa = 'wʲ'
        elif self.name == 'N':
            if self.bs == 'br':
                if self.nextphon != None and self.nextphon.name in ('C','G','格'):
                    self.ipa = 'ŋ'
                elif self.nextphon != None and self.nextphon.name in ('赫') and not (self.prephon != None and self.prephon.cv == 'v' and ('ː' not in self.prephon.ipa or self.prephon.ipa in ('aː' , 'æː')) and self.prephon.accent):
                        self.ipa = 'ŋ'
                elif self.prephon != None and self.prephon.cv == 'c' and self.prephon.name not in ('S','瑟') and self.prephon.begin:
                    self.ipa = 'r'
                elif self.prephon != None and self.prephon.name in ('M') and not self.end:
                    self.ipa = 'r'
                else:
                    self.ipa = 'ɴ'                
            elif self.bs == 'sl':
                if self.begin:
                    self.ipa = 'ɴʲ'
                elif self.nextphon != None and self.prephon != None and self.nextphon.name == 'G' and self.nextphon.end and self.prephon.cv == 'v' and not self.prephon.accent:
                    self.ipa = 'ɴʲ'
                elif self.nextphon != None and self.nextphon.name in ('C','G','格'):
                    self.ipa = 'ŋʲ'
                elif self.nextphon != None and self.nextphon.name in ('赫') and not (self.prephon != None and self.prephon.cv == 'v' and ('ː' not in self.prephon.ipa or self.prephon.ipa in ('aː' , 'æː')) and self.prephon.accent):
                        self.ipa = 'ŋʲ'
                elif self.prephon != None and self.prephon.name in ('M') and not self.end:
                    self.ipa = 'rʲ'
                elif self.prephon != None and self.prephon.name in ('姆','博'):
                    self.ipa = 'ɴʲ'
                elif self.nextphon != None and self.nextphon.name == 'T':
                    self.ipa = 'ɴʲ'
                elif self.prephon != None and self.prephon.cv == 'c' and self.prephon.name not in ('S','瑟') and self.prephon.begin:
                    self.ipa = 'rʲ'
                else:
                    self.ipa = 'nʲ'
            if self.nextphon != None and  self.nextphon.name in ('B','博','F','M','赫') and self.prev != None and ('ː' not in self.prev.ipa or self.prev.ipa in ('aː' , 'æː')) and self.prev.accent:
                self.ipa += 'ə'
        elif self.name == '尼':
            if self.bs == 'br':
                self.ipa = 'ɴ'
            elif self.bs == 'sl':
                self.ipa = 'ɴʲ'
            if self.nextphon != None and  self.nextphon.name in ('B','博','F','M','赫') and self.prev != None and ('ː' not in self.prev.ipa or self.prev.ipa in ('aː' , 'æː')) and self.prev.accent:
                self.ipa += 'ə'
        elif self.name == 'P':
            if self.bs == 'br':
                self.ipa = 'p'
            elif self.bs == 'sl':
                self.ipa = 'pʲ'
        elif self.name == '佩':
            if self.bs == 'br':
                self.ipa = 'f'
            elif self.bs == 'sl':
                self.ipa = 'fʲ'
        elif self.name == '热':
            if self.bs == 'br':
                self.ipa = 'r'
            elif self.bs == 'sl':
                self.ipa = 'rʲ'
            if self.nextphon != None and  self.nextphon.name in ('B','博','F','M','G','赫') and self.prev != None and ('ː' not in self.prev.ipa or self.prev.ipa in ('aː' , 'æː')) and self.prev.accent:
                self.ipa += 'ə'
            if self.prephon != None and self.prephon.name in ('N','尼'):
                self.ipa = 't' + self.ipa
        elif self.name == 'R':
            if self.bs == 'br':
                self.ipa = 'r'
            elif self.bs == 'sl':
                if self.begin:
                    self.ipa = 'r'
                elif self.prephon != None and self.prephon.name in ('S'):
                    self.ipa = 'r'
                elif self.nextphon != None and self.nextphon.name in ('T','D','N','L','尼','勒','特'):
                    self.ipa = 'r'
                else:
                    self.ipa = 'rʲ'
            if self.prephon != None and self.prephon.name in ('N','尼'):
                self.ipa = 't' + self.ipa
            if self.nextphon != None and self.nextphon.name in ('B','博','F','M','G','赫') and self.prev != None and ('ː' not in self.prev.ipa or self.prev.ipa in ('aː' , 'æː')) and self.prev.accent:
                self.ipa += 'ə'
        elif self.name == 'S':
            if self.bs == 'br':
                self.ipa = 's'
            elif self.bs == 'sl':
                self.ipa = 'sʲ'
        elif self.name == '瑟':
            if self.bs == 'br':
                self.ipa = 'h'
            elif self.bs == 'sl':
                if self.nextphon != None and self.nextphon.ipa in ('ɑː','oː','uː','u'):
                    self.ipa = 'xʲ'
                else:
                    self.ipa = 'h'
        elif self.name == 'T':
            if self.bs == 'br':
                if self.prephon != None and not self.prephon.accent and self.prephon.ipa == 'ə' and self.end:
                    self.ipa = 'd'
                else:
                    self.ipa = 't'                
            elif self.bs == 'sl':
                self.ipa = 'tʲ'
        elif self.name == '特':
            if self.bs == 'br':
                self.ipa = '和'
            elif self.bs == 'sl':
                if self.begin and self.nextphon != None and self.nextphon.ipa == 'u':
                    self.ipa = 'xʲ'
                elif (self.prephon != None and self.nextphon != None) and self.prephon.name == 'UAI' and self.nextphon.name == 'E' and self.prephon.accent:
                    self.ipa = 'iː'
                else:
                    self.ipa = '和'
        elif self.name == 'V':
            if self.bs == 'br':
                self.ipa = 'w'
            elif self.bs == 'sl':
                self.ipa = 'wʲ'
    def longvowel(self):
        longvdic = {'i':'iː' , 'u':'uː' , 'e':'ai' , 'o':'au' , 'aː' : 'ɑː' , 'æː':'ɑː'}
        if self.ipa in longvdic:
            if self.nextphon != None and self.nextphon.name in ('勒','尼','热','M') and self.sylvcount == 1:
                return longvdic[self.ipa]
            if self.ipa not in ('aː', 'æː'):
                for bisyl in [('L','S'),('B','R'),('B','L')]:
                    if self.nextphon != None and self.nextphon.nextphon != None and (self.nextphon.name,self.nextphon.nextphon.name)==bisyl:
                        return longvdic[self.ipa]
            for bisyl in [('博','N'),('姆','N'),('博','R'),('姆','R'),('姆','L'),('博','尼'),('姆','尼'),('博','热'),('姆','热'),('姆','勒'),('R','L'),('R','N'),('R','D')]:
                if self.nextphon != None and self.nextphon.nextphon != None and (self.nextphon.name,self.nextphon.nextphon.name)==bisyl:
                    return longvdic[self.ipa] 
        return self.ipa
    def sandhi(self):
        if self.begin:
            if self.name == 'G':
                if self.nextphon != None and self.nextphon.name == 'C':
                    self.nextphon.ipa = ''
            elif self.name == 'B':
                if self.nextphon != None and self.nextphon.name == 'P':
                    self.nextphon.ipa = ''
            elif self.name == 'M':
                if self.nextphon != None and self.nextphon.name == 'B':
                    self.nextphon.ipa = ''
            elif self.name == '博':
                if self.nextphon != None and self.nextphon.name == 'F':
                    self.nextphon.ipa = ''
            elif self.name == 'N':
                if self.nextphon != None and self.nextphon.name == 'D':
                    self.nextphon.ipa = ''
                elif self.nextphon != None and self.nextphon.name == 'G':
                    self.nextphon.ipa = ''
            elif self.name == 'D':
                if self.nextphon != None and self.nextphon.name == 'T':
                    self.nextphon.ipa = ''
        if self.ipa == '艾i':
            self.prephon.ipa = 'ai'
            self.ipa = ''
        if self.ipa == '奥u':
            self.prephon.ipa = 'au'
            self.ipa = ''   
        if self.ipa == '长u':
            self.prephon.ipa = 'uː'
            self.ipa = ''
            if self.nextphon != None and self.prephon != None:
                self.nextphon.prephon = self.prephon
                self.prephon.nextphon = self.nextphon
        self.ipa = self.longvowel()
        if self.ipa == '和':
            if self.prephon != None and self.nextphon != None and self.prephon.cv == 'v' and self.nextphon.cv == 'v':
                if self.prephon.ipa[-1]=='ː' or self.nextphon.ipa[-1]=='ː':
                    if self.prephon.ipa[-1]=='ː' and self.nextphon.ipa[-1]!='ː' and self.nextphon.ipa != '':
                        self.ipa = ''
                        self.nextphon.ipa = ''
                    elif self.nextphon.ipa[-1]=='ː' and self.prephon.ipa[-1]!='ː'  and self.prephon.ipa != '':
                        self.ipa = ''
                        self.prephon.ipa = ''
                    else:
                        self.ipa = ''
                        self.prephon.ipa = self.prephon.ipa[:-1]
                else:
                    if self.prephon.accent:
                        self.ipa = ''
                        self.nextphon.ipa = ''
                        if 'ː' in self.prephon.ipa:
                            self.prephon.ipa = self.prephon.ipa
                        else:
                            self.prephon.ipa = self.prephon.ipa + 'ː'
                    else:
                        self.ipa = ''
                        self.prephon.ipa = 'iː'
                        self.nextphon.ipa = ''
                self.nextphon.prephon = self.prephon
                self.prephon.nextphon = self.nextphon
            else:
                if self.end:
                    self.ipa = ''
                elif self.prephon != None and self.prephon.cv=='v':
                    self.ipa=''
                elif self.prephon != None and self.prephon.name in ('R'):
                    self.ipa=''
                elif self.nextphon != None and self.nextphon.name in ('R'):
                    self.ipa=''
                else:
                    self.ipa = 'h'
        if self.ipa == 'oː':
            if self.prephon != None and self.prephon.name in ('N','尼','M','姆'):
                self.ipa = 'uː'
            elif self.nextphon != None and self.nextphon.name in ('N','尼','M','姆'):
                self.ipa = 'uː'
        if self.ipa != '' and self.ipa[-1] == 'ə' and 'ː' not in self.ipa:
            if (self.nextphon != None and any([i in self.nextphon.ipa for i in ('aeiouæɑ')])):
                self.ipa = self.ipa[:-1]
        if self.ipa == 'a':
            if self.nextphon != None and self.nextphon.ipa in ('i','u','iː','uː'):
                self.ipa += self.nextphon.ipa[0]
                self.nextphon.ipa = ''
        if self.ipa == 'ə' and 'ː' not in self.ipa:
            if (self.prephon != None and any([i in self.prephon.ipa for i in ('aeiouæɑ')])):
                self.ipa = ''
        if self.prephon != None and self.prephon.ipa == self.ipa.strip('ː'):
            self.prephon.ipa = self.ipa
            self.ipa = ''
        if self.prephon != None and self.prephon.ipa == self.ipa:
            self.ipa = ''

    def relink(self):
        while self.prephon != None and self.prephon.ipa == '':
            self.prephon = self.prephon.prephon
        if self.prephon == None:
            self.begin = True
        while self.nextphon != None and self.nextphon.ipa == '':
            self.nextphon = self.nextphon.nextphon
        if self.nextphon == None:
            self.end = True
    def cyrilic(self):
        conslist = {'b': 'б', 'd': 'д', 'f': 'ф', 'g': 'г', 'h': 'һ', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'w': 'в', 'x': 'х', 'ŋ': 'ӈ', 'ɣ': 'ғ', 'ɴ': 'ң', 'ʟ': 'ӆ'}
        vowellist = {'e': ('э', 'е'), 'o': ('о', 'ё'), 'eː': ('ээ', 'еэ'), 'oː': ('оо', 'ёо'), 'i': ('ы', 'и'), 'iːə': ('ыә', 'иә'), 'iː': ('ый', 'ий'), 'ə': ('ә', 'јә'), 'ɑː': ('ӓӓ', 'јӓ'), 'u': ('у', 'ю'), 'uːə': ('уә', 'юә'), 'uː': ('уу', 'юу'), 'a': ('а', 'я'), 'aː': ('аа', 'яа'), 'ai': ('ай', 'яй'), 'au': ('аў', 'яў'), 'æː': ('ӕ', 'јӕ')}
        try:
            if self.ipa == '':
                self.cyril = ''
                return
            if self.ipa.strip('ʲ') in vowellist:
                if self.begin:
                    self.cyril = vowellist[self.ipa][0]
                else:
                    if self.prephon != None and self.prephon.ipa[-1]=='ʲ':
                        self.cyril = vowellist[self.ipa][1]
                    else:
                        self.cyril = vowellist[self.ipa][0]
            elif self.ipa.strip('ʲ') in conslist:
                if 'ʲ' not in self.ipa:
                    if self.nextphon != None and 'ʲ' in self.nextphon.ipa:
                        self.cyril = conslist[self.ipa.strip('ʲ')] + 'ъ'
                    else:
                        self.cyril = conslist[self.ipa.strip('ʲ')]
                elif 'ʲ' in self.ipa:
                    if self.nextphon != None and self.nextphon.ipa.strip('ʲ') in conslist and 'ʲ' not in self.nextphon.ipa:
                        self.cyril = conslist[self.ipa.strip('ʲ')] + 'ь'
                    elif self.end:
                        self.cyril = conslist[self.ipa.strip('ʲ')] + 'ь'
                    else:
                        self.cyril = conslist[self.ipa.strip('ʲ')]
                    if self.ipa.strip('ʲ') == 's':
                        self.cyril = self.cyril.replace('с','ш')
            else:
                self.cyril = self.ipa
                for i in vowellist:
                    self.cyril = self.cyril.replace('ʲ'+i,vowellist[i][1])
                    self.cyril = self.cyril.replace(i,vowellist[i][0])
                for i in conslist:
                    self.cyril = self.cyril.replace(i,conslist[i])
                self.cyril = self.cyril.replace('ʲ','')
            if self.begin:
                if self.cyril in ('ы','ыә', 'ый'):
                    self.cyril = self.cyril.replace('ы','и')
        except (KeyboardInterrupt,SystemError) as e:
                raise e
        except Exception as e:
                raise IrishIPAError
