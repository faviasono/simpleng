import os
from os.path import join, dirname
import google.generativeai as genai
from dotenv import load_dotenv
from bookai.models.base_summarizer import SummarizerBaseModel
import json

# Load the environment variables
load_dotenv(join(dirname(__file__), "../", ".env"))

SYSTEM_INSTRUCTIONS = "Return the simplified version of the text provided as you need to help the reader understand complex sentences. Do not overcomplicate or change the content,meaning. Also, return the phrasal verbs with their meaning as well as the difficult words with their meaning"


class LLM:
    def __init__(self, model_name="gemini-2.0-flash-exp", temperature=0.1, top_p=0.95, top_k=40, max_output_tokens=8192):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # Create the model
        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": "application/json",
        }
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=SYSTEM_INSTRUCTIONS,
        )

    def analyze_text(self, text):
        chat_session = self.model.start_chat(history=[])
        try:
            response = chat_session.send_message(text)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    llm = LLM()
    text = "“Every fall into love involves the triumph of hope over self-knowledge. We fall in love hoping we won't find in another what we know is in ourselves, all the cowardice, weakness, laziness, dishonesty, compromise, and stupidity. We throw a cordon of love around the chosen one and decide that everything within it will somehow be free of our faults. We locate inside another a perfection that eludes us within ourselves, and through our union with the beloved hope to maintain (against the evidence of all self-knowledge) a precarious faith in our species.”"
    output = llm.analyze_text(text)
    print(output)
    print("Done!")
