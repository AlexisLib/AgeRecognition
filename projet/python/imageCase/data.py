#Parametres

#2x + 3
# trainX = [[1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7], [1,8], [1,9], [1,10]]
# trainY = [4.897, 7.094, 9.064, 11.049, 12.859, 15.054, 17.005, 18.852, 20.864, 23.065]
# XToPredict = [1,11]



# trainX = [
# 			[1, 0.72, 0.32],
# 			[1, 0.75, 0.12],
# 			[1, 0.53, 0.65],
# 			[1, 0.27, 0.82],
# 			[1, 0.49, 0.15],
# 			[1, 0.02, 0.19],
# 			[1, 0.35, 0.87],
# 			[1, 0.99, 0.71],
# 			[1, 0.98, 0.92],
# 			[1, 0.73, 0.19]
# 		]

# # trainY = [6.93, 5.99, 1.46, 1.44, 4.51, 1.25, 2.53, 6.88, 6.36]
# trainY = [6.93, 5.99, 1.46, 1.44, 4.51, 1.25, 2.53, 6.88, 6.25, 6.36]
# XToPredict = [1, 0.98, 0.92]

# 4.5*x1 - 2.3*x2 + 1
trainX = [[1,x1,x2] for x1 in range(30) for x2 in range(30)]
trainY = [4.5*x1 - 2.3*x2 + 1 for x1 in range(30) for x2 in range(30)]

XToPredict = [1,31,31]


# NE PAS TOUCHER
arrayWeight = []							# poids
sampleCount = len(trainY)					# number exemples
inputCountPerSample = len(trainX[0])		# number caracteristique par exemple

XToPredictSize = len(XToPredict)

#tranforme en double
for el in trainX:
	el = list(map(float, el))

trainY = list(map(float, trainY))
XToPredict = list(map(float, XToPredict))


