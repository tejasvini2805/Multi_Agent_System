# run.py
from orchestrator import SessionManager

def main():
    print("Multi-Agent CLI (type 'exit' to quit)")
    print("You can say things like: 'I want to learn Python', 'Interview me for a Python dev role', 'Prep me for a debate on AI jobs'")
    mgr = SessionManager()
    while True:
        user = input("\nYou: ").strip()
        if user.lower() in ("exit", "quit"):
            break
        agent_name, reply = mgr.route(user)
        print(f"\n[{agent_name.upper()} AGENT]:\n{reply}")

if __name__ == "__main__":
    main()
