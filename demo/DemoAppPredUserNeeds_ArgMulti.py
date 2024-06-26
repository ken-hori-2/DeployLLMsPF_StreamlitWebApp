from openai import OpenAI
import streamlit as st
import streamlit_antd_components as sac
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# i = 0

def chat():
    i = 0

    st.title("ChatGPT by Streamlit (Prediction User Needs Arg Multi)")
    st.write("**it is a simple chatbot made only with OpenAI and Streamlit. You can set system prompts, model, and temperature as options.**")
    # client = OpenAI(api_key=st.session_state.openai_api_key)

    if "openai_model" not in st.session_state:
        # st.session_state["openai_model"] = "gpt-4-turbo-preview"
        # st.session_state["openai_model"] = "gpt-4o"
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "Clear" not in st.session_state:
        st.session_state.Clear = False
   
    if "temperature" not in st.session_state:
        # st.session_state.temperature = 0.7
        st.session_state.temperature = 0.0
    

    # 2024/05/23
    pre_template = "You are an AI chatbot having a conversation with a human."
    # """あなたは人間と話すチャットボットです。ユーザーの要求に答えてください。"""
    
    
    # Todo
    """ 2024/05/24 Next Todo (事前にどの情報が来るか教える)"""
    """ 入力される情報は、時間と行動状態です。(例：time:10:00, Action:)"""

    

    # 2024/05/23
    
    if "system_prompt" not in st.session_state:
        # st.session_state.system_prompt = "You are an AI chatbot having a conversation with a human."
        st.session_state.system_prompt = pre_template

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role":"system", 
                "content":st.session_state.system_prompt
            }
        ]

    with st.expander("Options"):
        # st.selectbox("Model", ("gpt-4-turbo-preview", "gpt-3.5-turbo"), help="Choose the AI model to use. 'gpt-4-turbo-preview' is the latest model with more advanced capabilities, while 'gpt-3.5-turbo' is an older but still powerful version.", key="openai_model")
        st.selectbox(
            "Model", 
            ("gpt-4o", "gpt-3.5-turbo"), 
            help="Choose the AI model to use. 'gpt-4o' is the latest model with more advanced capabilities, while 'gpt-3.5-turbo' is an older but still powerful version.", 
            key="openai_model"
            )
        st.text_area(
            "System Prompt", 
            #  value="You are an AI chatbot having a conversation with a human.", 
            value=pre_template, 
            help="Can only be set at the time of the first message sent.Set the initial prompt for the AI system which sets the context of the conversation. This can influence how the AI responds.", 
            key="system_prompt"
            )
        st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            help="Adjust the creativity of the AI's responses. A lower temperature means more deterministic and predictable responses, while a higher temperature results in more varied and sometimes more creative responses.", 
            key="temperature"
            )

    for message in st.session_state.messages:
        if not message["role"]=="system":
            if message["role"]=="user":
                with st.chat_message(message["role"], avatar = "😊"):
                    st.markdown(message["content"])
            elif message["role"]=="assistant":
                with st.chat_message(message["role"], avatar = "🤖"):
                    st.markdown(message["content"])

    # UI画面で入力 (promptに値が格納されていたらTrue)
    # if prompt := st.chat_input("What is your state of action?"): # "What is up?"): # これまでのやり方
    # ここにスマホ側からデータを受信したらpromptに書き込めばいい？ # if prompt := スマホのデータ
    prompt = "12:00 WALKING" # おそらく、WEB上のAPPにアクセスがあると(GET?)、chat()が実行されている？
    if prompt:
    # テスト
        st.write("test:", i)
        i+=1
    
        if st.session_state.openai_api_key == "":
            sac.alert(
                label='warning', 
                description='Please add your OpenAI API key to continue.', 
                color='red', 
                banner=[False, True], 
                icon=True, 
                size='lg'
            )
            st.stop()
        

        
        
        llm = ChatOpenAI(temperature=st.session_state.temperature, streaming=True, model=st.session_state["openai_model"], openai_api_key=st.session_state.openai_api_key)
        prompt_PreInput = PromptTemplate(
            # input_variables=["UserAction"],
            input_variables=["time", "UserAction"],
            # template="{job}に一番オススメのプログラミング言語は何?"
            # その後、現在が{time}、ユーザーの行動状態が{UserAction}の場合どの機能を提案するか教えてください。
            # template="""
            #     以下はユーザーの1日の行動と使った機能です。
            #     このユーザーの傾向を述べてください。(例: 1. 時間帯ごとの行動パターン: , 2. 行動状態: )
            #     その後、現在が11時30分、ユーザーの行動状態が{UserAction}の場合どの機能を提案するか教えてください。
            #     その際、各機能の提案する確率と最終的な提案(Final Answer:)も教えてください。

            #     7:30, STABLE, 天気情報
            #     8:00, WALKING, 経路検索
            #     8:30, STABLE, 楽曲再生
            #     9:00, STABLE, 会議情報
            #     11:00, WALKING, 会議情報
            #     12:00, STABLE, レストラン検索
            #     12:30, STABLE, 楽曲再生
            #     15:00, WALKING, 会議情報
            #     17:30, STABLE, 経路検索
            #     18:00, STABLE, 楽曲再生
            #     19:00, RUNNING, 楽曲再生
            #     19:30, RUNNING, 楽曲再生

            #     あなたが提案できる機能は
            #     "会議情報", "楽曲再生", "経路検索", "リアルタイム情報検索", "レストラン検索", "ニュース情報", "天気情報"
            #     です。
            #     """
            # template="""
            #     現在時刻が11時30分、ユーザーの行動状態が{UserAction}の場合以下のうちのどの機能を提案するか教えてください。
            #     あなたが提案できる機能は、「"会議情報", "楽曲再生", "経路検索", "リアルタイム情報検索", "レストラン検索", "ニュース情報", "天気情報"」です。
            #     各機能の提案する確率と最終的な提案(Final Answer:)も教えてください。
            #     """
            template="""
                現在時刻が{time}、ユーザーの行動状態が{UserAction}の場合、あなたが持つ機能のうち、どの機能を提案するか教えて。
                あなたが提案できる機能は、
                "会議情報", "楽曲再生", "経路検索", "リアルタイム情報検索", "レストラン検索", "ニュース情報", "天気情報"
                です。
                各機能の提案する確率と最終的な提案(Final Answer:)、選択した理由も教えなければならない。
                """
            # template="""
            #     以下はユーザーのある1日の行動と使った機能です。
            #     このユーザーの傾向を述べて。(例: 1. 時間帯ごとの行動パターン: , 2. 行動状態: )
            #     その後、現在が{time}、ユーザーの行動状態が{UserAction}の場合どの機能を提案するか教えて。
            #     各機能の提案する確率と最終的な提案(Final Answer:)も教えて。
            #     -----
            #     7:30, STABLE, 天気情報
            #     8:00, WALKING, 経路検索
            #     8:30, STABLE, 楽曲再生
            #     9:00, STABLE, 会議情報
            #     11:00, WALKING, 会議情報
            #     12:00, STABLE, レストラン検索
            #     12:30, STABLE, 楽曲再生
            #     15:00, WALKING, 会議情報
            #     17:30, STABLE, 経路検索
            #     18:00, STABLE, 楽曲再生
            #     19:00, RUNNING, 楽曲再生
            #     19:30, RUNNING, 楽曲再生
            #     -----
            #     あなたが提案できる機能は
            #     "会議情報", "楽曲再生", "経路検索", "リアルタイム情報検索", "レストラン検索", "ニュース情報", "天気情報"
            #     です。
            #     """
        )
        chain = LLMChain(llm=llm, prompt=prompt_PreInput, output_key="response")
        # print(chain("データサイエンティスト"))

        

        st.session_state.messages.append(
            {
                "role": "user", 
                "content": prompt
            }
        )
        with st.chat_message("user", avatar = "😊"):
            st.markdown(prompt)

        # with st.chat_message("assistant" , avatar = "🤖"):
        #     message_placeholder = st.empty()
        #     full_response = ""

        #     stream = client.chat.completions.create(
        #         model=st.session_state["openai_model"],
        #         messages=[
        #             {
        #                 "role": m["role"], 
        #                 "content": m["content"]
        #             }

        #             for m in st.session_state.messages
        #         ],
        #         stream=True,
        #     )

        #     for chunk in stream:
        #         if chunk.choices[0].delta.content is not None:
        #             full_response += chunk.choices[0].delta.content
        #         message_placeholder.markdown(full_response + "▌")
        #     message_placeholder.markdown(full_response)
        # st.session_state.messages.append(
        #     {
        #         "role": "assistant", 
        #         "content": full_response
        #     }
        # )
        # st.session_state.Clear = True

        
        # テスト
        # prompt = "11:30" + " " + "WALKING"
        # a,b=prompt.split()
        InputTime, InputUserAction = prompt.split()
        with st.chat_message("assistant" , avatar = "👩‍🎓"):
            # st_callback = StreamlitCallbackHandler(st.container())
            # cfg = RunnableConfig()
            # cfg["callbacks"] = [st_callback]
            # response = agent.invoke(user_prompt, cfg)
            
            
            # response = chain(prompt)
            from langchain.chains import SequentialChain
            overall_chain = SequentialChain(
                chains=[chain],
                input_variables=["time", "UserAction"],
                output_variables=["response"], # あくまで辞書型のなんていう要素に出力が格納されるかの変数
                verbose=True,
            )

            response = overall_chain({
                # "time" : "11時30分",
                # "time" : "12時05分",
                "time" : InputTime,
                # "UserAction" : "STABLE",
                "UserAction" : InputUserAction,
                # "UserAction" : "RUNNING",
            })
            response = response["response"]
            st.write(response)

        
        
        # 会話履歴を残さない場合はコメントアウト
        # これは画面上の履歴かも
        # st.session_state.messages.append(
        #     {
        #         "role": "assistant", 
        #         "content": response
        #     }
        # )

        
        st.session_state.Clear = True

    if st.session_state.Clear:
        if st.button('clear chat history'):
            st.session_state.messages = []
            full_response = ""
            st.session_state.Clear = False 
            st.rerun()

if __name__ == "__main__":
    if not hasattr(st.session_state, "openai_api_key"):
        try:
            st.session_state.openai_api_key = os.environ["OPENAI_API_KEY"]
        except:
            st.session_state.openai_api_key = ""
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        if not openai_api_key == "":
            st.session_state.openai_api_key = openai_api_key
        st.write("if you are running the app locally,  \nthere is no need to enter the key  \nif it is already set as an environment variable.")
    chat()