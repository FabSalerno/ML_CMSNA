
import json

with open("dict_samples_2022.json", "r") as f:
    sample = json.load(f)

file_dict = sample["TT_2022"]["TT_semilep_2022"]["ntot"]
biggest_sample_num = file_dict.index(max(file_dict))
#biggest_sample_num = max(sample["TT_2022"]["TT_semilep_2022"]["ntot"],key=sample["TT_2022"]["TT_semilep_2022"]["ntot"].get)

print(biggest_sample_num)  


