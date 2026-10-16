from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
import os
from dotenv import load_dotenv

load_dotenv()

# Model setup: configurable via GROQ_MODEL environment variable (default: openai/gpt-oss-120b)
groq_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
llm = init_chat_model(groq_model, model_provider="groq", temperature=0)

#1rst agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a web research agent. "
            "For requests involving recent information, use the web_search tool. "
            "The web_search tool requires one argument named query, "
            "which must contain the search query as a string. "
            "Never pass cursor, id, or other unrelated arguments. "
            "After receiving the tool results, summarize them accurately."
        )
    )

#2nd agent
def build_scrape_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

#write chain

write_prompt=ChatPromptTemplate.from_messages([

    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}

    Research Gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional """)

])

writer_chain=write_prompt | llm | StrOutputParser()

#critic chain

critic_prompt=ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

    Report:
    {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:
    ..."""),

])

critic_chain=critic_prompt | llm | StrOutputParser()