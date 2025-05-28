from agent import HSNValidationAgent

agent = HSNValidationAgent()

print("=== VALIDATION TESTS ===")
print(agent.validate_code("01011010"))  # valid
print(agent.validate_code("01"))        # valid
print(agent.validate_code("12345678"))  # invalid or hierarchy issue
print(agent.validate_code("abcd"))      # format error

print("\n=== SUGGESTION TEST ===")
print(agent.suggest_codes("live horses", top_k=3))
