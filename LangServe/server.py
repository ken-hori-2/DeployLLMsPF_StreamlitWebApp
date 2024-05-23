from fastapi import FastAPI
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langserve import add_routes

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="LangchainのRunnableインターフェースを使ったシンプルなAPIサーバー",
)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)
# add_routes(
#     app,
#     ChatAnthropic(),
#     path="/anthropic",
# )

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run(app, host="localhost", port=8000)

    # app.run(host='0.0.0.0', port=80) # 888) # 0)
    uvicorn.run(app, host="0.0.0.0", port=8000)