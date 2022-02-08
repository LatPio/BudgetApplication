dict1 = {'1.2': [1,2,3], '2.2': [4,5,6], '3.3': [7,8,9]}
print({k:sum(v) for k,v in dict1.items()})