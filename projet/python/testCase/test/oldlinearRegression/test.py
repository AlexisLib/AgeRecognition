# fonction combinaisons(Liste L, Liste F, k) {
#    si k supérieur au nombre d'éléments de F {
#         quitter
#    } sinon si k est égal à 0, {
#         afficher  L
#    } sinon {
#         pour tous les éléments x de l'ensemble F  {
#              Liste G = les éléments de F placés après x dans L
#              Liste L2  = L plus x
#                          (on a concaténé x à la droite de la liste L)
#              combinaisons(L2, G , k-1)
#         }
# }

# combinaisons("", (1,2,3,4,5,6), 3);

def getIdx(tab, value):
	for idx, el in enumerate(tab,0):
		if el == value:
			return idx
	return -1 

def combinaison(L, F, k):
	if (k > len(F)):
		return 
	elif (k == 0):
		print(L)
	else:
		L2 = []
		for x in F:
			G = [ f for f in F if getIdx(L,f) > getIdx(L,x) ]
			L2 = list(L)
			L2.append(x) 
			print(L2)
			combinaison(L2, G, k-1)

# for x,y in combinaison([], [1,2,3,4,5,6], 3):
#     print(x,y)
combinaison([], [1,2,3,4,5,6], 3)
print("end")
