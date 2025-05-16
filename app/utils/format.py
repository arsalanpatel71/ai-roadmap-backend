import html

def format_chat_history(chat_history: list) -> str:
    formatted_text = "# AI Roadmap Discussion\n\n"
    
    for message in chat_history:
        role = message["role"].capitalize()
        content = message["content"]
        formatted_text += f"## {role}\n{content}\n\n"
    
    return formatted_text 

def format_chat_history_for_html(chat_history: list) -> str:
    html_output = ""
    for message in chat_history:
        role = message.get("role", "Unknown").capitalize()
        content = message.get("content", message.get("message", ""))
        
        content_escaped = html.escape(content)
        content_formatted = content_escaped.replace("\n", "<br />")

        css_class = "assistant" if role.lower() == "assistant" else "user"
        
        html_output += f'<div class="message-block {css_class}">'
        html_output += f'<h3>{html.escape(role)}</h3>'
        html_output += f'<div class="message-text-content"><p>{content_formatted}</p></div>'
        html_output += '</div>\n'
    return html_output 