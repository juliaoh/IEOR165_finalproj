import json
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--biz')


def extract_data(biz):
	biz_f = open(biz)
	biz_jsons = biz_f.readlines()
	matrix = []
	for biz_json in biz_jsons:
		try:
			biz = json.loads(biz_json)
			data = [biz["stars"], biz["review_count"]]
			matrix.append(data)
		except Exception as e:
			#skip over malformed ones
			print(e)
			print(biz_json)
	biz_f.close()
	return matrix


if __name__ == "__main__":
	args = parser.parse_args()
	matrix = extract_data(args.biz)
	f = open('star_to_review_matrix.pkl', 'wb')
	pickle.dump(matrix, f)
	f.close()

