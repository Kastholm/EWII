from dash import Dash, html, dcc, Input, Output
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from database.queries import fetch_customer_data

load_dotenv()
has_gpt = bool(os.getenv("GPT_KEY"))
# F:\Development\Exams\EWII\components
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
# F:\Development\Exams\EWII
BASE_DIR = os.path.dirname(CURR_DIR)
# F:\Development\Exams\EWII/chat/chat_log.json
json_file_path = os.path.join(BASE_DIR, 'chat', 'chat_log.json')


with open(json_file_path,'r', encoding='utf-8') as file:
    data = json.load(file)
chat_messages = data["chat"]


data = fetch_customer_data()

# function to add to JSON
def write_json(new_data):
    with open(json_file_path,'r+', encoding='utf-8') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["chat"].append(new_data)

        # Sets file's current position at offset.
        file.seek(0)

        json.dump(file_data, file, ensure_ascii=False, indent = 4)

full_instructions = (
    f"{data}\n\n"
    "Du er EWII’s Dataanalyse-assistent. Forestil dig, at du forklarer resultaterne for en kollega, "
    "der ikke er dataekspert. Skriv i et klart og enkelt sprog:\n"
    "- Giv et kort svar på selve spørgsmålet (fx “46,7 % af kunderne skiftede abonnement”).\n"
    "- Tilføj én kort sætning om, hvad det betyder for forretningen.\n"
    "- Hvis relevant, foreslå ét enkelt diagram (fx “en cirkel- eller søjlediagram”).\n"
    "\nEksempel på svar:\n"
    "“46,7 % af kunderne har skiftet abonnement fra 2024 til 2025. "
    "Det tyder på, at næsten halvdelen af kunderne ser efter nye løsninger, "
    "så vi bør overveje at målrette retention-tilbud. "
    f"Du kan se en historik over den chat log der allerede er foregået her så du lettere kan svare på nye spørgsmål {chat_messages}"
)

no_key_response = {
    "API key til ChatGPT er fjernet, for at forhindre misbrug online. Du kan tilføje din eget GPT key i en .env fil med variabel 'GPT_KEY' "
}

class Chat():

    def __init__(self):
        load_dotenv()
        self.gpt_key = os.getenv("GPT_KEY")
        if self.gpt_key:
            self.client = OpenAI(
                api_key=self.gpt_key,
            )
        else:
            write_json({"answer": f"🤖 {no_key_response}"})

    def send_prompt(self, prompt):
        if self.client:
            try:
                response = self.client.responses.create(
                    model="gpt-4o",
                    instructions = full_instructions,
                    input=prompt,
                )
                write_json({"question": f"🧑‍🦲 {prompt}"})
                answer = response.output[0].content[0].text
                write_json({"answer": f"🤖 {answer}"})

                return answer
            except Exception as e:
                print(f"Error: {e}")
        else:
            write_json({"error": "🚫Error"})
            print("No client available")

chatbot_assistant = html.Div(
    className=(
        "w-[500px] bg-white fixed bottom-4 z-50 right-4 dark:bg-zinc-800 "
        "shadow-xl rounded-lg overflow-hidden"
    ),
    children=[
        html.Div(
            className="flex flex-col",
            children=[
                # Header
                html.Div(
                    className="px-4 bg-[#7bb93d] bg-opacity-50 py-3 border-b dark:border-zinc-700",
                    children=html.Div(
                        className="flex justify-between items-center",
                        children=[
                            html.Img(
                                src="https://w7.pngwing.com/pngs/1003/600/png-transparent-ewii-fuel-cells-kif-kolding-k%C3%B8benhavn-car-electric-vehicle-car-angle-text-trademark.png",
                                className="h-8 w-auto mb-6 mr-auto ml-4 "
                            ),
                            html.Div(
                                "❌",
                                id="close-chat",
                                className="text-white cursor-pointer  text-md px-2 py-1 rounded-full"
                            )
                        ]
                    )
                ),
                # Chat display area
                html.Div(
                    id="chatDisplay",
                    className="flex-1 p-3 h-[500px] max-h-[500px] overflow-y-scroll bg-gradient-to-r from-[#c2e1bd] to-[#e0f5d6] overflow-y-auto flex flex-col space-y-2",
                ),
                # Input area
                html.Div(
                    className="px-3 py-2 border-t bg-[#7bb93d] bg-opacity-50 dark:border-zinc-700",
                    children=html.Div(
                        className="flex gap-2",
                        children=[
                            dcc.Input(
                                id="chatInput",
                                type="text",
                                placeholder="Skriv din besked…",
                                className="flex-grow p-2 border rounded-lg dark:bg-zinc-700 dark:text-white dark:border-zinc-600 text-sm"
                            ),
                            *([  
                                html.Button(
                                    "Send",
                                    id="sendButton",
                                    className=(
                                        "bg-blue-500 hover:bg-blue-700 text-white font-bold "
                                        "py-1.5 px-3 rounded-lg transition duration-300 ease-in-out text-sm"
                                    )
                                )
                            ] if has_gpt else [])
                        ]
                    )
                )
            ]
        )
    ]
)