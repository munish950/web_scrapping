from bs4 import BeautifulSoup
from urllib import request, parse
#import mysql.connector


def main(dbcon, mydb):
	# Call function with default parameter
	params = '?groups=top_250&page=1&ref_=adv_nxt'
	scrapPageData(params, dbcon, mydb)	
	
# Recursive function
def scrapPageData(params, dbcon, mydb):
	base_url = 'https://www.imdb.com/search/title/'		
	dataurl = parse.urljoin(base_url,params);

	url_content = request.urlopen(dataurl).read()
	soup = BeautifulSoup(url_content, 'html.parser')
	contentDiv = soup.body.find_all('div', class_="lister-item")
	
	
	# Loop over each data Div
	for divData in contentDiv:
		movie_name = divData.h3.a.string
		movie_link = divData.h3.a['href']
		movie_rating = divData.find('div', class_="ratings-imdb-rating")['data-value']
		movie_year = divData.find('span', class_='lister-item-year').string.lstrip('(').rstrip(')')		
		try:
			insert_query = '''INSERT INTO mv_collection (name,link,release_year,rating) VALUES (%s, %s, %s, %s)'''
			result = dbcon.execute(insert_query, (str(movie_name),str(movie_link),str(movie_year),str(movie_rating)))			
		except:
			print('Error occur while inserting records.')
			exit()
	
	mydb.commit()
		
	navigateTag = soup.body.find('div', class_='desc')
	
	try:
		navigateUrl = navigateTag.find('a', class_="lister-page-next")['href']
		if navigateUrl:
			# Call Recursive function	
			scrapPageData(navigateUrl, dbcon, mydb)
	except:
		exit()
		

if __name__ == "__main__":
	print('No direct access allowed')
	exit()
	#main(dbcon)
	

	