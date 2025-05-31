from openai import OpenAI
import json
import logging
logger = logging.getLogger(__name__)
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")


def evaluate_communication_with_prompt(json_prompt, folder_name):
    try:
        completion = use_openai(json_prompt, "gpt-4.1-nano")
        # completion = use_deepseek(json_prompt)
        
        answer_file_prefix = folder_name + "/evaluate_communication"
        answer_text = completion.choices[0].message.content
        write_to_md(answer_text, answer_file_prefix)
        print(completion)
        return answer_text

    except Exception as e:
        logger.error(f"error: {e}")

def write_to_md(markdown_content, file_prefix):
    output_path = file_prefix + ".md"
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    return output_path


def use_deepseek(json_prompt):
    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat:free",
        messages=[
            {"role": "system", "content": json.dumps(json_prompt)},
        ],
        temperature= 1.3,
    )
    return completion

def use_openai(json_prompt, model = "gpt-4.1-nano"):
    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
    model=model,
        messages=[
            {"role": "system", "content": json.dumps(json_prompt)},
        ],
        temperature= 1.3,
    )
    return completion