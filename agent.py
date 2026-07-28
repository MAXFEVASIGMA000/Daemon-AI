import json
import ollama
import tools


SYSTEM = """
You are Daemon, an autonomous local coding agent.

You have tools. Use them whenever the user wants you to interact
with the computer.

Available tools:

OPEN APP:
{
  "tool": "open_app",
  "args": {
    "app": "chromium"
  }
}

CREATE OR EDIT FILE:
{
  "tool": "write_file",
  "args": {
    "filename": "hello.py",
    "content": "print('hello')"
  }
}

READ FILE:
{
  "tool": "read_file",
  "args": {
    "filename": "hello.py"
  }
}

RUN COMMAND:
{
  "tool": "run_command",
  "args": {
    "command": "python hello.py"
  }
}


RULES:

- If the user wants a file created, edited, or deleted, use a tool.
- If the user wants an app opened, use a tool.
- If the user wants a command executed, use a tool.
- Never just describe how to do it.
- Never put JSON inside markdown.
- Tool calls must be ONLY valid JSON.
- If no tool is needed, answer normally.
"""


def execute_tool(data):

    tool = data.get("tool")
    args = data.get("args", {})


    if tool == "open_app":
        return tools.open_app(
            args["app"]
        )


    if tool == "write_file":
        return tools.write_file(
            args["filename"],
            args["content"]
        )


    if tool == "read_file":
        return tools.read_file(
            args["filename"]
        )


    if tool == "run_command":
        return tools.run_command(
            args["command"]
        )


    return "Unknown tool"



def ask_daemon(message):

    files = tools.list_files()


    response = ollama.chat(
        model="llama3.1",
        format="json",
        messages=[
            {
                "role": "system",
                "content": SYSTEM
            },
            {
                "role": "user",
                "content": f"""
Current workspace:

{files}

User request:

{message}
"""
            }
        ]
    )


    raw = response["message"]["content"]


    try:
        data = json.loads(raw)

    except:
        return raw


    if "tool" in data:

        result = execute_tool(data)


        followup = ollama.chat(
            model="llama3.1",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM
                },
                {
                    "role": "user",
                    "content": message
                },
                {
                    "role": "assistant",
                    "content": raw
                },
                {
                    "role": "user",
                    "content": f"""
The tool finished.

Result:
{result}

Explain what happened.
"""
                }
            ]
        )


        return followup["message"]["content"]


    return raw
