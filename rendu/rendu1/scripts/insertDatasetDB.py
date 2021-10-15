""" [age]_[gender]_[race]_[date&time].jpg
[age] is an integer from 0 to 116, indicating the age
[gender] is either 0 (male) or 1 (female)
[race] is an integer from 0 to 4, denoting White, Black, Asian, Indian, and Others (like Hispanic, Latino, Middle Eastern).
[date&time] is in the format of yyyymmddHHMMSSFFF, showing the date and time an image was collected to UTKFace
"""

import os
import mysql.connector as mariadb

repository = os.path.normpath("D:/Cours/3IBD/projetAnnuel/dataset")


def createRequest(metadata):
	return "INSERT INTO PICTURE(name, age, gender, race, dateCollect) VALUES ('{}',{},{},{},'{}-{}-{}');".format(metadata["name"], metadata["age"], metadata["gender"], metadata["race"], metadata["date"][:4], metadata["date"][4:6],metadata["date"][6:8])

def countString(string, char):
	res = 0
	for element in string:
		if (element in char):
			res += 1
	return res

if __name__ == '__main__':

	try:
		mariadb_connection = mariadb.connect(host='192.168.1.20', port=3307 ,user='application', password='8*vcjn.nwACH+m6f', database='dataset')
		cursor = mariadb_connection.cursor()
		print("ok")

		metadata = {}

		for file in os.listdir(repository):		
			print(file)

				try:
					if(countString(file,'_') != 3):

						raise formNameFile()

					metadata["name"] = file
					metadata["age"], metadata["gender"], metadata["race"], metadata["date"] = file[:-13].split('_')

					if( int(metadata["age"]) < 0 or int(metadata["age"])  >116):
						print('1')
						raise Exception()

					if( int(metadata["gender"]) != 0 and int(metadata["gender"]) != 1):
						print('22')
						raise Exception()

					if( int(metadata["race"]) !=0  and int(metadata["race"]) != 1 and int(metadata["race"]) != 2 and int(metadata["race"]) != 3 and int(metadata["race"]) != 4):
						print('3')
						raise Exception()

					try:
						cursor.execute(createRequest(metadata))
					except mariadb.Error as error:
						print("Error: {}".format(error))

				except:
					print("Error name file : " + file)
			
		
		mariadb_connection.commit()
		mariadb_connection.close()

	except:
		print("error db")




