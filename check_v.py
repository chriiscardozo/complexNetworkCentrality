i = 0

arr = {}

while i < 60:
	n = input()
	n = int(n)
	if n in arr:
		arr[n] += 1
	else:
		arr[n] = 1

	i += 1

print '\n\n***\n\n'
for i in arr:
	if arr[i] == 6:
		print i
