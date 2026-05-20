import time

# =========================================================
# ADD TRACE
# =========================================================

def add_trace(state, message):

    if "trace_logs" not in state:
        state["trace_logs"] = []

    timestamp = time.strftime("%H:%M:%S")

    log = f"[{timestamp}] {message}"

    print(log)

    state["trace_logs"].append(log)

# =========================================================
# START TIMER
# =========================================================

def start_timer(state):

    state["start_time"] = time.time()

# =========================================================
# END TIMER
# =========================================================

def end_timer(state):

    if "start_time" in state:

        total = round(
            time.time() - state["start_time"],
            2
        )

        state["execution_time"] = total

        add_trace(
            state,
            f"Total execution time: {total}s"
        )