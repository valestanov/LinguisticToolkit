ymabclist = {"à":[2,"a"], "ằ":[2,"ă"], "ầ":[2,"â"], "è":[2,"e"], "ề":[2,"ê"], "ì":[2,"i"], "ò":[2,"o"], "ồ":[2,"ô"], "ờ":[2,"ơ"], "ù":[2,"u"], "ừ":[2,"ư"], "ỳ":[2,"y"], "ả":[3,"a"], "ẳ":[3,"ă"], "ẩ":[3,"â"], "ẻ":[3,"e"], "ể":[3,"ê"], "ỉ":[3,"i"], "ỏ":[3,"o"], "ổ":[3,"ô"], "ở":[3,"ơ"], "ủ":[3,"u"], "ử":[3,"ư"], "ỷ":[3,"y"], "ã":[4,"a"], "ẵ":[4,"ă"], "ẫ":[4,"â"], "ẽ":[4,"e"], "ễ":[4,"ê"], "ĩ":[4,"i"], "õ":[4,"o"], "ỗ":[4,"ô"], "ỡ":[4,"ơ"], "ũ":[4,"u"], "ữ":[4,"ư"], "ỹ":[4,"y"], "á":[5,"a"], "ắ":[5,"ă"], "ấ":[5,"â"], "é":[5,"e"], "ế":[5,"ê"], "í":[5,"i"], "ó":[5,"o"], "ố":[5,"ô"], "ớ":[5,"ơ"], "ú":[5,"u"], "ứ":[5,"ư"], "ý":[5,"y"], "ạ":[6,"a"], "ặ":[6,"ă"], "ậ":[6,"â"], "ẹ":[6,"e"], "ệ":[6,"ê"], "ị":[6,"i"], "ọ":[6,"o"], "ộ":[6,"ô"], "ợ":[6,"ơ"], "ụ":[6,"u"], "ự":[6,"ư"], "ỵ":[6,"y"]}
special = {'â': 'aa', 'ê': 'ee', 'ô': 'oo', 'ă': 'aw', 'ơ': 'ow', 'ư': 'uw', 'đ': 'dd'}
sdlist = {1:'z',2:'f',3:'r',4:'x',5:'s',6:'j'}
qncabc = 'aáàâăãấầắằẫẵảẩẳạậặbcdđeéèêẽếềễẻểẹệghiíìĩỉịklmnoóòôõốồỗỏơổọớờỡộởợpqrstuúùũủưụứừữửựvxyýỳỹỷỵabcdefghijklmnopqrstuvwxyz'

def isqnc(text):
    for i in text:
        if i not in qncabc:
            return False
    return True

def qncsyltotelex(qncsyl):
    try:
        if qncsyl == '' or not isqnc(qncsyl):
            raise NoPhoneme(qncsyl)
        syl = qncsyl
        sd = ''
        #声调识别
        sd = 1 #未标调的默认即平声
        for ymabc in ymabclist:
            if ymabc in qncsyl:
                ymbox = ymabclist[ymabc]
                syl = qncsyl.replace(ymabc,ymbox[1])
                sd = ymbox[0]
                break
        sd = int(sd) #转换成数字型，以免数字与文本类型不匹配无法识别
        for i in special:
            syl = syl.replace(i,special[i])
        syl = syl.strip() + sdlist[sd]
        return syl
    except NoPhoneme as e:
        return qncsyl

class NoPhoneme(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

def qnctotelex(text):
    word = ''
    telextext = ''
    text = text.lower()
    text += ' '
    for i in text:
        if i in qncabc:
            word += i
        else:
            telextext += qncsyltotelex(word)
            telextext += i
            word = ''
    telextext = telextext[:-1]
    return telextext



            
        
            
        

