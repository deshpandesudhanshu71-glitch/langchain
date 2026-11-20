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
    tools = [get_product_price, apply_discount]
    tool_dict = {t.name: t for t in tools}
    llm = init_chat_model(f"ollama:{MODEL}", temperature=0)
    llm_with_tools = llm.bind_tools(tools) 

    print(f"Question: {question}")
    print("=" * 60)

    message = [
        SystemMessage(
            content = (
                 "You are a helpful shopping assistant. "
                "You have access to a product catalog tool "
                "and a discount tool.\n\n"
                "STRICT RULES — you must follow these exactly:\n"

            )
        ),
          HumanMessage(content=question),
    ]

    for iteration in range(1, MAX_ITERATION + 1):
        print(f"\n--- Iteration {iteration} ---")

        ai_message = llm_with_tools.invoke(message)

        tool_calls = ai_message.tool_calls

        # If no tool calls, this is the final answer
        if not tool_calls:
            print(f"\nFinal Answer: {ai_message.content}")
            return ai_message.content 

        # process only FIRST tool calls - force one tool per iteration
        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call.get("id")
        print(f"  [Tool Selected] {tool_name} with args: {tool_args}") 

        tool_to_use = tool_dict.get(tool_name)
        if tool_to_use is None: 
            raise ValueError(f"Tool '{tool_name}' not found") 

        observation = tool_to_use.invoke(tool_args)

        print(f" [Tool result] {observation}") 

        message.append(ai_message)
        message.append(
            ToolMessage(content = str(observation), tool_call_id=tool_call_id)
        )
              
    print ("Error: Max iteration reached without a final answer")
    return None


if __name__ == "__main__": 
    print("Hello Langchain Agent (.blind_tools)!")
    print ()
    result = run_agent("What is the price of a laptop after applying a gold discount ? ")