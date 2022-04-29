import os

from db.__config import BASE

def getBase()->str:
    return BASE

def setBase(path:str)->None:
    os.rename(path,BASE)
