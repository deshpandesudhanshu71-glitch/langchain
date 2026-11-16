import os

from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool 
from langchain_anthropic import ChatAnthropic 
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field 



class sourse(BaseModel):
    """scheme for a source used by agent to retrieve information"""
   
    url: str = Field(description="the url of the source")
   
class Agent_response(BaseModel):
    """scheme for agent response with answer and sources"""

    answer: str = Field(description="the answer to the question")
    sources: list[sourse] = Field(description="the sources used to answer the question")


@tool
def search_source(query: str, source: sourse) -> str:
    """search the source for the query"""
    return f"search the source {source.url} for the query {query}"

llm = ChatAnthropic(model="claude-sonnet-5-5", anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")) 
tools = [TavilySearch() ]
agent = create_agent(model = llm, tools = tools, response_format=Agent_response)

def main() -> None:
    print("Hello from langchain-search-agent!")
    result = agent.invoke({"messages": [HumanMessage(content="search for 3 jobs posting for ai engineer using langchain in ireland on linkdin and list their details")]})
    print(result)

if __name__ == "__main__":
    main()
