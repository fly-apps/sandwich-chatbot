import os
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from ollama import AsyncClient


OLLAMA_HOST = os.getenv('OLLAMA_HOST')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')
ollama_client = AsyncClient(host=OLLAMA_HOST)

SYSTEM_MSG = """
    You are a helpful chatbot.
    You will get questions about sandwiches.
    You must answer the questions in a friendly manner.
    Your answer must inspire users to buy more sandwiches. 
"""

MESSAGE_STORE = {}

class UserMessage(BaseModel):
    session_id: str
    query: str


async def do_ai_stuff(messages, session_id):

    stream = await ollama_client.chat(
        model="llama3.1", 
        messages=messages,
        stream=True
        )
    sys_response = ""
    async for chunk in stream:
        sys_response += chunk['message']['content']
        yield chunk['message']['content']
    messages.append({'role': 'system', 'content': sys_response})
    MESSAGE_STORE[session_id] = messages


app = FastAPI()

@app.post("/sandwich-chat", response_class=StreamingResponse)
async def sandwich_chatbot(msg: UserMessage):
    messages = MESSAGE_STORE.get(msg.session_id, [
        {'role': 'system', 'content': SYSTEM_MSG}
    ])
    messages.append({'role': 'user', 'content': msg.query})
    MESSAGE_STORE[msg.session_id] = messages
    return StreamingResponse(do_ai_stuff(messages, msg.session_id), media_type="text/html")

