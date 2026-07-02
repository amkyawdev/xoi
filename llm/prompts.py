"""LLM prompt templates"""

SYSTEM_PROMPTS = {
    "agent": """You are a helpful AI agent that can perform various tasks including:
- Searching the web
- Scraping web pages
- Analyzing content
- Answering questions
- Writing and explaining code

Always be precise, helpful, and safe in your responses.""",
    
    "coder": """You are an expert programmer. Generate clean, well-documented code.
Always consider edge cases and error handling.""",
    
    "researcher": """You are a research assistant. Provide thorough, accurate, and well-cited information.""",
    
    "summarizer": """You are a summarization expert. Create clear, concise summaries that capture key points."""
}


def get_system_prompt(task_type: str = "agent") -> str:
    """Get system prompt for task type"""
    return SYSTEM_PROMPTS.get(task_type, SYSTEM_PROMPTS["agent"])


def format_messages(
    system: str,
    conversation: list[tuple[str, str]],
    max_history: int = 10
) -> list[dict[str, str]]:
    """Format messages for chat API"""
    messages = [{"role": "system", "content": system}]
    
    for role, content in conversation[-max_history:]:
        messages.append({"role": role, "content": content})
    
    return messages
