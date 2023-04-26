# Data-Design-Representation
These are two individual web-scrapping projects I did for DDR course in UCD MSBA program

There are two parts in the first Individual project.
In the first part. I was asked to grap the data for the sold amazon gift card in ebay and find out the rate of cards sold at the price less than its value.
and here are the detailed requirements:

a) use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".

b) take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

c) write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.

d) using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.

e) using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.

f) What fraction of Amazon gift cards sells above face value? Why do you think this is the case?

 

In the second part, I was asked to use "BeautifulSoup" to place an order in a sport gambling website and the detailed requirements are following:

a) Following the steps we discussed in class and write code that automatically logs into the website fctables.comLinks to an external site..

b) Verify that you have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/Links to an external site..  Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.
