from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

client = Anthropic(
    api_key=ANTHROPIC_API_KEY
)


def ask_claude(messages):

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system="تو یک دستیار هوش مصنوعی فارسی زبان هستی.",
        messages=messages
    )

    return response.content[0].text