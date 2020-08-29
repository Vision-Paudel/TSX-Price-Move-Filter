# TSX-Price-Move-Filter
Simple Price Move Filter

Dependency (requires module install):

```command line
pip install requests
pip install bs4
pip install lxml

```
Like any web scrapper, may break when website is updated. 
Some values are hard coded such as last symbol for each letter which need to be periodically updated.

Use:

Asks for percentage move to filter
Gets the TSX codes from eoddata.com/stocklist/TSX
Gets real-time price for the codes from web.tmxmoney.com
Sleeps for 30 mins before checking if the price has gone up by the percentage amount, then filters and displays it.
