from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv() #env 파일에서 api_key를 가져옴
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def sentence_analysis(sentence):

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a great sentence analyst. You'll tell me the important words, the grammar used."
            },
            {
                "role": "user",
                "content": f"Analyze the following sentence:\n\n{sentence}\n\nProvide the analysis in JSON format with 'main word' and 'grammar used' keys with korean. "
                           f"plus, You'll tell me the important words or idioms"
                           f"For example:{{\"word\": [\"word1\",\"Korean translation\", \"word2\",\"Korean translation\"], \"grammar\": [\"part of speech for word1\", \"part of speech for word2\"],\"idioms\":[\"word1\",\"Korean translation\" \"word2\"],\"Korean translation\"}}"
                           f"If the idiom doesn't exist, mark it as [\"NONE\"]"
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=1024,  # chat 에서 생성해낼 수 있는 최대 tokens 수
        stop=None,  # 대화의 종류를 명시, None -> 종료 조건 x
        temperature=0.3,  # 0~2사이의 값, 높을 수록 더 랜덤한 response 발생, 낮을 수록 보다 정확한 정보 제공
    )

    # 응답에서 결과 추출
    result = response.choices[0].message.content

    return result

