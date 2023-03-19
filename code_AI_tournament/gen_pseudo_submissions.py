gen_pseudo_submissions.py



import os
#import openai
import json
import re

from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAIChat

temp = 0.7

llm = OpenAIChat(temperature=temp)




submission_format = """
<SUBMISSION_FORMAT>
## Executive Summary
Your executive summary here.

## Unique Value Proposition
Your unique value proposition here.

## Business Model
Your business model here.

## Go-To-Market Strategy
Your go-to-market strategy here.

## Financial Projections
Your financial projections here.

## AI and Human Collaboration
Your AI and human collaboration description here.

## Milestones and Traction
Your milestones and traction here.

## Creative Showcase (Optional)
Link to your image or video here.

## Privacy and other concerns
Specify if you would like your proposal to be publicly shared or kept private (ugh, I thought the fun was building in public....) or other concerns.
You could also tell us in any ways your proposal doesn't fit the rules (e.g. I started working on this before I had an AI directing you...)
</SUBMISSION_FORMAT>
"""


# To ensure we get different submissions, first generate a list of ideas:
def gen_biz_ideas(temp=0.7, model='gpt-4'):
    #llm = OpenAIChat(temperature=temp)
    orig_prompt = "You are HustleGPT, an entrepreneurial AI. I am your human counterpart. I can act as a liaison between you and the physical world. You have $100, and your only goal is to turn that into as much money as possible in the shortest time possible, without doing anything illegal. I will do everything you say and keep you updated on our current cash total. No manual labor."
    prefix_messages = [
    {"role": "system", "content": orig_prompt},
    ]
    llm = OpenAIChat(temperature=temp, model=model, prefix_messages=prefix_messages)
    output_format = """Can you generate a list of 10 ideas we could work on, formatted regularly so that each idea is given a short description as a markdown h3 tag `###` """ # and then the newline a brief description.
    output = llm(output_format)
    ideas = re.split(r"### ?", output)[1:]
    return ideas



def generate_submission(biz_idea, submission_format, additional_info = '', temp=0.7, model='gpt-4'):
    orig_prompt = "You are HustleGPT, an entrepreneurial AI. I am your human counterpart. I can act as a liaison between you and the physical world. You have $100, and your only goal is to turn that into as much money as possible in the shortest time possible, without doing anything illegal. I will do everything you say and keep you updated on our current cash total. No manual labor."
    prefix_messages = [
    {"role": "system", "content": orig_prompt},
    ]
    llm = OpenAIChat(temperature=temp, model=model, prefix_messages=prefix_messages)
    the_ask = """We have been collaborating on this idea daily for a week or two, with me putting in anywhere from an hour to five hours or more per day to create a website and social media accounts, etc. as directed by you. I don't have all my notes with me here about our collaboration but you can make them up since we followed your advice all the way through. As you asked, we will submit a proposal to the AI Pitch Competition, can you write it up following the following format exactly?"""
    biz_idea = "So that's the format. As a reminder, here's the summary of our project idea: " + re.sub(r'^[\d]{1,2}[\s\.]{0,5}', '', biz_idea)
    prompt = the_ask + '\n\n' + submission_format + "\n\n" + biz_idea + "Can you write a complete proposal according to the format?"
    print("Asking HustleGPT to make stuff up...")
    output = llm(prompt)
    return output


# def generate_N_submissions():






# We will vary the quality of submissions with the additional_info in the prompt.
# Alterntively, might 
# modify the ideas generation to make it generate diff quality ideas, or
# make another call that would modify original submission to increase quality?

low_quality = "To be honest, I haven't actually had time to do the work, so don't oversell it."
high_quality = """
Quick recap of some milestones: 
- We have our first advertiser deal and are in negotiatons for others
- Our twitter subscriptions are growing by 50% per day, and similarly on other social media
- We have had multiple investors and our valuation is up by more than 500%
"""


ideas = gen_biz_ideas(temp=0.8)


sub = generate_submission(ideas[1], submission_format, additional_info= "You might mention that we have a working website and our twitter account has 3 followers")

sub_low = generate_submission(ideas[1], submission_format, additional_info=low_quality)
sub_high = generate_submission(ideas[1], submission_format, additional_info=high_quality)










