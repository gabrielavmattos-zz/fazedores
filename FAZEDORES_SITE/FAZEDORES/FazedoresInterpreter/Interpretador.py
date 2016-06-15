import string
class Interpretador:
    def __init__(self, algoritmo):
            self.__algoritmo = algoritmo
            
    def getAlgoritmo(self):
        return self.__algoritmo
    
    def setAlgoritmo(self, algoritmo):
        self.__nome = nome    

    algoritmo = property(fget=getAlgoritmo, fset=setAlgoritmo)
    
    def interpreta():
        return(getAlgoritmo().upper())