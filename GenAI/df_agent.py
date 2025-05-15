import os 
import pandas as pd

from IPython.display import Markdown, HTML, display
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

# subscription_key = "Bh8WpJT8gIkNSiRnWnrDGdK9lqMPTJJuh6zcsxdp2cSlgMy1Q8K8JQQJ99BEACHYHv6XJ3w3AAAAACOGQJV0"


# model = AzureChatOpenAI(
#     openai_api_version="2024-12-01-preview",
#     azure_deployment="gpt-4o",
#     azure_endpoint="https://aihub5774811166.openai.azure.com/",
#     api_key=subscription_key,
# )

# df = pd.read_csv("C:\Projects\CUSTOMER_DATA_V.csv").fillna(value = 0)

# from langchain.agents.agent_types import AgentType
# #from langchain.agents import create_pandas_dataframe_agent
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# agent = create_pandas_dataframe_agent(llm=model,df=df,verbose=True,allow_dangerous_code=True)

# response=agent.invoke("What financial products can we offer to the customer C0001 based on his financial goals?")
# print(response)
# print(response['output'])
# print(type(response))

def df_fn(df,query):
    subscription_key = "Bh8WpJT8gIkNSiRnWnrDGdK9lqMPTJJuh6zcsxdp2cSlgMy1Q8K8JQQJ99BEACHYHv6XJ3w3AAAAACOGQJV0"


    model = AzureChatOpenAI(
        openai_api_version="2024-12-01-preview",
        azure_deployment="gpt-4o",
        azure_endpoint="https://aihub5774811166.openai.azure.com/",
        api_key=subscription_key,
    )

    df = df

    from langchain.agents.agent_types import AgentType
    #from langchain.agents import create_pandas_dataframe_agent
    from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

    agent = create_pandas_dataframe_agent(llm=model,df=df,verbose=True,allow_dangerous_code=True)

    agent.invoke(query)