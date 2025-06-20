from datetime import datetime
from ..processing.json_io import write_to_json
import logging
logger = logging.getLogger(__name__)

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

def create_multi_turn_prompt(transcript, data_dir):
    try:
        logger.info("creating prompt")
        details = {}
        
        details["transcript"] = transcript
        
        context = '''
        The previous message is a transcript of a meeting together with the identified speech emotions.
        You are to evaluate the team communication using the meeting transcript and the speech emotions.
        Do not give me a summary of the meeting. Evaluate the meeting based on the CLEAR model below.
        
        CLEAR Model
        C stands for Curious, Caring & Open-Minded
        Evaluation of 'C' are when team members
        - Ask open-ended questions
        - Show empathy
        - Not defensive
        - Withhold their judgement
        - If others on the team make a mistake, it is not held against them
        - If it is not difficult to ask other members of this team for help
        - If no one on this team show that they would deliberately act in a way that undermines their team member's efforts
        
        L stands for Listen To One Another
        Evaluation of 'L' are when team members
        - Pay attention to what other team members are saying
        - Avoid distractions or distracting others

        E stands for Encourage Everyone To Contribute
        Evaluation of 'E' are when team members
        - Are able to bring up problems and tough issues
        - Do not reject others for being different
        - Feel safe to take a risk on this team
        - Value and utilize other team member's unique skills and talents

        A stands for Avoid Dominating or Interrupting.
        Evaluation of 'A' are when team members
        - Have self-awareness and allow others to speak
        - Not interrupt others

        R stands for Repeat & Review People’s Points.
        Evaluation of 'R' are when team members
        - Paraphrase team member's sentences
        - Request clarification when in doubt
        
        Can you provide a score from 0 to 1 for each of the 5 areas. 
        Evaluate based on criterias that are present in the transcript and evaluate based on the whole team. Do not single out individual team members.
        0 signifies that little apitude is shown while 1 signifies exemplary performance. 
        Give a brief explanation of your score.
        At the end, can you provide areas that the team did well in.
        Then, provide 3 recommendations for improvements using the evaluation criteria.
        Could you include the final scores at the end of the response in a json block like 
        ```json
        {
            "C": ,
            "L": ,
            "E": ,
            "A": ,
            "R": 
            }
        ```
        '''
        
        json_prompt = {
            "context": context,
            "meeting details": details
        }
        
        content_file_prefix = data_dir + "/json_prompt_" + timestamp
        write_to_json(json_prompt, content_file_prefix)
        
        return transcript, context
        
    except Exception as e:
        logger.error(f"error creating prompt: {e}")
        raise