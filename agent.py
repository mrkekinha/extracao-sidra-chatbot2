from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from tools.sidra_tool import consultar_sidra
from tools.scraping_tool import buscar_info_web
import os
from dotenv import load_dotenv
from langchain.tools import Tool

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0, model_name="llama3-8b-8192", api_key=groq_api_key)
memory = ConversationBufferMemory(memory_key="chat_history")

tools = [
    Tool(
        name="consultar_sidra",
        func=consultar_sidra,
        description=(
            "Use esta ferramenta para consultar dados do IBGE no SIDRA. "
            "Ela responde perguntas como 'qual o PIB do meu município?', 'população de Timóteo', "
            "'produção de leite em MG', ou sempre que o usuário fornecer 'tabela=xxxx; nivel=municipal'."
        ),
        return_direct=True
    ),
    Tool(
        name="Busca Web",
        func=buscar_info_web,
        description="Use para buscar dados no site do IBGE se a SIDRA não responder."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True
)