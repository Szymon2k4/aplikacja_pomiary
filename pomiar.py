class Pomiar():
    def __init__(self, nazwa:str, typ_bez: str, typ_bez_liczba: str, ipz_zmierzone:str):
        self.nazwa = nazwa
        self.typ_bez = typ_bez
        self.typ_bez_liczba = typ_bez_liczba
        self.ipz_zmierzone = ipz_zmierzone
        self.wartosci = {'A': 3, 'B': 5, 'C': 10, 'D': 20}


    def prad_zwarciowy_zabezpieczenia(self):
        return self.wartosci[self.typ_bez] * float(self.typ_bez_liczba)
    
    def ipz_zabezpieczenia(self):
        return 230/self.prad_zwarciowy_zabezpieczenia()
    
    def obliczony_prad_zwarciowy(self):
        return 230/float(self.ipz_zmierzone)
    
    def ocena(self):
        if self.obliczony_prad_zwarciowy() > self.prad_zwarciowy_zabezpieczenia():
            return 'TAK'
        else:
            return 'NIE'