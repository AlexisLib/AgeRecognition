import os, sys
sys.path.append("D:/Cours/3IBD/projetAnnuel/api/")
from myDB import MyDB
from random import randint,shuffle

ratioTest = 0.20 

try:
	db = MyDB()

	db.query("UPDATE PICTURE SET isTrain = 1;")

	for age in range(1,116):
		for gender in range(0,1):
			for race in range(0,4):
				#recupère le nombre de photo
				query = "SELECT count(name) FROM PICTURE WHERE age=%s and gender=%s and race=%s;" % (age, gender, race)
				db.query(query)
				number = int( db.fetchone()[0] )
				print(number)

				if number >= 5:
					#recupere les photos
					query = "SELECT name FROM PICTURE WHERE age=%s and gender=%s and race=%s;" % (age, gender, race)
					db.query(query)
					pictures = db.fetchall()
					shuffle(pictures)
					pictures = pictures[:int(len(pictures)*ratioTest)]
					print("Taille sous-set %s" % len(pictures))

					for picture in pictures:
						query = "UPDATE PICTURE SET isTrain = 0 WHERE name='%s';" % picture
						db.query(query)
						print(query)
except:
	print("Error database")
