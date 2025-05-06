
print('本程序只处理双音节，且不处理轻声b！轻声的变调规则：前字不变，后字只改变声调。')

class pinghua_sm:
    def __init__(self,phzsm,ipasm,pysm,vhbian,vhbianpy,nbian,nbianpy):
        self.phzsm = phzsm
        self.ipasm = ipasm
        self.pysm = pysm
        #遇见vh类或者n类时候的变音
        self.vhbian = vhbian
        self.vhbianpy = vhbianpy
        self.nbian = nbian
        self.nbianpy = nbianpy

pinghua_smlist = [['b', 'p', 'b', 'β', 'w', 'm', 'm'],
                  ['p', 'pʰ', 'p', 'β', 'w', 'm', 'm'],
                  ['m', 'm', 'm', 'm', 'm', 'm', 'm'],
                  ['d', 't', 'd', 'l', 'l', 'n', 'n'],
                  ['t', 'tʰ', 't', 'l', 'l', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['l', 'l', 'l', 'l', 'l', 'n', 'n'],
                  ['s', 's', 's', 'l', 'l', 'n', 'n'],
                  ['c', 'ts', 'z', 'ʒ', 'j', 'ʒ', 'j'],
                  ['ch', 'tsʰ', 'c', 'ʒ', 'j', 'ʒ', 'j'],
                  ['g', 'k', 'g', '', '', 'ŋ', 'ng'],
                  ['k', 'kʰ', 'k', '', '', 'ŋ', 'ng'],
                  ['ng', 'ŋ', 'ng', 'ŋ', 'ng', 'ŋ', 'ng'],
                  ['h', 'h', 'h', '', '', 'ŋ', 'ng'],
                  ['', '', '', '', '', 'ŋ', 'ng']]
pinghua_smdict = {}
for sm in pinghua_smlist:
    pinghua_smdict[sm[0]] = pinghua_sm(sm[0],sm[1],sm[2],sm[3],sm[4],sm[5],sm[6])

class pinghua_ym:
    def __init__(self,phztg, phzls, ipatg, ipals, pytg, pyls, lb):
        #松紧韵平话字loose-tight
        self.phzls = phzls
        self.phztg = phztg
        #松紧韵IPA
        self.ipals = ipals
        self.ipatg = ipatg
        #松紧韵拼音
        self.pyls = pyls
        self.pytg = pytg
        #韵母标签（vh类？n类？k类）
        self.lb = lb

pinghua_ymlist = [['a', 'a', 'a', 'ɑ', 'a', 'a', 'v'], ['ia', 'ia', 'ia', 'iɑ', 'ia', 'ia', 'v'], ['ua', 'ua', 'ua', 'uɑ', 'ua', 'ua', 'v'], ['ae', 'ae', 'ɛ', 'ɑ', 'e', 'a', 'v'], ['ie', 'ie', 'ie', 'iɛ', 'ie', 'ie', 'v'], ['oe', 'oe', 'o', 'ɔ', 'o', 'o', 'v'], ['io', 'io', 'yo', 'yɔ', 'yuo', 'yuo', 'v'], ['uo', 'uo', 'uo', 'uɔ', 'uo', 'uo', 'v'], ['eo', 'aeo', 'œ', 'ɔ', 'eo', 'o', 'v'], ['au', 'au', 'au', 'ɑu', 'au', 'au', 'v'], ['eu', 'aiu', 'ɛu', 'ɑu', 'eu', 'au', 'v'], ['ieu', 'ieu', 'ieu', 'iɛu', 'ieu', 'ieu', 'v'], ['iu', 'eu', 'ieu', 'iɛu', 'ieu', 'ieu', 'v'], ['oi', 'oei', 'øy', 'ɔy', 'eoyu', 'oyu', 'v'], ['ai', 'ai', 'ai', 'ɑi', 'ai', 'ai', 'v'], ['uai', 'uai', 'uai', 'uɑi', 'uai', 'uai', 'v'], ['uoi', 'uoi', 'uoi', 'uɔi', 'uoi', 'uoi', 'v'], ['ui', 'oi', 'uoi', 'uɔi', 'uoi', 'uoi', 'v'], ['i', 'e', 'i', 'ɛi', 'i', 'ei', 'v'], ['u', 'o', 'u', 'ou', 'u', 'ou', 'v'], ['yu', 'eoyu', 'y', 'øy', 'yu', 'eoyu', 'v'], ['ang', 'ang', 'aŋ', 'ɑŋ', 'ang', 'ang', 'n'], ['iang', 'iang', 'iaŋ', 'iɑŋ', 'iang', 'iang', 'n'], ['uang', 'uang', 'uaŋ', 'uɑŋ', 'uang', 'uang', 'n'], ['ieng', 'ieng', 'ieŋ', 'iɛŋ', 'ieng', 'ieng', 'n'], ['iong', 'iong', 'yoŋ', 'yɔŋ', 'yuong', 'yuong', 'n'], ['uong', 'uong', 'uoŋ', 'uɔŋ', 'uong', 'uong', 'n'], ['ing', 'eng', 'iŋ', 'ɛiŋ', 'ing', 'eing', 'n'], ['ung', 'ong', 'uŋ', 'ouŋ', 'ung', 'oung', 'n'], ['yung', 'eoyung', 'yŋ', 'øyŋ', 'yung', 'eoyung', 'n'], ['eng', 'aing', 'ɛiŋ', 'aiŋ', 'eing', 'aing', 'n'], ['ong', 'aung', 'ouŋ', 'ɔuŋ', 'oung', 'oung', 'n'], ['eong', 'aeong', 'øyŋ', 'ɔyŋ', 'eoyung', 'oyung', 'n'], ['ah', 'ah', 'aʔ', 'ɑʔ', 'ak', 'ak', 'h'], ['iah', 'iah', 'iaʔ', 'iɑʔ', 'iak', 'iak', 'h'], ['uah', 'uah', 'uaʔ', 'uɑʔ', 'uak', 'uak', 'h'], ['aeh', 'aeh', 'eʔ', 'ɛʔ', 'ek', 'ek', 'h'], ['ieh', 'ieh', 'ieʔ', 'iɛʔ', 'iek', 'iek', 'h'], ['oeh', 'oeh', 'oʔ', 'ɔʔ', 'ok', 'ok', 'h'], ['ioh', 'ioh', 'yoʔ', 'yɔʔ', 'yuok', 'yuok', 'h'], ['uoh', 'uoh', 'uoʔ', 'uɔʔ', 'uok', 'uok', 'h'], ['eoh', 'eoh', 'øʔ', 'œʔ', 'eok', 'eok', 'h'], ['ak', 'ak', 'aʔ', 'ɑʔ', 'ak', 'ak', 'k'], ['iak', 'iak', 'iaʔ', 'iɑʔ', 'iak', 'iak', 'k'], ['uak', 'uak', 'uaʔ', 'uɑʔ', 'uak', 'uak', 'k'], ['aek', 'aek', 'eʔ', 'ɛʔ', 'ek', 'ek', 'k'], ['iek', 'iek', 'ieʔ', 'iɛʔ', 'iek', 'iek', 'k'], ['oek', 'oek', 'oʔ', 'ɔʔ', 'ok', 'ok', 'k'], ['iok', 'iok', 'yoʔ', 'yɔʔ', 'yuok', 'yuok', 'k'], ['uok', 'uok', 'uoʔ', 'uɔʔ', 'uok', 'uok', 'k'], ['eok', 'eok', 'øʔ', 'œʔ', 'eok', 'eok', 'k'], ['ik', 'ek', 'iʔ', 'ɛiʔ', 'ik', 'eik', 'k'], ['uk', 'ok', 'uʔ', 'ouʔ', 'uk', 'ouk', 'k'], ['yuk', 'eoyuk', 'yʔ', 'øyʔ', 'yuk', 'eoyuk', 'k'], ['ek', 'aik', 'ɛiʔ', 'aiʔ', 'eik', 'aik', 'k'], ['ok', 'auk', 'ouʔ', 'ɔuʔ', 'ouk', 'ouk', 'k'], ['eok', 'aeok', 'øyʔ', 'ɔyʔ', 'eoyuk', 'oyuk', 'k']]
pinghua_ymdict = {}
for ym in pinghua_ymlist:
    pinghua_ymdict[ym[0]] = pinghua_ym(ym[0],ym[1],ym[2],ym[3],ym[4],ym[5],ym[6])

class pinghua_sd:
    def __init__(self,phz,py,wudu,no,lb):
        self.phz = phz
        self.py = py
        self.wudu = wudu
        self.no = no
        self.lb = lb

pinghua_sdlist = [['l', 'l', '44', '1', 't'], ['z', 'z', '52', '2', 't'], ['j', 'j', '33', '3', 't'], ['q', 'hs', '212', '5', 'l'], ['x', 'x', '242', '6', 'l'], ['s', 'ss', '23', '7', 'l'], ['c', 'c', '4', '8', 't'], ['h', 'h', '21', '21', 't'], ['v', 's', '24', '24', 't']]
pinghua_sddict = {}
for sd in pinghua_sdlist:
    pinghua_sddict[sd[0]] = pinghua_sd(sd[0],sd[1],sd[2],sd[3],sd[4])

sd_sandhi = [['l', 'l', 'l', ''], ['l', 'z', 'l', ''], ['l', 'j', 'z', ''], ['l', 'q', 'z', ''], ['l', 'x', 'z', ''], ['l', 's', 'z', ''], ['l', 'c', 'l', ''], ['z', 'l', 'l', ''], ['z', 'z', 'j', ''], ['z', 'j', 'j', ''], ['z', 'q', 'h', ''], ['z', 'x', 'h', ''], ['z', 's', 'h', ''], ['z', 'c', 'j', ''], ['j', 'l', 'h', ''], ['j', 'z', 'h', ''], ['j', 'j', 'v', ''], ['j', 'q', 'l', ''], ['j', 'x', 'l', ''], ['j', 's', 'l', ''], ['j', 'c', 'h', ''], ['q', 'l', 'l', ''], ['q', 'z', 'l', ''], ['q', 'j', 'z', ''], ['q', 'q', 'z', ''], ['q', 'x', 'z', ''], ['q', 's', 'z', ''], ['q', 'c', 'l', ''], ['x', 'l', 'l', ''], ['x', 'z', 'l', ''], ['x', 'j', 'z', ''], ['x', 'q', 'z', ''], ['x', 'x', 'z', ''], ['x', 's', 'z', ''], ['x', 'c', 'l', ''], ['s', 'l', 'l', 'h'], ['s', 'z', 'l', 'h'], ['s', 'j', 'z', 'v'], ['s', 'q', 'z', 'l'], ['s', 'x', 'z', 'l'], ['s', 's', 'z', 'l'], ['s', 'c', 'l', 'h'], ['c', 'l', 'l', ''], ['c', 'z', 'j', ''], ['c', 'j', 'j', ''], ['c', 'q', 'h', ''], ['c', 'x', 'h', ''], ['c', 's', 'h', ''], ['c', 'c', 'j', '']]
sd_sandhi_dict = {}
for sds in sd_sandhi:
    if sds[3].strip() == '':
        sd_sandhi_dict[(pinghua_sddict[sds[0]],pinghua_sddict[sds[1]])] = pinghua_sddict[sds[2]]
    else:
        sd_sandhi_dict[(pinghua_sddict[sds[0]],pinghua_sddict[sds[1]])] = (pinghua_sddict[sds[2]], pinghua_sddict[sds[3]])

class pinghua_syl:
    def __init__(self,sm,ym,sd):
        self.sm = sm
        self.ym = ym
        self.sd = sd
    def get_py(self,prev_syl=None,next_syl=None):
        if prev_syl == None:
            pysm = self.sm.pysm
        else:
            if prev_syl.ym.lb in ['v','h']:
                pysm = self.sm.vhbianpy
            elif prev_syl.ym.lb in ['n']:
                pysm = self.sm.nbianpy
            else:
                pysm = self.sm.pysm
        if next_syl == None:
            pysd = self.sd.py
            if self.sd.lb == 't':
                pyym = self.ym.pytg
            elif self.sd.lb == 'l':
                pyym = self.ym.pyls
        else:
            pyym = self.ym.pytg
            if self.sd.phz == 's':
                if self.ym.lb in ['k']:
                    pysd = sd_sandhi_dict[(self.sd,next_syl.sd)][1].py
                else:
                    pysd = sd_sandhi_dict[(self.sd,next_syl.sd)][0].py
            else:
                pysd = sd_sandhi_dict[(self.sd,next_syl.sd)].py
        pysd = pysd.replace('v','s')
        return pysm + pyym + pysd
    def get_ipa(self,prev_syl=None,next_syl=None):
        if prev_syl == None:
            ipasm = self.sm.ipasm
        else:
            if prev_syl.ym.lb in ['v','h']:
                ipasm = self.sm.vhbian
            elif prev_syl.ym.lb in ['n']:
                ipasm = self.sm.nbian
            else:
                ipasm = self.sm.ipasm
        if next_syl == None:
            ipasd = self.sd.wudu
            if self.sd.lb == 't':
                ipaym = self.ym.ipatg
            elif self.sd.lb == 'l':
                ipaym = self.ym.ipals
        else:
            ipaym = self.ym.ipatg
            if self.sd.phz == 's':
                if self.ym.lb in ['k']:
                    ipasd = sd_sandhi_dict[(self.sd,next_syl.sd)][1].wudu
                else:
                    ipasd = sd_sandhi_dict[(self.sd,next_syl.sd)][0].wudu
            else:
                ipasd = sd_sandhi_dict[(self.sd,next_syl.sd)].wudu
        return ipasm + ipaym + ipasd
        
pinghua_syldict = {}

for smphz in pinghua_smdict:
    for ymphz in pinghua_ymdict:
        sm = pinghua_smdict[smphz]
        ym = pinghua_ymdict[ymphz]
        if ym.lb not in ['h','k']:
            #舒声调
            for sdphz in 'lzjqx':
                sd = pinghua_sddict[sdphz]
                if sd.lb == 't':
                    phz = sm.phzsm + ym.phztg + sd.phz
                elif sd.lb == 'l':
                    phz = sm.phzsm + ym.phzls + sd.phz
                pinghua_syldict[phz] = pinghua_syl(sm,ym,sd)
        else:
            #入声调
            for sdphz in 'sc':
                sd = pinghua_sddict[sdphz]
                if sd.lb == 't':
                    phz = sm.phzsm + ym.phztg + sd.phz
                elif sd.lb == 'l':
                    phz = sm.phzsm + ym.phzls + sd.phz
                pinghua_syldict[phz] = pinghua_syl(sm,ym,sd)

pinghua_ymdict['ng'] = pinghua_ym('ng','ng','ŋ', 'ŋ', 'ng', 'ng', 'n')
pinghua_syldict['ngx'] = pinghua_syl(pinghua_smdict[''],pinghua_ymdict['ng'],pinghua_sddict['x'])

def pinghua_to_pinyin(pinghua):
    pinghuas = pinghua.lower().strip().split(' ')
    syls = [pinghua_syldict[syl] for syl in pinghuas]
    pys = []
    for n,syl in enumerate(syls):
        try:
            if n == 0:
                raise IndexError
            else:
                prevsyl = syls[n-1]
        except IndexError:
            prevsyl = None
        try:
            nextsyl = syls[n+1]
        except IndexError:
            nextsyl = None
        pys.append(syl.get_py(prev_syl=prevsyl,next_syl=nextsyl))
    return ' '.join(pys)

def pinghua_to_ipa(pinghua):
    pinghuas = pinghua.lower().strip().split(' ')
    syls = [pinghua_syldict[syl] for syl in pinghuas]
    ipas = []
    for n,syl in enumerate(syls):
        try:
            if n == 0:
                raise IndexError
            else:
                prevsyl = syls[n-1]
        except IndexError:
            prevsyl = None
        try:
            nextsyl = syls[n+1]
        except IndexError:
            nextsyl = None
        ipas.append(syl.get_ipa(prev_syl=prevsyl,next_syl=nextsyl))
    return ' '.join(ipas)
