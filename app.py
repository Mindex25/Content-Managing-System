from database import Database
from flask import Flask, g, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


# Essaie de parse une chaîne de carctères en date selon ISO8601
# Return True si l'entrée respecte le format
def valider_date_iso8601(date_publication):
    try:
        datetime.fromisoformat(date_publication)
        return True
    except ValueError:
        return False


def valider_string(string, longueur_max):
    if string == "" or len(string) > longueur_max:
        return False
    return True


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.disconnect()


@app.route("/", methods=["GET", "POST"])
def acceuil():
    if request.method == "GET":
        articles = get_db().get_articles_recents()
        return render_template("index.html", articles=articles)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/resultats", methods=["GET", "POST"])
def afficher_resultats():
    recherche = request.args.get("recherche")
    articles = get_db().get_resultats_recherche(recherche)
    return render_template("resultats.html", articles=articles)


@app.route("/article/<identifiant>", methods=["GET"])
def afficher_article(identifiant):
    article = get_db().get_article(identifiant)
    return render_template("article.html", article=article)


@app.route("/admin", methods=["GET"])
def afficher_articles():
    articles = get_db().get_articles()
    return render_template("admin.html", articles=articles)


@app.route("/admin/modifier/<id_article>", methods=["GET", "POST"])
def modifier_article(id_article):
    article = get_db().get_id(id_article)

    if request.method == "GET":
        return render_template("modifier.html", article=article)
    else:
        titre = request.form["champ-titre"]
        paragraphe = request.form["champ-paragraphe"]
        get_db().modifier_article(id_article, titre, paragraphe)
        return redirect("/admin")


@app.route("/admin-nouveau", methods=["GET", "POST"])
def creer_nouveau():
    if request.method == "GET":
        return render_template("admin-nouveau.html")
    else:
        titre = request.form["champ-titre"]
        auteur = request.form["champ-auteur"]
        identifiant = request.form["champ-identifiant"]
        date_publication = request.form["champ-date_publication"]
        paragraphe = request.form["champ-paragraphe"]
        champ_invalide = None

        if not valider_string(titre, 100):
            champ_invalide = (
                "Veuillez entrer le titre de l article (100 char max)"
            )
        if not valider_string(auteur, 100):
            champ_invalide = (
                "Veuillez entrer le nom de l auteur (100 char max)"
            )
        if not valider_string(identifiant, 50):
            champ_invalide = (
                "Veuillez entrer l identifiant de l article (50 char max)"
            )
        if (
            not valider_date_iso8601(date_publication)
            or date_publication == ""
        ):
            champ_invalide = (
                "Veuillez entrer la date de publication selon le format ISO801"
            )
        if not valider_string(paragraphe, 500):
            champ_invalide = (
                "Veuillez entrer le contenu de l article (500 char max)"
            )

        if champ_invalide:
            return render_template(
                "admin-nouveau.html", champ_invalide=champ_invalide
            )

        get_db().ajouter_article(
            titre, identifiant, auteur, date_publication, paragraphe
        )
        return redirect("/admin")


if __name__ == "__main__":
    app.run()
