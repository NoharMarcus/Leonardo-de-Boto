#-------------------------Calc class------------------------------#
"""
Class containing our math functions:
input : (x - x_cordinate - double
         y - y_cordinate - double
         d - length of diamond edge - double
         debug - debug mode - boolean           )

CalculateAlphaAndBeta(self) -> calculates the 2 angles
                                alpha and beta (alpha < beta)
                                between the positive x-axis
                                and the diamond edges.
                                Results are in RADIAN
"""
#------------------ Imports ---------------------
import numpy as np
from math import isclose
#------------------------------------------------
class Calc:
    def __init__(self,x,y,d,debug = True): # IMPORTANT : TAKES X, Y
        #----------------------Init param-----------------------
        self.x = x
        self.y = y
        self.d = d
        self.debug = debug
        #----------------------Init variables-------------------
        self.alpha = 0
        self.beta = 0
        if debug:
            self.gamma = 0
            self.delta = 0
            self.epsilon = 0

    # ----------------------------------------------------------
    def CalculateAlphaAndBeta(self):
        RSqr = self.x**2 + self.y**2
        dSqr = self.d**2
        cos_gamma = -(RSqr - 2*dSqr) / (2*dSqr)
        gamma = np.arccos(cos_gamma)
        delta = np.pi - gamma
        epsilon = np.arctan2(self.y, self.x)
        self.alpha = epsilon - delta / 2
        self.beta = epsilon + delta / 2
        #converting to degrees
        self.alpha = (180 / np.pi) *  self.alpha
        self.beta = (180 / np.pi) *  self.beta
        if self.debug:
            self.gamma = gamma
            self.delta = delta
            self.epsilon = epsilon

# ----------------------------------------------------------
# helper function :
@staticmethod
def Rad2Degree(RadAngle):
    return (180 / np.pi) * RadAngle



# --------------------- Testing ----------------------------
if __name__ == "__main__":
    calculator = Calc(100,-65,120)
    calculator.CalculateAlphaAndBeta()
    print("alpha is : " , Rad2Degree(calculator.alpha), " degrees")
    print("beta is : " , Rad2Degree(calculator.beta), " degrees")

    calculator2 = Calc(100,65, 120)
    calculator2.CalculateAlphaAndBeta()
    print("alpha is : ", calculator2.alpha, " degrees")
    print("beta is : ", calculator2.beta, " degrees")

#===================================== Sanity check =======================================#
    
    Rsqr = calculator.x**2 + calculator.y**2
    dsqr = calculator.d**2
    if isclose(Rsqr, 2*dsqr* (1+ np.cos(calculator.beta-calculator.alpha)), abs_tol=1e-9):
        print("Sanity check went well")

