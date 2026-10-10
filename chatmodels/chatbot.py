from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AImessage, SystemMessage , HumanMessage

model = ChatMistralAI(model = "mistral-small-2506",temperature=0.9)

print("choose your AI mode")
print("press 1 for Angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice = int(input("tell your respose :- "))


if choice == 1:
  mode = "You are an angry AI agent. You respond aggresively and impatiently"

elif choice == 2 :
  mode = "You are an angry AI agent. You respond with humor and jokes"

elif choice == 3:
  mode = " You are an angry AI agent. You respond aggresively and impatiently"

messages  = [
    SystemMessage(content = mode)
]

print("-------------Welcome type 0 to exit the application------------------")

while True:

  prompt = input("You : ")
  messages.append(HumanMessage(content = prompt))
  if prompt == "0":
    break
  response = model.invoke(prompt)
  messages.append(AImessage(content = response.content))
  print("Bot :  ",response.content)

print(messages)