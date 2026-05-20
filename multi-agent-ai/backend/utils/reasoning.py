def add_reasoning(state, message):

    if "reasoning" not in state:
        state["reasoning"] = []

    state["reasoning"].append(message)

    return state