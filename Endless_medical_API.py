import streamlit as st
import os
import json
import random
from collections import OrderedDict
import requests
url = "http://api.endlessmedical.com/v1/dx/"

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Endless Medical API Application</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>provide you disease prediction anbalysis based on symptoms given by user </h3>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: black;'>All you need to do is : Select the number of symptoms -> Select each symptom -> Insert a number for each symptom based on the description given at the left side </h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: black;'>Then click the button Analysis </h6>", unsafe_allow_html=True)


file_dir = os.path.dirname(os.path.realpath('__file__'))
#For accessing the file in a folder contained in the current folder
SymptomsOutput = os.path.join(file_dir, 'Data/SymptomsOutput.json')

# df = pd.read_json(SymptomsOutput)



with open(SymptomsOutput) as f:
    SymptomsOutput = json.loads(f.read())
    # print(SymptomsOutput[0]['text'])



list_of_names = [""]
for i in range(len(SymptomsOutput)):
    list_of_names.append(SymptomsOutput[i]['name'])   



count = 0
col1, col2, col3 = st.columns(3)
syptom_number = st.sidebar.number_input("Select the number of symptoms :", min_value=1, max_value=len(list_of_names), value=2)
st.sidebar.header("Symptom Description")

option_syptom = []
value_symptom = []
for iter_symptom in range(syptom_number):
    st.sidebar.markdown(f"_Symptom_ {iter_symptom+1}")
    option = col1.selectbox(
        f'Select symptom_{iter_symptom+1} : ', list_of_names, key = count)
    option_syptom.append(option)
    for i in range(len(SymptomsOutput)):  
        if SymptomsOutput[i]['name'] == option and SymptomsOutput[i]['type'] == "categorical" :
            st.sidebar.write(SymptomsOutput[i]["text"])
            values = []
            for j in SymptomsOutput[i]["choices"]:
                values.append(j['value'])
                st.sidebar.write(str(j['value']) + " -> " +j['text'])
            value_in = col2.number_input("Insert a number", min_value = min(values), max_value=max(values), value= SymptomsOutput[i]["default"], key=count+1)
            value_symptom.append(value_in)
            st.sidebar.markdown("""
            ---
            """)
        elif SymptomsOutput[i]['name'] == option :
            st.sidebar.write(SymptomsOutput[i]["text"])
            value_in = col2.number_input("Insert a number", min_value = SymptomsOutput[i]["min"], max_value=SymptomsOutput[i]["max"], value= SymptomsOutput[i]["default"], key = count+2)
            value_symptom.append(value_in)
            st.sidebar.markdown("""
            ---
            """)
    count += 3
dict_symptoms = OrderedDict(zip(option_syptom, value_symptom))

st.write("Click the button Analysis to make the calculations and view the results called by endlessmedical APIs")
get_API = col2.button("*********** Analyze ***********")






def diagnostic_function(dict_symptoms):
    init_output = requests.get(url +"InitSession")
    session_id = init_output.json()['SessionID']
    param_atou = {
        "SessionID":session_id,
        "passphrase":"I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and Endless Medical services. The Terms of Use are available on endlessmedical.com" 
        }

    requests.post(url +"AcceptTermsOfUse", params=param_atou)

    param = {
        "SessionID":session_id,
        }


    for key,value in dict_symptoms.items():
        param_symptom = param.copy()
        param_symptom.update({"name":key, "value":value})
        requests.post(url +"UpdateFeature", params=param_symptom)

    patient_on_analysis = requests.get(url +"Analyze", params=param).json()

    patient_diag = {}
    for i in range(3):
        desease_name = list(patient_on_analysis["Diseases"][i].items())[0][0]
        list_symptoms = patient_on_analysis["VariableImportances"][i][desease_name][:2]
        patient_diag[desease_name] = list_symptoms

    return patient_diag


if get_API:
    st.write(diagnostic_function(dict_symptoms))