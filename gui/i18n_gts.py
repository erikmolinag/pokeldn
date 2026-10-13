"""Spanish for upstream 0.19-0.22 screens (gts). Same rule as gui/i18n.py ES: the English text is the key;
gui/i18n.py merges this dict into ES."""
ES_GTS = {
    # the GTS (gui/views/gts.py): a listing is a "publicación", an offer on it an "oferta"
    "Any Pokemon": "Cualquier Pokémon",
    "Offered": "Ofrecido",
    "Wanted": "Pedido",
    "Deposit a Pokemon": "Depositar un Pokémon",
    "Yours": "Tuyos",
    "Listing": "Publicación",
    "{n} of {total} relays connected": "{n} de {total} relés conectados",
    "Connecting to the relays...": "Conectando con los relés...",
    "1 open listing": "1 publicación abierta",
    "{n} open listings": "{n} publicaciones abiertas",
    "No open listing matches. Deposit one of yours from the left.":
        "Ninguna publicación abierta coincide. Deposita uno de los tuyos desde la izquierda.",
    "Reading the listings from the relays...": "Leyendo las publicaciones de los relés...",
    "Nothing listed or offered.": "Nada publicado ni ofrecido.",
    "{species} level {level} for {wants}": "{species} nivel {level} por {wants}",
    "{species} for {name}": "{species} por {name}",
    "{species} offered for {name}": "{species} ofrecido por {name}",
    "{name}, level {low} to {high}": "{name}, nivel {low} a {high}",
    "Pick a listing to see the Pokemon and what its trainer asks for. A trade happens the next time the "
    "lister's app is open; until then your offer waits outside your bank.":
        "Elige una publicación para ver el Pokémon y lo que pide su entrenador. El intercambio se hace la próxima "
        "vez que la app de quien lo publicó esté abierta; mientras tanto, tu oferta espera fuera de tu banco.",
    "Asks for": "Pide",
    "From {trainer}, open until {date}": "De {trainer}, abierta hasta el {date}",
    "a trainer": "un entrenador",
    "Your Pokemon that answer it": "Tus Pokémon que cumplen lo pedido",
    "In {game}, OT {ot}": "En {game}, EO {ot}",
    "Your bank holds no legal {wants} that is not queued for a trade.":
        "Tu banco no tiene ningún {wants} legal que no esté en cola para un intercambio.",
    "Offer": "Ofrecer",
    "Asks for {wants}. Open until {date}; 1 offer answered.":
        "Pide {wants}. Abierta hasta el {date}; 1 oferta respondida.",
    "Asks for {wants}. Open until {date}; {n} offers answered.":
        "Pide {wants}. Abierta hasta el {date}; {n} ofertas respondidas.",
    "Traded with {name}; what came back is in the bank.":
        "Intercambiado con {name}; lo que recibiste está en el banco.",
    "Take it down": "Retirarlo",
    "Offered for {species} level {level} from {trainer}.": "Ofrecido por {species} nivel {level} de {trainer}.",
    "The trade happens the next time the lister's app is open. If it ends unanswered, your Pokemon comes back "
    "to the bank.":
        "El intercambio se hace la próxima vez que la app de quien lo publicó esté abierta. Si termina sin "
        "respuesta, tu Pokémon vuelve al banco.",
    "Clear from the list": "Quitar de la lista",
    "PKHeX is checking it...": "PKHeX lo está revisando...",
    "Offered. Yours lists the answer once the lister's app sends it.":
        "Ofrecido. En Tuyos verás la respuesta cuando la app de quien lo publicó la mande.",
    "Offer {name}?": "¿Ofrecer {name}?",
    "It leaves your bank and waits for the lister's app. You get {species} if your offer is the first that "
    "answers the listing; otherwise it comes back. Nothing on the relays can make the lister send theirs: a "
    "trade depends on the other app being the real one.":
        "Sale de tu banco y espera a la app de quien lo publicó. Recibes {species} si tu oferta es la primera que "
        "cumple la publicación; si no, vuelve. Nada en los relés puede obligar a quien lo publicó a mandar el "
        "suyo: el intercambio depende de que la otra app sea la auténtica.",
    "Taking it down...": "Retirándolo...",
    "Taken down. The Pokemon is back in the bank.": "Retirado. El Pokémon está de vuelta en el banco.",
    "The bank holds no legal Pokemon that is not queued for a trade.":
        "El banco no tiene ningún Pokémon legal que no esté en cola para un intercambio.",
    "PKHeX is still reading the species list; try again in a moment.":
        "PKHeX todavía está leyendo la lista de especies; intenta otra vez en un momento.",
    "Pick your Pokemon and the one you ask for.": "Elige tu Pokémon y el que pides.",
    "The levels go from 1 to 100, the first no higher than the second.":
        "Los niveles van de 1 a 100, y el primero no puede ser mayor que el segundo.",
    "Listed for 30 days. Your app trades it when it is open and a matching offer arrives.":
        "Publicado por 30 días. Tu app lo intercambia cuando esté abierta y llegue una oferta que cumpla.",
    "Your Pokemon": "Tu Pokémon",
    "Ask for": "Pides",
    "Lowest level": "Nivel mínimo",
    "Highest level": "Nivel máximo",
    "It leaves the bank while listed. The first offer that answers it is traded, by this app, the next time it "
    "is open. Take it down from Yours to get it back.":
        "Sale del banco mientras esté publicado. La primera oferta que lo cumpla se intercambia, desde esta app, la "
        "próxima vez que esté abierta. Retíralo desde Tuyos para recuperarlo.",
    "Deposit": "Depositar",
    # gts.STATUS
    "Listed": "Publicado",
    "Traded": "Intercambiado",
    "Taken down": "Retirado",
    "Ended": "Vencido",
    "Waiting for the lister": "Esperando a quien lo publicó",
    "Back in the bank": "De vuelta en el banco",
    # pokeldn.app.gts: a GtsError, or why an offer came back (shown capitalized, with a period)
    "This listing is no longer open.": "Esta publicación ya no está abierta.",
    "PKHeX could not read it ({error})": "PKHeX no lo pudo leer ({error})",
    "PKHeX finds it not legal ({report})": "PKHeX lo marca como no legal ({report})",
    "The lister asks for {name}.": "Quien lo publicó pide {name}.",
    "The lister asks for level {low} to {high}.": "Quien lo publicó pide nivel {low} a {high}.",
    "Another offer was taken first.": "Se aceptó otra oferta primero.",
    "The listing has ended.": "La publicación terminó.",
    "The offer carries no Pokemon.": "La oferta no trae ningún Pokémon.",
    "Refused.": "Rechazado.",
    "The lister's answer carries no Pokemon.": "La respuesta de quien lo publicó no trae ningún Pokémon.",
    "It is not the game the listing showed.": "No es el juego que mostraba la publicación.",
    "It is not the Pokemon the listing showed.": "No es el Pokémon que mostraba la publicación.",
    "The lister took the listing down.": "Quien lo publicó retiró la publicación.",
    "The listing ended with no answer.": "La publicación terminó sin respuesta.",

    # pokeldn.pokemon.summary's parts (gui/views/bank.py summary_part)
    "level {level}": "nivel {level}",
    "shiny": "shiny",
    "holding {item}": "lleva {item}",
    # pokemon.HOME_TRACKER_WARNINGS
    "PKHeX flags the missing HOME tracker": "PKHeX marca que le falta el rastreador de HOME",
    "Can't be deposited in HOME": "No se puede depositar en HOME",

    # the bank (gui/views/bank.py): editing and importing
    "Reading it...": "Leyéndolo...",
    "Saved. PKHeX checks again where it can go.": "Guardado. PKHeX vuelve a revisar a dónde puede ir.",
    "Import Pokemon": "Importar Pokémon",
    "Reading {name}...": "Leyendo {name}...",
    "Reading {name} ({n} of {total})...": "Leyendo {name} ({n} de {total})...",
    "{n} already in the bank": "{n} ya en el banco",
    "{n} not imported": "{n} sin importar",
    "1 file unreadable": "1 archivo ilegible",
    "{n} files unreadable": "{n} archivos ilegibles",
    "{n} Pokemon banked": "{n} Pokémon al banco",
    "Nothing new to bank": "Nada nuevo para el banco",
    "PKHeX checks every Pokemon. Your files are not changed.":
        "PKHeX revisa cada Pokémon. Tus archivos no se modifican.",
    "No Pokemon in this file.": "No hay Pokémon en este archivo.",
    "Unknown Pokemon": "Pokémon desconocido",
    "Kept as a {game} Pokemon": "Se guarda como Pokémon de {game}",
    # ImportDialog.STATES
    "Banked": "Guardado",
    "Already in the bank": "Ya estaba en el banco",
    "Not imported": "No importado",
    # pokeldn.app.bank.import_file
    "This file is too big to be a Pokemon or a game save.":
        "Este archivo es demasiado grande para ser un Pokémon o una partida.",
    "Edit {name}": "Editar {name}",
    "Moves": "Movimientos",
    "Only what the game itself lets a player change. PKHeX checks every edit; one that would make it not legal "
    "is refused.":
        "Solo lo que el propio juego deja cambiar. PKHeX revisa cada cambio; si uno lo haría no legal, se rechaza.",
    "The level goes from {level} to 100.": "El nivel va de {level} a 100.",
    "It needs at least one move.": "Necesita al menos un movimiento.",
    "A move appears twice.": "Hay un movimiento repetido.",
    "Not saved: {problem}": "No se guardó: {problem}",
}
