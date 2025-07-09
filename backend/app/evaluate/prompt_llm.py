from openai import OpenAI
import json
import logging
logger = logging.getLogger(__name__)
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")


now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")


def evaluate_communication_with_prompt(json_prompt, folder_name, model):
    try:
        if "deepseek" in model:
            if not openrouter_api_key:
                raise EnvironmentError("Set OPENROUTER_API_KEY in environment variables.")
            logger.info("Using Deepseek API")
            completion = use_deepseek(json_prompt)
        elif model == "gpt-4.1-nano":
            if not openai_api_key:
                raise EnvironmentError("Set OPENAI_API_KEY in environment variables.")
            logger.info("Using OPENAI API")
            completion = use_openai(json_prompt, "gpt-4.1-nano")
        else:
            logger.info("Model not found")
            return
        
        answer_file_prefix = folder_name + "/evaluate_communication_" + model
        answer_text = completion.choices[0].message.content
        write_to_md(answer_text, answer_file_prefix)
        logger.info(completion)
        return answer_text

    except Exception as e:
        logger.error(f"error: {e}")
        raise

def write_to_md(markdown_content, file_prefix):
    output_path = file_prefix + ".md"
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    return output_path


def use_deepseek(json_prompt):
    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key,
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