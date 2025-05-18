import html

def format_chat_history(chat_history: list) -> str:
    formatted_text = "# AI Roadmap Discussion\n\n"
    
    for message in chat_history:
        role = message["role"].capitalize()
        content = message["content"]
        formatted_text += f"## {role}\n{content}\n\n"
    
    return formatted_text 

def format_chat_history_for_html(chat_history: list, user_name: str = None) -> str:
    html_output = ""
    for message in chat_history:
        is_user = message.get("sender", message.get("role", "")).lower() == "user"
        
        display_name = user_name if is_user else "AI Assistant"
        
        if is_user:
            content = message.get("message", "")
        else:
            content = message.get("message", message.get("content", ""))
        
        content_escaped = html.escape(content)
        content_formatted = content_escaped.replace("\n", "<br />")
        
        css_class = "user" if is_user else "assistant"
        
        html_output += f'<div class="message-block {css_class}">'
        html_output += f'<h3>{html.escape(display_name)}</h3>'
        html_output += f'<div class="message-text-content"><p>{content_formatted}</p></div>'
        html_output += '</div>\n'
    
    return html_output 