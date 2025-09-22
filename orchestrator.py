from agents import LearningAgent, InterviewAgent, DebateAgent

class SessionManager:
    def __init__(self):
        self.learning = LearningAgent()
        self.interview = InterviewAgent()
        self.debate = DebateAgent()
        self.jd = None            # Optional Job Description
        self.active_agent = None  # Track current agent
        self.history = ""         # Keep conversation history

    def route(self, user_input, jd=None):
        # Reset conversation if user types "reset"
        if user_input.lower() in ["reset", "start over", "end"]:
            self.active_agent = None
            self.history = ""
            self.jd = None
            return "system", "Conversation reset. You can start a new topic."

        # Update JD if provided
        if jd:
            self.jd = jd

        # Determine agent if none is active
        if not self.active_agent:
            text = user_input.lower()
            if "learn" in text or "study" in text or "roadmap" in text:
                self.active_agent = "learning"
            elif "interview" in text or "mock" in text or "job" in text:
                self.active_agent = "interview"
            elif "debate" in text or "argue" in text or "discussion" in text:
                self.active_agent = "debate"
            else:
                return "system", (
                    "I’m not sure which agent to route this to. "
                    "Try saying 'learn', 'interview', or 'debate'."
                )

        # Route input to active agent with history
        if self.active_agent == "learning":
            reply = self.learning.handle(user_input, history=self.history)
        elif self.active_agent == "interview":
            reply = self.interview.handle(user_input, jd=self.jd, history=self.history)
        elif self.active_agent == "debate":
            reply = self.debate.handle(user_input, history=self.history)
        else:
            reply = "Something went wrong."

        # Append to session history
        self.history += f"\nUser: {user_input}\n{self.active_agent.capitalize()} Agent: {reply}"
        return self.active_agent, reply
