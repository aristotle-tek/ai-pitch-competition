
import random
import os
import pandas as pd

import requests

import numpy as np
import pandas as pd
import re


import os
import openai
import json
import time




def extract_dict_from_json(json_string_wextra):
    json_string = re.findall(r'{[\s\S]*}', json_string_wextra)[0]
    data = json.loads(json_string)
    return(data)



def parse_json_for_overallscore(content):
    try:
        scores = content["overall_score"]
        grade1 = scores["pitch1"]
        grade2 = scores["pitch2"]
        return [grade1, grade2]
    except:
        print("failed parsing dict")
        return [np.NaN, np.NaN]



def text_status(status):
    if status == '🟧🟩':
        status_descr = "For-profit business that has made a sale"
    elif status == '🟧⬜️':
        status_descr = "For-profit business that has NOT YET made a sale"
    elif status[0] =='🟦' : # '🟦⬜️'
        status_descr = "Nonprofit"
    else: status_descr = "other"
    return(status_descr)

def webtext_or_none(webtext):
    webtext_nosp = re.sub(r'\s', '', webtext)
    if len(webtext_nosp)< 10:
        return("No website text")
    else:
        return(webtext)





data_dir = "/pitch_competition/hustleGPT/"



# Products and Services (combines 👕Products, 🛠️Business Resources, 😊Wellbeing, and 🦮Pets)

# This category focuses on businesses that create tangible products or provide services in various industries, including wellness, pets, and B2B solutions.

# Entertainment and Lifestyle (combines 🎸Entertainment, 🍔Food and Drink, 🖌️Art, and 📚Education)
# This category involves businesses related to arts, entertainment, food, and education, catering to diverse consumer interests and preferences.

# Sustainability and Social Impact (combines 🌱Eco-friendly)
# This category is dedicated to businesses that prioritize environmentally friendly solutions and contribute positively to society.

categories = ["🤖ChatGPT and AI", 'Products and Services','']

pitchs = pd.read_csv("AI_Gen_Pitches.csv")

#pitchs.category.value_counts()

#pitchs1 = pitchs[pitchs.category=="🤖ChatGPT and AI"]


#to = Tournament()

whichdata = "all_1shot"

whichmodel = 'gpt-3.5-turbo'


sleeptime = 11

pairings_id = 'na'


system_text = """
You are a an expert entrepreneur and angel investor who will evaluate competing pitches for new business ideas.
You will be evaluating a series of pitches for HustleGPT, wherein humans collaborate with ChatGPT to develop new businesses (and
in a few cases, to build on existing businesses).


The categories of pitches are:
🤖ChatGPT and AI         33
🛠️Business Resources    25
👕Products               18
😊Wellbeing              15
🎸Entertainment          14
🚀Miscellaneous          13
🍔Food and Drink         11
🖌️Art                   11
🌱Eco-friendly           10
🕹️Games                 10
🦮Pets                    8
📚Education               2

Evaluate the following pitch and give it a rating from 0 to 10 according to the following criteria:
1. Scalability and market potential; Potential for revenue growth, as measured by the speed at which they will be able to get to $100,000 cash on hand
2. Creativity or novelty - is the idea new or just recycling existing ideas?
3. Transformative potential - is the proposal an innovative business that transforms the world in a positive way?
4. Leveraging collaboration - to what extent is the business a smart way to make use of collaboration between a human and an AI agent ChatGPT?
5. Risks and challenges - How immune is the business to potential risks and future challenges, whether from competitors, government regulation, or technological change?
The output will be a python dictionary with ratings on the five dimensions and an overall score, as follows:
(with `N10` standing in for a score from 0-10, and `N100` standing in for a score from 0-100:
{
    "growth_potential":
        {"pitch1": N10,
         "pitch2": N10},
    "creativity":
        {"pitch1": N10,
         "pitch2": N10},
    "transformative_potential":
        {"pitch1": N10,
         "pitch2": N10},
    "leveraging_collaboration":
        {"pitch1": N10,
        "pitch2": N10},
    "risk_immunity":
        {"pitch1": N10,
        "pitch2": N10},
    "overall_score":
        {"pitch1": N100,
        "pitch2": N100}
}
"""


format_text = """
Format the output as a python dictionary with ratings on the four dimensions and an overall score, as follows:
(with `N10` standing in for a score from 0-10, and `N100` standing in for a score from 0-100:
{
    "growth_potential": N10,
    "creativity": N10,
    "transformative_potential": N10,
    "leveraging_collaboration": N10,
    "overall_score": N100
}
"""


class Text_1shot_eval():
    def __init__( self, openai_api_key, systemprompt, formatprompt):
        openai.api_key =openai_api_key
        self.openai_api_key = openai_api_key
        self.systemprompt = systemprompt
        self.formatprompt = formatprompt

    def oneshot_eval_with_supptext(self, text1, supptext1, model='gpt-3.5-turbo'):
        prompts = [{"role": "system", "content": self.systemprompt}]
        prompts.append({"role": "user", "content": """First, for background, here is some background, 
            such as text from the website of the competitor, if it exists: \n<text_pitch>\n""" + \
            supptext1 + """</text_pitch>\nIs this clear so far? Respond 'yes.' or 'no.' """ })
        prompts.append({"role": "assistant", "content": """yes.""" })
        prompts.append({"role": "user", "content": """Great! Now, with that in mind, here is the pitch to grade:\n<pitch>\n""" + \
            text1 + "</pitch>\n" + self.formatprompt })
        try:
            print("Calling OpenAI API...")
            response = openai.ChatCompletion.create(
                model=model,
                messages=prompts,
                temperature=0,
            )
            return response
        except:
            print("failed getting GPT response, retrying after 12s pause...")
            time.sleep(12)
            print("Calling OpenAI API...")
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=prompts,
                    temperature=0,
                )
                return response
            except:
                print("failed getting GPT response, retrying after 1m pause...")
                time.sleep(62)
                response = openai.ChatCompletion.create(
                model=model,
                messages=prompts,
                temperature=0,
                )
                return response    

    def parse_string_list(self, response):
        # parse a string list that has two numbers in it like: "sdfi= [32, 19]"
        # return [32, 19]
        content = response.choices[0].message.content
        try:
            grades = re.findall(r'\d+', content)
            grades = [float(g) for g in grades]
            return grades
        except:
            print("failed parsing string list")
            return [np.NaN, np.NaN]

    def parse_dict_for_overallscore(self, response):
        # NB This is misnamed - it actually parses the API response!
        content = response.choices[0].message.content
        content = json.loads(content)
        try:
            scores = content["overall_score"]
            grade1 = scores["pitch1"]
            grade2 = scores["pitch2"]
            #grades = re.findall(r'\d+', content)
            #grades = [float(g) for g in grades]
            return [grade1, grade2]
        except:
            print("failed parsing dict")
            return [np.NaN, np.NaN]



Evaluator = Text_1shot_eval("api_key..." \
    system_text, format_text)


results_log = []

for i, row in pitchs.iterrows():
    print(i)
    biz_name = row['bname']
    to_id = "df_row" + str(i)

    pitch1 = row['content']

    supptext1 = "NAME: " + biz_name   + "\nSTATUS: " + text_status(row['status'])   + "\nWEBTEXT:\n" + webtext_or_none(row['text'])
    #print(supptext1)
    response = Evaluator.oneshot_eval_with_supptext(pitch1, supptext1, model=whichmodel) #'gpt-3.5-turbo')


    json_res = response.choices[0].message.content
    try:
        results_list = Evaluator.parse_dict_for_overallscore(response)
    except:
        py_dict = extract_dict_from_json(json_res)
        try:
            result = py_dict['overall_score'] # parse_json_for_overallscore(py_dict)
        except:
            result = np.NaN
    print(results_list)
    results_log.append([biz_name, result, json_res, i])



rdf = pd.DataFrame(results_log)
rdf.columns = ['name', 'result', 'json_res', 'row_id']

rdf.to_csv(data_dir + whichdata + "_apr1.csv")



import seaborn as sns
sns.histplot(data=rdf, x="result")

import matplotlib.pyplot as plt
plt.show()




rdf.sort_values('result')


