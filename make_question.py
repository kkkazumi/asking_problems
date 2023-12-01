import numpy as np
import pandas as pd
from operator import itemgetter

keys = np.genfromtxt("dictionary_key.txt",dtype="str")
#print(keys)

#problems_data = pd.read_csv("test_db.csv")
#print(problems_data)


f = open("test_db2.csv", "r", encoding="utf-8")
_problems_data = f.read()
f.close()
problems_data=_problems_data.split("\n")
problems_db_list = []
key_counts_list = []
for i in range(len(problems_data)):
	dict_problem = {}
	problems_text = problems_data[i].split(",")
	key_counts = 0
	if(problems_text[0]!=""):
		dict_problem["problem"] = problems_text[0]
		#print(problems_data[i])
		dysfunction_list = []
		for key in keys:
			if(key in problems_data[i]):
				dysfunction_list.append(str(key))
				#dict_problem[str(key)] = 1
				key_counts+=1
		dict_problem["dysfunction"]=dysfunction_list
		dict_problem["key_counts"]=key_counts
		key_counts_list.append(key_counts)
		problems_db_list.append(dict_problem)

def get_common_dysfunction_count(personal_dict):
	personal_dysfunctions_list = personal_dict["dysfunction"]
	common_count_list = []
	for prob in problems_db_list:
		#print(prob["dysfunction"])
		common_dysfunction = list(set(prob["dysfunction"]).intersection(personal_dysfunctions_list))
		common_count_list.append(len(common_dysfunction))
	return common_count_list

def get_next_question(common_count_list,question_list):
	min_list = [i for i, v in enumerate(common_count_list) if v == min(common_count_list)]
	min_list = [new_list for new_list in min_list if new_list not in question_list]

	#check_common_rate = np.array(key_counts_list)/np.array(common_count_list)
	small_common_keycounts = [key_counts_list[t] for t in min_list]
	next_index = min_list[small_common_keycounts.index(max(small_common_keycounts))]

	return problems_db_list[next_index]["problem"]
	

def record_question_index(question_str,asked_question_list):
	for i in range(len(problems_db_list)):
		if(question_str==problems_db_list[i]["problem"]):
			asked_question_list.append(i)
	return asked_question_list

def estimate_problem(personal_dict):
	common_dysfunction_count_list = get_common_dysfunction_count(personal_dict)
	each_problem_rate = np.array(common_dysfunction_count_list)/np.array(key_counts_list) 
	return each_problem_rate
		
question_list = []
dysfunction_order_db = sorted(problems_db_list,key=itemgetter("key_counts"),reverse=True)

first_question = dysfunction_order_db[0]["problem"]
question = first_question

ASKING_LIMIT_TIME = 3

personal_dict = {}
personal_dict["dysfunction"] = []

for t in range(ASKING_LIMIT_TIME):
	record_question_index(question,question_list)
	print(question,question_list)
	answer=input()
	if(answer=="yes"):
		personal_dict["dysfunction"].extend(problems_db_list[question_list[-1]]["dysfunction"])
	question=get_next_question(get_common_dysfunction_count(personal_dict),question_list)

print(estimate_problem(personal_dict))
