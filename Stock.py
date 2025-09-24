
class Stock:

  def __init__(self, StockID, value, amount):
    self.StockID = StockID
    self.value = value
    self.paid = value*amount
    self.amount = amount
    self.performance = 0

  def printStockInfo(self):
    #print(self.paid, "    ", self.amount, "    ", self.value)
    print("you have bought", self.amount, "shares for a total of ", self.paid)
    print("the total amount of all shares you own is now ", self.value * self.amount)
  
  def calculatePerformance(self):
    self.performance = (self.paid / self.value) * 100
    if (self.performance == self.paid):
        print("Your stock is the same value as you have paid")
    elif (self.performance > 0):
      print("Your stock has increased in value ", self.performance, " percent.")
    else:
      print("the stock has decreased in value ", self.performance, " percent.")

  def getStockValue(self):
    self.value = 0





