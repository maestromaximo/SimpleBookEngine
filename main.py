import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openai.api_key = 'your-api-key'
client = openai.Client()


def run_function(function_name, arguments):
    # Dummy function to simulate running a function based on the name and arguments
    # In reality, this function should run the actual business logic or API call.
    # This is just a placeholder for demonstration purposes.
    pass  # Replace or expand this with actual code to run your functions.

def query_openai_with_tools(query, context=None, model="gpt-3.5-turbo", force_tool=None, tools_list=[]):
    """
    Send a query to OpenAI's API with optional function calls using the updated client object.

    :param query: The user's query or message.
    :param context: List of previous messages in the conversation for context.
    :param force_tool: Optionally force a specific tool call.
    :param tools_list: List of tool schemas to be used by the API.
    :return: The response from the OpenAI API and the new context.
    """
    # Preparing the messages for the API call
    if context is None:
        context = [{"role": "system", "content": "You are a helpful assistant."}]
    messages = context + [{"role": "user", "content": query}]
    
    # Calling the API using the client object
    response = client.chat.completions.create(
        model=model,  # Change this to the model you intend to use
        messages=messages,
        tools=tools_list,
        tool_choice=force_tool or "auto",  # Default is 'auto', but can be overridden
    )
    
    # Extracting and handling tool calls if they exist
    response_message = response.choices[0].message
    new_context = context + [response_message]  # Update context with the assistant's reply
    if response_message.get('tool_calls'):
        # Process each tool call
        for tool_call in response_message['tool_calls']:
            function_name = tool_call['function']['name']
            function_args = json.loads(tool_call['function']['arguments'])
            
            # Run the specified function and get the response
            function_response = run_function(function_name, function_args)
            
            # Append the function response to the new context
            new_context.append({
                "tool_call_id": tool_call['id'],
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
        
        # Make another API call to continue the conversation with the updated context
        second_response = client.chat.completions.create(
            model=model,  # Change as needed
            messages=new_context,
            tool_choice="none",  # This time we don't want to initiate new tool calls
        )
        final_response = second_response.choices[0].message
        new_context += [final_response]  # Update the context with the final response
    else:
        # If no tool calls, use the first response as the final response
        final_response = response_message
    
    return final_response, new_context

response = query_openai_with_tools("Hello, how are you?")  # Example usage without context
print(response)