from rag.prompt import get_custom_prompt

def test_custom_prompt_structure():
    prompt = get_custom_prompt()
    assert "{context}" in prompt.template
    assert "{question}" in prompt.template
