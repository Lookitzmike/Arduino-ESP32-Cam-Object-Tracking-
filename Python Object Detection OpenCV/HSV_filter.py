class HSV_filter:

    # Custom data structure to store HSV filter values
    def __init__(self, H_min=None, S_min=None, V_min=None, H_max=None, S_max=None, V_max=None, 
                    Sat_add=None, Sat_sub=None, Bright_add=None, Bright_sub=None):
        self.H_min = H_min
        self.S_min = S_min
        self.V_min = V_min
        self.H_max = H_max
        self.S_max = S_max
        self.V_max = V_max
        self.Sat_add = Sat_add
        self.Sat_sub = Sat_sub
        self.Bright_add = Bright_add
        self.Bright_sub = Bright_sub

