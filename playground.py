import requests
from lifted.either import Either
import pyramda as r
import re
from lifted.util import *

predicate = r.compose(r.equals(200), r.getattr('status_code'))  
def isvalid(x):
    if hasattr(x,'map'):
        return all(x.map(predicate))
    else:
        return predicate(x)


#Either.of = classmethod( lambda cls,x: cls.right(x) if isvalid(x) else cls.left(x) )


def get(url):
    resp = requests.get(url)
    return Either.right(resp) if isvalid( resp ) else Either.left(resp)

@r.curry
def parse(search_for,content):
    return Either.of( excepting( content.find )(search_for) )







def wiki_test():
    res = (
        decorate(excepting,r.add(2))
            .promap( 
                excepting(float), 
                r.if_else( 
                    r.if_else(isvalid,r.gt(10),r.always(False)), Either.right, Either.left 
                ) 
            )( ['15'] )
    )

    url = 'https://en.wikipedia.org/wiki/The_Terminal'

    result = (
    Either
        .right(url)
        .chain( get )
        .chain( lambda x: (
            (parse(b'href="/wiki/Rotten_Tomatoes',x.content)
                .chain( lambda y: x.content[y-100:y+100] ),
                x
            )
            )
        )
    )




#parser = lambda content, substr: parse(substr,content).chain(   )

# Either.right(url).chain( get ).chain( parse('Rotten') )
'''
url = 'https://en.wikipedia.org/wiki/The_Terminal'

result = Either.right(url).chain( get ).chain( lambda x: (
        parse(b'Rotten',x.content)
            .chain( lambda y: x.content[y:y+100] )
    )
)

'''

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
# from tabulate import tabulate
# import os

# ###################################################################################################################
# #launch url
# url = "http://kanview.ks.gov/PayRates/PayRates_Agency.aspx"

# # create a new Firefox session
# driver = webdriver.Firefox()
# driver.implicitly_wait(30)
# driver.set_page_load_timeout(60)
# driver.get(url)

# #After opening the url above, Selenium clicks the specific agency link
# python_button = driver.find_element_by_id('MainContent_uxLevel1_Agencies_uxAgencyBtn_33') #FHSU
# python_button.click() #click fhsu link

# #Selenium hands the page source to Beautiful Soup
# soup_level1=BeautifulSoup(driver.page_source, 'lxml')

# datalist = [] #empty list
# x = 0 #counter

# #Beautiful Soup finds all Job Title links on the agency page and the loop begins
# for link in soup_level1.find_all('a', id=re.compile("^MainContent_uxLevel2_JobTitles_uxJobTitleBtn_")):
    
#     #Selenium visits each Job Title page
#     python_button = driver.find_element_by_id('MainContent_uxLevel2_JobTitles_uxJobTitleBtn_' + str(x))
#     python_button.click() #click link
    
#     #Selenium hands of the source of the specific job page to Beautiful Soup
#     soup_level2=BeautifulSoup(driver.page_source, 'lxml')

#     #Beautiful Soup grabs the HTML table on the page
#     table = soup_level2.find_all('table')[0]
    
#     #Giving the HTML table to pandas to put in a dataframe object
#     df = pd.read_html(str(table),header=0)
    
#     #Store the dataframe in a list
#     datalist.append(df[0])
    
#     #Ask Selenium to click the back button
#     driver.execute_script("window.history.go(-1)") 
    
#     #increment the counter variable before starting the loop over
#     x += 1
    
#     #end loop block
    
# #loop has completed

# #end the Selenium browser session
# driver.quit()

# #combine all pandas dataframes in the list into one big dataframe
# result = pd.concat([pd.DataFrame(datalist[i]) for i in range(len(datalist))],ignore_index=True)

# #convert the pandas dataframe to JSON
# json_records = result.to_json(orient='records')

# #pretty print to CLI with tabulate
# #converts to an ascii table
# print(tabulate(result, headers=["Employee Name","Job Title","Overtime Pay","Total Gross Pay"],tablefmt='psql'))

# # #get current working directory
# # path = os.getcwd()

# # #open, write, and close the file
# # f = open(path + "\\fhsu_payroll_data.json","w") #FHSU
# # f.write(json_records)
# # f.close()

# ###################################################################################################################

def bsoup4_wiki_test():
    @r.curry
    def find_all(tag,el):
        return Either.of( excepting(el.findAll)(tag) )

    #import the library used to query a website
    import urllib.request as urllib2
    #specify the url
    wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
    wiki = 'https://en.wikipedia.org/wiki/The_Terminal'
    wiki = 'https://en.wikipedia.org/wiki/2007_in_film'
    wiki = 'https://en.wikipedia.org/wiki/List_of_romantic_comedy_films'
    #Query the website and return the html to the variable 'page'
    page = urllib2.urlopen(wiki)
    #import the Beautiful soup functions to parse the data returned from the website
    from bs4 import BeautifulSoup
    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page)
    all_tables=soup.find_all('table')
    right_table=soup.find('table', class_='wikitable')

    #Generate lists
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]
    for row in right_table.findAll("tr"):
        cells = row.findAll('td')
        states=row.findAll('th') #To store second column data
        if len(cells)==6: #Only extract table body not heading
            A.append(cells[0].find(text=True))
            B.append(states[0].find(text=True))
            C.append(cells[1].find(text=True))
            D.append(cells[2].find(text=True))
            E.append(cells[3].find(text=True))
            F.append(cells[4].find(text=True))
            G.append(cells[5].find(text=True))

    #import pandas to convert list to data frame
    import pandas as pd
    df=pd.DataFrame(A,columns=['Number'])
    df['State/UT']=B
    df['Admin_Capital']=C
    df['Legislative_Capital']=D
    df['Judiciary_Capital']=E
    df['Year_Capital']=F
    df['Former_Capital']=G


    # get_tds = ( lambda x:
    #     traverse(Either,find_all('td'))(x)
    #         .chain( fmap( r.map( r.getattr('text') ) ) )
    # )

    # get_text = ( lambda x:
    #     x.chain( fmap( r.map( r.getattr('text') ) ) )
    # )

    get_tds_ths = (
        lambda x:
            Tuple( ( traverse(Either, find_all("td"))(x), traverse(Either, find_all("th"))(x)  ) )
    )

    get_some = (
        lambda x: 
            x.chain( find_all("tr") )
                .chain( Tuple )
                .bind( Either.of )
                .chain( get_tds_ths )
    )

    cc = (
        Tuple( all_tables )
            .map( Either.right ).map( get_some ).map( lambda x: x.map(get_text) )
    )

    df = (
        pd.DataFrame(
            r.filter( lambda x: len(x)==5, cc[3][0] ), 
            columns= r.filter( lambda x: len(x)==5, cc[3][1]  )[0] 
        )
    )

    # b = a[0] # values
    # #b = a[1] # headers
    # b.chain( r.identity ).map( lambda y: r.map(lambda z: z.find(text=True),y ) )

    # c = b.chain( r.identity ).map( lambda y: r.map(lambda z: z,y ) )

    # ## good! 
    # c = b.chain( fmap( r.map( r.getattr('text') ) ) )