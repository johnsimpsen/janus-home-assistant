from enum import Enum
from src.listener.listener import listen
from src.agent.agent import prompt_llm
from src.agent.commands import validate_command, run_command


class _Context:
    def __init__(self):
        self.user_input = None
        self.llm_output = None
        self.command = None
        self.response = None
        self.error_status = None

    def reset_current_request(self):
        """current request is cleared and a new request may be started"""
        self.user_input = None
        self.llm_output = None
        self.command = None
        self.response = None
        self.error_status = None

    def __str__(self):
        return (f"user_input: {self.user_input}\n"
                f"llm_output: {self.llm_output}\n"
                f"command: {self.command}\n"
                f"response: {self.response}\n"
                f"error: {self.error_status}\n")


class State(Enum):
    LISTENING = "listening"
    PROCESSING = "processing"
    VALIDATING = "validating"
    EXECUTING = "executing"
    FINISHING = "finishing"
    QUIT = "quit"
    ERROR = "error"


class StateMachine:
    def __init__(self, debug_mode=False):
        self._current_state = State.LISTENING  # begin as IDLE
        self.context = _Context()  # data about the current request
        self.running = True  # is the agent currently running?
        self.DEBUG_MODE = debug_mode  # bypasses llm input

    def run(self):
        """manages the current behavior based on the state"""

        while self.running:
            try:
                match self._current_state:
                    case State.LISTENING:
                        self._listening()
                    case State.PROCESSING:
                        self._processing()
                    case State.VALIDATING:
                        self._validating()
                    case State.EXECUTING:
                        self._executing()
                    case State.FINISHING:
                        self._finishing()
                    case State.QUIT:
                        break
                    case State.ERROR:
                        self._error(Exception("Something went wrong"))
                    case _:
                        pass
            except Exception as e:
                self.set_state(State.ERROR)
                self._error(e)

    def set_state(self, new_state):
        """Change the current state to the new one"""
        if self._current_state == new_state:
            print(f"State is already: {new_state}")
        else:
            self._current_state = new_state

    # STATE BEHAVIORS

    def _listening(self):
        """listens for speaking and then audio is converted to text"""
        if self.DEBUG_MODE:
            self.context.user_input = input("Prompt: ")
        else:
            self.context.user_input = listen()

        self.set_state(State.PROCESSING)

    def _processing(self):
        """user speech text is fed to a llm to be processed into a command"""

        # check if the program should be ended
        if self.context.user_input.lower() == "q" or self.context.user_input.lower() == "quit":
            self.set_state(State.QUIT)
            return

        self.context.llm_output = prompt_llm(self.context.user_input)

        self.set_state(State.VALIDATING)

    def _validating(self):
        """processed commands are checked for errors and then formatted"""
        self.context.command = validate_command(self.context.llm_output)

        self.set_state(State.EXECUTING)

    def _executing(self):
        """attempt to execute a command and then wait for its response"""

        self.context.response = run_command(self.context.command)

        self.set_state(State.FINISHING)

    def _finishing(self):
        """clear command context and transition back to LISTENING"""
        print(self.context)
        self.context.reset_current_request()
        self.set_state(State.LISTENING)

    def _error(self, error):
        """handle any errors, clear context, then transition back to LISTENING"""
        self.context.error_status = error
        #print(f"An error has occurred: {error}")
        print(self.context)

        self.context.reset_current_request()
        self.set_state(State.LISTENING)  # return to LISTENING state after error has been dealt with
