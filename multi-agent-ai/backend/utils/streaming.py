# =========================================================
# STREAM FUNCTION
# =========================================================

def stream_llm_response(llm_model, prompt):

    response = llm_model.stream(prompt)

    full_response = ""

    for chunk in response:

        if chunk.content:

            full_response += chunk.content

            yield full_response
