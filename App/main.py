from __future__ import annotations

import os
import ast
import json
from enum import Enum

from rich import print
from rich import box
from rich.table import Table
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.tree import Tree

from App.ShowManager.Proxy import *
from App.ShowManager.Shot import Shot
from App.ShowManager.Show import Show


class State(Enum):
    """ This enum list several states the interface use to write its panels and options """
    PROJECT_INSPECTOR, SHOW_INSPECTOR, LANDING, SHOT_INSPECTOR = 0, 1, 2, 3


class Command:
    """ This class defines a command object, each command contains a code and a set of arguments, with those I can deduce what the user wanted to do with my application """

    def __init__(self, code, description, *arguments: str):
        self.code: str = code
        """ The command's keyword code """

        self.description: str = description
        """ The command's description """

        self.arguments: tuple[str, ...] = arguments
        """ List of arguments this command can be created with """

    def arguments_as_str(self) -> str:
        """ A string definition of the argument's list used to write what arguments a command requires """
        return f'[white]<[/white][magenta]{"[/magenta][white]> = <[/white][magenta]".join(self.arguments)}[/magenta][white]>[/white]' if self.arguments else ""

    def __eq__(self, other: Command) -> bool:
        """ Compare 2 commands and return if they are the same """
        return other.code.lower() == self.code.lower()

    def __ne__(self, other: Command) -> bool:
        """ Compare 2 commands and return if they are not the same """
        return other.code.lower() != self.code.lower()

    @staticmethod
    def interpret_input(input_value: str, *commands: Command) -> Command | None:
        """ This method reads the user input as a string, then test against a collection of commands to find what command the user attempted to use """
        result = None
        empty_command = None  # this is reserved for a command that only have arguments and no code, I'll treat it at the end

        for command in commands:
            if not command.code:
                empty_command = command
            else:
                split_string = input_value.split(" ", 1)
                code = split_string[0]
                arguments = split_string[1] if len(split_string) > 1 else ""

                if command.code.lower() == code.lower():
                    return Command(code, "", *[argument.strip() for argument in arguments.split('=')])

        if not result:
            if empty_command:
                return Command("", "", *[argument.strip() for argument in input_value.split('=')])
            else:
                return None  # This means the interpreter failed to understand what code is this


TITLE = "Show Manager"
""" const tool title """

BACK = Command("Back", "Return to previous menu.")
""" const back command """

EXIT = Command("Exit", "Exit program")
""" const exit command """

console = Console()
""" rich console object """

project_name = ""
""" inspected project's name """

folder_path = ""
""" inspected project's folder path """

inspected_show = ""
""" inspected show's name """

inspected_shot = ""
""" inspected shot's name """

run = True
""" variable that control the application loop """


def is_string_in_list(string: str, string_list: list[str]) -> bool:
    """ this method verifies if a string is within a string array, but different from string in array, this method is not case-sensitive """
    lowercase_string = string.lower()
    lowercase_list = [s.lower() for s in string_list]
    return lowercase_string in lowercase_list


def clear():
    """ This method clears the console """
    os.system('cls' if os.name == 'nt' else 'clear')


def display_instructions(message, ask_message: str = "", ask_delegate = None, title: str = TITLE) -> str:
    """ this method display a render-able rich object then poses a prompt asking something of the user """
    clear()
    print(Panel.fit(message, title=title))
    if ask_delegate:
        return ask_delegate(ask_message)


def draw_json_table(data: str) -> Table:
    """ This method draws a table base on a json string """
    table = Table(box=box.SIMPLE)
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", justify="left", style="magenta")
    dictionary = json.loads(data)
    for key, value in dictionary.items():
        table.add_row(key.capitalize().replace('_', ' ').strip(), str(value))
    return table


def draw_command_table(*commands: Command) -> Table:
    """ This method draws a command table base on a list of commands and their descriptions """
    command_table = Table(box=box.SIMPLE)
    command_table.add_column("[red]Command[/red]", justify="left", style="red", no_wrap=True)
    command_table.add_column("Description", justify="left")
    for command in commands:
        command_table.add_row(f"{command.code}{' ' if command.code else ''}{command.arguments_as_str()}", command.description)
    return command_table


def draw_element_list(elements: list[str], default_message, root_name) -> str | Tree:
    """ Draw a list using rich tree viewer """
    message = default_message
    if elements:
        message = Tree(root_name)
        [message.add(shot) for shot in elements]
    return message


def state_landing() -> State:
    """ First state of UIs state machine, it's the landing view when the application starts """
    global project_name, folder_path

    has_folder_message = f"Path to {folder_path} loaded.\n\nPlease provide a new folder path or press enter to accept this folder.\nThen provide a project name."
    no_folder_message = f"Please provide a folder and a project name."

    command = display_instructions(has_folder_message if folder_path else no_folder_message, "Folder path", Prompt.ask)
    if command:
        folder_path = command

    if os.path.exists(folder_path):
        project_name = Prompt.ask("Project name")
        project_folder = os.path.join(folder_path, project_name)

        manager.set_folder(project_folder)

        if manager.file_exists():
            if display_instructions(f"A Project was found in folder.", "Load project?", Confirm.ask):
                load(project_folder)
                return State.PROJECT_INSPECTOR

        elif not manager.folder_exists():
            if display_instructions(f"No project was found in folder.", "Build new project?", Confirm.ask):
                install(project_folder)
                return State.PROJECT_INSPECTOR


def state_project_inspector():
    """ Second state, this state display information of a project """
    global inspected_show, run

    shows = get_shows_list()

    show_list = draw_element_list(shows, "Project does not have any shows.\nType a show name to create a new show.", "Shows")

    CREATE = Command("", "Create/Get a show named <[magenta]Name[/magenta]>", "Name")
    command_table = draw_command_table(CREATE, BACK, EXIT)

    user_input = display_instructions(Group(show_list, command_table), "Command", Prompt.ask, f"Project: {project_name}")

    user_command = Command.interpret_input(user_input, CREATE, BACK, EXIT)

    if user_command == CREATE:
        inspected_show = user_command.arguments[0]
        if not is_string_in_list(inspected_show, shows):
            if display_instructions(f"{inspected_show} does not exist.", "Create new show?", Confirm.ask, f"New {inspected_show} show"):
                create_show(inspected_show)
                return State.SHOW_INSPECTOR
        else:
            return State.SHOW_INSPECTOR
    elif user_command == BACK:
        return State.LANDING

    elif user_command == EXIT:
        run = False


def state_show_inspector():
    """ Third state, this state display information of a show """
    global inspected_show, inspected_shot, run

    show_data = draw_json_table(get_show_data(inspected_show))
    shots = get_shot_list(inspected_show)
    shots_list = draw_element_list(shots, "Show does not have any shots.", "Shots")

    SET = Command("Set", "Set value of <[cyan]Key[/cyan]> to <[magenta]Value[/magenta]>.", "Key", "Value")
    CREATE = Command("", "Create/Get a shot named <[magenta]Name[/magenta]>", "Name")
    DELETE = Command("Delete", "Delete this show.")
    command_table = draw_command_table(SET, CREATE, DELETE, BACK, EXIT)

    user_input = display_instructions(Group(show_data, shots_list, command_table), "Command", Prompt.ask, f"{inspected_show} data")
    user_command = Command.interpret_input(user_input, SET, CREATE, DELETE, BACK, EXIT)

    if user_command == DELETE:
        delete_show(inspected_show)
        return State.PROJECT_INSPECTOR

    elif user_command == SET:
        if len(user_command.arguments) == 2:
            key = user_command.arguments[0].strip().lower().replace(" ", "_")
            try:
                value = Show().__dict__[key]
                if isinstance(value, list) or isinstance(value, set):
                    value = [element for element in user_command.arguments[1].strip("[]{}").split(",")]
                elif isinstance(value, dict):
                    value = ast.literal_eval(user_command.arguments[1])
                else:
                    value = user_command.arguments[1]
                set_show_data(inspected_show, {key: value})
            except:
                return

    elif user_command == CREATE:
        inspected_shot = user_command.arguments[0]
        if not is_string_in_list(inspected_shot, shots):
            if display_instructions(f"{inspected_shot} does not exist.", "Create new shot?", Confirm.ask, f"New {inspected_shot} shot"):
                create_shot(inspected_show, inspected_shot)
                return State.SHOT_INSPECTOR
        else:
            return State.SHOT_INSPECTOR

    elif user_command == BACK:
        return State.PROJECT_INSPECTOR

    elif user_command == EXIT:
        run = False


def state_shot_inspector():
    """ Last state, this one shows information of a shot """
    global inspected_show, inspected_shot, run

    shot_data = draw_json_table(get_shot_data(inspected_show, inspected_shot))

    SET = Command("Set", "Set value of <[cyan]Key[/cyan]> to <[magenta]Value[/magenta]>.", "Key", "Value")
    DELETE = Command("Delete", "Delete this shot.")
    command_table = draw_command_table(SET, DELETE, BACK, EXIT)

    user_input = display_instructions(Group(shot_data, command_table), "Command", Prompt.ask, f"{inspected_show}.{inspected_shot} data")
    user_command = Command.interpret_input(user_input, SET, DELETE, BACK, EXIT)

    if user_command == DELETE:
        delete_shot(inspected_show, inspected_shot)
        return State.SHOW_INSPECTOR

    elif user_command == SET:
        if len(user_command.arguments) == 2:
            key = user_command.arguments[0].strip().lower().replace(" ", "_")
            try:
                value = Shot().__dict__[key]
                if isinstance(value, list) or isinstance(value, set):
                    value = [element for element in user_command.arguments[1].strip("[]{}").split(",")]
                elif isinstance(value, dict):
                    value = ast.literal_eval(user_command.arguments[1])
                else:
                    value = user_command.arguments[1]
                set_shot_data(inspected_show, inspected_shot, {key: value})
            except:
                return

    elif user_command == BACK:
        return State.SHOW_INSPECTOR

    elif user_command == EXIT:
        run = False


if __name__ == '__main__':
    state = State.LANDING
    new_state = None
    while run:
        clear()
        try:
            if state == State.LANDING:
                new_state = state_landing()

            elif state == State.PROJECT_INSPECTOR:
                new_state = state_project_inspector()

            elif state == State.SHOW_INSPECTOR:
                new_state = state_show_inspector()

            elif state == State.SHOT_INSPECTOR:
                new_state = state_shot_inspector()
        except:
            pass

        if new_state:
            state = new_state
