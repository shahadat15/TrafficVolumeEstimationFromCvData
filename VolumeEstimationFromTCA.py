import csv
import os
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import random
import math

## Input by user

Mean_Market_penetration = 2.018
SD_Market_penetration = 0.31
min_limit = 2.677
Max_limit = 14.06
Number_of_runs = 100  # The total number of simulation run want to do
filename = "ResultArterialVol_2" # output file name

file_name = "fzpfile_freeway_70P.csv" #input file name

location_of_detector1 = 3000 #270
location_of_detector2 = 4150 #720
location_of_detector3 = 5550 #1270
location_of_detector4 = 6800#1740
location_of_detector5 = 7200#2070

Min_x = 2400
Max_x = 2800

vol = []

for i in range(Number_of_runs):
	#########set input parameter in the TCAinput.xml file

	# read the file
	tree = ET.parse('TCAinput.xml')
	root = tree.getroot()
	root.tag

	# for child in root:
	# print(child.tag, child.attrib)

	# root[0][1].text

	# change the seed number
	for rank in root.iter('Seed'):
		new_rank = random.randint(342000, 343000)
		rank.text = str(new_rank)
	# rank.set('updated', 'yes')

	# change the market penetration
	for rank1 in root.iter('BSMMarketPenetration'):
		new_rank1 = int(
			round(math.exp(np.random.normal(loc=Mean_Market_penetration, scale=SD_Market_penetration, size=None))))
		if new_rank1 < min_limit:
			new_rank1 = min_limit
		elif new_rank1 > Max_limit:
			new_rank1 = Max_limit
		rank1.text = str(new_rank1)
		
	for rank2 in root.iter('FileName'):
        new_rank2 = str(file_name)
        rank2.text = str(new_rank2)
	# write the file into TCAinput.xml
	tree.write('TCAinput.xml')

	############ Call the TCA to run the program
	os.system("TCA2.py")

	#### Analysis with the output
	data1 = pd.read_csv("BSM_Trans.csv")
	# data1.head()

	data2 = data1[["PSN", "localtime", "spd", "x", "y"]]
	data2 = data2[(data2.x>Min_x)&(data2.x<Max_x)]
	data3 = data2.sort_values("PSN")


	a1 = 0
	#i = 0
	nv = 0

	data4 = data3.groupby("PSN")


	def calcu1(dd):
		tt = dd["localtime"].max() - dd["localtime"].min()
		if tt < 150:
			a1 = dd["y"].max()
			a2 = dd["y"].min()
			if ((a2 < location_of_detector1) & (a1 > location_of_detector1)):
				return 1
			else:
				return 0
		else:
			return 0

	def calcu2(dd):
		tt = dd["localtime"].max() - dd["localtime"].min()
		if tt < 150:
			a1 = dd["y"].max()
			a2 = dd["y"].min()
			if ((a2 < location_of_detector2) & (a1 > location_of_detector2)):
				return 1
			else:
				return 0
		else:
			return 0

	def calcu3(dd):
		tt = dd["localtime"].max() - dd["localtime"].min()
		if tt < 150:
			a1 = dd["y"].max()
			a2 = dd["y"].min()
			if ((a2 < location_of_detector3) & (a1 > location_of_detector3)):
				return 1
			else:
				return 0
		else:
			return 0

	def calcu4(dd):
		tt = dd["localtime"].max() - dd["localtime"].min()
		if tt < 150:
			a1 = dd["y"].max()
			a2 = dd["y"].min()
			if ((a2 < location_of_detector4) & (a1 > location_of_detector4)):
				return 1
			else:
				return 0
		else:
			return 0

	def calcu5(dd):
		tt = dd["localtime"].max() - dd["localtime"].min()
		if tt < 150:
			a1 = dd["y"].max()
			a2 = dd["y"].min()
			if ((a2 < location_of_detector5) & (a1 > location_of_detector5)):
				return 1
			else:
				return 0
		else:
			return 0


	nv1 = data4.aggregate(calcu1)
	nv2 = data4.aggregate(calcu2)
	nv3 = data4.aggregate(calcu3)
	nv4 = data4.aggregate(calcu4)
	nv5 = data4.aggregate(calcu5)
	count1 = nv1.sum()[1]
	count2 = nv2.sum()[1]
	count3 = nv3.sum()[1]
	count4 = nv4.sum()[1]
	count5 = nv5.sum()[1]

	count = [count1,count2,count3,count4,count5]
	vol.append(count)
	print i

print np.mean(vol)
print np.std(vol)
np.savetxt('%s.csv' % filename, vol, delimiter=",", fmt='%10.5f')
