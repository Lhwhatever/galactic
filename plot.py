import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


DEG2RAD = np.pi / 180
H2RAD = np.pi / 12
HEXED = np.linspace(-np.pi, np.pi, 6, endpoint=True)

COLORS = pd.read_csv("Colors.csv")

SAGITTARIUS_ASTAR = (17.7611224722, -29.0078105556)

def color_lookup(h, num, y): #E.g. for G2V, h = 'G', num = 2.0, y = 'V'
    if h[0] == 'D':
        i = COLORS['Class'].tolist().index('{0}{1}'.format(h, int(num)))
        return COLORS.iloc[i, 6]
    if h == 'L':
        return '#eb4b25'
    elif num % 1:
        try:
            i = COLORS['Class'].tolist().index('{0}{1}({2})'.format(h, num, y))
            return COLORS.iloc[i, 6]
        except ValueError:
            part = num % 1
            i_0 = COLORS['Class'].tolist().index('{0}{1}({2})'.format(h, int(num - part), y))
            i_1 = COLORS['Class'].tolist().index('{0}{1}({2})'.format(h, int(num - part) + 1, y))
        
            r_0, g_0, b_0 = COLORS.iloc[i_0, 3:6]
            r_1, g_1, b_1 = COLORS.iloc[i_1, 3:6]
        
            return '#{0:02x}{1:02x}{2:02x}'.format(int(r_0 + (r_1 - r_0) * part),
                                                   int(g_0 + (g_1 - g_0) * part),
                                                   int(b_0 + (b_1 - b_0) * part))
    else:
        i = COLORS['Class'].tolist().index('{0}{1}({2})'.format(h, int(num), y))
        return COLORS.iloc[i, 6]


class Main:
    
    @staticmethod
    def sph2xyz(r, ra, dec):
        return r * np.cos(ra) * np.cos(dec), r * np.sin(ra) * np.cos(dec), -r * np.sin(dec)
    
    @staticmethod
    def load_stars():
        return pd.read_csv("Stars.csv").sort_values(by='ABS_MAGN').drop_duplicates('SYSTEM').sort_values(by='DIST')
    
    def __init__(self):
        self.fig = plt.figure(figsize=(29.7,20))
        self.ax = self.fig.gca(projection='3d')
        
        self.get_stars()
        self.x, self.y, self.z = self.sph2xyz(self.r, self.ra, self.pol)
        
        self.azimuthal = np.linspace(-np.pi, np.pi, 360)
        
    def get_stars(self):
        self.stars = self.load_stars()
        #print(self.stars)
        
        self.r = self.stars['DIST']
        
        ra = self.stars['RA'].str.split(':', expand=True).apply(pd.to_numeric)
        self.ra = (ra.loc[:,0] + ra.loc[:,1]/60 + ra.loc[:,2]/3600) * H2RAD
        
        dec_m = self.stars['DEC'].str.startswith('-') * 2 - 1
        dec = self.stars['DEC'].str.replace('-', '').str.split(':', expand=True).apply(pd.to_numeric)
        self.pol = dec_m * (dec.loc[:,0] + dec.loc[:,1]/60 + dec.loc[:,2]/3600) * DEG2RAD
        #print(self.pol)
    
    def draw_directions(self, xy, R_max):
        self.ax.quiver(0, 0, xy, 0, 0, 1, color='0.5', pivot='tail')
        self.ax.text(0, 0, xy * 0.97, 'North', color='0.4')
        
        self.ax.quiver(R_max, 0, 0, 1, 0, 0, color='0.5', pivot='tail')
        self.ax.text(R_max * 0.97, 0, 0.05, 'Vernal\nEquinox', color='0.4')
        
        X, Y = R_max * np.cos(SAGITTARIUS_ASTAR[0] * H2RAD), R_max * np.sin(SAGITTARIUS_ASTAR[0] * H2RAD)
        x, y, z = self.sph2xyz(R_max, SAGITTARIUS_ASTAR[0] * H2RAD, SAGITTARIUS_ASTAR[1] * DEG2RAD)
        #print(X)
        #print(Y)
        self.ax.quiver(X, Y, 0, x, y, -z, color='0.5', pivot='tail')
        self.ax.text(X * 0.97, Y * 0.97, 0, 'Sagittarius A*', color='0.4')
        
    def set_limits(self, R_max):
        xy = 1.1 * max(-min(self.x), max(self.x), -min(self.y), max(self.y))
        self.ax.set_xlim3d(-xy, xy)
        self.ax.set_ylim3d(-xy, xy)
        self.ax.set_zlim3d(-xy, xy)
        
        self.draw_directions(xy, R_max)
        
        
    def load_axis(self):
        self.ax.set_axis_off()
        self.ax.set_axis_bgcolor('black')
        R_max = int(np.ceil(max(self.r) / 2)) * 2
        self.set_limits(R_max)
        
        for r in range(1, R_max//2+1):
            R = r * 2
            self.ax.plot(R * np.cos(self.azimuthal), R * np.sin(self.azimuthal), 0, color='0.15')
            #if not r % 2: self.ax.text(0, R, 0, str(r*2) + 'ly', color='0.6')
        
        for h in range(0, 24, 2):
            self.ax.plot([0, R_max * np.cos(h * H2RAD)], [0, R_max * np.sin(h * H2RAD)], [0, 0], color='0.15')
            #if not h % 4: self.ax.text(R_max * 1.05 * np.cos(h * H2RAD), R_max * 1.05 * np.sin(h * H2RAD),
            #                           0, str(h) + 'h', color='0.6')
    
    def draw_stars(self):
        for s, x, y, z in zip(self.stars.iterrows(), self.x, self.y, self.z):
            S = s[1]
            color = color_lookup(S['CLASS_H'], S['CLASS_NUM'], S['CLASS_Y'])
            #print("Star {} has color {}".format(S['SYSTEM'], color))
            self.ax.scatter(x, y, z, s=40, c=color)
            
            #print(hexagon)
            print("{}: {}, {}, {}".format(S['SYSTEM'], x, y, z))
            
            shade = str(0.4 * np.exp(0.06 * -S['ABS_MAGN']))
            if x and y and z: self.ax.plot(x + 0.1 * np.cos(HEXED), y + 0.1 * np.sin(HEXED), 0, color=shade)
            self.ax.text(x, y, z + max(self.z) * (0.02 if z >= 0 else -0.04), S['SYSTEM'], color='0.4')
            #self.ax.plot([0, x], [0, y], [0, 0], color=shade)
            self.ax.plot([x, x], [y, y], [0, z], color=shade)
    
    def main(self):
        self.load_axis()
        self.draw_stars()

if __name__ == "__main__":
    Main().main()
    plt.show()
