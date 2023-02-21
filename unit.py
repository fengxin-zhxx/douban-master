from database import *

with open('quotes.txt','w+') as f:
    sql = 'select quote from movie'
    quotes = execute_sql(sql, 1)
    # print(quotes[0])
    for quote in quotes[0]:
        f.write(quote)
    

