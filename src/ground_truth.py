import pandas as pd
import pickle

val_df = pd.read_csv("data/emoji_val.2csv",index_col=0)
emoji_list = emoji_set = val_df["emoji"].values.tolist()

val_df["full_desc"] = val_df.full_desc.apply(lambda x: x.strip('][').split(', '))
val_df["desc2"] = val_df.desc2.apply(lambda x: x.strip('][').split(', ') if isinstance(x,str) else "")

for i in val_df.index:
    for j in range(len(val_df.full_desc[i])):
        val_df.full_desc[i][j] = val_df.full_desc[i][j].strip("/'")
    if val_df.desc2[i]:
        for k in range(len(val_df.desc2[i])):
            val_df.desc2[i][k] = val_df.desc2[i][k].strip("/'")
            
# build validation dictionary
val_dict = {}
lst = []
for i in val_df.index.tolist():
    lst.extend(val_df.full_desc[i])
    lst.extend(val_df.desc2[i])
    
vals = list(set(lst))
for val in vals:
    val_dict[val] = []
    for index in val_df.index:
        
        if val in val_df.full_desc[index]:
            val_dict[val].append(val_df.emoji[index])
        elif val in val_df.desc2[index]:
            val_dict[val].append(val_df.emoji[index])



with open('val_dict.pickle', 'wb') as handle:
    pickle.dump(val_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

## update validation set
# val_dict2 = dict();
# for key, value in val_dict.items():
#     if re.split('[- ]', key) == 1:
#         a = key.strip('[():“”]')
#         if a not in val_dict2:
#             val_dict2[a] = value
#         else:
#             val_dict2[a].append(value)
#     else:
#         for i in re.split('[- ]', key):
#             i2 = i.strip('[():“”]')
#             if i2 not in val_dict2:
#                 val_dict2[i2] = value
#             else:
#                 val_dict2[i2].append(value)
            
# with open('val_dict2.pickle', 'wb') as handle:
#     pickle.dump(val_dict2, handle, protocol=pickle.HIGHEST_PROTOCOL)