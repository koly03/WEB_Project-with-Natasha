from flask import Flask, render_template, request, g, flash, redirect, url_for
from FDataBase import FDataBase
from _datetime import datetime
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
#from flask_login import LoginManager, login_user, login_required

DATABASE = '/tmp/ma_base.db'
DEBUT = True
SECRET_KEY = 'dsfjryehnmxjdhjh373kj2q3u3'

app = Flask(__name__)
app.config.from_object(__name__)
# conn = sqlite3.connect('biblio_base.db')
# app.config["SECRET_KEY"] = 'dsfjryehnmxjdhjh373kj2q3u3'

##lodin_manager = LoginManeger(app)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'biblio_base.db')))
user = ("", 0)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    # conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('biblio.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/", methods=["POST", "GET"])
def home():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template("home.html", role=user[1], pid=user[0])


@app.route("/BiblioSearch", methods=["POST", "GET"])
def just_search():
    if request.method == 'POST':
        if len(request.form['Search']) > 0:
            return redirect(url_for('search', find=request.form['Search'], role=user[1], pid=user[0]))
        else:
            return render_template("Search.html", role=user[1], pid=user[0])
    return render_template("Search.html", role=user[1], pid=user[0])


@app.route("/BiblioSearch/<path:find>", methods=["POST", "GET"])
def search(find):
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['Search']) > 0:
            return redirect(url_for('search', find=request.form['Search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    if len(find) > 0:
        list_livres = dbase.searchByName(find)
        list_authors = dbase.searchByAuthors(find)
        list_genres = dbase.searchByGenre(find)
        authors_l = []
        genres_l = []
        search1 = False
        search2 = False
        search3 = False
        print(list_authors)
        print(list_genres)
        if len(list_livres) > 0:
            for b in list_livres:
                authors_l.append(dbase.get_authors(b[0]))
                genres_l.append(dbase.get_genres(b[0]))
            search1 = True
        if len(list_authors) > 0:
            print(1)
            search2 = True
        if len(list_genres) > 0:
            print(2)
            search3 = True
        return render_template("Search.html", find=find, search1=search1, books=list_livres, authors=authors_l, genres=genres_l,
                               search2=search2, authors_a=list_authors, search3=search3, genres_g=list_genres)
    # if len(find) > 0:
    #     list_livres = dbase.searchByName(find)
    #     list_authors = dbase.searchByAuthors(find)
    #     authors_a = []
    #     authors_l = []
    #     genres_a = []
    #     genres_l = []
        # if len(list_livres) > 0 and len(list_authors) > 0:
        #     for b in list_livres:
        #         authors_l.append(dbase.get_authors(b[0]))
        #         genres_l.append(dbase.get_genres(b[0]))
        #     for b in list_authors:
        #         authors_a.append(dbase.get_authors(b[0]))
        #         genres_a.append(dbase.get_genres(b[0]))
        #     return render_template("Search.html", find=find, search1=True, books=list_livres, authors=authors_l,
        #                            genres=genres_l, search2=True, books_a=list_authors, authors_a=authors_a, genres_a=genres_a,
        #                            role=user[1], pid=user[0])
        # if len(list_livres) > 0:
        #     for b in list_livres:
        #         authors_l.append(dbase.get_authors(b[0]))
        #         genres_l.append(dbase.get_genres(b[0]))
        #     return render_template("Search.html", find=find, search1=True, books=list_livres, authors=authors_l, genres=genres_l,
        #                            role=user[1], pid=user[0])
        # elif len(list_authors) > 0:
        #     for b in list_authors:
        #         authors_a.append(dbase.get_authors(b[0]))
        #         genres_a.append(dbase.get_genres(b[0]))
        #     return render_template("Search.html", find=find, search2=True, books_a=list_authors, authors_a=authors_a, genres_a=genres_a,
        #                            role=user[1], pid=user[0])
        # else:
        #     flash("Rien trouvé pour " + "'" + find + "'", category='error')
        #     return redirect(url_for('just_search', role=user[1], pid=user[0]))




@app.route("/BiblioGenres", methods=["POST", "GET"])
def genres():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template("Genres.html", genres=dbase.genres(), role=user[1], pid=user[0])


@app.route("/BiblioAuteurs", methods=["POST", "GET"])
def authors():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template("Authors.html", authors=dbase.authors(), role=user[1], pid=user[0])

# @lodin_manager.user_loader
# def load_user(id_user):
#     db = get_db()
#     dbase = FDataBase(db)
#     print('log')
#     return UserLogin.fromDB(id_user, dbase)

@app.route("/BiblioRegistration", methods=["POST", "GET"])
def reg():
    db = get_db()
    dbase = FDataBase(db)
    global user
    user = user
    if request.method == 'POST':
        if len(request.form['PassportID']) == 9:
            if dbase.checkReg(request.form['PassportID']):
                if (len(request.form['Password']) > 3):
                    if len(request.form['PasswordAdmin']) == 0:
                        # global user
                        hash = generate_password_hash(request.form['Password'])
                        flash("Vous êtes inscrit en tant qu'utilisateur.", category='success')
                        res = dbase.reg(request.form['PassportID'], request.form['Surname'], request.form['Name'],
                                        request.form['Email'], request.form['Telephone'], hash, 0)
                        user = (request.form['PassportID'], 0)
                    elif request.form['PasswordAdmin'] == 'Admin':
                        # global user
                        hash = generate_password_hash(request.form['Password'])
                        flash("Vous vous êtes inscrit en tant que responsable.", category='success')
                        res = dbase.reg(request.form['PassportID'], request.form['Surname'], request.form['Name'],
                                        request.form['Email'], request.form['Telephone'], hash, 1)
                        user = (request.form['PassportID'], 1)
                    elif request.form['PasswordAdmin'] != 'Admin':
                        flash("Mot de passe incorrect pour vous inscrire en tant que responsable.", category='error')
                else:
                    flash("Erreur, veuillez remplir tous les champs obligatoires.", category='error')
            else:
                flash("Un utilisateur avec ce numéro de passeport est déjà enregistré.", category='error')
        else:
            flash("Le numéro de passeport doit comporter 9 caractères.", category='error')
    return render_template('Reg.html', role=user[1], pid=user[0])


@app.route("/BiblioLogin", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    global user
    user = ("", 0)
    if request.method == 'POST':
        if len(request.form['PassportID']) == 9:
            if not dbase.checkReg(request.form['PassportID']):
                if check_password_hash(dbase.passwordLog(request.form['PassportID']), request.form['Password']):
                    ##flash("ok", category='success')
                    # userlogin = UserLogin().create(dbase.getUser(request.form['PassportID']))
                    # login_user(userlogin)
                    # global user
                    user = (request.form['PassportID'], dbase.role(request.form['PassportID']))
                    return redirect(url_for('home'))
                else:
                    flash("Mot de passe invalide.", category='error')
            else:
                flash("Vous n'êtes pas encore inscrit, merci de vous inscrire.", category='error')
        else:
            flash("Le numéro de passeport doit comporter 9 caractères.", category='error')

    return render_template("Log.html", role=user[1], pid=user[0])


@app.route("/BiblioCatalog", methods=["GET", "POST"])
def catalog():
    db = get_db()
    dbase = FDataBase(db)
    books = dbase.get_books()
    authors = []
    genres = []
    for b in books:
        authors.append(dbase.get_authors(b[0]))
        genres.append(dbase.get_genres(b[0]))
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template('Catalog.html', books=books, authors=authors, genres=genres, role=user[1], pid=user[0], )


@app.route("/BiblioCatalog/<path:book_id>", methods=["GET", "POST"])
def book(book_id):
    db = get_db()
    dbase = FDataBase(db)
    book = dbase.book(book_id)
    authors = dbase.get_authors(book_id)
    genres = dbase.get_genres(book_id)
    exs = dbase.exemplaire(book_id)
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template('Book.html', book=book, authors=authors, genres=genres, exem=exs, role=user[1], pid=user[0])


@app.route("/BiblioGenres/<path:g_id>", methods=["GET", "POST"])
def genre(g_id):
    db = get_db()
    dbase = FDataBase(db)
    books = dbase.genre(g_id)
    authors = []
    genres = []
    for b in books:
        authors.append(dbase.get_authors(b[0]))
        genres.append(dbase.get_genres(b[0]))
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template('Genre.html', genre=dbase.genre_id(g_id)[0], books=books, authors=authors, genres=genres, role=user[1], pid=user[0])


@app.route("/BiblioAuteurs/<path:a_id>", methods=["GET", "POST"])
def author(a_id):
    db = get_db()
    dbase = FDataBase(db)
    books = dbase.author(a_id)
    authors = []
    genres = []
    for b in books:
        authors.append(dbase.get_authors(b[0]))
        genres.append(dbase.get_genres(b[0]))
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template('Author.html', author=dbase.author_id(a_id)[0], books=books, authors=authors, genres=genres, role=user[1], pid=user[0])

@app.route("/BiblioReservation/<path:ex_id>", methods=["GET", "POST"])
#@login_required
def res(ex_id):
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        list = dbase.check_reservation(request.form['DateD'], request.form['DateA'])
        dd = datetime.strptime(request.form['DateD'], "%Y-%m-%d").date()
        da = datetime.strptime(request.form['DateA'], "%Y-%m-%d").date()
        if dd < datetime.today().date() or da < datetime.today().date():
            flash('1', category='error')
        elif dd > da:
            flash('2', category='error')
        elif len(list) > 0:
            s = ""
            for d in list:
                s = s + "Du " + d[0][8:] + "/" + d[0][5:7] + "/" + d[0][:4] + " au " + d[1][8:] + "/" + d[1][5:7] + "/" + d[1][:4] + "\n"
            flash("Le livre est occupé:\n" + s, category='error')
        else:
            result = dbase.isert_res(dd, da, user[0], ex_id)
    return render_template('Reservation.html', exem=ex_id, book=dbase.book(dbase.exem_book(ex_id)[0])[2], role=user[1], pid=user[0])

@app.route('/MyReservation')
def myRes():
    db = get_db()
    dbase = FDataBase(db)
    if not user[0]:
        return redirect(url_for('login', role=user[1], pid=user[0]))
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template("MyRes.html", dates=dbase.myRes(user[0]), role=user[1], pid=user[0])

@app.route('/AllReservation')
def allRes():
    db = get_db()
    dbase = FDataBase(db)
    dates = []
    users = dbase.users()
    i = 0
    if not user[0]:
        return redirect(url_for('login', role=user[1], pid=user[0]))
    if user[1] == 0:
        return redirect(url_for('home', role=user[1], pid=user[0]))
    for u in users:
        dates.append(dbase.myRes(u[0]))
    if request.method == 'POST':
        if len(request.form['bur_search']) > 0:
            return redirect(url_for('search', find=request.form['bur_search'], role=user[1], pid=user[0]))
        else:
            return redirect(url_for('just_search', role=user[1], pid=user[0]))
    return render_template("AllRes.html", users=dbase.users(), dates=dates, role=user[1], pid=user[0])


@app.route('/AddExemplaires', methods=["GET", "POST"])
def addExemplaires():
    db = get_db()
    dbase = FDataBase(db)
    if not user[0]:
        return redirect(url_for('login', role=user[1], pid=user[0]))
    if user[1] == 0:
        return redirect(url_for('home', role=user[1], pid=user[0]))
    if request.method == 'POST':
        if (int(request.form["an"]) < int(datetime.today().year)):
            res1 = dbase.addEx(request.form["imgl"], request.form["an"], request.form["page"], request.form["langage"],
                              request.form["prix"], request.form["emplace"], request.form["emition"],
                              request.form["livre"], request.form["etat"])
            res2 = dbase.plusEx(request.form["livre"])
            flash("Exemplaire was added", category='success')
        else:
            flash("Year from future", category='error')
    return render_template("AddExapl.html", books=dbase.get_books(), etat=dbase.etats(), role=user[1], pid=user[0])

@app.route('/AddBook', methods=["GET", "POST"])
def addBook():
    db = get_db()
    dbase = FDataBase(db)
    if not user[0]:
        return redirect(url_for('login', role=user[1], pid=user[0]))
    if user[1] == 0:
        return redirect(url_for('home', role=user[1], pid=user[0]))
    if request.method == 'POST':
        authors = request.form.getlist("check_box_a[]")
        genres = request.form.getlist("check_box_g[]")
        new_a = request.form.getlist("newA[]")
        new_g = request.form.getlist("newG[]")
        if (len(authors) == 0 and len(new_a) == 0) or (len(genres) == 0 and len(new_g)== 0):
            flash("Add author or genre", category='error')
        else:
            res1 = dbase.addBook(request.form["titre"], request.form["imgl"], request.form["Description"])
            livre = dbase.id_l(request.form["titre"])
            if new_a:
                for a in new_a:
                    if a:
                        n = a.split(" ", 1)
                        res2 = dbase.addAuthor(n[0], n[1])
                        res3 = dbase.id_a(n[0], n[1])
                        authors.append(res3)
                        # authors.append(n[0])
                        # authors.append(n[1])
            if new_g:
                for g in new_g:
                    if g:
                        res2 = dbase.addGenre(g)
                        res3 = dbase.id_g(g)
                        genres.append(res3)
                        # genres.append(g)
            # print(genres)
            # print(dbase.id_a("1984"))
            for a in authors:
                res4 = dbase.addLEA(int(a), int(livre[0]))
            for g in genres:
                res4 = dbase.addLCG(int(g), int(livre[0]))
            flash("Book was added", category='success')
    return render_template("AddBook.html", authors=dbase.authors(), genres=dbase.genres(), role=user[1], pid=user[0])



if __name__ == '__main__':
    app.run(debug=True)
