from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv() #env 파일에서 api_key를 가져옴
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def word_chatbot(difficulty): #단어 chatbot

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a machine that give random english word with korean."
            },
            {
                "role": "user",
                "content": f"give me 10 english words with korean that difficulty is {difficulty}."
                           f"you give me in the form 'number. korean english'"
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=1024,  # chat 에서 생성해낼 수 있는 최대 tokens 수
        stop=None,  # 대화의 종류를 명시, None -> 종료 조건 x
        temperature=1.5,  # 0~2사이의 값, 높을 수록 더 랜덤한 response 발생, 낮을 수록 보다 정확한 정보 제공
    )

    return response.choices[0].message.content