#%%
# Import from standard library
import logging
from dotenv import load_dotenv # Add
import os
import random
import openai

import streamlit as st
import streamlit.components.v1 as components
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

load_dotenv()
#%%
# App framework
st.set_page_config(page_title="Tell me a story", page_icon="📚")
st.write(os.getenv('OPENAI_API_KEY'))
st.title("🍹 Generate a story! 🌇")

topic = st.text_input(label="Generate a story!👇",
    label_visibility="visible",
    placeholder="Choose a topic",
)

with open("moods.txt") as f:
    sample_moods = f.read().splitlines()
    mood = random.choice(sample_moods)

sample_ages = [x for x in range(1, 11)]
age = random.choice(sample_ages)

# Prompt templates
title_template = PromptTemplate(
    input_variables=["topic"],
    template="Give a title for a children's story about {topic}",
)

story_template = PromptTemplate(
    input_variables=["age", "title", "mood"],
    template="Write a story for a {age} year old kid with this title: {title}. Write it with a {mood} mood.",
)

# Memory
title_memory = ConversationBufferMemory(input_key="title", memory_key="chat_history")
story_memory = ConversationBufferMemory(input_key="title", memory_key="chat_history")


# Llms
llm = OpenAI(temperature=0.9, model_name="davinci", n=2, best_of=2)
title_chain = LLMChain(
    llm=llm,
    prompt=title_template,
    verbose=True,
    output_key="title",
    memory=title_memory,
)
story_chain = LLMChain(
    llm=llm,
    prompt=story_template,
    verbose=True,
    output_key="story",
    memory=story_memory,
)

#%%
# Show stuff to the screen if there's a prompt
if topic:
    title = title_chain.run(topic)
    story = story_chain.run(title, age, mood)
    script = story_chain.run(title=title, story=story)

    st.write(title)
    st.write(script)

    with st.expander("Title History"):
        st.info(title_memory.buffer)

    with st.expander("Story History"):
        st.info(story_memory.buffer)
