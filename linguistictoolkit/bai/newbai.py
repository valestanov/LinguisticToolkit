import sys, os.path

smdic = {"":"",
"b":"p",
"p":"pʰ",
"f":"f",
"v":"v",
"m":"m",
"d":"t",
"t":"tʰ",
"z":"ts",
"c":"tsʰ",
"s":"s",
"ss":"z",
"n":"n",
"l":"l",
"zh":"tʂ",
"ch":"tʂʰ",
"sh":"ʂ",
"r":"ʐ",
"j":"tɕ",
"q":"tɕʰ",
"x":"ɕ",
"y":"j",
"g":"k",
"k":"kʰ",
"h":"x",
"hh":"ɣ",
"ng":"ŋ",
}
ymdic = {"i":"i-",
"ei":"e-",
"er":"ə-r",
"a":"a-",
"o":"o-",
"u":"u-",
"e":"ɯ-",
"v":"v-",
"ao":"a-u",
"ou":"o-u",
"ie":"ie-",
"ier":"iə-r",
"ia":"ia-",
"iao":"ia-u",
"iei":"ie-",
"io":"io-",
"ie":"iɯ-",
"iou":"io-u",
"ui":"ui-",
"uei":"ue-",
"uer":"uə-r",
"ua":"ua-",
"uo":"uo-"}
sddic = {
    "o":("⁴⁴","̩"),
    "x":("³³",""),
    "l":("⁵⁵",""),
    "t":("³¹",""),
    "f":("³⁵",""),
    "z":("³²",""),
    "p":("⁴²","̩"),
    "d":("²¹","̩")
    }

def baisyl(bai):
    sm = ''
    ym = ''
    sd = ''
    if bai[0] != 'v':
        for i in range(len(bai)):
            if bai[i] in 'aeiouv':
                sm = bai[0:i]
                ymsd = bai[i:]
                break
    elif bai[0] == 'v':
        if len(bai) == 1 or (bai[1] in 'xltfzbpd'):
            sm = ''
            ymsd = bai
        else:
            sm = 'v'
            ymsd = bai[1:]
    for i in range(len(ymsd)):
        if ymsd[i] in 'xltfzbpd':
            ym = ymsd[:i]
            sd = ymsd[i:]
        else:
            ym = ymsd
            sd = 'o'
    smipa = smdic[sm]
    if sm in ['z','c','s','ss'] and ym == 'i':
        ymipa = 'ɿ-'
    elif sm in ['j','q','x','y'] and ym == 'ui':
        ymipa = 'y-'
    else: ymipa = ymdic[ym]        
    sdipa = sddic[sd]
    ipa = smipa + ymipa.replace('-',sdipa[1]) + sdipa[0]
    return ipa

def baitoipa(bai):
    bai = bai.lower()
    word = ''
    ipa = ''
    for i in bai:
        if i in 'abcdefghijklmnopqrstuvwxyz':
            word += i
        else:
            if word == '':
                ipa += i
            else:
                try:
                    ipa += baisyl(word)
                except:
                    ipa += word
                ipa += i
                word = ''
    if word != '':
        try:
            ipa += baisyl(word)
        except:
            ipa += word
        word = ''
    return ipa

def filetoroman():
    folder = sys.path[0]
    inputfile = os.path.join(folder,'Inputfile.txt')
    outputfile = os.path.join(folder,'Outputfile.txt')
    with open(inputfile,'r',encoding='utf-8') as ipfile:
        baitext = ipfile.read()
    ipatext = baitoipa(baitext)
    with open(outputfile,'w',encoding='utf-8') as opfile:
        opfile.write(ipatext)
    return
