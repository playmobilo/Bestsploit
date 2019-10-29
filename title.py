exploit_name = "45271.txt"
with open('/home/akos/bme/szakdolgozat/exploit-db/files_exploits.csv','r') as file:
	#lista = file.split('\n')
	#print(len(lista))
	#txt = file.read()
	#txt1 = txt.split('\n')
	#print(txt)
	#if txt1 != None:
	#	if exploit_name in txt:
	#		tolist = txt.split(',')
	#		print("success")
	#		print(tolist[15])

	for line in file: 
		if exploit_name in line:
			txt = line.split(',')
			print(txt[2])