import asyncio
from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT, API_KEY, DEPLOYMENT_NAME
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:

    # 1.1 Create DialClient
    dial_client = DialClient(
        deployment_name=DEPLOYMENT_NAME,
    )

    # 1.2 Create CustomDialClient
    custom_client = CustomDialClient(
        deployment_name=DEPLOYMENT_NAME,
        api_key=API_KEY,
    )

    # 2. Create conversation
    conversation = Conversation()

    # 3. Get system prompt
    system_prompt = input(
        "Enter system prompt (press Enter to use default): "
    ).strip()

    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    conversation.add_message(
        Message(role=Role.SYSTEM, content=system_prompt)
    )

    print("\nType 'exit' to quit\n")

    # 4. Infinite loop
    while True:
        user_input = input("You: ").strip()

        # 5. Exit condition
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        # 6. Add user message
        conversation.add_message(
            Message(role=Role.USER, content=user_input)
        )

        # 7. Call client
        try:
            if stream:
                assistant_message = await dial_client.stream_completion(
                    conversation.messages
                )
            else:
                assistant_message = dial_client.get_completion(
                    conversation.messages
                )
        except Exception as e:
            print(f"\nError communicating with API: {str(e)}")
            print("Please check your network connection and API credentials.")
            print("Try again or type 'exit' to quit.\n")
            continue

        # 8. Add assistant message to history
        conversation.add_message(assistant_message)

        print("\nAssistant:", assistant_message.content)
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(start(True))



    
    #TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    # 1.2. Create CustomDialClient
    # 2. Create Conversation object
    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    # 4. Use infinite cycle (while True) and get yser message from console
    # 5. If user message is `exit` then stop the loop
    # 6. Add user message to conversation history (role 'user')
    # 7. If `stream` param is true -> call DialClient#stream_completion()
    #    else -> call DialClient#get_completion()
    # 8. Add generated message to history
    # 9. Test it with DialClient and CustomDialClient
    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response


# asyncio.run(
#     start(True)
# )
