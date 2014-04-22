import random
import pickle
import argparse
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--pkl')
parser.add_argument('--csv')

if __name__ == "__main__":
	args = parser.parse_args()
	matrix_f = open(args.pkl, 'rb')
	matrix = pickle.load(matrix_f)
	random_100 = []
	for _ in range(100):
		index = random.randint(0, len(matrix)-1)
		random_100.append(matrix.pop(index))
	matrix_f.close()
	f = open("random_100.pkl", 'wb')
	pickle.dump(random_100, f)
	f.close()
	if args.csv == "yes":
		with open("random_100.csv", 'w') as fp:
			writer = csv.writer(fp, delimiter=',')
			writer.writerows(random_100)
			fp.close()
		
