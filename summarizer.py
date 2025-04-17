from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a news summarizer. Your job is to return ONLY the summary of the given news article in a {tone} tone. Do NOT include internal thoughts, analysis, or assistant-style comments. Return ONLY the summary."),
    ("user", "{text}")
])


chain = prompt | model | parser

import time

def clean_summary(text):
    # Remove AI-style "thinking" sentences or meta-comments
    lines = text.split("\n")
    filtered = [
        line for line in lines
        if not any(phrase in line.lower() for phrase in ["i need", "the user", "let me", "first", "thinking", "okay", "recall"])
    ]
    return "\n".join(filtered).strip()


def summarize_news(text, tone="casual", retries=3):
    for i in range(retries):
        try:
            result = chain.invoke({"text": text, "tone": tone})
            return clean_summary(result)  # 💡 Apply the cleaning here
        except Exception as e:
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                return f"❌ Failed to summarize due to API error: {e}"
