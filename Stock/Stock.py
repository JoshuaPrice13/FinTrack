#from polygon import RESTClient

from polygon import RESTClient




class Stock:
  #when creating stock pass in this order: name(ie: AAPL), the current price, how many shares
  def __init__(self, StockID: str, value: float, amount: int):



    self.StockID = StockID
    self.value = value
    self.paid = value*amount
    self.amount = amount
    self.performance = 0

  def printStockInfo(self):
    #print(self.paid, "    ", self.amount, "    ", self.value)
    print("you have bought", self.amount, "shares for a total of ", self.paid)
    print("the total value of all shares you own is now ", self.value * self.amount)
  
  def calculatePerformance(self):
    print("Calculating performance:", self.paid, self.value, (self.paid/self.amount))
    self.performance = (1 - (self.value / (self.paid / self.amount))) * 100
    #return self.performance
    if (self.value == self.paid/self.amount):
        print("Your stock is the same value as you have paid")
    elif (self.value > (self.paid/self.amount)):
      print("Your stock has increased in value ", self.performance, " percent.")
    else:
      print("the stock has decreased in value ", self.performance, " percent.")
    return self.performance

  def updateStock(self):
    client = RESTClient("ptnWWdAXRkeO307_jzWunijWb2iNndIu")
    try:
      sID = self.StockID
      details = client.get_ticker_details(
        str(sID),
      )
    except:
        print("Stock not in known stocks, will not update\n")
        return -1
    #print(details)

    self.value = details.market_cap / details.share_class_shares_outstanding
    self.calculatePerformance()
    #print(self.value)
    #self.printStockInfo()
    return 0


  def buyShares(self, amount, value):
    if (value <= 0 or amount <= 0):
      print("value of the shares / amount of shares cannot be < or = to 0")
      return -1
    
    self.paid += amount * value
    self.amount += amount

  def sellShares(self, amount, value):
    if (value <= 0 or amount <= 0):
      print("value of the shares / amount of shares cannot be < or = to 0")
      return -1
    
    if (self.amount - amount > 0):
      self.amount -= amount
      self.paid -= amount * value
    else:
      return -1

  def getStockPerformance(self):
    print("paid:", self.paid, "\n")
    print("paid:", self.paid, "\n")
    if (self.amount >= 0):
      if(self.paid > 0):
        return ((self.amount * self.paid) / self.value) * 100
      else:
        return (self.amount / self.value) * 100
    return -1
    
    
  





