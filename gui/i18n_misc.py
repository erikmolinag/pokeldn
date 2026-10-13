"""Spanish for upstream 0.19-0.22 screens (misc). Same rule as gui/i18n.py ES: the English text is the key;
gui/i18n.py merges this dict into ES."""
ES_MISC = {
    # pop-ups (gui/popups.py translates each one's words as it shows): the programs the app starts, which a
    # pop-up's header names (gui/views/boards.py, gui/views/controller.py); the default button, "OK", is in
    # gui/i18n_plugins.py
    "Board installer": "Instalador de la placa",
    "Controller service": "Servicio del mando",

    # the app's own pop-ups (gui/main.py updated_notice, plugin_stopped_notice)
    "pokeldn updated to {version}": "pokeldn se actualizó a {version}",
    "The update did not install": "La actualización no se instaló",
    "pokeldn {version} could not replace this app: {error}. This app is unchanged.":
        "pokeldn {version} no pudo reemplazar esta app: {error}. Esta app no cambió.",
    "it opened the old version": "se abrió la versión anterior",
    "A plugin was turned off": "Se desactivó un plugin",
    "pokeldn closed or stopped answering last time while starting the plugin {name}. It is off now; turn it on "
    "again on the Plugins page once its author has a fix.":
        "La última vez, pokeldn se cerró o dejó de responder mientras iniciaba el plugin {name}. Ahora está "
        "desactivado; vuelve a activarlo en la página Plugins cuando su autor tenga una solución.",
    "Open Plugins": "Abrir Plugins",
    "Not now": "Ahora no",

    # the tools (gui/views/games.py)
    "From the plugin {name}": "Del plugin {name}",
    "Could not read the options: {error}": "No se pudieron leer las opciones: {error}",

    # pokeldn.app.command: what the checklist says is missing, and why a switch is held off
    "Choose the Mystery Gift Pokemon first.": "Primero elige el Pokémon del Regalo Misterioso.",
    "Code: all eight digits, or none.": "Código: los ocho dígitos, o ninguno.",
    "This gift is legal only with a handler, which its own trainer's save clears: it goes with your trainer.":
        "Este regalo solo es legal si tiene un entrenador actual, y la partida de su propio entrenador lo "
        "borra: se envía con tu entrenador.",
    "This gift has its card's own trainer and goes as made.":
        "Este regalo tiene el entrenador de su propia tarjeta y se envía tal como está.",

    # why a HOME gift's card goes without a HOME tracker (pokeldn.swsh.events.HOME_WHY); the tracker warnings
    # themselves (pokeldn.pokemon.HOME_TRACKER_WARNINGS) are in gui/i18n_gts.py, beside the bank
    "Pokemon HOME gave this gift with its own tracker. The console makes the Pokemon from this card without "
    "one, whatever the HOME tracker setting, and Pokemon HOME currently accepts it.":
        "Pokémon HOME dio este regalo con su propio rastreador. La consola crea el Pokémon de esta tarjeta sin "
        "uno, sin importar el ajuste del rastreador de HOME, y por ahora Pokémon HOME lo acepta.",
}
