from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.agents import (
    load_tools,
    create_openai_tools_agent,
    AgentExecutor
)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    k=3,
    return_messages=True
)

# template = """你是一個友善的學習助理，你接下來會跟使用者來對話。
# {tools}

# User: {input}
# {agent_scratchpad}"""

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            """
            你是一個友善的學習助理，你接下來會透過中文跟使用者來對話，並使用工具解決問題。
            """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template(
            """
            使用者: {input}
            {agent_scratchpad}
            """
        )
    ]
)

agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, 
    tools=tools, 
    memory=memory, 
    handle_parsing_errors=True, 
    verbose=True
)

def generate_reply(input_text: str):
    response = agent_executor.invoke({
        "input": input_text
    })

    print(response.get("output"))

    return response.get("output")
