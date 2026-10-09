"""poke-app's interface language: Spanish or English. The English text is the key; a string with no
Spanish entry shows in English. `tr` takes str.format fields: tr("{n} traded", n=3)."""

LANGUAGES = (("es", "Español"), ("en", "English"))
_state = {"code": "es"}


def set_language(code: str) -> None:
    _state["code"] = code if code in dict(LANGUAGES) else "es"


def language() -> str:
    return _state["code"]


def tr(text: str, **fields) -> str:
    if not text:
        return text
    out = ES.get(text, text) if _state["code"] == "es" else text
    return out.format(**fields) if fields else out


ES = {
    # shell
    "Home": "Inicio",
    "Play": "Jugar",
    "Games": "Juegos",
    "Board": "Placa",
    "Docs": "Guía",
    "Settings": "Ajustes",
    "Update": "Actualizar",
    "Close welcome": "Cerrar bienvenida",
    "Welcome to pokeldn": "Bienvenido a pokeldn",
    "Trade and send gifts over local wireless, right from your computer.":
        "Intercambia y envía regalos por comunicación inalámbrica local, desde tu computadora.",
    "Choose prod.keys dumped from your own console. The keys decrypt local wireless messages and stay "
    "on this computer.":
        "Elige el prod.keys extraído de tu propia consola. Las claves descifran la comunicación inalámbrica "
        "local y se quedan en esta computadora.",
    "Plug in your ESP32 with a USB data cable.": "Conecta tu ESP32 con un cable USB de datos.",
    "Read your trainer from the console, so the Pokemon built here are yours.":
        "Lee tu entrenador desde la consola, para que los Pokémon que generes sean tuyos.",
    "Pick a game, choose a tool and follow the console steps.":
        "Elige una herramienta y sigue los pasos en la consola.",
    "Read the setup guide": "Leer la guía de instalación",
    "Drop prod.keys here, or add keys later in Settings.":
        "Suelta aquí el prod.keys, o agrégalo después en Ajustes.",
    "Add keys later in Settings.": "Agrega las claves después en Ajustes.",
    "Later": "Después",
    "Choose prod.keys": "Elegir prod.keys",
    "pokeldn {version} is available": "pokeldn {version} está disponible",
    "What's new": "Novedades",
    "Download": "Descargar",
    "Copied": "Copiado",

    # home
    "Hello, {name}!": "¡Hola, {name}!",
    "Welcome, trainer!": "¡Bienvenido, entrenador!",
    "Your trainer card": "Tu tarjeta de entrenador",
    "TRAINER CARD": "TARJETA DE ENTRENADOR",
    "Name": "Nombre",
    "Trainer ID": "ID de entrenador",
    "Secret ID": "ID secreto",
    "Game": "Juego",
    "Language": "Idioma",
    "Gender": "Sexo",
    "Boy": "Chico",
    "Girl": "Chica",
    "Shiny value": "Valor shiny",
    "Read from your console": "Leído de tu consola",
    "Typed in by hand": "Escrito a mano",
    "Read from my console": "Leer de mi consola",
    "Read again": "Leer otra vez",
    "Edit": "Editar",
    "No trainer yet": "Todavía no hay entrenador",
    "Connect the board, join the Direct Corner on your console and pokeldn reads your name, Trainer ID "
    "and Secret ID in seconds. Nothing is traded.":
        "Conecta la placa, entra al Direct Corner en tu consola y pokeldn lee tu nombre, tu ID de "
        "entrenador y tu ID secreto en segundos. No se intercambia nada.",
    "Every Pokemon you build here carries this trainer as its original trainer: the game treats it as "
    "caught in your own save, so it obeys at any level and shows your name.":
        "Cada Pokémon que generes aquí lleva a este entrenador como entrenador original: el juego lo "
        "trata como atrapado en tu propia partida, así que te obedece a cualquier nivel y muestra tu "
        "nombre.",
    "Shiny Pokemon are built for your Trainer ID and Secret ID, so they are shiny in your game.":
        "Los Pokémon shiny se generan para tu ID de entrenador y tu ID secreto, así que salen shiny "
        "en tu juego.",
    "What do you want to do?": "¿Qué quieres hacer?",
    "Trade": "Intercambiar",
    "Send a Pokemon built for your save, or receive one.": "Envía un Pokémon hecho para tu partida o recibe uno.",
    "Mystery Gift": "Regalo Misterioso",
    "Items, eggs, event Pokemon and game boosts.": "Objetos, huevos, Pokémon de evento y mejoras para el juego.",
    "Back up your save": "Respaldar tu partida",
    "Copy your whole save to this computer.": "Copia tu partida completa a esta computadora.",
    "Check that pokeldn's firmware answers.": "Comprueba que el firmware de pokeldn responde.",
    "Your board": "Tu placa",

    # games view and session
    "Read my trainer": "Leer mi entrenador",
    "Trade (Host)": "Intercambio (anfitrión)",
    "Trade (Join)": "Intercambio (unirse)",
    "Your console joins pokeldn": "Tu consola se une a pokeldn",
    "pokeldn joins your console": "pokeldn se une a tu consola",
    "Basic": "Básico",
    "Advanced": "Avanzado",
    "Read the docs for this game": "Leer la guía de este juego",
    "Not available yet": "Todavía no disponible",
    "Soon": "Pronto",
    "Nothing to fill in.": "No hay nada que llenar.",
    "Game language": "Idioma del juego",
    "Detected automatically": "Se detecta automáticamente",
    "English · French · German · Italian · Spanish · Japanese":
        "Inglés · Francés · Alemán · Italiano · Español · Japonés",
    "After you choose pokeldn in the Friend list, your game reports its language.":
        "Cuando eliges pokeldn en la lista de amigos, tu juego informa su idioma.",
    "Search the options": "Buscar opciones",
    "Advanced options": "Opciones avanzadas",
    "The tested defaults work for most players. Change these only when a guide or a bug report "
    "asks you to. A value set here overrides the Basic tab.":
        "Los valores probados funcionan para casi todos. Cámbialos solo si una guía o un reporte de error "
        "te lo pide. Lo que pongas aquí reemplaza lo de la pestaña Básico.",
    "No option matches.": "Ninguna opción coincide.",
    "This tool takes no options beyond its Basic fields.": "Esta herramienta no tiene más opciones que las básicas.",
    "No description.": "Sin descripción.",
    "Show all": "Mostrar todo",
    "Session": "Sesión",
    "Idle": "Inactiva",
    "Ready": "Lista",
    "Show the command": "Mostrar el comando",
    "Copy the log": "Copiar el registro",
    "Open the Received folder": "Abrir la carpeta de recibidos",
    "The session's output appears here.": "Aquí aparece lo que va pasando en la sesión.",
    "Output": "Registro",
    "On the console": "En la consola",
    "Before you start": "Antes de empezar",
    "Switch keys added": "Claves de Switch agregadas",
    "Add your Switch keys": "Agrega tus claves de Switch",
    "Choose prod.keys in Settings.": "Elige el prod.keys en Ajustes.",
    "Pokemon to offer": "Pokémon para ofrecer",
    " Pick a species, then press Build.": " Elige una especie y presiona Generar.",
    "Check the options": "Revisa las opciones",
    "Ready to start": "Todo listo",
    "Stop": "Detener",
    "Start": "Empezar",
    "Stop {name} and start": "Detener {name} y empezar",
    "Offering": "Ofreciendo",
    "{n} traded": "{n} intercambiados",
    "{done} of {total} traded": "{done} de {total} intercambiados",
    "{n} trades, in order": "{n} intercambios, en orden",
    "Backing up the save": "Respaldando la partida",
    "Putting the save on the console": "Pasando la partida a la consola",
    "{done} of {total} {unit}. Keep the Switch near the board.":
        "{done} de {total} {unit}. Mantén la Switch cerca de la placa.",
    "Received": "Recibido",
    "Not read by PKHeX": "PKHeX no lo pudo leer",
    "Not started": "No empezó",
    "Stopped": "Detenida",
    "Finished": "Terminada",
    "Failed ({code})": "Falló ({code})",
    "Running {time}": "En curso {time}",
    "Trainer found": "Entrenador encontrado",
    "Saved as your trainer. Now choose Cancel and Yes on the console: nothing is traded.":
        "Guardado como tu entrenador. Ahora elige Cancelar y Sí en la consola: no se intercambia nada.",
    "Saved as your trainer.": "Guardado como tu entrenador.",

    # catalog: FireRed / LeafGreen
    "FireRed & LeafGreen": "Rojo Fuego y Verde Hoja",
    "FireRed": "Rojo Fuego",
    "LeafGreen": "Verde Hoja",
    "English": "Inglés",
    "French": "Francés",
    "German": "Alemán",
    "Italian": "Italiano",
    "Spanish": "Español",
    "Japanese": "Japonés",
    "Korean": "Coreano",
    "Version": "Versión",
    "Console": "Consola",
    "Gift": "Regalo",
    "Channel": "Canal",
    "Trainer language": "Idioma del entrenador",
    "Read your trainer name, Trainer ID and Secret ID from the console, so the Pokemon built here are yours.":
        "Lee tu nombre, tu ID de entrenador y tu ID secreto desde la consola, para que los Pokémon que "
        "generes aquí sean tuyos.",
    "Start, then wait for 'Hosting Direct Corner' in the log.":
        "Presiona Empezar y espera a que el registro diga 'Hosting Direct Corner'.",
    "Pokemon Center 2F, third attendant, Direct Corner, Trade Center, Join Group, then pick POKELDN.":
        "Centro Pokémon, 2.º piso, tercer encargado, Direct Corner, Trade Center, Join Group y elige POKELDN.",
    "Your trainer card appears here as soon as the console joins.":
        "Tu tarjeta de entrenador aparece aquí en cuanto la consola se une.",
    "Walk to your seat at the trade table and press A. Leaving by the door instead leaves the console on "
    "'Please wait'.":
        "Camina hasta tu asiento en la mesa de intercambio y presiona A. Si sales por la puerta, la consola se "
        "queda en 'Please wait'.",
    "On the trade menu, choose Cancel and Yes: nothing is traded.":
        "En el menú de intercambio elige Cancelar y Sí: no se intercambia nada.",
    "Host a Direct Corner trade. The console joins pokeldn's group.":
        "Organiza un intercambio en el Direct Corner. La consola se une al grupo de pokeldn.",
    "Start the host and wait for 'Hosting Direct Corner' in the log.":
        "Inicia el anfitrión y espera a que el registro diga 'Hosting Direct Corner'.",
    "Choose the Pokemon to trade and confirm.": "Elige el Pokémon que vas a intercambiar y confirma.",
    "With several queued, trade again after each save; the host offers the next one.":
        "Si hay varios en cola, vuelve a intercambiar después de cada guardado; el anfitrión ofrece el siguiente.",
    "Back on the trade menu after the last save, wait for the host's prompt, then Cancel and Yes.":
        "De vuelta en el menú de intercambio tras el último guardado, espera el aviso del anfitrión y elige "
        "Cancelar y Sí.",
    "The game pokeldn's own trainer reports on the link, and the one the Pokemon is built for.":
        "El juego que informa el entrenador de pokeldn en la conexión, y para el que se genera el Pokémon.",
    "The language pokeldn's own trainer reports on the link.":
        "El idioma que informa el entrenador de pokeldn en la conexión.",
    "The wireless channel of the network pokeldn hosts.": "El canal inalámbrico de la red de pokeldn.",
    "Join a trade group the console leads.": "Únete a un grupo de intercambio que dirige la consola.",
    "Start the joiner first: it scans until the console appears.":
        "Inicia primero la búsqueda: busca hasta que aparece la consola.",
    "Pokemon Center 2F, third attendant, Direct Corner, Trade Center, Become Leader.":
        "Centro Pokémon, 2.º piso, tercer encargado, Direct Corner, Trade Center, Become Leader.",
    "Accept POKELDN when it appears, then choose and confirm.":
        "Acepta a POKELDN cuando aparezca, luego elige y confirma.",
    "With several queued, trade again after each save; the joiner offers the next one.":
        "Si hay varios en cola, vuelve a intercambiar después de cada guardado; pokeldn ofrece el siguiente.",
    "Send Pokemon, items or game boosts, back up or restore your save, or read your trainer IDs "
    "through Mystery Gift.":
        "Envía Pokémon, objetos o mejoras para el juego, respalda o restaura tu partida, o lee tus ID de "
        "entrenador por Regalo Misterioso.",
    "Title screen: Mystery Gift, Wonder Cards, Friend. For news: the second entry, Wonder News.":
        "Pantalla de título: Mystery Gift, Wonder Cards, Friend. Para noticias: la segunda opción, Wonder News.",
    "Start the host, then pick POKELDN when it appears.": "Inicia el anfitrión y elige POKELDN cuando aparezca.",
    "Answer Yes if the console asks to replace its card.": "Responde Sí si la consola pide reemplazar su tarjeta.",
    "For boosts, save backups and restores, readouts or your own console code, keep the app running "
    "until the Session log shows the result.":
        "Para mejoras, respaldos y restauraciones de partida, lecturas o código propio, deja la app "
        "funcionando hasta que el registro de la sesión muestre el resultado.",
    "Back out of the search screen between two runs.": "Sal de la pantalla de búsqueda entre dos envíos.",
    "The console's cartridge: another one is refused before anything is sent.":
        "El cartucho de la consola: si es otro, se rechaza antes de enviar nada.",
    "Pick a species; PKHeX builds a legal one for this game.":
        "Elige una especie; PKHeX genera uno legal para este juego.",
    "Add a trade to queue more: one session trades them in order.":
        "Agrega un intercambio para poner más en cola: una sesión los intercambia en orden.",
    "New PID each run": "PID nuevo en cada envío",
    "Time limit (seconds)": "Tiempo límite (segundos)",

    # settings
    "Language of the app": "Idioma de la app",
    "The language of every screen. Pokemon, moves and items keep your game's names.":
        "El idioma de todas las pantallas. Los Pokémon, movimientos y objetos conservan los nombres de tu juego.",
    "The app": "La app",
    "Your trainer": "Tu entrenador",
    "Your setup": "Tu configuración",
    "Storage": "Almacenamiento",
    "Bug reports": "Reportes de errores",
    "The original trainer of every Pokemon you build: read it from your console, or type it as your game's "
    "trainer card shows it.":
        "El entrenador original de cada Pokémon que generes: léelo desde tu consola o escríbelo tal como lo "
        "muestra la tarjeta de entrenador de tu juego.",
    "pokeldn's trainer on the link": "Entrenador de pokeldn en la conexión",
    "The partner your console sees during a trade or a gift. It is not your trainer: the Pokemon you build "
    "carry the trainer card above.":
        "El compañero que ve tu consola durante un intercambio o un regalo. No es tu entrenador: los Pokémon que "
        "generes llevan la tarjeta de entrenador de arriba.",
    "Switch keys": "Claves de Switch",
    "prod.keys dumped from your own console. Needed to talk to the games; it never leaves this computer.":
        "El prod.keys extraído de tu propia consola. Hace falta para hablar con los juegos y nunca sale de esta "
        "computadora.",
    "Received Pokemon": "Pokémon recibidos",
    "Open it": "Abrir",
    "Where the Pokemon a console sends you are saved.": "Dónde se guardan los Pokémon que te manda una consola.",
    "Local files": "Archivos locales",
    "Free space used by session records, logs, temporary offers and unused built Pokemon. Your received "
    "Pokemon, selected offers, keys, firmware and settings are kept.":
        "Libera el espacio de registros de sesión, logs, ofertas temporales y Pokémon generados sin usar. Tus "
        "Pokémon recibidos, ofertas elegidas, claves, firmware y ajustes se conservan.",
    "Record every session": "Grabar cada sesión",
    "Open the records": "Abrir los registros",
    "Keeps a small record of each session. When something fails, attach the latest file to your report.":
        "Guarda un pequeño registro de cada sesión. Si algo falla, adjunta el último archivo a tu reporte.",
    "Hide advanced settings": "Ocultar ajustes avanzados",
    "Show advanced settings": "Mostrar ajustes avanzados",
    "Serial speed": "Velocidad serie",
    "How fast the computer talks to the board. Keep the default unless a guide says otherwise.":
        "Qué tan rápido habla la computadora con la placa. Deja el valor normal salvo que una guía diga otra cosa.",
    "921600 (default)": "921600 (normal)",
    "1500000 (faster, needs a good cable)": "1500000 (más rápido, necesita buen cable)",
    "Record the board's serial traffic": "Grabar el tráfico serie de la placa",
    "Adds the board's counters and every serial message to the session record. Only for radio problems someone "
    "asked you to report.":
        "Agrega los contadores de la placa y cada mensaje serie al registro de la sesión. Solo para problemas de "
        "radio que alguien te pidió reportar.",
    "Pokemon sprites": "Sprites de Pokémon",
    "Clear the cache": "Vaciar la caché",
    "Sprites come from PokeAPI and are kept on this computer after the first download. The app works without "
    "them.":
        "Los sprites vienen de PokeAPI y se guardan en esta computadora después de la primera descarga. La app "
        "funciona sin ellos.",
    "About this app": "Acerca de esta app",
    "A Pokemon-styled edition of pokeldn {version} by Decryptu, for FireRed and LeafGreen. pokeldn is AGPLv3; "
    "Pokemon are checked with PKHeX.Core (GPLv3). Not affiliated with Nintendo, Game Freak or The Pokemon "
    "Company.":
        "Una edición con estilo Pokémon de pokeldn {version}, de Decryptu, para Rojo Fuego y Verde Hoja. pokeldn "
        "es AGPLv3; los Pokémon se revisan con PKHeX.Core (GPLv3). Sin relación con Nintendo, Game Freak ni The "
        "Pokémon Company.",
    "Checking local files...": "Revisando archivos locales...",
    "Clearing local files...": "Borrando archivos locales...",
    "Clear local files": "Borrar archivos locales",
    "Checking...": "Revisando...",
    "You have the latest version ({version}).": "Tienes la última versión ({version}).",
    "GitHub did not answer. Check your connection.": "GitHub no respondió. Revisa tu conexión.",
    "pokeldn {version} is available.": "pokeldn {version} está disponible.",
    "{n} files removed": "{n} archivos borrados",
    "{size} can be freed · {count} files": "Se pueden liberar {size} · {count} archivos",
    "No local files to clear.": "No hay archivos locales para borrar.",
    " Some folders could not be read.": " Algunas carpetas no se pudieron leer.",
    "Freed {size} · {n} files removed.": "Se liberaron {size} · {n} archivos borrados.",
    " {n} files could not be removed; try again.": " {n} archivos no se pudieron borrar; intenta otra vez.",
    " Files in use or changed since the check were kept.":
        " Se conservaron los archivos en uso o que cambiaron desde la revisión.",
    "Could not clear local files: {error}": "No se pudieron borrar los archivos locales: {error}",
    "Finish the current run or board check before clearing local files.":
        "Termina la sesión o la revisión de la placa antes de borrar archivos locales.",
    "Clear local files?": "¿Borrar archivos locales?",
    "Cancel": "Cancelar",
    "Clear files": "Borrar archivos",
    "Found": "Encontrado",
    "No file at this path": "No hay ningún archivo en esa ruta",
    "Remove {n} files and free about {size}. This deletes saved session records, logs, temporary offers and "
    "unused built Pokemon. Save any records needed for a bug report first. Your received Pokemon, selected "
    "offers, keys, firmware and settings are kept.":
        "Se borrarán {n} archivos y se liberarán unos {size}: registros de sesión, logs, ofertas temporales y "
        "Pokémon generados sin usar. Guarda antes los registros que necesites para un reporte. Tus Pokémon "
        "recibidos, ofertas elegidas, claves, firmware y ajustes se conservan.",
    "GitHub": "GitHub",
    "Discord": "Discord",
    "parts": "partes",

    # the game-style menu (gui/views/menu.py, screen.py, main.py)
    "TRADE": "INTERCAMBIAR",
    "Send or receive Pokemon": "Manda o recibe Pokémon",
    "MYSTERY GIFT": "REGALO MISTERIOSO",
    "Eggs, items and events": "Huevos, objetos y eventos",
    "POKEMON": "POKÉMON",
    "Build Pokemon for your save": "Genera Pokémon de tu partida",
    "MY TRAINER": "MI ENTRENADOR",
    "Read your TID and SID": "Lee tu TID y SID",
    "MY SAVE": "MI PARTIDA",
    "Back up and restore": "Respaldar y restaurar",
    "OPTIONS": "OPCIONES",
    "Board, language and keys": "Placa, idioma y claves",
    "Board ready on {port}": "Placa lista en {port}",
    "TRAINER ID": "ID ENTRENADOR",
    "SECRET ID": "ID SECRETO",
    "SHINY VALUE": "VALOR SHINY",
    "Trainer": "Entrenador",
    "Your trainer is not read yet": "Todavía no leíste tu entrenador",
    "Read your name, Trainer ID and Secret ID from the console.":
        "Lee tu nombre, tu ID de entrenador y tu ID secreto desde la consola.",
    "Read now": "Leer ahora",
    "READY TO TRADE": "LISTOS PARA INTERCAMBIAR",
    "Back": "Volver",
    "Back to the menu (Esc)": "Volver al menú (Esc)",
    "Guide": "Guía",
    "Move": "Mover",
    "Choose": "Elegir",
    "Build the Pokemon you will trade: they belong to your trainer.":
        "Genera los Pokémon que vas a intercambiar: son de tu entrenador.",
    "Copy your whole save to this computer, or put one back.":
        "Copia tu partida completa a esta computadora, o pon una de vuelta.",
    "Board, language, keys and the guide.": "Placa, idioma, claves y la guía.",
    "Trade them now": "Intercambiarlos ahora",
    "BANK": "BANCO",
    "Keep Pokemon between games": "Guarda Pokémon entre juegos",
    "Keep Pokemon on this computer and send them back to a game.":
        "Guarda Pokémon en esta computadora y mándalos de vuelta a un juego.",
    "Control": "Control",
    "Your console joins pokeldn, which meets your partner online":
        "Tu consola se une a pokeldn, que se encuentra con tu compañero por internet",
    "Trade (Online)": "Intercambio (en línea)",

    # the owner of built Pokemon
    "Built for your trainer: {name} · ID {tid}": "Se genera para tu entrenador: {name} · ID {tid}",
    "No trainer yet: built Pokemon will belong to pokeldn, not to you.":
        "Todavía no hay entrenador: los Pokémon generados serán de pokeldn, no tuyos.",
}

from gui.i18n_extra import ES_EXTRA  # noqa: E402
ES.update(ES_EXTRA)
