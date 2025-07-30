class DataBud:
    def __init__(self, data=None):

        if data is None:
            self.SavingsAccounts = {
                "liquid": 9000, 
                "ira": 8750,
                "schwab": 16000
            }

            self.OnHand = {
                "cash": 100,
                "checking": 500
            }

            self.MonthlyEarnings = {
                1: 0, 
                2: 0,
                3: 0, 
                4: 0, 
                5: 0, 
                6: 0, 
                7: 0, 
                8: 0, 
                9: 0,
                10: 0, 
                11: 0, 
                12: 0
            }

            self.GigDiary = {
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: [],
                7: [],
                8: [],
                9: [],
                10: [],
                11: [],
                12: []
            }
        else:
            self.SavingsAccounts = data[0]
            self.OnHand = data[1]
            self.MonthlyEarnings = {int(k): data[2][k] for k in data[2]}
            self.GigDiary = {int(k): data[3][k] for k in data[3]}

        self.data = [self.SavingsAccounts, self.OnHand, self.MonthlyEarnings, self.GigDiary]

    def savAcc(self):
        return self.SavingsAccounts
    
    def OH(self):
        return self.OnHand
    
    def monEar(self):
        return self.MonthlyEarnings
    
    def GD(self):
        return self.GigDiary
