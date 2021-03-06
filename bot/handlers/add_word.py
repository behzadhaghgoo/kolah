from bot.models.game import GameManager, Game
from bot.helpers import update_statuses

def add_word(update, context):
    print("add word")
    try:
        context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except:
        pass
    
    games = Game.objects(players=update.effective_chat.id, status="Getting Words")
    if len(games) != 1:
        print("games:", len(games))
        return
    
    game = games[0]
    word = update.message.text.split("/add_word")[0].strip()
    print(word, game)
    if word != "":
        game = GameManager.add_words(game, word)
        update_statuses(context.bot, game)