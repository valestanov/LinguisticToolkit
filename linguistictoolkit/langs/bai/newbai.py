class NoPhoneme(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

smdic = {'b': 'p', 'p': 'ph', 'm': 'm', 'f': 'f', 'v': 'v', 'd': 't', 't': 'th', 'n': 'n', 'l': 'l', 'g': 'k', 'k': 'kh', 'ng': 'ŋ', 'h': 'x', 'hh': 'ɣ', 'j': 'tɕ', 'q': 'tɕh', 'x': 'ɕ', 'y': 'j', 'z': 'ts', 'c': 'tsh', 's': 's', 'ss': 'z', 'zh': 'tʂ', 'ch': 'tʂh', 'sh': 'ʂ', 'r': 'ʐ', '': ''}
ymdic = {'i': 'i-', 'ei': 'e-', 'ai': 'ɛ-', 'a': 'ɑ-', 'o': 'o-', 'u': 'u-', 'e': 'ɯ-', 'v': 'v-', 'iai': 'iɛ-', 'ia': 'iɑ-', 'iao': 'ia-u', 'io': 'io-', 'iou': 'io-u', 'ie': 'iɯ-', 'ui': 'ui-', 'uai': 'uɛ-', 'ua': 'uɑ-', 'uo': 'uo-', 'ao': 'a-u', 'ou': 'o-u', 'in': 'i-n', 'ein': 'e-n', 'ain': 'ɛ-n', 'an': 'ɑ-n', 'on': 'o-n', 'en': 'ɯ-n', 'vn': 'v-n', 'iain': 'iɛ-n', 'ian': 'iɑ-n', 'ion': 'io-n', 'ien': 'iɯ-n', 'uin': 'ui-n', 'uain': 'uɛ-n', 'uan': 'uɑ-n'}
sddic = {'l': '⁵⁵', 'b': '_⁵⁵', 'f': '³⁵', 'x': '³³', '': '_⁴⁴', 'z': '³²', 't': '³¹', 'p': '_⁴²', 'd': '_²¹'}
def baisylcheck(sm,ym,sd):
    smipa = smdic[sm]
    ymipa = ymdic[ym]
    sdipa = sddic[sd]

    if len(ym)>=2 and ym[:2] == 'ui':
        if sm in 'jqxy':
            ymipa = ymipa.replace('ui','y')

    if ym == 'i':
        if sm in ('z','c','s','ss'):
            ymipa = 'ɿ-'
            
    if sm == '':
        if ym[0] in ('i','u'):
            if len(ym) == 1:
                ym = ym.replace('i','yi').replace('u','wu')
            else:
                ym = ym[0].replace('i','y').replace('u','w') + ym[1:]

    syl = sm+ym+sd
    if '_' in sdipa:
        ipa = smipa+ymipa.replace('-','̠')+sdipa.replace('_','')
    else:
        ipa = smipa+ymipa.replace('-','')+sdipa.replace('_','')
    ipa = ipa.replace('ni','ȵi')
    return (syl, ipa)

baisyldic = {}
for sm in smdic:
    for ym in ymdic:
        for sd in sddic:
            syl,ipa = baisylcheck(sm,ym,sd)
            baisyldic[syl] = ipa

if __name__== "__main__":
    print(f'生成音节 {len(baisyldic)} 个，初始化完成。')

def baisyltoipa(syl):
    syl = syl.strip()
    try:
        if syl in baisyldic:
            return baisyldic[syl]
        else:
            raise NoPhoneme(f"音节有误：{syl}")
    except NoPhoneme as e:
        if syl != '': print(e)
        return syl

def baitoipa(text):
    baiabc = 'abcdefghijklmnopqrstuvwxyz'
    word = ''
    ipatext = ''
    text = text.lower()
    text += ' '
    for i in text:
        if i in baiabc:
            word += i
        else:
            ipatext += baisyltoipa(word)
            ipatext += i
            word = ''
    ipatext = ipatext[:-1]
    return ipatext
    
