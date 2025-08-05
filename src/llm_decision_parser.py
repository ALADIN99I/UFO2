def parse_llm_decisions(log_file):
    """
    Parses the LLM trade decisions from the simulation log file.

    Args:
        log_file (str): The path to the log file.
    """
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_decision_block = False
    decision_lines = []
    all_decisions = []

    for line in lines:
        print(line) # a temporary print statement for debugging
        if line.startswith("LLM Trade Decision:"):
            in_decision_block = True
            decision_lines = []
        elif in_decision_block and line.startswith("["):
            in_decision_block = False
            all_decisions.append("".join(decision_lines))
        elif in_decision_block:
            decision_lines.append(line)

    if not all_decisions:
        print("No LLM trade decisions found in the log file.")
        return

    print("--- LLM Trade Decisions ---")
    for i, decision in enumerate(all_decisions, 1):
        print(f"--- Decision {i} ---")
        print(decision.strip())
        print("\n")

if __name__ == '__main__':
    parse_llm_decisions('full_day_simulation_20250804.txt')
