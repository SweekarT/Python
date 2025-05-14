def geography(user_input):
    """Gives the geographical data of a place."""
    op = 'This is the geography of '+user_input
    print(op)
    return op

def history(user_input):
    """Gives the historical data of a place."""
    op = 'This is the history of '+user_input
    print(op)
    return op


import os
from openai import AzureOpenAI
import json


endpoint = endpoint
model_name = model_name
deployment = deployment
subscription_key = subscription_key
api_version = api_version

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


print("Chatbot: Hello! How can I assist you today? Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Ending the conversation. Have a great day!")
        break

    try:
        messages = [
            {"role": "user",
             "content": user_input
             }
        ]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "geography",
                    "description": "Gives the geographical data of a place.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_input": {
                                "type": "string",
                                "description": "The name of the place to get geographical data for."
                            }
                        },
                        "required": ["user_input"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "history",
                    "description": "Gives the historical data of a place.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_input": {
                                "type": "string",
                                "description": "The name of the place to get historical data for."
                            }
                        },
                        "required": ["user_input"]
                    }
                }
            }
        ]
        response = client.chat.completions.create(
            model=deployment,  # Use deployment name, not model name
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=200
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:  # Check if there are any tool calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)


                if function_name == "geography":
                    function_response = geography(user_input=function_args["user_input"])
                elif function_name == "history":
                    function_response = history(user_input=function_args["user_input"])
                else:
                    function_response = "Error: Unknown function"

                messages.append(response_message)  # Append the assistant message
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # Append the tool response


            # Get a new response from the model to incorporate the tool results

            second_response = client.chat.completions.create(
                model=deployment,
                messages=messages,
            )
            print("Chatbot:", second_response.choices[0].message.content.strip())

        else:
            print("Chatbot:", response_message.content.strip())  # Print the direct response if no tool call

    except Exception as e:

        print("Chatbot: Sorry, something went wrong.", str(e))
