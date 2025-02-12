def convert_us_format(s):
    return float((s.replace("%", "")).replace(",", "")) 

def update_dict(dict1, dict2):
    for key, value in dict2.items():
        dict1[key] = dict1.get(key, 0) + value
    return dict1

def return_top_k(dictionary, kmax=30):
    sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    top_k = sorted_items[:kmax]
    return {key: value for key, value in top_k}

def add_other(dictionary):
    total_percentage = sum(dictionary.values())
    dictionary["Others"] = max(0, 100 - total_percentage)
    return dictionary