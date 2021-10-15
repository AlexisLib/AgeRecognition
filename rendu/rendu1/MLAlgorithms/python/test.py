def multMat(a, b):
	ret = 0
	for i in range(len(a)):
		ret += a[i] * b[i]
	return ret

lr = 1.05
result = [0,0,0]

datas = [
			[1, 0.72, 0.32, 6.93],
			[1, 0.75, 0.12, 5.99],
			[1, 0.53, 0.65, 1.46],
			[1, 0.27, 0.82, 1.44],
			[1, 0.49, 0.15, 4.51],
			[1, 0.02, 0.19, 1.25],
			[1, 0.35, 0.87, 2.53],
			[1, 0.99, 0.71, 6.88],
			[1, 0.98, 0.92, 6.25],
			[1, 0.73, 0.19, 6.36]
		]

weight = [	
			0.1,
			0.1,
			0.1
		]

for epo in range(1, 31):
	for i in range(10):
		mat = multMat(weight, datas[i])
		result[0] += -1 * (datas[i][3] - mat)

		mat = multMat(weight, datas[i])
		result[1] += -datas[i][1] * (datas[i][3] - mat)

		mat = multMat(weight, datas[i])
		result[2] += -datas[i][2] * (datas[i][3] - mat)

	# print(result)
	result = [x * 1/10 for x in result ]
	# print(result)

	weight = [ weight[x] - lr * result[x]  for x in range(len(result)) ]
	
	#print("%s :" % epo, end=' ' )
	#print(weight, end='\n\n')

print(weight)

# weight(1:3)
# x1(3:1)



