from enum import Enum
from src.agent.agent import prompt_llm
from src.command.commands import parse_command, run_command


class _Context:
    def __init__(self):
        self.user_input = None
        self.llm_output = None
        self.command = None
        self.response = None
        self.error_status = None

    def reset_current_request(self):
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
                f"error: {self.error_status}")


class State(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    VALIDATING = "validating"
    EXECUTING = "executing"
    FINISHING = "finishing"
    QUIT = "quit"
    ERROR = "error"


class StateMachine:
    def __init__(self):
        self._current_state = State.IDLE # begin as IDLE
        self.context = _Context() # data about the current request
        self.running = True # is the agent currently running?

    def run(self):
        """manages the current behavior based on the state"""

        while self.running:
            try:
                match self._current_state:
                    case State.IDLE:
                        self._idle()
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

    def _idle(self):
        """program clears all context and then listens for activation word: janus"""
        # TODO: implement speech listener module
        self.set_state(State.PROCESSING)

    def _processing(self):
        """speech prompts are converted to text and fed to a llm to be processed into a command"""
        user_input = input("Prompt: ") # TODO: Replace with speech to text module
        self.context.user_input = user_input

        if user_input.lower() == "q" or user_input.lower() == "quit":
            self.set_state(State.QUIT)
            return

        self.context.llm_output = prompt_llm(user_input)

        self.set_state(State.VALIDATING)

    def _validating(self):
        """processed commands are checked for errors and then formatted"""
        self.context.command = parse_command(self.context.llm_output)

        self.set_state(State.EXECUTING)

    #
    def _executing(self):
        """attempt to execute a command and then wait for its response"""
        self.context.response = run_command(self.context.command)

        self.set_state(State.FINISHING)

    def _finishing(self):
        """clear command context and transition back to IDLE"""
        self.context.reset_current_request()
        self.set_state(State.IDLE)

    def _error(self, error):
        """handle any errors, clear context, then transition back to IDLE"""
        print(f"An error has occurred: {error}")
        print(self.context)

        self.context.reset_current_request()
        self.set_state(State.IDLE)  # return to IDLE state after error has been dealt with

