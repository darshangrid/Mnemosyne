import json

from flask import jsonify

from service.MongoService import MongoService
from service.MnemsoyneService import MnemsoyneService
from config import Config
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).absolute().parents[2].absolute()
sys.path.insert(0, str(PROJECT_ROOT))
#print(PROJECT_ROOT)
#from gpt4free.g4f.client import Client

def main():
    mongo_service = MongoService(Config())
    ms = MnemsoyneService(Config())
    # mongo_service.insert_data("https://akshaybahadur.medium.com/gymlytics-519caa05f045")
    # mongo_service.retrieve_data("Personalization?")
    knowledge_obj_generator = ms.retrieve_knowlede("Who is Akshay Bahadur, explain his life at CMU")
    for response in knowledge_obj_generator:
    # Here `response` will be either partial streamed answers or the final JSON.
        try:
            # Try to load the response as JSON (final result)
            result_json = json.loads(json.dumps(response))
            print("Final JSON Response:", result_json)
        except json.JSONDecodeError:
            # If it's not valid JSON yet, it's part of the streamed answer
            print("Streamed Answer:", response)
        # print(chunk)
        # if chunk == "STREAM_START\n":
        #     # Start of answer stream
        #     pass
        # elif chunk == "\nSTREAM_END\n":
        #     # End of answer stream, full JSON coming next
        #     pass
        # elif chunk.startswith("{"):
        #     # This is the full JSON
        #     full_response = json.loads(chunk)
        #     print(full_response)
        #     # Process the full response
        # else:
        #     # This is a chunk of the streamed answer
        #     print(chunk, end='|',flush=True)


if __name__ == "__main__":
    main()