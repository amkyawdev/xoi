"""Tokenizer utilities"""

from typing import list


class TokenCounter:
    """Count tokens in text"""
    
    # Approximate tokens per character
    TOKENS_PER_CHAR = 0.25
    
    def count(self, text: str) -> int:
        """Count approximate tokens in text"""
        return int(len(text) * self.TOKENS_PER_CHAR)
    
    def count_messages(self, messages: list[dict[str, str]]) -> int:
        """Count tokens in messages"""
        total = 0
        for msg in messages:
            total += self.count(msg.get("content", ""))
            total += 4  # Overhead per message
        return total


# Global token counter
counter = TokenCounter()


def count_tokens(text: str) -> int:
    """Count tokens in text"""
    return counter.count(text)


def count_message_tokens(messages: list[dict[str, str]]) -> int:
    """Count tokens in messages"""
    return counter.count_messages(messages)
