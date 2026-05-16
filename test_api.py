import asyncio
from app import chat, ChatRequest, Message

async def main():
    print("Test 1")
    req1 = ChatRequest(messages=[
        Message(role="user", content="I am looking for an assessment")
    ])
    res1 = await chat(req1)
    print(res1.model_dump())

    print("\nTest 2")
    req2 = ChatRequest(messages=[
        Message(role="user", content="I am looking for an assessment"),
        Message(role="assistant", content="What seniority do you need?"),
        Message(role="user", content="mid-level Java developer")
    ])
    res2 = await chat(req2)
    print(res2.model_dump())

if __name__ == "__main__":
    asyncio.run(main())
