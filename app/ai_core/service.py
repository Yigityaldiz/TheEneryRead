import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.ai_core.tools import TOOLS_SCHEMA, get_machine_status, get_alerts_tool

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def process_chat_message(user_message: str):
    messages = [
        {"role": "system", "content": "You are an AI Energy Assistant. You help factory managers monitor their energy consumption and anomalies. Use the available tools to answer questions accurately. If you don't know the answer, say so."},
        {"role": "user", "content": user_message}
    ]

    # 1. First Call to LLM
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 2. Check if tool call is needed
    if tool_calls:
        messages.append(response_message)  # extend conversation with assistant's reply

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Executing tool: {function_name} with args: {function_args}")

            function_response = None
            if function_name == "get_machine_status":
                function_response = await get_machine_status(
                    machine_name=function_args.get("machine_name")
                )
            elif function_name == "get_alerts_tool":
                function_response = await get_alerts_tool()
            
            # Add function response to messages
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        # 3. Second Call to LLM (with tool outputs)
        second_response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return second_response.choices[0].message.content

    return response_message.content
