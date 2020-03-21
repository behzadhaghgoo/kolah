from .models.game import Game
from .models.player import Player

joining_status = """
بازیکنان فعال:
%s
"""



def update_message(telegram_bot, player, text):
    if player.status_message_id is None:
        print("creating new message")
        message = telegram_bot.send_message(chat_id=player.chat_id, text=text)
        player.status_message_id = message.message_id
        player.save()
    else:
        print("editing message")
        telegram_bot.edit_message_text(text, chat_id=player.chat_id, message_id=player.status_message_id)


def update_statuses(telegram_bot, game):
    print("game.status = {}".format(game.status))
    game.reload()
    players = Player.objects(chat_id__in=game.players)
    players_dict = dict()
    for player in players:
        players_dict[player.chat_id] = player

    active_players_text = "\n".join(["%d.%s" % (index + 1, player.name) for index, player in enumerate(players)])
    if game.status == "Joining":
        for player in players:
            update_message(telegram_bot, player, joining_status % active_players_text)

    if game.status == "Team Assignment":
        teams_str = ""
        for i, team in enumerate(game.teams):
            teams_str += "team {}: {} - {} \n".format(i, players_dict[team.players[0]].name, players_dict[team.players[1]].name)
        for player in players:
            update_message(telegram_bot, player, teams_str)
            
    if game.status == "Getting Words":
        message = """کلمه وارد کن گل من
         {} کلمه وارد شده تا الان""".format(len(game.words))
        for player in players:
            update_message(telegram_bot, player, message)

    if game.status == "Done":
        pass