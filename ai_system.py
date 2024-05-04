from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
API_EKY = os.getenv('GROQ_API_KEY')


async def qa_system(context, question):

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
                "content": 'Ответь на следующий вопрос, используя только информацию из предоставленного контекста.' 
                + 'Если ты не можешь найти ответ на вопрос в заданной области, напиши в ответ:' 
                + '"Вопрос не соответствует контексту". Вопрос:' + question
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


async def run_qa_system(context, question):
    response = await qa_system(context, question)
    return response
