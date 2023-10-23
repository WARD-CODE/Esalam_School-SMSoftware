import sqlite3

def db_modefication(tableau,row_id,donnee):
    conn = sqlite3.connect("salam_school.db")
    curs = conn.cursor()
    
    curs.execute("""UPDATE {tab} SET 
                                    num = donnee[0],
                                    phase = donnee[1],
                                    niveau = donnee[2],
                                    spec = donnee[3], 
                                    matiere = donnee[4],
                                    prof_id = donnee[5],
                                    horraire = donnee[6],
                                    mat_prix = donnee[7],
                                    mat_prix = donnee[8]
                                WHERE rowid = {rid}""".format(tab = str(tableau), rid = row_id),donnee)
    conn.commit()
    conn.close()

def db_supprission(tableau,row_id):

    conn = sqlite3.connect("salam_school.db")
    curs = conn.cursor()

    curs.execute("""DELETE FROM {tab} WHERE rowid = {rid}""".format(tab = str(tableau), rid = row_id))

    conn.commit()
    conn.close()




