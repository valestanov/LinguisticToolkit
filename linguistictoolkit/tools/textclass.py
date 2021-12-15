
class Language():
    def __init__(self,name,iso=None):
        self.name = name
        self.ortho = []
        self.converter = {}
        if iso is not None:
            self.setISO(iso)         
    def setISO(self,iso):
        self.ISO=iso
    def getISO(self):
        return ISO
    def getOrthoList(self):
        return self.ortho
    def getConverter(self):
        return self.converter

class Orthography():
    def __init__(self,name,lang):
        self.name=name
        self.lang=lang
        self.lang.ortho.append(self)
    def setCharattr(self,charattrfunc):
        self.charattr = charattrfunc
    def getCharattr(self,char):
        return self.charattr(char)
    def setCombinable(self,combfunc):
        self.combfunc = combfunc
    def getCombinable(self,word,char):
        return self.combfunc(word,char)
    def setConvert(self,newortho,convfunc):
        self.lang.converter[(self,newortho)]=convfunc
    def getConvert(self,word,newortho):
        return self.lang.converter[(self,newortho)](word)

class TextFragment():
    def __init__(self,text,ortho):
        self.text=text
        self.ortho=ortho
        self.lang=self.ortho.lang
    def getText(self):
        return self.text
    def getLang(self):
        return self.lang
    def getOrtho(self):
        return self.ortho
    def getLen(self):
        return len(self.text)
    def longer(self,word):
        self.text += word
    def getWordstrain(self):
        #Return a iterable generator of word list. Each element is a member of Class Word with attribution information.
        #返回词表的可迭代生成器。每个元素都是携带了属性的Word类成员。
        #Parameter combkey should be a function to judge, whether a new alphabet can be merged with the present word.
        #combkey参数：判断一个词后面可不可以附加某个字母。
        i = 0
        length = self.getLen()
        word = None
        for i in range(length+1):
            try:
                char = self.text[i]
                charattr = self.ortho.getCharattr(char)
                if word is not None:
                    if self.ortho.getCombinable(word,char):
                        word.longer(char)
                    else:
                        yield word
                        word = Word(char,self.ortho,charattr)
                else:
                    word = Word(char,self.ortho,charattr)
            except IndexError:
                if word is not None:
                    yield word
                return
    def Convert(self,newortho):
        wordstrain = self.getWordstrain()
        newtext = TextFragment('',newortho)
        for word in wordstrain:
            try:
                nextfrag = self.ortho.getConvert(word,newortho)
            except:
                nextfrag = word.getText()
            newtext.longer(nextfrag)
        return newtext
    
class Word(TextFragment):
    def __init__(self,text,ortho,wordattr):
        self.text=text
        self.ortho=ortho
        self.lang=self.ortho.lang
        self.wordattr=wordattr
    def getWordattr(self):
        return self.wordattr
