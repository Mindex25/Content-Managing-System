import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("articles.db")
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def ajouter_article(
        self, titre, identifiant, auteur, date_publication, paragraphe
    ):
        connection = self.get_connection()
        connection.execute(("INSERT INTO article("
                            "titre, identifiant, auteur,"
                            "date_publication, paragraphe)"
                            "VALUES(?, ?, ?, ?, ?)"),
                           (titre, identifiant, auteur, date_publication,
                            paragraphe))
        connection.commit()

    def get_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT id, titre, identifiant, date_publication FROM article"
        )
        articles = cursor.fetchall()
        return articles

    def get_article(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute((
            "SELECT titre, identifiant, auteur, date_publication, paragraphe "
            "FROM article where identifiant=?"),
            (identifiant,))
        article = cursor.fetchone()
        return article

    def get_id(self, id_article):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("SELECT id, titre, paragraphe FROM article WHERE id=?"),
            (id_article,),
        )
        article = cursor.fetchone()
        return article

    def get_articles_recents(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT * FROM article "
            "WHERE date_publication < date('now')"
            "ORDER BY date_publication DESC limit 5"
        )
        articles = cursor.fetchall()
        return articles

    def get_resultats_recherche(self, recherche):
        cursor = self.get_connection().cursor()
        cursor.execute((
            "SELECT titre, date_publication, identifiant "
            "FROM article WHERE titre LIKE ? or paragraphe LIKE ?"),
            ('%'+recherche+'%', '%'+recherche+'%'))
        articles = cursor.fetchall()
        return articles

    def modifier_article(self, id_article, titre, paragraphe):
        connection = self.get_connection()
        connection.execute(
            ("UPDATE article SET titre=?, paragraphe=? WHERE id=?"),
            (titre, paragraphe, id_article,),
        )
        connection.commit()
