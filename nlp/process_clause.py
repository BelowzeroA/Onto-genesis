from nlp.models.clause import *
from nlp.cleverise_api import *

clause = Clause("[чтобы] [отменить] [авторизованную заявку], нужно [следовать инструкции 1]")
api = CleveriseApi()
result = api.get_nlp_analysys(clause.source)

from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer'
)

# chatbot.train([
#     "Hi, can I help you?",
#     "Sure, I'd to book a flight to Iceland.",
#     "Your flight has been booked."
# ])

chatbot.train([
    "как отменить авторизованную заявку",
    "[чтобы] [отменить] [авторизованную заявку], нужно [следовать инструкции 1]",
    "Как отменить обычную заявку",
    "[чтобы] [отменить] [неавторизованную заявку], [пометьте ее на удаление]"
])

# Get a response to the input text 'How are you?'
response = chatbot.get_response('как мне отменить заявку')

print(response)