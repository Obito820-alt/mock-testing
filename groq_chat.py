"""A small wrapper around the Groq chat-completions API."""


def ask_groq(question: str, client=None) -> str:
    """Send a question to Groq and return the assistant's text.

    Passing a client makes the function easy to test without a real API call.
    """
    if not question.strip():
        raise ValueError("Question cannot be empty")

    if client is None:
        from groq import Groq

        client = Groq()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": question}],
        max_tokens=1024,
    )
    return response.choices[0].message.content
