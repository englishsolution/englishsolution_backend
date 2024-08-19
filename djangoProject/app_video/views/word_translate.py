from dotenv import load_dotenv
from openai import OpenAI
import os,json


load_dotenv() #env 파일에서 api_key를 가져옴
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def word_translate(word):

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a great word translater. If suggest a english word, then you translate to korean and say it's type like '명사'."
            },
            {
                "role": "user",
                "content": f"Translate: {word}."
                           f"If word is apple, For example: {{\"word\": \"apple\" , \"korean\":\"사과\", \"type\":\"명사\"}}"
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=1024,  # chat 에서 생성해낼 수 있는 최대 tokens 수
        stop=None,  # 대화의 종류를 명시, None -> 종료 조건 x
        temperature=0.1,  # 0~2사이의 값, 높을 수록 더 랜덤한 response 발생, 낮을 수록 보다 정확한 정보 제공
    )

    # 응답에서 결과 추출
    result = response.choices[0].message.content

    try:
        result_dict = json.loads(result)

        # 딕셔너리에서 값 추출
        word = result_dict.get('word')
        korean = result_dict.get('korean')
        word_type = result_dict.get('type')

        print(f"Word: {word}, Korean: {korean}, Type: {word_type}")

    except json.JSONDecodeError:
        print("Result is not a valid JSON format.")
    except KeyError as e:
        print(f"Missing key in the result: {e}")


    return word,korean,word_type
