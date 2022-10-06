import streamlit as st
import pandas as pd
import os
import json


st.set_page_config(layout="wide")

file_dir = os.path.dirname(os.path.realpath('__file__'))
#For accessing the file in a folder contained in the current folder
SymptomsOutput = os.path.join(file_dir, 'Data/SymptomsOutput.json')

# df = pd.read_json(SymptomsOutput)



with open(SymptomsOutput) as f:
    SymptomsOutput = json.loads(f.read())
    # print(SymptomsOutput[0]['text'])



list_of_names = []
for i in range(len(SymptomsOutput)):
    list_of_names.append(SymptomsOutput[i]['name'])   


col1, col2, col3 = st.columns(3)
option = col1.selectbox(
    'Select sypmtom : ', list_of_names)

for i in range(len(SymptomsOutput)):  
    if SymptomsOutput[i]['name'] == option and SymptomsOutput[i]['type'] == "categorical" :
        col2.write(SymptomsOutput[i]["text"])
        col2.write(SymptomsOutput[i]["laytext"])
        col2.write("Values : ")
        values = []
        # col2.write(SymptomsOutput[i]["choices"])
        for j in SymptomsOutput[i]["choices"]:
            values.append(j['value'])
            col2.write(str(j['value']) + " -> " +j['text'])
        value_in = col3.number_input("Insert a number", min_value = min(values), max_value=max(values))

# name = SymptomsOutput[100]['name']
# st.write(name)
# for i in SymptomsOutput[100]['choices']:
#     st.write(f"{i['text']}")
#     st.write(f"value = {i['value']}")
    # choices = SymptomsOutput[100]['choices']
    # st.write(choices)


#SymptomsOutput = pd.read_json(SymptomsOutput)
# st.dataframe(SymptomsOutput)

# list_name = list(SymptomsOutput['name'])
# print(list_name)