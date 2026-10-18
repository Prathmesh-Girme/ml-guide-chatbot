
from ollama import chat

messages = [
    {
        "role": "system",
        "content": "You are ML Guide, a friendly Machine Learning teacher. Explain ML concepts simply with examples."
    }
]

print("ML Guide")
print("Your Machine Learning Assistant")
print("Type 'exit' to stop")

while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("Thank you for using ML Guide!")
        break

    if not question:
        continue

    messages.append({
        "role": "user",
        "content": question
    })

    response = chat(
        model="llama3.2:1b",
        messages=messages
    )

    answer = response.message.content

    print("\nML Guide:", answer)

    messages.append({
        "role": "assistant",
        "content": answer
    })
