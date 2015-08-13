import csv
import os
import shutil
import pycountry
import re

if not os.path.exists('./country-codes/cache'):
	os.makedirs('./country-codes/cache')

out_data = []

with open('./country-codes/data/country-codes.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile)
	header = csvreader.next()
	for row in csvreader:
		add_array = []
		if len(row) == 20:
			add_array.append(pycountry.countries.get(alpha2=row[2]).name)
			add_array.append(row[1])
			add_array.append(pycountry.countries.get(alpha2=row[2]).alpha2)
			add_array.append(pycountry.countries.get(alpha2=row[2]).alpha3)
			add_array.append(pycountry.countries.get(alpha2=row[2]).numeric)
			for x in range(5,len(row)):
				if row[x] != '':
					add_array.append(row[x])
				else:
					add_array.append('NULL')
		elif len(row) == 21:
			# print row
			pass

		elif len(row) == 22:
			add_array.append(pycountry.countries.get(alpha2=row[4]).name)
			add_array.append(row[3] + ' ' + row[2])
			add_array.append(pycountry.countries.get(alpha2=row[4]).alpha2)
			add_array.append(pycountry.countries.get(alpha2=row[4]).alpha3)
			add_array.append(pycountry.countries.get(alpha2=row[4]).numeric)
			for x in range(7,len(row)):
				if row[x] != '':
					add_array.append(row[x])
				else:
					add_array.append('NULL')

		elif len(row) == 23:
			pass
			# print row

		elif len(row) == 26:
			add_array.append(pycountry.countries.get(alpha2=row[4]).name)
			add_array.append(row[3] + ' ' + row[2])
			add_array.append(pycountry.countries.get(alpha2=row[4]).alpha2)
			add_array.append(pycountry.countries.get(alpha2=row[4]).alpha3)
			add_array.append(pycountry.countries.get(alpha2=row[4]).numeric)
			add_array.append(str(['x'+row[8], 'x'+row[9]]))
			# for x in range(8,len(row)):
			# 	if row[x] != '':
			# 		add_array.append(row[x])
			# 	else:
			# 		add_array.append('NULL')
			print row
			print add_array
		
		elif len(row) == 32:
			pass

		else:
			# pass
			print row
			# print row
		out_data.append(add_array)
	print header


# shutil.rmtree('./country-codes/cache')