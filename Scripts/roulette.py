import random
import time

st_num = ['Okura', 'Onodera', 'Suzuki', 'Xu']

while(1):
	if len(st_num) == 1:
		print("The roulette is over")
		break

	print("input 'd' to remove a participant")
	print("input 's' to start the roulette")
	print("input '0' to end the roulette")
	print("Command:")
	ini = input()

	if ini == 'd':
		print("Who do you want to remove?")
		print(st_num)
		rem = input()
		st_num.remove(rem)
		print("done")

	elif ini == 's':
		n = random.randint(1, len(st_num)) - 1
		print("loading...")
		time.sleep(1)
		demo1 = random.randint(1, len(st_num)) - 1
		print('-', st_num[demo1])
		time.sleep(3)
		demo2 = random.randint(1, len(st_num)) - 1
		print('-', st_num[demo2])
		time.sleep(3)
		demo3 = random.randint(1, len(st_num)) - 1
		print('-', st_num[demo3])
		time.sleep(2)
		demo4 = random.randint(1, len(st_num)) - 1
		print('-', st_num[demo4])
		time.sleep(1)
		demo5 = random.randint(1, len(st_num)) - 1
		print('-', st_num[demo5])

		print("\n↓result↓\n")
		time.sleep(3)
		print('->', st_num[n])
		time.sleep(5)
		print("------------------------------------------------")
		st_num.remove(st_num[n])

	elif ini == '0':
		print("The roulette is over")
		break

	else:
		print("retry")