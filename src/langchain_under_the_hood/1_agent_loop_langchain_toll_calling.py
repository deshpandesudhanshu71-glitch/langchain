from dotenv import load_dotenv

load_dotenv() 

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable 


MAX_ITERATION = 10
MODEL = "qwen3:1.7b" 


# __ tools fot eh application ___ 
@tool
def get_product_price(product:str) -> float:
    """ Look up the price of a product in a catalog. """ 
    print(f" >>executing get_product_price (product = '{product}')") 
    prices = {"laptop": 1299.99, "headphones": 149.90, "Keyboard" : 89.50} 

    return prices.get(product, 0)


@tool
def apply_discount(price:float, discount_tier:str) -> float: 
    """ apply the discount tier to a price and return the final price. Avialable tiers : bronze, silver, gold"""
    print(f"  >>Executing tht apply_discount(price = {price}, discount_tier  = {discount_tier})")

    discount_percentage = {"bronze": 5, "silver" : 12, "gold": 23} 

    discount = discount_percentage.get(discount_tier, 0) 
    return round(price * (1 - discount/100), 2)


#__Agent Loop __ 

@traceable(name = "Langchain in AgentLoop")
def run_agent(question : str): 
    pass 

if __name__ == "__main__": 
    print("Hello Langchain Agent (.blind_tools)!")
    print ()
    result = run_agent("What is the price of a laptop after applying a gold discount ? ")