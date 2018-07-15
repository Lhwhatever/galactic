import numpy as np
import re


numbers = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5
}


def T2RGB(T):
    t = T/100
    t = np.piecewise(t, [t < 10, t <= 400], [np.nan, t, np.nan])
    r = np.piecewise(t, [t <= 66],
                     [1, lambda t: 1.29293618606 * np.power(t - 60, -0.1332047592)])
    g = np.piecewise(t, [t <= 66],
                     [lambda t: 0.39008157876 * np.log(t) - 0.63184144378,
                     lambda t: 1.1298908609 * np.power(t - 60, -0.0755148492)])
    b = np.piecewise(t, [t <= 19, t < 66],
                    [0,
                    lambda t: 0.54320678911 * np.log(t - 10) - 1.19625408914,
                    1])
    rgb = np.vstack((r, g, b)).T
    rgb[rgb > 1] = 1
    rgb[rgb < 0] = 0
    return rgb


class Spectral:
    
    star = re.compile(r'\b(?P<mk>[OBAFGKM])(?P<number>[0-9](\.[0-9])?)(?P<evo>I|II|III|IV|V)(?P<other>\w)?\b')
    brown = re.compile(r'\b(?P<mk>[LTY])(?P<number>[0-9](\.[0-9])?)\b')
    degenerate = re.compile(r'\bD(?P<comp>[ABCOZQX])(?P<index>[0-9](\.[0.9])?)\b')
    
    mk_star = 'OBAFGKM'
    mk_dwarf = 'LTY'
    mk_degenerate = 'D'
    
    def __init__(self, identification):
        self.mk = identification[0]
        self.id = identification
        
        regex = None
        
        if self.mk in self.mk_star: # normal star
            regex = self.star
        elif self.mk in self.mk_dwarf: # brown dwarf
            regex = self.brown
        elif self.mk in self.mk_degenerate:
            regex = self.degenerate
            
        self.match = regex.search(self.id)
        self.number = self._number()
        self.temperature = self._temp()
        self.evo = self._roman(self.match.group('evo'))
    
    def _number(self):
        
        if self.mk in self.mk_star:
            return self.mk_star.index(self.mk) * 10 + float(self.match.group('number'))
        elif self.mk == 'Y':
            return 20
        elif self.mk in self.mk_dwarf:
            return self.mk_dwarf.index(self.mk) * 10 + float(self.match.group('number'))
        elif self.mk in self.mk_degenerate:
            return float(self.match.group('index'))
    
    def _temp(self):
        if self.mk in self.mk_star:
            pass
        elif self.mk in self.mk_degenerate:
            return 54000 / self.number
    
    @classmethod
    def _roman(cls, number):
        return numbers[number]