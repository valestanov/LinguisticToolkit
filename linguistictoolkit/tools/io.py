def readlist(langfile):
    senlist = []
    with open(langfile,'r',encoding='utf-8') as f:
        senlist = f.readlines()
    senlist = [sen.strip('\ufeff\n').strip() for sen in senlist]
    return senlist

def writelist(thelist,langfile,form):
    with open(langfile,'w',encoding='utf-8') as f:
        for i in thelist:
            f.writelines(form % tuple(i))

def fileoutput(inputfile,outputfile,func):
    with open(inputfile,'r',encoding='utf-8') as ipfile:
        inputtext = ipfile.read()
    outputtext = func(inputtext)
    with open(outputfile,'w',encoding='utf-8') as opfile:
        opfile.write(outputtext)
    return


