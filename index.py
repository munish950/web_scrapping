import mysql.connector
import scrap 
import re

# Initialization point
def init():
	try:
		mydb = mysql.connector.connect(host = "localhost",user = "root",passwd = "",database= "test")
		dbcon = mydb.cursor()
	except:
		print('Error! Please check your DB Connection')
		exit()
	
	# Initialize loop
	first_menu = 99
	while first_menu:
		try:
			first_menu = int(input('Choose one: \n 1. Display All \n 2. Search Data \n 3. Refetch Data \n 0.Exit \n'))
		except:
			print('Select only from give Options \n')
			continue
		
		
		if first_menu == 1:
			sql = "SELECT * FROM mv_collection LIMIT "
			getRecords(dbcon, sql)		
		elif first_menu == 2:
			search = 99
			while search:
				try:
					print('Leave field empty if not required (atleast one field is mandatory)')
					search_year = 0
					get_rating = 0
					search_name = ''
					sql_query = 'SELECT * FROM mv_collection WHERE '
					search_name = input('name: ').strip()
					search_release_year = input('Release Year (Provide as \'>2018\' OR \'<2018\' OR \'2018\'): ').strip()
					search_rating = input('Rating (Provide as \'>5.6\' OR \'<5.6\' OR \'5.6\'): ').strip()
					
					if search_name:
						sql_query+= "name LIKE '%%%s%%' and" %(search_name)
					
					if search_release_year:
						if search_release_year[0] == '>' or search_release_year[0] == '<':
							if search_release_year[1:].isdigit():
								search_year = search_release_year[0]+' '+search_release_year[1:]
								sql_query+= " release_year %s and" %(search_year)
						elif search_release_year.isdigit():
							search_year = search_release_year
							sql_query+= " release_year LIKE '%s' and" %(search_year)
						else:
							print('Search Year Input is not valid')
					
					if search_rating:
						if search_rating[0] == '>' or search_rating[0] == '<':					
							get_rating = search_rating[0]+' '+search_rating[1:]
							sql_query+= " rating %s and" %(get_rating)
						elif re.match('^[0-9]+([.][0-9]{1,2})?$', search_rating):				
							get_rating = search_rating
							sql_query+= " rating LIKE %s and" %(get_rating)
						else:
							print('Search Rating Input is not valid')
					
					if search_name or search_year or get_rating:
						# Remove last 'and' from query 
						k = sql_query.rfind('and')
						sql_query = sql_query[:k]
						sql_query+= 'LIMIT '
						print(sql_query)
						get_return_val = getRecords(dbcon, sql_query)
						if get_return_val == 0:
							break
						
					else:
						print('Please provide atleast one search parameter')
					
				except Exception as e:
					print('Invalid Selection \n')
		elif first_menu == 3:			
			try:			
				warning = int(input('Do you want to Truncate table and reinsert Data! \n 1. Yes \n 0. No \n'))
				if warning == 1:
					# Truncate Table Data
					truncate_query = 'TRUNCATE table mv_collection'		
					dbcon.execute(truncate_query)
					mydb.commit()
					scrap.main(dbcon, mydb)
				elif warning != 0:
					print('Invalid Selection \n')
			except:
				print('Select only from give Options \n')
		elif first_menu != 0:
			print('Select only from give Options \n')



		

		
def getRecords(dbcon, sql):
	limit = 0
	navigate_menu = 99
	prev = '1. PREV \n'
	next = '2. NEXT \n'
	rep_flag = True
	return_val = 0
	while navigate_menu:
		if rep_flag == True:				
			get_records = sql+ str(limit) +",20"
			dbcon.execute(get_records)
			result = dbcon.fetchall()
		
		if len(result) > 0:
			if rep_flag == True:
				print('Id | Name | Link | Release year | Rating')
				for row in result:
					print(row[0],' | ',row[1],' | ',row[2],' | ',row[3],' | ',row[4])
						
			try:					
				navigate_menu = int(input('\n Select One \n'+prev+next+'0. Back \n'))				
			except:					
				print('Invalid Selection \n')
				rep_flag = False
				continue
			
			if navigate_menu == 1:
				#prev selected
				rep_flag = True
				if limit >= 10:
					limit-=10
					prev = '1. PREV \n'
				else:
					prev = ''
					rep_flag = False
				
			elif navigate_menu == 2:
				#next selected
				rep_flag = True
				limit+=10
				next = '2. NEXT \n'
				prev = '1. PREV \n'
				
			elif navigate_menu != 0:
				print('Invalid Selection \n')
				rep_flag = False							
			
		else:
			next = ''
			print('No More Records to display')
			rep_flag = False
			navigate_menu = 0

	return return_val
	
	
# Initialize application
init()

	
	

