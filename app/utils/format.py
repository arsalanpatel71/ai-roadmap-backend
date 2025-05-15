def format_chat_history(chat_history: list) -> str:
    formatted_text = "# AI Roadmap Discussion\n\n"
    
    for message in chat_history:
        role = message["role"].capitalize()
        content = message["content"]
        formatted_text += f"## {role}\n{content}\n\n"
    
    return formatted_text 