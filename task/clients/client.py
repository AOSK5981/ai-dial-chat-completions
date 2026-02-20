from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT, API_KEY
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        #TODO:
        # Documentation: https://pypi.org/project/aidial-client/ (here you can find how to create and use these clients)
        # 1. Create Dial client

        self.client = Dial(
            base_url=DIAL_ENDPOINT,
            api_key=API_KEY,
            timeout=60.0
        )
        # 2. Create AsyncDial client
        self.async_client = AsyncDial(
            base_url=DIAL_ENDPOINT,
            api_key=API_KEY,
            timeout=60.0
        )

    def get_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with client
        #    Hint: to unpack messages you can use the `to_dict()` method from Message object
        # 2. Get content from response, print it and return message with assistant role and content
        # 3. If choices are not present then raise Exception("No choices in response found")

        payload_messages = [m.to_dict() for m in messages]

        response = self.client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=payload_messages,
            stream=False
        )

        if not response.choices:
            raise Exception("No choices in response found")

        content = response.choices[0].message.content

        return Message(
            role=Role.ASSISTANT,
            content=content
        )
        

    async def stream_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with async client
        #    Hint: don't forget to add `stream=True` in call.
        # 2. Create array with `contents` name (here we will collect all content chunks)
        # 3. Make async loop from `chunks` (from 1st step)
        # 4. Print content chunk and collect it contents array
        # 5. Print empty row `print()` (it will represent the end of streaming and in console we will print input from a new line)
        # 6. Return Message with assistant role and message collected content

        payload_messages = [m.to_dict() for m in messages]

        stream = await self.async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=payload_messages,
            stream=True
        )

        contents: list[str] = []

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta and delta.content:
                contents.append(delta.content)

        print()

        if not contents:
            raise Exception("No content received during streaming")

        return Message(
            role=Role.ASSISTANT,
            content="".join(contents)
        )