from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
API_EKY = os.getenv('GROQ_API_KEY')


async def qa_system(context, user_context, question):

    client = Groq(
        api_key=API_EKY)
    
    response = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {
              "role": "system",
              "content": context
            },
            {
                "role": "user",
                "content": user_context + question
            }
        ],
        temperature=0.1,
        max_tokens=512,
        top_p=1,
        stream=False,
        stop=None,
    )

    print(f'\n{response.choices[0].message.content}')
    return f'\n{response.choices[0].message.content}'


async def run_qa_system(context, user_context, question):
    response = await qa_system(context, user_context, question)
    return response


