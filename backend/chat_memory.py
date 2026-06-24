from collections import defaultdict


class ChatMemory:

    def __init__(self):
        self.history = defaultdict(list)


    def add_message(
        self,
        session_id,
        role,
        message
    ):
        self.history[session_id].append(
            {
                "role": role,
                "message": message
            }
        )


    def get_history(
        self,
        session_id,
        max_messages=10
    ):
        return self.history[session_id][-max_messages:]


    def clear(
        self,
        session_id
    ):
        self.history[session_id] = []


memory = ChatMemory()