import warnings
warnings.filterwarnings("ignore")

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command":"python3",
                "args": ["maths.py"],
                "transport":"stdio"
            },
            "weather" : {
                "url":"http://127.0.0.1:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )

    tools = await client.get_tools()

    model = ChatGroq(model="openai/gpt-oss-120b")

    agent = create_agent(
        model=model,
        tools=tools
    )

    # res = await agent.ainvoke({
    #     "messages": [{"role":"user", "content":"what is (2 * 3) + 9"}]
    # })

    res = await agent.ainvoke({
        "messages": [{"role":"user", "content": "Fetch me the weather details of Washington"}]
    })

    print(res["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())