#!/usr/bin/env python

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware # add

# from langchain_community.chat_models import BedrockChat 
from langchain.chat_models import ChatOpenAI

from langserve import add_routes

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="LangServe",
    version="1.0",
    description="LangChain Server",
)

# add
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add_routes(
#     app,
#     BedrockChat(model_id="anthropic.claude-instant-v1"),
#     path="/bedrock",
# )
add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
