"""All profile content in English and German.

Edit text here, then rebuild:
  uv run --with fonttools --with brotli python .github/scripts/build_assets.py
  uv run python .github/scripts/build_readme.py
The tech stack lives in tech.py.
"""

LANGS = ("en", "de")

# What I'm working on right now. Shown in the hero inspector ("Currently building").
# You can also edit it directly in the hero SVGs: search for "STATUS".
STATUS = "Tellersonne"

LINKS = {
    "company": "https://www.uplytech.de",
    "linkedin": "https://www.linkedin.com/in/tim-hauke-b3b24b2b5",
    "email": "timhauke@uplytech.de",          # UplyTech, direct
    "email_company": "contact@uplytech.de",   # UplyTech, general
    "email_private": "timhauke99@gmail.com",  # personal, not UplyTech
    "discord": "https://discord.gg/DtHPAEHxZk",
    "profile": "https://github.com/VectoDE",
}

HERO = {
    "en": dict(
        roles=["Founder & managing director of UplyTech", "Full-stack developer since 2017", "Web apps, APIs and Discord bots",
               "AI, automation and SaaS"],
        intro=["I plan, build and run software for companies,", "from the first sketch to the server it runs on."],
        available="Available for projects",
        panel_tabs=("Design", "Inspect"),
        layer="Frame",
        profile_title="Profile",
        profile=[("Role", "Founder & developer"), ("Company", "UplyTech"), ("Based in", "Itzehoe, Germany"),
                 ("Building since", "2017"), ("Languages", "German, English")],
        stack_title="Stack",
        status_title="Currently building",
        zoom="Fit",
    ),
    "de": dict(
        roles=["Gründer & Geschäftsführer von UplyTech", "Full-Stack-Entwickler seit 2017", "Web-Apps, APIs und Discord-Bots",
               "KI, Automatisierung und SaaS"],
        intro=["Ich plane, entwickle und betreibe Software für", "Unternehmen, vom ersten Entwurf bis zum Server."],
        available="Offen für Projekte",
        panel_tabs=("Design", "Prüfen"),
        layer="Rahmen",
        profile_title="Profil",
        profile=[("Rolle", "Gründer & Entwickler"), ("Firma", "UplyTech"), ("Standort", "Itzehoe"),
                 ("Aktiv seit", "2017"), ("Sprachen", "Deutsch, Englisch")],
        stack_title="Stack",
        status_title="Aktuelles Projekt",
        zoom="Einpassen",
    ),
}
HERO_STACK = ["TypeScript", "Next.js", "Node.js", "Python", "Go", "Docker", "Cloudflare"]

SECTIONS = {
    "about": {"en": ("About me", "who and where"), "de": ("Über mich", "wer und wo")},
    "hire": {"en": ("For recruiters and clients", "roles, focus, contact"), "de": ("Für Recruiter und Kunden", "Rollen, Schwerpunkte, Kontakt")},
    "services": {"en": ("What I do", "for clients"), "de": ("Was ich mache", "für Kunden")},
    "projects": {"en": ("Featured projects", "selected work"), "de": ("Ausgewählte Projekte", "eine Auswahl")},
    "timeline": {"en": ("Timeline", "2014 to today"), "de": ("Werdegang", "2014 bis heute")},
    "stack": {"en": ("Tech stack", "everything I have worked with"), "de": ("Tech-Stack", "alles, womit ich gearbeitet habe")},
    "certificates": {"en": ("Certifications", "{count} certificates"), "de": ("Zertifikate", "{count} Nachweise")},
    "stats": {"en": ("GitHub activity", "updated daily"), "de": ("GitHub-Aktivität", "täglich aktualisiert")},
    "orgs": {"en": ("Organisations", "teams and communities"), "de": ("Organisationen", "Teams und Communitys")},
    "links": {"en": ("Find me elsewhere", "social, video, code"), "de": ("Hier findest du mich", "Social, Video, Code")},
    "support": {"en": ("Support my work", "sponsors and tips"), "de": ("Unterstützen", "Sponsoring und Trinkgeld")},
}

# key, name, repo/site url, icon, status {en, de}, text {en, de}, stack
PROJECTS = [
    ("tellersonne", "Tellersonne", "https://tellersonne.app", "sun",
     {"en": "Live at tellersonne.app", "de": "Live auf tellersonne.app"},
     {"en": "A calm cooking app for iOS, Android and tablets, with public recipe pages and a web admin panel. No ads, no tracking.",
      "de": "Eine ruhige Koch-App für iOS, Android und Tablets, mit öffentlichen Rezeptseiten und Web-Adminbereich. Ohne Werbung, ohne Tracking."},
     ["TypeScript", "Cloudflare", "iOS", "Android"]),
    ("vectobeat", "VectoBeat", "https://vectobeat.uplytech.de", "wave",
     {"en": "Live and open source", "de": "Live und Open Source"},
     {"en": "Discord music bot with Lavalink v4 audio, playlists, fast queue handling and a dynamic equalizer, plus a Next.js control panel.",
      "de": "Discord-Musikbot mit Lavalink-v4-Audio, Playlists, schneller Warteschlange und dynamischem Equalizer, dazu ein Next.js-Control-Panel."},
     ["Python", "discord.py", "Lavalink", "Next.js"]),
    ("nodcord", "NodCord", "https://github.com/VectoDE/NodCord", "nodes",
     {"en": "Open source", "de": "Open Source"},
     {"en": "An Express API with a built-in Discord bot and dashboard. Your frontend runs inside the API or on its own.",
      "de": "Eine Express-API mit eingebautem Discord-Bot und Dashboard. Dein Frontend läuft in der API oder eigenständig."},
     ["TypeScript", "Express", "discord.js"]),
    ("servercommander", "ServerCommander", "https://github.com/VectoDE/ServerCommander", "terminal",
     {"en": "Open source", "de": "Open Source"},
     {"en": "A modular command-line tool for managing local and remote servers over SSH, FTP and more.",
      "de": "Ein modulares Kommandozeilen-Tool, mit dem du lokale und entfernte Server per SSH, FTP und mehr verwaltest."},
     ["Go", "CLI", "SSH"]),
    ("self-updater", "Self-Updater", "https://github.com/VectoDE/Self-Updater", "sync",
     {"en": "Open source", "de": "Open Source"},
     {"en": "Watches a GitHub or GitLab repository and updates your app under PM2 or Docker when something new lands.",
      "de": "Beobachtet ein GitHub- oder GitLab-Repository und aktualisiert deine App unter PM2 oder Docker, sobald etwas Neues kommt."},
     ["TypeScript", "PM2", "Docker"]),
    ("linux-setup", "Linux Server Setup", "https://github.com/VectoDE/Linux-Server-Setup-Script", "server",
     {"en": "Open source", "de": "Open Source"},
     {"en": "Turns a fresh Debian, Ubuntu, CentOS or RHEL machine into a production web server with Nginx, PHP, MySQL, Node.js, Fail2Ban and SSL.",
      "de": "Macht aus einer frischen Debian-, Ubuntu-, CentOS- oder RHEL-Maschine einen Produktions-Webserver mit Nginx, PHP, MySQL, Node.js, Fail2Ban und SSL."},
     ["Shell", "Nginx", "Linux"]),
    ("portfolio", "Portfolio", "https://github.com/VectoDE/Portfolio", "window",
     {"en": "Open source", "de": "Open Source"},
     {"en": "Portfolio site with its own dashboard and API for managing projects and content.",
      "de": "Portfolio-Website mit eigenem Dashboard und eigener API für Projekte und Inhalte."},
     ["TypeScript", "Next.js", "Express", "Prisma"]),
    ("vectolyncloud", "VectolynCloud", "https://github.com/VectoDE/VectolynCloud", "server",
     {"en": "Open source, OpenSSF passing", "de": "Open Source, OpenSSF Passing"},
     {"en": "Kit for running your own Minecraft network. Its own cloud manages proxies, servers and plugins, and Java and Bedrock players play together.",
      "de": "Baukasten für ein eigenes Minecraft-Netzwerk. Die eigene Cloud verwaltet Proxys, Server und Plugins, Java- und Bedrock-Spieler spielen zusammen."},
     ["Java", "Gradle", "Docker"]),
    ("relationnotes", "RelationNotes", "https://github.com/VectoDE/Notebook-LM-Klon", "nodes",
     {"en": "Open source", "de": "Open Source"},
     {"en": "Research notebook in the style of NotebookLM: hybrid search over your own sources, running as one Cloudflare Worker with D1 and R2.",
      "de": "Recherche-Notizbuch nach dem Vorbild von NotebookLM: hybride Suche über eigene Quellen, läuft als ein Cloudflare Worker mit D1 und R2."},
     ["TypeScript", "Hono", "Cloudflare"]),
    ("lifeverse", "LifeVerse", "https://github.com/VectoDE/LifeVerse", "orbit",
     {"en": "Game, partly in concept", "de": "Spiel, teilweise in Konzeption"},
     {"en": "Concept for an open-world life simulator with a dynamic story, AI-driven characters and multiplayer.",
      "de": "Konzept für eine Open-World-Lebenssimulation mit dynamischer Story, KI-gesteuerten Figuren und Mehrspieler-Modus."},
     ["Game design", "Multiplayer"]),
]

TIMELINE = {
    "en": [("2014", ["First contact with", "computers and tech"]), ("2016", ["Learned to code", "from YouTube"]),
           ("2017", ["Founded the", "PlayGS network"]), ("2021", ["First", "certificates"]),
           ("2023", ["PHP, Laravel, Linux,", "volunteer CMO"]), ("2024", ["NodCord and the", "UplyTech API"]),
           ("2025", ["VectoBeat and", "new UplyTech site"]), ("2026", ["Started", "Tellersonne"])],
    "de": [("2014", ["Erster Kontakt mit", "Computern und Technik"]), ("2016", ["Programmieren", "über YouTube gelernt"]),
           ("2017", ["Gründung des", "PlayGS-Netzwerks"]), ("2021", ["Erste", "Zertifikate"]),
           ("2023", ["PHP, Laravel, Linux,", "ehrenamtl. CMO"]), ("2024", ["NodCord und die", "UplyTech-API"]),
           ("2025", ["VectoBeat und neue", "UplyTech-Website"]), ("2026", ["Start von", "Tellersonne"])],
}
TODAY = {"en": "Today", "de": "Heute"}

FOOTER = {
    "en": dict(head="Have a project in mind?", sub="Write in German or English. UplyTech requests go to the company addresses.",
               business="UplyTech", private="Personal"),
    "de": dict(head="Du hast ein Projekt im Kopf?", sub="Schreib auf Deutsch oder Englisch. Anfragen zu UplyTech bitte an die Firmenadressen.",
               business="UplyTech", private="Privat"),
}

LANG_SWITCH = {"en": "English", "de": "Deutsch"}

STATS = {
    "en": dict(title="GitHub activity", updated="Updated", contributions="contributions, last year",
               commits="commits, last year", streak="days in a row, now",
               repos="public repositories", stars="stars", followers="followers",
               weekly="Contributions per week", busiest="Busiest week",
               languages="Languages in my public repositories and those of UplyTech and PlayGS",
               other="Other", date_fmt="%d %b %Y"),
    "de": dict(title="GitHub-Aktivität", updated="Aktualisiert", contributions="Beiträge, letztes Jahr",
               commits="Commits, letztes Jahr", streak="Tage in Folge, aktuell",
               repos="öffentliche Repositories", stars="Sterne", followers="Follower",
               weekly="Beiträge pro Woche", busiest="Stärkste Woche",
               languages="Sprachen in meinen öffentlichen Repositories und denen von UplyTech und PlayGS",
               other="Andere", date_fmt="%d.%m.%Y"),
}

CODING_SINCE = 2016

AWARDS = {
    "en": dict(title="Milestones", years="years of coding", certs="certificates", streak="days best streak",
               langs="languages on GitHub", projects="featured projects", gold="Gold", silver="Silver", bronze="Bronze"),
    "de": dict(title="Meilensteine", years="Jahre Programmieren", certs="Zertifikate", streak="Tage beste Serie",
               langs="Sprachen auf GitHub", projects="vorgestellte Projekte", gold="Gold", silver="Silber", bronze="Bronze"),
}

# ---------------------------------------------------------------- README text

LI_CERTS = "https://www.linkedin.com/in/tim-hauke-b3b24b2b5/details/certifications/"

TEXT = {
    "en": dict(
        hero_alt="Tim Hauke (VectoDE): founder of UplyTech and full-stack developer from Itzehoe, Germany",
        about=[
            "I'm Tim, a self-taught full-stack developer from Itzehoe in northern Germany. I run [UplyTech](https://www.uplytech.de), "
            "an IT service company that builds websites, web apps, APIs and custom software for clients, and then hosts and maintains what it ships.",
            "My first contact with computers and tech came in 2014, and in 2016 I started teaching myself to code from YouTube tutorials. That led to "
            "[PlayGS](https://www.playgs.de) in 2017, a Minecraft network with its own plugins, a shop and a TeamSpeak, which I still run. "
            "Before all of this took over my evenings I played football for SSC Phönix Kisdorf. Most of my own projects started as fixes "
            "for my own problems, like a music bot for my Discord server or a script that redeploys apps when I push. "
            "Most of my time right now goes into **Tellersonne**, my cooking app for iOS and Android, live at [tellersonne.app](https://tellersonne.app).",
        ],
        facts=[("Based in", "Itzehoe, Schleswig-Holstein, Germany"),
               ("Company", "Founder and managing director of [UplyTech](https://www.uplytech.de)"),
               ("Working on", "[Tellersonne](https://tellersonne.app), recipes without ads or tracking"),
               ("Day-to-day stack", "TypeScript, Next.js, Node.js, Python, Go, Prisma, Docker, Cloudflare"),
               ("Stacks", "MEVN, MERN, MEEN and MENN, plus Electron, TypeScript, MySQL, Prisma and Tailwind CSS"),
               ("Languages", "German (native), English"),
               ("Open to", "Client projects and collaborations on web apps, software, APIs and Discord bots"),
               ("Fun fact", "I like taking a system that grew messy and making it fast and easy to scale"),
               ("Contact", "UplyTech: [contact@uplytech.de](mailto:contact@uplytech.de) or [timhauke@uplytech.de](mailto:timhauke@uplytech.de). "
                           "Personal, not UplyTech: [timhauke99@gmail.com](mailto:timhauke99@gmail.com)")],
        services=[
            "Company websites, web apps and dashboards, usually Next.js, React or Vue with a Node.js or Laravel backend",
            "Custom software such as internal tools, admin panels, CLIs and Electron desktop apps",
            "REST and GraphQL APIs with authentication, and Discord bots with their own web dashboard",
            "Linux servers with Docker and Nginx, CI/CD on GitHub Actions, hosting and technical support",
            "AI and automation: connecting tools, automating repetitive work and building SaaS products around it",
            "IT consulting when you need to pick a stack, scope a project or clean up an existing codebase",
        ],
        project_links="Live sites",
        projects_short="Every project in one sentence",
        hire_intro="Looking to hire me, or to start a project with UplyTech? These are the facts recruiters and clients ask for first.",
        hire=[("Roles", "Full-stack and backend development, DevOps and server operations. On the web projects I deliver through UplyTech I also plan and lead the technical side"),
              ("Day to day", "Development, deployment and operations for [UplyTech](https://www.uplytech.de) clients, from the interface to the server"),
              ("Main stack", "TypeScript with Next.js, React and Node.js · Python with FastAPI and discord.py · Go for command-line tools · "
                               "PostgreSQL and Prisma · Docker, Linux and Cloudflare · CI with CodeQL, OpenSSF Scorecard and signed releases"),
              ("Typical work", "Company websites and web apps, admin dashboards, REST APIs, Discord bots with a web dashboard, "
                               "Linux servers with monitoring"),
              ("Experience", "Coding since 2016, self-taught. Running live services since 2017, starting with the PlayGS Minecraft network"),
              ("Proof", "{count} course certificates from Programming Hub, LinkedIn Learning and freeCodeCamp, {pdfs} of them with a PDF, public code in the repositories below, and "
                        "[VectolynCloud](https://www.bestpractices.dev/projects/16102) with the OpenSSF Best Practices badge (passing)"),
              ("Availability", "Open to client projects and collaborations"),
              ("Location and languages", "Itzehoe, Germany · German (native), English"),
              ("Contact", "[contact@uplytech.de](mailto:contact@uplytech.de) or [LinkedIn](https://www.linkedin.com/in/tim-hauke-b3b24b2b5)")],
        smaller="Smaller tools and templates",
        smaller_head=("Project", "What it does", "Language"),
        smaller_rows=[
            ("PHP-API", "REST API with SQLite storage, JWT login and user management", "PHP"),
            ("Password-Checker", "Checks whether a password shows up in known leaks and how strong it is", "Go"),
            ("ID-Generator", "Builds custom IDs from your own pattern, for example `KG [project]#1-2 [role]\\2024`", "JavaScript"),
            ("ExpressJS-Template", "Starting point for Node.js web apps on Express", "JavaScript"),
            ("HTML-Template", "One `index.html` that shows nearly every HTML5 element with accessibility best practices", "HTML"),
            ("Homelab-Stack", "My homelab setup (work in progress)", ""),
        ],
        timeline_text="Timeline as text",
        timeline_rows=[
            ("2014", "First contact with computers and tech"),
            ("2016", "Started learning to code from YouTube tutorials"),
            ("2017", "Founded [PlayGS](https://www.playgs.de), a Minecraft network with every game mode on one server, own plugins, a shop and TeamSpeak"),
            ("2021", "First certificates in HTML, Node.js and building websites"),
            ("2023", "Worked through PHP, Laravel, Java, Linux, networking, Git and GraphQL. Volunteer CMO at BonToGo (Nov 2023 to Jun 2024): marketing plan and social media"),
            ("2024", "Released NodCord and built the UplyTech API. Courses on LinkedIn Learning and the freeCodeCamp Responsive Web Design certification"),
            ("2025", "ServerCommander, my portfolio, the Linux setup script and Self-Updater. Relaunched the UplyTech website, founded the esports club MitFits Gaming and shipped VectoBeat"),
            ("2026", "Handed MitFits Gaming over to a community member and started Tellersonne"),
        ],
        core_label="First choice on client work",
        stack_intro="Everything I have worked with, sorted by area. Icons come from skillicons.dev; anything without an icon there gets a text badge.",
        stack_details="All {count} entries as text, with where each one is used",
        stack_legend="A repository link means you can read that code yourself. *private repo* means it is in my own code, "
                     "but the repository is not public. No note means I have worked with it, but there is no public code to show.",
        private_label="private repo",
        ideas="Languages I have not used yet, each with project ideas I might build: [PROJECT-IDEAS.md](PROJECT-IDEAS.md)",
        certs_intro="{count} certificates from Programming Hub (Google Developers Launchpad), LinkedIn Learning (some accredited by PMI) "
                    "and freeCodeCamp. The PDFs are in [`/certificates`](certificates).",
        cert_head=("Certificate", "Issuer", "Issued", "Proof"),
        cert_groups=["Web development", "Infrastructure and tools", "Marketing, business and law", "Communication"],
        proof=("PDF", "Verify", "LinkedIn"),
        stats_alt="GitHub activity: contributions and commits in the last year, current streak, repositories, stars, followers and languages",
        stats_note="Built from the GitHub API by a daily workflow in this repository.",
        org_head=("Organisation", "Role"),
        orgs=[("UplyTech", "https://github.com/UplyTech", "Founder. IT services: development, design, video and marketing ([www.uplytech.de](https://www.uplytech.de))"),
              ("PlayGS Netzwerk", "https://github.com/PlayGS-Netzwerk", "Founder since 2017. Minecraft network with every game mode in one place ([playgs.de](https://www.playgs.de))"),
              ("ServerwerkNET", "https://github.com/ServerwerkNET", "Development organisation for [serverwerk.net](https://serverwerk.net)"),
              ("MitFits Gaming", "https://github.com/Mitfits-Gaming", "Founded the esports club in April 2025, handed over in September 2026")],
        link_rows=["Social", "Video and music", "Gaming", "Code", "UplyTech"],
        support="If one of my tools saved you time, you can support my open-source work here.",
        footer_alt="Have a project in mind? UplyTech: contact@uplytech.de, timhauke@uplytech.de. Personal: timhauke99@gmail.com",
        views="Profile views",
        made_by="Made by VectoDE, founder of UplyTech",
        trophies_alt="Milestones: years of coding, certificates, longest streak, languages and projects",
        month={"Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "May": "May", "Jun": "Jun", "Jul": "Jul",
               "Aug": "Aug", "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dec"},
    ),
    "de": dict(
        hero_alt="Tim Hauke (VectoDE): Gründer von UplyTech und Full-Stack-Entwickler aus Itzehoe",
        about=[
            "Ich bin Tim, Full-Stack-Entwickler aus Itzehoe und habe mir das Programmieren selbst beigebracht. Ich führe [UplyTech](https://www.uplytech.de), "
            "einen IT-Dienstleister, der Websites, Web-Apps, APIs und individuelle Software für Kunden baut und das Ergebnis danach auch hostet und pflegt.",
            "2014 hatte ich den ersten Kontakt mit Computern und Technik, 2016 habe ich angefangen, mir das Programmieren mit YouTube-Tutorials beizubringen. Daraus wurde 2017 "
            "[PlayGS](https://www.playgs.de), ein Minecraft-Netzwerk mit eigenen Plugins, Shop und TeamSpeak, das ich bis heute betreibe. "
            "Bevor das meine Abende gefüllt hat, habe ich beim SSC Phönix Kisdorf Fußball gespielt. Die meisten meiner eigenen Projekte "
            "sind aus eigenen Problemen entstanden, etwa ein Musikbot für meinen Discord-Server oder ein Skript, das Apps nach jedem Push neu ausrollt. "
            "Die meiste Zeit steckt gerade in **Tellersonne**, meiner Koch-App für iOS und Android, live auf [tellersonne.app](https://tellersonne.app).",
        ],
        facts=[("Standort", "Itzehoe, Schleswig-Holstein"),
               ("Firma", "Gründer und Geschäftsführer von [UplyTech](https://www.uplytech.de)"),
               ("Aktuelles Projekt", "[Tellersonne](https://tellersonne.app), Rezepte ohne Werbung und Tracking"),
               ("Täglicher Stack", "TypeScript, Next.js, Node.js, Python, Go, Prisma, Docker, Cloudflare"),
               ("Stacks", "MEVN, MERN, MEEN und MENN, dazu Electron, TypeScript, MySQL, Prisma und Tailwind CSS"),
               ("Sprachen", "Deutsch (Muttersprache), Englisch"),
               ("Offen für", "Kundenprojekte und Zusammenarbeit bei Web-Apps, Software, APIs und Discord-Bots"),
               ("Fun Fact", "Ich nehme gern ein System, das unübersichtlich gewachsen ist, und mache es schnell und skalierbar"),
               ("Kontakt", "UplyTech: [contact@uplytech.de](mailto:contact@uplytech.de) oder [timhauke@uplytech.de](mailto:timhauke@uplytech.de). "
                           "Privat, nicht UplyTech: [timhauke99@gmail.com](mailto:timhauke99@gmail.com)")],
        services=[
            "Firmenwebsites, Web-Apps und Dashboards, meist mit Next.js, React oder Vue und einem Backend in Node.js oder Laravel",
            "Individuelle Software wie interne Tools, Adminbereiche, CLIs und Desktop-Apps mit Electron",
            "REST- und GraphQL-APIs mit Authentifizierung sowie Discord-Bots mit eigenem Web-Dashboard",
            "Linux-Server mit Docker und Nginx, CI/CD über GitHub Actions, Hosting und technischer Support",
            "KI und Automatisierung: Tools verbinden, wiederkehrende Arbeit automatisieren und SaaS-Produkte darauf aufbauen",
            "IT-Beratung, wenn ein Stack gewählt, ein Projekt geplant oder eine bestehende Codebasis aufgeräumt werden soll",
        ],
        project_links="Live-Seiten",
        projects_short="Alle Projekte in einem Satz",
        hire_intro="Du willst mich einstellen oder ein Projekt mit UplyTech starten? Hier stehen die Angaben, nach denen Recruiter und Kunden zuerst fragen.",
        hire=[("Rollen", "Full-Stack- und Backend-Entwicklung, DevOps und Serverbetrieb. Bei Webprojekten, die ich über UplyTech umsetze, übernehme ich auch die technische Planung und Leitung"),
              ("Im Alltag", "Entwicklung, Auslieferung und Betrieb für Kunden von [UplyTech](https://www.uplytech.de), von der Oberfläche bis zum Server"),
              ("Hauptstack", "TypeScript mit Next.js, React und Node.js · Python mit FastAPI und discord.py · Go für Kommandozeilen-Tools · "
                                  "PostgreSQL und Prisma · Docker, Linux und Cloudflare · CI mit CodeQL, OpenSSF Scorecard und signierten Releases"),
              ("Typische Aufträge", "Firmenwebsites und Web-Apps, Admin-Dashboards, REST-APIs, Discord-Bots mit Web-Dashboard, "
                                    "Linux-Server mit Monitoring"),
              ("Erfahrung", "Ich programmiere seit 2016 und habe es mir selbst beigebracht. Seit 2017 laufen Dienste von mir im Dauerbetrieb, "
                            "angefangen mit dem Minecraft-Netzwerk PlayGS"),
              ("Nachweise", "{count} Kurszertifikate von Programming Hub, LinkedIn Learning und freeCodeCamp, {pdfs} davon mit PDF, öffentlicher Code in den Repositories weiter unten und "
                            "[VectolynCloud](https://www.bestpractices.dev/projects/16102) mit dem OpenSSF-Best-Practices-Badge (Passing)"),
              ("Verfügbarkeit", "Offen für Kundenprojekte und Zusammenarbeit"),
              ("Standort und Sprachen", "Itzehoe · Deutsch (Muttersprache), Englisch"),
              ("Kontakt", "[contact@uplytech.de](mailto:contact@uplytech.de) oder [LinkedIn](https://www.linkedin.com/in/tim-hauke-b3b24b2b5)")],
        smaller="Kleinere Tools und Vorlagen",
        smaller_head=("Projekt", "Was es macht", "Sprache"),
        smaller_rows=[
            ("PHP-API", "REST-API mit SQLite, JWT-Login und Benutzerverwaltung", "PHP"),
            ("Password-Checker", "Prüft, ob ein Passwort in bekannten Leaks auftaucht und wie stark es ist", "Go"),
            ("ID-Generator", "Erzeugt IDs nach eigenem Muster, zum Beispiel `KG [project]#1-2 [role]\\2024`", "JavaScript"),
            ("ExpressJS-Template", "Ausgangspunkt für Node.js-Web-Apps mit Express", "JavaScript"),
            ("HTML-Template", "Eine `index.html`, die fast jedes HTML5-Element mit Barrierefreiheits-Best-Practices zeigt", "HTML"),
            ("Homelab-Stack", "Mein Homelab-Setup (im Aufbau)", ""),
        ],
        timeline_text="Werdegang als Text",
        timeline_rows=[
            ("2014", "Erster Kontakt mit Computern und Technik"),
            ("2016", "Mit YouTube-Tutorials angefangen, programmieren zu lernen"),
            ("2017", "[PlayGS](https://www.playgs.de) gegründet, ein Minecraft-Netzwerk mit allen Spielmodi auf einem Server, eigenen Plugins, Shop und TeamSpeak"),
            ("2021", "Erste Zertifikate in HTML, Node.js und Website-Erstellung"),
            ("2023", "PHP, Laravel, Java, Linux, Netzwerke, Git und GraphQL gelernt. Ehrenamtlicher CMO bei BonToGo (Nov. 2023 bis Juni 2024): Marketingplan und Social Media"),
            ("2024", "NodCord veröffentlicht und die UplyTech-API gebaut. Kurse bei LinkedIn Learning und die Zertifizierung Responsive Web Design von freeCodeCamp"),
            ("2025", "ServerCommander, mein Portfolio, das Linux-Setup-Skript und Self-Updater. Neue UplyTech-Website, Gründung des E-Sport-Clubs MitFits Gaming und Start von VectoBeat"),
            ("2026", "MitFits Gaming an ein Community-Mitglied übergeben und mit Tellersonne begonnen"),
        ],
        core_label="Erste Wahl bei Kundenprojekten",
        stack_intro="Alles, womit ich gearbeitet habe, nach Bereichen sortiert. Die Icons stammen von skillicons.dev; was dort kein Icon hat, bekommt ein Text-Badge.",
        stack_details="Alle {count} Einträge als Text, mit Fundstelle",
        stack_legend="Ein Repository-Link heißt: Den Code kannst du selbst lesen. *privates Repo* heißt: Es steckt in meinem eigenen Code, "
                     "das Repository ist aber nicht öffentlich. Ohne Vermerk: Ich habe damit gearbeitet, es gibt nur keinen öffentlichen Code dazu.",
        private_label="privates Repo",
        ideas="Sprachen, die ich noch nicht genutzt habe, jeweils mit Projektideen, die ich vielleicht umsetze: [PROJECT-IDEAS.de.md](PROJECT-IDEAS.de.md)",
        certs_intro="{count} Zertifikate von Programming Hub (Google Developers Launchpad), LinkedIn Learning (teilweise PMI-akkreditiert) "
                    "und freeCodeCamp. Die PDFs liegen in [`/certificates`](certificates).",
        cert_head=("Zertifikat", "Aussteller", "Datum", "Nachweis"),
        cert_groups=["Webentwicklung", "Infrastruktur und Werkzeuge", "Marketing, Business und Recht", "Kommunikation"],
        proof=("PDF", "Prüfen", "LinkedIn"),
        stats_alt="GitHub-Aktivität: Beiträge und Commits im letzten Jahr, aktuelle Serie, Repositories, Sterne, Follower und Sprachen",
        stats_note="Wird täglich von einem Workflow in diesem Repository aus der GitHub-API erzeugt.",
        org_head=("Organisation", "Rolle"),
        orgs=[("UplyTech", "https://github.com/UplyTech", "Gründer. IT-Dienstleistungen: Entwicklung, Design, Video und Marketing ([www.uplytech.de](https://www.uplytech.de))"),
              ("PlayGS Netzwerk", "https://github.com/PlayGS-Netzwerk", "Gründer seit 2017. Minecraft-Netzwerk mit allen Spielmodi an einem Ort ([playgs.de](https://www.playgs.de))"),
              ("ServerwerkNET", "https://github.com/ServerwerkNET", "Entwicklungsorganisation für [serverwerk.net](https://serverwerk.net)"),
              ("MitFits Gaming", "https://github.com/Mitfits-Gaming", "E-Sport-Club im April 2025 gegründet, im September 2026 übergeben")],
        link_rows=["Social Media", "Video und Musik", "Gaming", "Code", "UplyTech"],
        support="Wenn dir eines meiner Tools Zeit gespart hat, kannst du meine Open-Source-Arbeit hier unterstützen.",
        footer_alt="Du hast ein Projekt im Kopf? UplyTech: contact@uplytech.de, timhauke@uplytech.de. Privat: timhauke99@gmail.com",
        views="Profilaufrufe",
        made_by="Gemacht von VectoDE, Gründer von UplyTech",
        trophies_alt="Meilensteine: Jahre Programmieren, Zertifikate, längste Serie, Sprachen und Projekte",
        month={"Jan": "Jan.", "Feb": "Feb.", "Mar": "März", "Apr": "Apr.", "May": "Mai", "Jun": "Juni", "Jul": "Juli",
               "Aug": "Aug.", "Sep": "Sep.", "Oct": "Okt.", "Nov": "Nov.", "Dec": "Dez."},
    ),
}

# Badges: (key, icon, label or None, value, link or None). Icons are in icons.json
# (Simple Icons) or drawn in build_assets.py (globe, mail, pin, code, building, award, chat, live).
BADGES = {
    "contact": [
        ("web", "globe", None, "www.uplytech.de", LINKS["company"]),
        ("linkedin", "linkedin", None, "Tim Hauke", LINKS["linkedin"]),
        ("discord", "discord", None, {"en": "Join the server", "de": "Zum Server"}, LINKS["discord"]),
        ("mail-company", "mail", "UplyTech", LINKS["email_company"], "mailto:" + LINKS["email_company"]),
        ("mail-private", "gmail", {"en": "Personal", "de": "Privat"}, LINKS["email_private"], "mailto:" + LINKS["email_private"]),
    ],
    "facts": [
        ("open", "live", None, {"en": "Available for projects", "de": "Offen für Projekte"}, "mailto:" + LINKS["email_company"]),
        ("founder", "building", {"en": "Founder", "de": "Gründer"}, "UplyTech", LINKS["company"]),
        ("location", "pin", {"en": "Based in", "de": "Standort"}, "Itzehoe, DE", None),
        ("since", "code", {"en": "Coding since", "de": "Programmiert seit"}, "2016", None),
        ("langs", "chat", {"en": "Speaks", "de": "Spricht"}, {"en": "German, English", "de": "Deutsch, Englisch"}, None),
    ],
}

# Certificate issuers shown as badges: (key, name as used in CERTS, icon, brand color)
ISSUERS = [
    ("programminghub", "Programming Hub", "award", None),
    ("linkedin", "LinkedIn Learning", "linkedin", "0A66C2"),
    ("freecodecamp", "freeCodeCamp", "freecodecamp", "0A0A23"),
]

SOCIAL = [
    [("Instagram", "E4405F", "instagram", "white", "https://www.instagram.com/vecto_de"),
     ("TikTok", "000000", "tiktok", "white", "https://www.tiktok.com/@vectode"),
     ("X", "000000", "x", "white", "https://x.com/vecto_de"),
     ("Snapchat", "FFFC00", "snapchat", "black", "https://www.snapchat.com/@vecto_de"),
     ("WhatsApp", "25D366", "whatsapp", "white", "https://api.whatsapp.com/send?phone=491726166860")],
    [("YouTube", "FF0000", "youtube", "white", "https://www.youtube.com/@vectode"),
     ("Twitch", "9146FF", "twitch", "white", "https://www.twitch.tv/vectode"),
     ("Spotify", "1DB954", "spotify", "white", "https://spotify.link/pA38mWNLJXb"),
     ("SoundCloud", "FF5500", "soundcloud", "white", "https://on.soundcloud.com/SzVNwEjI6ANTyxL0LE")],
    [("Steam", "000000", "steam", "white", "https://steamcommunity.com/id/vectode"),
     ("Epic Games", "313131", "epicgames", "white", "https://epicgames.com/id/vecto")],
    [("GitHub", "181717", "github", "white", "https://github.com/VectoDE"),
     ("GitLab", "FC6D26", "gitlab", "white", "https://gitlab.com/VectoDE"),
     ("DEV", "0A0A0A", "devdotto", "white", "https://dev.to/vectode")],
    [("UplyTech on Instagram", "E4405F", "instagram-uplytech", "white", "https://www.instagram.com/uplytech.de"),
     ("UplyTech on YouTube", "FF0000", "youtube-uplytech", "white", "https://www.youtube.com/@UplyTech")],
]

SUPPORT = [
    ("GitHub Sponsors", "EA4AAA", "githubsponsors", "white", "https://github.com/sponsors/VectoDE"),
    ("Patreon", "FF424D", "patreon", "white", "https://www.patreon.com/VectoDE"),
    ("Buy Me a Coffee", "FFDD00", "buymeacoffee", "black", "https://buymeacoffee.com/vectode"),
    ("PayPal", "00457C", "paypal", "white", "https://paypal.me/TimHauke"),
]

# group index, name {en, de}, issuer, (month, year), file or None, verify url or None
CERTS = [
    (0, {"en": "Responsive Web Design (Legacy V8, about 300 hours)", "de": "Responsive Web Design (Legacy V8, rund 300 Stunden)"}, "freeCodeCamp", ("Jun", 2024),
     "Responsive Web Design - freeCodeCamp.pdf", "https://www.freecodecamp.org/certification/vectode/responsive-web-design"),
    (0, "React.js: Ein Web-Interface entwickeln", "LinkedIn Learning", ("Apr", 2024), "React.js - Ein Webinterface erstellen - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/8316890e139e9ee84dac2b5a1f3ea742313405ed03db5a0f8cd815ae2d1a57c0"),
    (0, "Vue.js lernen", "LinkedIn Learning", ("Apr", 2024), "Vue.JS Lernen - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/c356d7ad31b20a54a77fa7974ea771cc16a68bb670c894f9023fd38fa380873f"),
    (0, "Webtechniken lernen 4: JavaScript", "LinkedIn Learning", ("Apr", 2024), "Webtechniken lernen 4 - JavaScript - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/e022cabee112be8be253cb5b327e3f2337ce63d0eb7aa05292547fa869fa94a4"),
    (0, "Webtechniken lernen 3: Responsive CSS-Layouts mit Media Queries, Flexbox und Grid", "LinkedIn Learning", ("Apr", 2024), "Webtechniken lernen 3 - Responsive CSS-Layouts - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/0218b627cfc9b8627d819870787bf129ad3fdcc64ab27ac1b2fad327843034b2"),
    (0, "Webtechniken lernen 2: CSS-Grundlagen", "LinkedIn Learning", ("Apr", 2024), "Webtechniken lernen 2 - CSS-Grundlagen - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/0ff6d7e2b2a908173c1482e8b2e44dce6c43928b1271375cf29e7f2e3324595b"),
    (0, "Webtechniken lernen 1: HTML", "LinkedIn Learning", ("Mar", 2024), "Webtechniken lernen 1 - HTML - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/0449b01c9aa6690d194c06dfcf9ac853abe3051ff1a03e79cef21cc742a8b81c"),
    (0, "Grundlagen der Webprogrammierung: Meine erste Website", "LinkedIn Learning", ("Mar", 2024), "Grundlagen der Webprogrammierung - Meine erste Website - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/f47b61d11d2dbfdefb9374ba527ed2c51c5ca6cec9d538d12a01ca4f02070412"),
    (0, "REST APIs lernen", "LinkedIn Learning", ("Mar", 2024), "REST APIs lernen - LinkedIn Zertifikat.pdf", None),
    (0, "GraphQL", "Programming Hub", ("Aug", 2023), "GraphQL.pdf", None),
    (0, "JavaScript Advanced", "Programming Hub", ("Jul", 2023), "JavaScript Advanced.pdf", None),
    (0, "JavaScript", "Programming Hub", ("Jul", 2023), "JavaScript.pdf", None),
    (0, "Laravel", "Programming Hub", ("Jul", 2023), "Laravel.pdf", None),
    (0, "PHP", "Programming Hub", ("Jun", 2023), "PHP.pdf", None),
    (0, "Java", "Programming Hub", ("Mar", 2023), "Java.pdf", None),
    (0, "Programming Fundamentals", "Programming Hub", ("Mar", 2023), "Fundamentals.pdf", None),
    (0, "Bulma CSS", "Programming Hub", ("Feb", 2023), "Bulma CSS.pdf", None),
    (0, "Next.js", "Programming Hub", ("Feb", 2023), "NextJS.pdf", None),
    (0, "Building a Website", "Programming Hub", ("Feb", 2023), "Building a Website 2.pdf", None),
    (0, "CSS", "Programming Hub", ("Feb", 2023), "CSS.pdf", None),
    (0, "Building a Website", "Programming Hub", ("Dec", 2021), "Building a Website.pdf", None),
    (0, "HTML Advanced", "Programming Hub", ("Dec", 2021), "HTML Advanced.pdf", None),
    (0, "HTML", "Programming Hub", ("Dec", 2021), "HTML.pdf", None),
    (0, "Node.js", "Programming Hub", ("Dec", 2021), "NodeJS.pdf", None),
    (1, "Microsoft Teams Grundkurs (PMI: 1.75 PDUs)", "LinkedIn Learning", ("Apr", 2024),
     ["Microsoft Teams Grundkurs - LinkedIn Zertifikat.pdf", "Microsoft Teams Grundkurs - Project Management Institute (PMI)®.pdf"], None),
    (1, "Git", "Programming Hub", ("Aug", 2023), "GIT.pdf", None),
    (1, "Linux", "Programming Hub", ("May", 2023), "Linux.pdf", None),
    (1, "IPv4 & Networking", "Programming Hub", ("Mar", 2023), "IPv4 & Networking.pdf", None),
    (1, "IT Basics", "Programming Hub", ("Mar", 2023), "IT Basics.pdf", None),
    (2, "Digital Marketing Advanced", "Programming Hub", ("Jan", 2025), "Digital Marketing Advanced.pdf", None),
    (2, "Digital Marketing", "Programming Hub", ("Nov", 2024), "Digital Marketing.pdf", None),
    (2, "Steuergrundlagen für Selbstständige, Kleinunternehmer:innen und Gründer:innen", "LinkedIn Learning", ("Apr", 2024),
     "Steuergrundlagen für Selbstständige, Kleinunternehmer-innen und Gründer-innen - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/5994c51b00031eee9ee54b46054039a852f1b8f2ad32582699e2d6bc07a0dce7"),
    (2, "Growth Hacking", "Programming Hub", ("Mar", 2024), None, None),
    (2, "Rechtsgrundlagen: Industrie 4.0 und Internet of Things (IoT)", "LinkedIn Learning", ("Mar", 2024), "Rechtsgrundlagen - Industrie 4.0 und IoT - LinkedIn Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/cdd0c587e2e94280324522277ae37cb636e95cd67fbb3233a3886a7d9c512986"),
    (2, "SEO", "Programming Hub", ("Feb", 2023), "SEO.pdf", None),
    (3, "Professionell netzwerken (PMI)", "LinkedIn Learning", ("Mar", 2024), ["Professionell netzwerken - LinkedIn Zertifikat.pdf", "Professionell netzwerken - Project Management Institute (PMI)®.pdf"], "https://www.linkedin.com/learning/certificates/8edc2fd2aa2c4cc3ffefcadef97bd9230e74141197e614d1eadda7b00c0def88"),
    (3, "Schlagfertigkeit: Nie wieder sprachlos", "LinkedIn Learning", ("Mar", 2024), "Schlagfertigkeit - nie wieder Sprachlos - LinkedIn Zertifikat.pdf", None),
    (3, "Die 7 schlimmsten Kommunikationsfehler", "LinkedIn Learning", ("Mar", 2024), "Die 7 schlimmsten Kommunikationsfehler - LinkedIn Certificate.pdf", "https://www.linkedin.com/learning/certificates/dab8bb262fd871a38cccad4046be2f4456082cee67e409d45f39337eae8b322d"),
    (3, "Small Talk und Netzwerken: 2 unterschätzte Karriere-Booster", "LinkedIn Learning", ("Mar", 2024), "Small Talk & Networking - LinkedIn Learning-Zertifikat.pdf", "https://www.linkedin.com/learning/certificates/799b9d01f2736f2764ad164ccf0f76f1f369922add62534f312c534aac641469"),
]
