"""Extracts from Yelp academic dataset JSON files and returns pkled matrix:
#FORMAT: [BIZ_AVG_STAR, USER_AVG_RATING, RATING]
"""

import json
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--biz')
parser.add_argument('--user')
parser.add_argument('--review')


def extract_tuple(biz, user, review):
	#Extract business data
	biz_f = open(biz)
	biz_jsons = biz_f.readlines()
	#{BIZ_ID: STAR}
	biz_dict = {}
	for biz_json in biz_jsons:
		try:
			biz = json.loads(biz_json)
			biz_id = biz["business_id"]
			biz_star = biz["stars"]
			biz_dict[biz_id] = biz_star
		except Exception as e:
			#skip over malformed ones
			print(e)
			print(biz_json)
	biz_f.close()

	#Extract user data
	user_f = open(user)
	user_jsons = user_f.readlines()
	#{USER_ID: AVG_STAR}
	user_dict = {}
	for user_json in user_jsons:
		try:
			user = json.loads(user_json)
			user_dict[user["user_id"]] = user["average_stars"]
		except Exception as e:
			print(e)
			print(user_json)
	user_f.close()


	#Extract review data
	review_f = open(review)
	review_jsons = review_f.readlines()
	# print("review json length " + str(len(review_jsons)))
	review_set = set()
	duplicate = 0
	for review_json in review_jsons:
		try:
			review = json.loads(review_json)
			#Only one review is taken into consideration per user per business for now
			data = (review["business_id"], review["user_id"], review["stars"])
			if data in review_set:
				duplicate+=1
			review_set.add(data)
		except Exception as e:
			print(e)
			print(review_json)
	review_f.close()

	# print(len(review_set))
	# print(duplicate)

	#Construct the matrix
	matrix = []
	for review in review_set:
		biz, user, star = review[0], review[1], review[2]
		#FORMAT: BIZ_AVG_STAR, USER_AVG_RATING, RATING
		triple = [biz_dict[biz], user_dict[user], star]
		matrix.append(triple)
	# print(len(matrix))
	return matrix



if __name__ == "__main__":
	"""
	Usage: python3 extract_rating.py --biz data/yelp_academic_dataset_business.json --review data/yelp_academic_dataset_review.json --user data/yelp_academic_dataset_user.json 

	"""
	args = parser.parse_args()
	matrix = extract_tuple(args.biz, args.user, args.review)
	f = open('triple_matrix.pkl', 'wb')
	pickle.dump(matrix, f)
	f.close()
	# check pickling successful
	# f = open('triple_matrix.pkl', 'rb')
	# matrix_pkl = pickle.load(f)
	# print(matrix == matrix_pkl)

	
