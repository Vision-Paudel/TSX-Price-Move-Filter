# TSX Stock Ticker Web Scrapping Code Written By Vision Paudel

import requests
import bs4
import lxml
import time

ticker_list = []
ticker_price = {}
ticker_price_movers = {}

print('Initializing Program...')
percentage_move = '$'
while not percentage_move.isdigit():
    percentage_move = input("Please enter the percentage move (as integer) to filter (i.e. 5): ")
percentage_move = int(percentage_move)

print('Getting ticker codes...')
list_of_Alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
list_of_last_tickers = ['AZZ','BYL.DB','CYH','DYA.WT','EXN.WT','FXM','GXE','HZU','IVQ.U','JWEL','KXS','LXR','MYA','NZC','OXC','PZW.F','QXM','RY.PR.Z','SZLS.WT','TZS','UXM.B','VXM.B','WXM','XXM.B','YXM.B','ZZZD']

for item in list_of_Alphabets:

    result = requests.get("http://www.eoddata.com/stocklist/TSX/" + item + ".htm")
    soup = bs4.BeautifulSoup(result.text,"lxml")
    list_from_soup = soup.select('.quotes td a')

    for code_item in list_from_soup:
        if len(code_item.getText()) == 0:
            continue
        elif code_item.getText() in list_of_last_tickers:
            ticker_list.append(code_item.getText())
            break
        else:
            ticker_list.append(code_item.getText())
    print("Codes starting with {} done.".format(item))
print('Printing ticker codes...')
print(ticker_list)

print('Checking price info for the first time...')

for ticker_item in ticker_list:
    result = requests.get("https://web.tmxmoney.com/quote.php?qm_symbol=" + ticker_item )
    soup = bs4.BeautifulSoup(result.text,"lxml")
    list_from_soup = soup.select('.price span')
    if len(list_from_soup) > 0:
        ticker_price[ticker_item] = float(list_from_soup[0].getText().replace(",",""))
        print(ticker_item + " : " + list_from_soup[0].getText())
    else:
        print(ticker_item + " not found in web.tmxmoney.com")

print("Done! Napping for 30 mins...")
time.sleep(1800)

while True:
    print("Waking up...")
    ticker_price_movers = {}
    for ticker_item in ticker_price.keys():
        result = requests.get("https://web.tmxmoney.com/quote.php?qm_symbol=" + ticker_item )
        soup = bs4.BeautifulSoup(result.text,"lxml")
        list_from_soup = soup.select('.price span')

        if len(list_from_soup) > 0:
            new_price = float(list_from_soup[0].getText().replace(",",""))
            if new_price >= (ticker_price[ticker_item] * (1.00 + percentage_move/100)):
                print("Price mover found:")
                ticker_price_movers[ticker_item] = new_price
            ticker_price[ticker_item] = float(list_from_soup[0].getText().replace(",",""))
            print(ticker_item + " : " + list_from_soup[0].getText())

    print("Any price movers are below:")    
    for ticker_item in ticker_price_movers.keys():
        print(ticker_item + " : {}".format(ticker_price_movers[ticker_item]))
    
    print("Done! Napping for 30 mins...")
    time.sleep(1800)
