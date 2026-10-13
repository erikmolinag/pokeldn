"""Spanish for upstream 0.19-0.22 screens (plugins). Same rule as gui/i18n.py ES: the English text is the key;
gui/i18n.py merges this dict into ES."""
ES_PLUGINS = {
    # the Plugins page (gui/views/plugins.py)
    "How to make one": "Cómo crear uno",
    "Add a plugin": "Agregar un plugin",
    "Installed · {n}": "Instalados · {n}",
    "This pokeldn runs plugin API {major}.{level}.": "Este pokeldn usa la API de plugins {major}.{level}.",
    "Look for changes and updates": "Buscar cambios y actualizaciones",
    "Open the plugins folder": "Abrir la carpeta de plugins",
    "Drop a .pokeplugin file here": "Suelta aquí un archivo .pokeplugin",
    "Add a .pokeplugin file": "Agrega un archivo .pokeplugin",
    "Plugins add tools and radios made by other people. You see what a plugin is and accept its risks before "
    "anything is installed.":
        "Los plugins agregan herramientas y radios hechas por otras personas. Antes de instalar nada, ves qué es "
        "el plugin y aceptas sus riesgos.",
    "Choose a file": "Elegir un archivo",

    # a plugin's card
    "Version {version}": "Versión {version}",
    "by {author}": "de {author}",
    "plugin API {api}": "API de plugins {api}",
    "none": "ninguna",
    "Version {version} is out": "Ya salió la versión {version}",
    "Downloading": "Descargando",
    "Update to {version}": "Actualizar a la {version}",
    "Loaded from POKELDN_PLUGINS: it is on while that variable names it.":
        "Cargado desde POKELDN_PLUGINS: está activo mientras esa variable lo nombre.",
    "Installed as a Python package.": "Instalado como paquete de Python.",
    "Open its tools": "Abrir sus herramientas",
    "Update from a file": "Actualizar desde un archivo",
    "Show in folder": "Mostrar en la carpeta",
    "Visit its page": "Visitar su página",
    "Turn on": "Activar",
    "Turn off": "Desactivar",
    "Not compatible": "No compatible",
    "Failed": "Falló",
    "On": "Activo",
    "Added by hand": "Agregado a mano",
    "Off": "Inactivo",
    "{game} · {n} tool": "{game} · {n} herramienta",
    "{game} · {n} tools": "{game} · {n} herramientas",
    "{tool} in {game}": "{tool} en {game}",

    # the radio card
    "The board (default)": "La placa (predeterminada)",
    "{radio} (its plugin is off)": "{radio} (su plugin está desactivado)",
    "Radio": "Radio",
    "What carries the wireless messages": "Por dónde viajan los mensajes inalámbricos",
    "Keep the board unless a plugin's instructions say otherwise. The Games page shows the radio in use before "
    "you start.":
        "Deja la placa, salvo que las instrucciones de un plugin digan otra cosa. La página Juegos muestra la "
        "radio en uso antes de empezar.",

    # notices and error dialogs
    "Dismiss": "Descartar",
    "The radio is back to the board.": "La radio volvió a ser la placa.",
    "Plugins reloaded. Looking for updates.": "Plugins recargados. Buscando actualizaciones.",
    "{name} {version} did not download": "{name} {version} no se descargó",
    "Sessions now use {radio}.": "Las sesiones ahora usan {radio}.",
    "Sessions now use the board.": "Las sesiones ahora usan la placa.",
    "{name} cannot be turned on": "{name} no se puede activar",
    "{name} failed to load. Its error is on its card.": "{name} no cargó. Su error está en su tarjeta.",
    "{name} is on.": "{name} está activo.",
    "{name} is off. Its tools are hidden until you turn it on again.":
        "{name} está desactivado. Sus herramientas quedan ocultas hasta que lo vuelvas a activar.",
    "Not a plugin": "No es un plugin",
    "Drop a file ending in .pokeplugin.": "Suelta un archivo que termine en .pokeplugin.",
    "Choose a plugin": "Elige un plugin",
    "Update {name}": "Actualizar {name}",
    "{file} cannot be installed": "{file} no se puede instalar",
    "A different plugin": "Es otro plugin",
    "{file} is {name}, not an update of {expected}.": "{file} es {name}, no una actualización de {expected}.",
    "OK": "Aceptar",

    # the risk screen every install, update and first turn-on goes through
    "Reinstall": "Reinstalar",
    "Install older version": "Instalar versión anterior",
    "by an unnamed author": "de un autor sin nombre",
    "Updates {name} from {old} to {new}. What it saved is kept.":
        "Actualiza {name} de la {old} a la {new}. Lo que guardó se conserva.",
    "Version {version} is already installed; this replaces its files.":
        "La versión {version} ya está instalada; esto reemplaza sus archivos.",
    "Installs {version} over the newer {current}.": "Instala la {version} encima de la {current}, que es más nueva.",
    "This plugin was copied into the plugins folder by hand and was never checked in the app.":
        "Este plugin se copió a mano en la carpeta de plugins y nunca se revisó en la app.",
    "{file} · {n} files · {size}": "{file} · {n} archivos · {size}",
    "Plugins run with full access": "Los plugins se ejecutan con acceso total",
    "It runs as a program on this computer, with your account's access to every file, your prod.keys included.":
        "Se ejecuta como un programa en esta computadora, con el acceso de tu cuenta a todos tus archivos, "
        "incluido tu prod.keys.",
    "It can use the network, your board and the sessions you start.":
        "Puede usar la red, tu placa y las sesiones que inicies.",
    "pokeldn's guardrails stop a plugin deleting or overwriting your files and running erase commands, but a "
    "plugin written to get around them can.":
        "Las protecciones de pokeldn impiden que un plugin borre o sobrescriba tus archivos y ejecute comandos de "
        "borrado, pero un plugin hecho para saltárselas sí puede.",
    "pokeldn does not review or support plugins, and cannot undo what one does.":
        "pokeldn no revisa ni da soporte a los plugins, y no puede deshacer lo que uno haga.",
    "I know this file does not come from the author of the version I had, and I install it anyway.":
        "Sé que este archivo no viene del autor de la versión que tenía, y lo instalo de todos modos.",
    "I understand these risks, and I trust the author of this plugin.":
        "Entiendo estos riesgos y confío en el autor de este plugin.",
    "Turn it on after installing": "Activarlo después de instalar",

    # who signed the file
    "Signed by the same author": "Firmado por el mismo autor",
    "The same key {fingerprint} signed the version installed before.":
        "La misma clave {fingerprint} firmó la versión que estaba instalada.",
    "Signed by its author": "Firmado por su autor",
    "Signed with key {fingerprint}. If the author publishes their key, compare it. Every update must carry the "
    "same key.":
        "Firmado con la clave {fingerprint}. Si el autor publica su clave, compárala. Cada actualización debe "
        "traer la misma clave.",
    "Not signed": "Sin firma",
    "Nothing proves who made this file or that it was not changed since.":
        "Nada prueba quién hizo este archivo ni que no se haya modificado desde entonces.",
    "Signed by someone else": "Firmado por otra persona",
    "Signed with key {fingerprint}, not the key of the author of the version installed before. Someone else may "
    "have made this file.":
        "Firmado con la clave {fingerprint}, no con la del autor de la versión que estaba instalada. Puede que "
        "otra persona haya hecho este archivo.",
    "No longer signed": "Ya no está firmado",
    "The version installed before was signed by its author; this file is not. Someone else may have made it.":
        "La versión que estaba instalada la firmó su autor; este archivo no. Puede que lo haya hecho otra persona.",

    # what its code does (pokeldn/app/plugin_store.py scan)
    "What its code does": "Qué hace su código",
    "No network, program, deletion or hidden code found in its files. A reading of the code cannot prove a "
    "plugin safe.":
        "No se encontró uso de red, programas, borrados ni código oculto en sus archivos. Leer el código no "
        "puede probar que un plugin sea seguro.",
    "Has Python files pokeldn cannot read": "Tiene archivos Python que pokeldn no puede leer",
    "Uses the internet or the network": "Usa internet o la red",
    "Starts other programs": "Inicia otros programas",
    "Calls native code directly, which the guardrails cannot watch":
        "Llama directamente a código nativo, que las protecciones no pueden vigilar",
    "Deletes files": "Borra archivos",
    "Runs code it builds while running, which this check cannot read":
        "Ejecuta código que arma mientras corre, que esta revisión no puede leer",
    "Names your Switch keys file": "Menciona tu archivo de claves de Switch",
    "Ships {n} compiled file this check cannot read": "Trae {n} archivo compilado que esta revisión no puede leer",
    "Ships {n} compiled files this check cannot read":
        "Trae {n} archivos compilados que esta revisión no puede leer",

    # after the risk screen
    "{name} was not installed": "{name} no se instaló",
    "installed": "instalado",
    "updated to {version}": "actualizado a la {version}",
    "reinstalled": "reinstalado",
    "now at {version}": "en la {version}",
    "{name} is {done} but failed to load. Its error is on its card.":
        "{name} quedó {done}, pero no cargó. Su error está en su tarjeta.",
    "{name} is {done} and on.": "{name} quedó {done} y activo.",
    "{name} is {done}. Turn it on when you want its tools.":
        "{name} quedó {done}. Actívalo cuando quieras usar sus herramientas.",

    # removing
    "{name} was not removed": "{name} no se quitó",
    "{name} is removed.": "Se quitó {name}.",
    "Remove {name}?": "¿Quitar {name}?",
    "Its files are deleted from this computer and its tools leave the Games page. A session it is running keeps "
    "going until it ends.":
        "Sus archivos se borran de esta computadora y sus herramientas salen de la página Juegos. Una sesión que "
        "esté ejecutando sigue hasta que termine.",
    "Also delete what it saved ({size}); otherwise installing it again finds it.":
        "Borrar también lo que guardó ({size}); si no, al instalarlo otra vez lo encuentra.",

    # pokeldn/plugins.py compatibility()
    "plugin.toml names no plugin API version (api = 1).":
        "plugin.toml no indica una versión de la API de plugins (api = 1).",
    "It needs plugin API {api} and this pokeldn runs plugin API {here}. Update pokeldn to use it.":
        "Necesita la API de plugins {api} y este pokeldn usa la API de plugins {here}. Actualiza pokeldn para "
        "usarlo.",
    "It was written for plugin API {major}, which this pokeldn runs plugin API {here} no longer supports. "
    "Ask its author for a newer version.":
        "Se escribió para la API de plugins {major}, que este pokeldn (API de plugins {here}) ya no admite. "
        "Pídele a su autor una versión más nueva.",
    "It uses plugin API {major}, which {release} stops supporting. Ask its author for a newer version.":
        "Usa la API de plugins {major}, que {release} deja de admitir. Pídele a su autor una versión más nueva.",

    # pokeldn/app/plugin_store.py PackageError
    "The plugin package could not be read ({error}).": "No se pudo leer el paquete del plugin ({error}).",
    "The package is too large to be a plugin.": "El paquete es demasiado grande para ser un plugin.",
    "{file} is not a plugin package ({error}).": "{file} no es un paquete de plugin ({error}).",
    "The package holds an unsafe path or is too large: {error}":
        "El paquete tiene una ruta insegura o es demasiado grande: {error}",
    "The package has too much Python source to review safely.":
        "El paquete tiene demasiado código Python para revisarlo con seguridad.",
    "The package holds an unsafe path: {path}": "El paquete tiene una ruta insegura: {path}",
    "The package has no plugin.toml at its top.": "El paquete no tiene un plugin.toml en su raíz.",
    "The package holds several plugins; install them one by one.":
        "El paquete trae varios plugins; instálalos uno por uno.",
    "plugin.toml must sit at the top of the package, beside the plugin's files.":
        "plugin.toml debe estar en la raíz del paquete, junto a los archivos del plugin.",
    "plugin.toml does not parse: {error}": "plugin.toml no se puede leer: {error}",
    "plugin.toml needs an id of lowercase letters, digits, dots, dashes or underscores.":
        "plugin.toml necesita un id de minúsculas, dígitos, puntos, guiones o guiones bajos.",
    "The package has no {module}.py next to plugin.toml.": "El paquete no tiene {module}.py junto a plugin.toml.",
    "This plugin was changed after its author signed it, or its signature is damaged. Get it again from its "
    "author.":
        "Este plugin se modificó después de que su autor lo firmara, o su firma está dañada. Vuelve a "
        "conseguirlo de su autor.",
    "The package changed after it was checked.": "El paquete cambió después de revisarse.",
    "Only a plugin installed in the app can be removed here.":
        "Aquí solo se puede quitar un plugin instalado en la app.",

    # an update's download (pokeldn/app/plugin_updates.py, pokeldn/app/update.py)
    "the plugin download is invalid": "la descarga del plugin no es válida",
    "the download is too large to be a plugin": "la descarga es demasiado grande para ser un plugin",
    "the download redirected to an unsafe address": "la descarga redirigió a una dirección insegura",
    "the download is not an HTTPS address": "la descarga no es una dirección HTTPS",
    "the download took too long": "la descarga tardó demasiado",
}
