from trello import *


CONFIG_FILE = "config.json"


if __name__ == "__main__":
    with open(CONFIG_FILE, "r") as file:
        config_data = json.load(file)

    client = TrelloClient(
        api_key=config_data["api_key"],
        token=config_data["token"]
    )

    board_id = "id of board"
    board = client.get_board(board_id)

    input()
