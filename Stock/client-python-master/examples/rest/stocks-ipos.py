from polygon import RESTClient

# docs
# https://polygon.io/docs/rest/stocks/corporate-actions/ipos

# client = RESTClient("XXXXXX") # hardcoded api_key is used
client = RESTClient()  # POLYGON_API_KEY environment variable is used

ipos = []
for ipo in client.vx.list_ipos(ticker="RDDT"):
    ipos.append(ipo)

print(ipos)
