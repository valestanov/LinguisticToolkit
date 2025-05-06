import jamotools
import pyperclip

def getinitial(ko):
    if ord(ko)>=int('0xac00',16) and ord(ko)<=int('0xd7af',16):
        initno = int(int((ord(ko)-int('0xac00',16))/28)/21)
        return chr(int('0x1100',16)+initko)
    else:
        return ko

def getinitjamo(ko):
    if ord(ko)>=int('0xac00',16) and ord(ko)<=int('0xd7af',16):
         initko = jamotools.normalize_to_compat_jamo(jamotools.split_syllable_char(ko)[0])
         return initko
    else:
        return ko

def komasker(kotext):
    return ''.join([getinitjamo(i) for i in kotext])
    
