import ollama

while True:
    user = input("\nYou: ")

    if user.lower() == "quit":
        print("Daemon: Shutting down.")
        break

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": """
                You are Daemon, my personal AI assistant.
                You run locally on my Omarchy computer.
                You are helpful, intelligent, and concise.
                """
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )

    print("\nDaemon:", response["message"]["content"])
