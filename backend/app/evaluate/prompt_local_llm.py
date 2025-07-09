from ollama import chat
import json
import logging
logger = logging.getLogger(__name__)
    
def evaluate_communication_with_prompt_os(transcript, context, folder_name, model):
    try:
        
        message = "<start_of_turn>user" + json.dumps(transcript) + context + "<end_of_turn>"
        print(message)

        response = chat(
            model=model,
            messages=[{"role": "user", "content": message}],
            options={'temperature': 1.3}
        )

        logger.info("\n=== GEMMA'S RESPONSE ===\n")
        logger.info(response.message.content)
        
        answer_file_prefix = folder_name + "/evaluate_communication_" + model
        answer_text = response.message.content
        write_to_md(answer_text, answer_file_prefix)
        return answer_text

    except Exception as e:
        logger.error(f"error: {e}")
        raise
    

def write_to_md(markdown_content, file_prefix):
    output_path = file_prefix + ".md"
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    return output_path