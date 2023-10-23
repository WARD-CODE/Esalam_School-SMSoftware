"""
----------------------------------------
this Script is writen for School
----------------------------------------
author : Mr Z.wardi
starting_date : 12-10-2021 at 14:30
subject :  school management system GUI
----------------------------------------
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QApplication,QDateTimeEdit
from PyQt5.uic import  loadUiType
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTime, QDate
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter

import datetime 
import sys
import sqlite3
from ast import literal_eval

ui,_ = loadUiType("sallam_school_app.ui")

class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Salam school management system")
        self.UI_components()
        

    def UI_components(self):

        #partie d'initialisation
        #----------------------------------------------------------------------------------------
        self.tabWidget.setCurrentIndex(0)#to set start with the first column of table on display
        self.tabWidget.tabBar().setVisible(False)#make table bar invisible
        self.tabWidget_3.tabBar().setVisible(False)#make table bar invisible
        self.admin_login_B.clicked.connect(self.login)
        self.buttons = [self.main_B,self.groupe_B,self.etudiant_B,self.prof_B,self.caisse_B]
        self.etdn_exempter_val_CB = "لا"
        self.etdn_paye_val_CB = "لا"
        self.donnee = list()
        self.donnee_g = None
        self.donnee_p = None
        self.jours = {
            "Saturday":"السبت",
            "Sunday":"الأحد",
            "Monday":"الاثنين",
            "Tuesday":"الثلاثاء",
            "Wednesday":"الأربعاء",
            "Thursday":"الخميس",
            "Friday":"الجمعة"
        }
        for i in range(len(self.buttons)):
            self.buttons[i].setVisible(False)
        
        
        """--------------------------------------------------------------------------------------"""

        #les buttons principales et les tableaux
        self.main_B.clicked.connect(self.main_B_func)
        self.groupe_B.clicked.connect(self.groupe_B_func)
        self.etudiant_B.clicked.connect(self.etudiant_B_func)
        self.prof_B.clicked.connect(self.prof_B_func)
        self.caisse_B.clicked.connect(self.caisse_B_func)
        self.fermer_B.clicked.connect(self.fermer_B_func)
        
        #les fonctions du groupe
        self.grp_ajout_B.clicked.connect(self.grp_ajout_B_func)
        self.groupe_dans_combobox()
        self.grp_list_TAB.itemClicked.connect(self.grp_select_TAB_Func)
        self.grp_supp_B.clicked.connect(self.grp_supp_B_func)
        self.grp_edit_B.clicked.connect(self.grp_edit_B_func)
        self.tabWidget_2.currentChanged.connect(self.tabWidget_2_func)
        #self.grp_rech_E.editingFinished.connect(self.grp_rech_E_func)
        #les fonctions de l'etudiant
        self.etdn_ajout_B.clicked.connect(self.etdn_ajout_B_func)
        self.etdn_phn_CB.stateChanged.connect(self.etdn_phn_CB_func)
        self.etdn_phnp_CB.stateChanged.connect(self.etdn_phnp_CB_func)
        self.etdn_exempter_CB.stateChanged.connect(self.etdn_exempter_CB_func)
        self.etdn_paye_CB.stateChanged.connect(self.etdn_paye_CB_func)
        self.etdn_grp_rech_C.currentIndexChanged.connect(self.etdn_grp_rech_C_Func)
        self.etdn_list_TAB.itemClicked.connect(self.etdn_select_TAB_Func)
        self.etdn_mise_B.clicked.connect(self.etdn_mise_B_func)
        self.etdn_supp_B.clicked.connect(self.etdn_supp_B_func)
        self.etdn_edit_B.clicked.connect(self.etdn_edit_B_func)
        self.etdn_prnt_B.clicked.connect(self.etdn_prnt_B_func)
        self.etdn_abst_B.clicked.connect(self.etdn_abst_B_func)
        self.etdn_jabst_B.clicked.connect(self.etdn_jabst_B_func)
        self.etdn_renouv_B.clicked.connect(self.etdn_renouv_B_func)
        self.etdn_st_B.clicked.connect(self.etdn_st_B_func)
        self.etdn_renouv_tout_B.clicked.connect(self.etdn_renouv_tout_B_func)
        #self.etdn_grp_rech_E.editingFinished.connect(self.etdn_grp_rech_E_func)
        #les fonctions du Prof
        self.prf_ajout_B.clicked.connect(self.prf_ajout_B_func)
        self.prf_list_TAB.itemClicked.connect(self.prf_select_TAB_Func)
        self.prf_supp_B.clicked.connect(self.prf_supp_B_func)
        self.prf_edit_B.clicked.connect(self.prf_edit_B_func)

        #les fonctions de la caisse
        #etudiant 
        self.csAdmin_B.clicked.connect(self.csAdmin_B_func)
        self.csProf_B.clicked.connect(self.csProf_B_func)
        self.csEtdn_B.clicked.connect(self.csEtdn_B_func)
        self.csetdn_imprim_B.clicked.connect(self.csetdn_imprim_B_func)

        self.init_donnees_dans_tables()
    #les methodes
    def login(self):
        """
        AL_un = self.admin_nu_E.text()
        AL_pswd = self.admin_pswd_E.text()
        """
        AL_un = "admin"
        AL_pswd = "admin"
        if str(AL_un)=="" and str(AL_pswd)=="":
            pass
        else:      
            AL_entered_data = [AL_un, AL_pswd]
            AL_main_data = ["admin", "admin"]

            if AL_entered_data == AL_main_data:
                QMessageBox().information(self,"تسجيل الدخول", "تم التسجيل بنجاح!", QMessageBox.Close, QMessageBox.Close)
                self.tabWidget.setCurrentIndex(0)
                for i in range(len(self.buttons)):#visible pour les buttons
                    self.buttons[i].setVisible(True)
                self.admin_inscr_GB.setVisible(False)#invisible pour le Login
            else:
                QMessageBox().warning(self,"تسجيل الدخول", "يوجد خطأ في اسم المستخدم أو كلمة المرور!",QMessageBox.Ok,QMessageBox.Ok)

    def main_B_func(self):
        self.tabWidget.setCurrentIndex(0)
    def groupe_B_func(self):
        self.tabWidget.setCurrentIndex(1)
    def etudiant_B_func(self):
        self.tabWidget.setCurrentIndex(2)
    def prof_B_func(self):
        self.tabWidget.setCurrentIndex(3)
    def caisse_B_func(self):
        self.tabWidget.setCurrentIndex(4)

    def fermer_B_func(self):
        reponse = QMessageBox.question(self,"تسجيل الخروج", "هل تريد المغادرة حقا؟",QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reponse == QMessageBox.Yes:
            self.close()
        else:
            pass

    #fonctions cummunes                                                                      
    def init_donnees_dans_tables(self):                         
        
        conn = sqlite3.connect("salam_school.db")
        curs = conn.cursor()
        
        tables ={
            'groupe':self.grp_list_TAB,
            'prof':self.prf_list_TAB
            }
        
        champs = {
            'groupe':'groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances',
            'prof':'prof_id,nom,prenom,num_tel,email,date_entree'
        }

        for nom,tab in tables.items():
            curs.execute("SELECT {} FROM {}".format(champs[nom],nom))
            d1 = curs.fetchall()
            
            #initialiser la table
            tab.setRowCount(0)
            tab.insertRow(0)
            #verifier le contenu de la base de donnees puis remplir la table
            if d1:
                for row,form in enumerate(d1):
                    for column, item in enumerate(form):
                        tab.setItem(row,column, QTableWidgetItem(str(item)))
                    row_position = tab.rowCount()
                    tab.insertRow(row_position)
        conn.commit()
        conn.close()

#----------------------------------------------------------espace groupe----------------------------------------------------------------
    
    def groupe_dans_combobox(self):

        conn = sqlite3.connect("salam_school.db")
        curs = conn.cursor()
        curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe")
        datas = curs.fetchall()
        for d1 in datas:
            data  ={
                    "رمز":d1[0],
                    "فوج":d1[1],
                    "طور":d1[2],
                    "مستوى":d1[3],
                    "تخصص":d1[4],
                    "مادة":d1[5]
                    }
            self.etdn_grp_C.addItem(str(data))
            self.etdn_grp_rech_C.addItem(str(data))

        curs.execute("SELECT nom,prenom FROM prof")
        datas = curs.fetchall()
        
        for d1 in datas:
            data = str(d1[0] + " " + d1[1])
            self.grp_prof_C.addItem(data)

        conn.commit()
        conn.close()
    
    def tabWidget_2_func(self):
        select_ligne = self.grp_list_TAB.currentRow()
        try: 
            if len(self.grp_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد الفوج",QMessageBox.Close,QMessageBox.Close)

        else:
            if self.tabWidget_2.currentIndex() == 1:
                temps_actuel = QTime.currentTime()
                jour_aujourdhui = str(datetime.date.today().strftime("%A"))

                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()
                curs.execute("SELECT groupe_id,horraire FROM groupe")
                grp = curs.fetchall()
                
                liste_groupes = []
                for i in range(len(grp)):
                    if self.jours[jour_aujourdhui] == (str(grp[i][1]).split('/'))[0]:
                        temps_in = QTime.fromString((str(grp[i][1]).split('/'))[1],"HH:mm")
                        temps_out = QTime.fromString((str(grp[i][1]).split('/'))[2],"HH:mm")
                        if temps_in <= temps_actuel <= temps_out:
                            liste_groupes.append(grp[i][0])
                if liste_groupes:
                    if len(liste_groupes)>1:
                        curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe WHERE groupe_id IN {}".format(tuple(liste_groupes)))
                    else:
                        curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe WHERE groupe_id = {}".format(liste_groupes[0]))
                    d1 = curs.fetchall()
                    #initialiser la table
                    self.grp_list_TAB_2.setRowCount(0)
                    self.grp_list_TAB_2.insertRow(0)
                    #verifier le contenu de la base de donnees puis remplir la table
                    
                    if d1:
                        for row,form in enumerate(d1):
                            for column, item in enumerate(form):
                                self.grp_list_TAB_2.setItem(row,column, QTableWidgetItem(str(item)))
                            row_position = self.grp_list_TAB_2.rowCount()
                            self.grp_list_TAB_2.insertRow(row_position)

                    conn.commit()
                    conn.close()

    def grp_tests_get(self):
        # les conditions de remplissage
        self.conditions_grp_1 = self.grp_niv_C.currentIndex() == 0 or str(self.grp_prixm_E.text()) == "" or str(self.grp_prixp_E.text()) == ""
        self.conditions_grp_2 = str(self.grp_prixm_E.text()).isalpha() or str(self.grp_prixp_E.text()).isalpha()

        if self.conditions_grp_1:
            QMessageBox.warning(self,"حقل فارغ", "أحد الحقول فارغة",QMessageBox.Ok,QMessageBox.Ok)
            
        elif self.conditions_grp_2:
            QMessageBox.warning(self,"قيمة غير مناسبة", "يرجى ادخال قيم مناسبة في الحقول!",QMessageBox.Ok,QMessageBox.Ok)
            self.grp_prixm_E.clear(), self.grp_prixp_E.clear()

        else:
            grp_num_S = int (self.grp_num_S.value())
            grp_phase_C = str(self.grp_phase_C.currentText())
            grp_niv_C = int(self.grp_niv_C.currentText())
            grp_spec_C = str(self.grp_spec_C.currentText())
            grp_mtr_C = str(self.grp_mtr_C.currentText())
            grp_prof_C = str(self.grp_prof_C.currentText())
            grp_nums_S = int(self.grp_nums_S.value())
            grp_prixm_E = int(self.grp_prixm_E.text())
            grp_prixp_E = int(self.grp_prixp_E.text())
            grp_horaire_C = str(self.grp_horaire_C.currentText() + "/" + self.grp_hr1_TE.text() + "/" + self.grp_hr2_TE.text())
            grp_obsv_T = str(self.grp_obsv_T.toPlainText())

            #creation de la donnee complete
            donnee = str((
                grp_num_S,
                grp_phase_C,
                grp_niv_C,
                grp_spec_C,
                grp_mtr_C,
                grp_prof_C,
                grp_nums_S,
                grp_prixm_E,
                grp_prixp_E,
                grp_horaire_C,
                grp_obsv_T
                ))
            return donnee
        
    def grp_ajout_B_func(self):

        donnee = self.grp_tests_get()
        if donnee:
            #connection dans la base de donnee
            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            nom_donnee = str(('num','phase','niveau','spec','matiere','prof_nom','nombre_seances','mat_prix','prof_prix','horraire','observation'))
            curs.execute("INSERT INTO groupe {} VALUES {}".format(nom_donnee,donnee))
            curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe ORDER BY rowid DESC LIMIT 1")
            d1 = curs.fetchone()

            data ={ 
                    "رمز":d1[0],
                    "فوج":d1[1],
                    "طور":d1[2],
                    "مستوى":d1[3],
                    "تخصص":d1[4],
                    "مادة":d1[5]
                    } 
            self.etdn_grp_C.addItem(str(data))
            self.etdn_grp_rech_C.addItem(str(data))

            curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe ORDER BY rowid DESC LIMIT 1")
            d1 = curs.fetchone()
            
            if d1:
                row_position = self.grp_list_TAB.rowCount()-1
                self.grp_list_TAB.insertRow(row_position)
                for column,item in enumerate(d1):
                    self.grp_list_TAB.setItem(row_position,column, QTableWidgetItem(str(item)))
            conn.commit()
            conn.close()
    
    def grp_select_TAB_Func(self):

        if self.grp_list_TAB.rowCount() == 0:
            pass
        else:
            ligne_select = self.grp_list_TAB.currentRow()
            self.donnee_g = int(self.grp_list_TAB.item(ligne_select,0).text())

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()

            curs.execute("SELECT * FROM groupe WHERE groupe_id = {id} LIMIT 1".format(id = self.donnee_g))
            d1 = curs.fetchone()
            period = str(d1[10]).split("/")

            self.grp_num_S.setValue(int(d1[1]))
            self.grp_phase_C.setCurrentIndex(self.grp_phase_C.findText(d1[2]))
            self.grp_niv_C.setCurrentIndex(self.grp_niv_C.findText(str(d1[3])))
            self.grp_spec_C.setCurrentIndex(self.grp_spec_C.findText(str(d1[4])))
            self.grp_mtr_C.setCurrentIndex(self.grp_mtr_C.findText(str(d1[5])))
            self.grp_prof_C.setCurrentIndex(self.grp_prof_C.findText(str(d1[6])))
            
            self.grp_horaire_C.setCurrentIndex(self.grp_horaire_C.findText(period[0]))

            self.grp_hr1_TE.setTime(QTime().fromString(period[1],"HH:mm"))
            self.grp_hr2_TE.setTime(QTime().fromString(period[2],"HH:mm"))

            self.grp_prixm_E.setText(str(d1[8]))
            self.grp_prixp_E.setText(str(d1[9]))
            self.grp_nums_S.setValue(int(d1[7]))
            self.grp_obsv_T.setPlainText(str(d1[11]))
            
            conn.commit()
            conn.close()

    def grp_supp_B_func(self):
        
        select_ligne = self.grp_list_TAB.currentRow()
        try: 
            if len(self.grp_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد الفوج",QMessageBox.Close,QMessageBox.Close)

        else:
            reponse = QMessageBox.question(self, "حذف فوج","هل تريد حذف الفوج حقا؟",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            
            if reponse == QMessageBox.No:
                pass
            else:
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()

                grp_id = int(self.grp_list_TAB.item(select_ligne,0).text())
                curs.execute("DELETE FROM groupe WHERE groupe_id = {}".format(grp_id))
                curs.execute("DELETE FROM etudiant WHERE groupe_id = {}".format(grp_id))
                self.grp_list_TAB.removeRow(select_ligne)
                c_index = self.etdn_grp_rech_C.currentIndex()

                if c_index == 0:
                    pass
                else:
                    grp_id2 = literal_eval(str(self.etdn_grp_rech_C.currentText()))  
                    if grp_id2["رمز"] == grp_id:
                        while (self.etdn_list_TAB.rowCount() > 0):
                            self.etdn_list_TAB.removeRow(0)
     
                    
                    
                conn.commit()
                conn.close()          
    
    def grp_edit_B_func(self):
        select_ligne = self.grp_list_TAB.currentRow()
        try: 
            if len(self.grp_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد الفوج",QMessageBox.Close,QMessageBox.Close)

        else:
            donnee = self.grp_tests_get()

            if donnee:
                #connection dans la base de donnee
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()
                
                curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere FROM groupe WHERE groupe_id = {} LIMIT 1".format(self.donnee_g))
                d1 = curs.fetchone()
                data ={ 
                        "رمز":d1[0],
                        "فوج":d1[1],
                        "طور":d1[2],
                        "مستوى":d1[3],
                        "تخصص":d1[4],
                        "مادة":d1[5]
                        } 
                self.etdn_grp_C.removeItem(self.etdn_grp_C.findText(str(data)))
                self.etdn_grp_rech_C.removeItem(self.etdn_grp_rech_C.findText(str(data)))

                nom_donnee = str(('num','phase','niveau','spec','matiere','prof_nom','nombre_seances','mat_prix','prof_prix','horraire','observation'))
                curs.execute("UPDATE groupe SET {} = {} WHERE groupe_id = {}".format(nom_donnee,donnee,self.donnee_g))

                curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe WHERE groupe_id = {} LIMIT 1".format(self.donnee_g))
                d1 = curs.fetchone()

                data ={ 
                        "رمز":d1[0],
                        "فوج":d1[1],
                        "طور":d1[2],
                        "مستوى":d1[3],
                        "تخصص":d1[4],
                        "مادة":d1[5]
                        } 
                
                self.etdn_grp_C.addItem(str(data))
                self.etdn_grp_rech_C.addItem(str(data))
                
                if d1:
                    for column,item in enumerate(d1):
                        self.grp_list_TAB.setItem(select_ligne,column, QTableWidgetItem(str(item)))

                conn.commit()
                conn.close()

    
            
#-------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------espace etudiant----------------------------------------------------------------
    def etdn_tests_get(self):
        self.conditions_etdn_1 = self.etdn_grp_C.currentIndex() == 0 or str(self.etdn_nom_E.text()) == "" or\
             str(self.etdn_prnm_E.text()) == "" or str(self.etdn_ads_E.text()) == "" or str(self.etdn_phn_E.text()) == "" or str(self.etdn_phnp_E.text()) == ""
        
        self.conditions_etdn_2 = str(self.etdn_nom_E.text()).isdigit() or str(self.etdn_prnm_E.text()).isdigit()

        if self.conditions_etdn_1:
            QMessageBox.warning(self,"حقل فارغ", "أحد الحقول فارغة",QMessageBox.Ok,QMessageBox.Ok)
            
        elif self.conditions_etdn_2:
            QMessageBox.warning(self,"قيمة غير مناسبة", "يرجى ادخال قيم مناسبة في الحقول!",QMessageBox.Ok,QMessageBox.Ok)
            self.etdn_nom_E.clear(), self.etdn_prnm_E.clear()

        else:
            #connection dans la base de donnee
            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()

            etdn_nom_E = str (self.etdn_nom_E.text())
            etdn_prnm_E = str(self.etdn_prnm_E.text())
            etdn_dnaissance_DE = str(self.etdn_dnaissance_DE.text())
            etdn_sex_C = str(self.etdn_sex_C.currentText())
            etdn_ads_E = str(self.etdn_ads_E.text())
            etdn_phn_E = str(self.etdn_phn_E.text())
            etdn_phnp_E = str(self.etdn_phnp_E.text())

            grp_text = literal_eval(self.etdn_grp_C.currentText())# pour convertir la chaine de caractere en dictionnaire
            etdn_grp_C = grp_text["رمز"]

            etdn_dmois_DE = str(self.etdn_dmois_DE.text())
            etdn_obsv_T = str(self.etdn_obsv_T.toPlainText())
            etdn_exempter_CB = str(self.etdn_exempter_val_CB)
            etdn_paye_CB = str(self.etdn_paye_val_CB)
            
            curs.execute("SELECT nombre_seances FROM groupe WHERE groupe_id = {id} LIMIT 1".format(id = int(etdn_grp_C)))
            etdn_seance_rest_var = curs.fetchone()[0]
            etdn_presence_var = 0
            etdn_absence_var = 0

            #creation de la donnee complete
            donnee = (
                etdn_nom_E,
                etdn_prnm_E,
                etdn_dnaissance_DE,
                etdn_sex_C, 
                etdn_ads_E, 
                etdn_phn_E ,
                etdn_phnp_E,
                etdn_grp_C,
                etdn_dmois_DE,
                etdn_obsv_T,
                etdn_exempter_CB,
                etdn_paye_CB,
                etdn_seance_rest_var,
                etdn_presence_var,
                etdn_absence_var,
                )
        
            conn.commit()
            conn.close()
            return donnee

    def etdn_ajout_B_func(self):

            donnee = self.etdn_tests_get()
            if donnee:
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()
                nom_donnee = str(('nom','prenom','date_naissance','sex','adresse','num_tel','num_telp','groupe_id','date_entree','observation','exempter','paye','seances_restantes','presence','absence'))
                curs.execute("INSERT INTO etudiant {} VALUES {}".format(nom_donnee,donnee))
                conn.commit()
                conn.close()

    def etdn_phn_CB_func(self):
        if self.etdn_phn_CB.isChecked():
            self.etdn_phn_E.setEnabled(False)
            self.etdn_phn_E.setText("0000000000")
        else:
            self.etdn_phn_E.setEnabled(True)
            self.etdn_phn_E.clear()
    
    def etdn_phnp_CB_func(self):
        if self.etdn_phnp_CB.isChecked():
            self.etdn_phnp_E.setEnabled(False)
            self.etdn_phnp_E.setText("0000000000")
        else:
            self.etdn_phnp_E.setEnabled(True)
            self.etdn_phnp_E.clear()
    
    def etdn_paye_CB_func(self):
        if self.etdn_paye_CB.isChecked():
            self.etdn_paye_val_CB = "نعم"
            self.etdn_exempter_val_CB = "لا"
            self.etdn_exempter_CB.setEnabled(False)
        else:
            self.etdn_paye_val_CB = "لا"
            self.etdn_exempter_CB.setEnabled(True)
    
    def etdn_exempter_CB_func(self):
        if self.etdn_exempter_CB.isChecked():
            self.etdn_exempter_val_CB = "نعم"
            self.etdn_paye_val_CB = "لا"
            self.etdn_paye_CB.setEnabled(False)
        else:
            self.etdn_exempter_val_CB = "لا"
            self.etdn_paye_CB.setEnabled(True)

    def etdn_grp_rech_C_Func(self):

        if self.etdn_grp_rech_C.currentIndex() == 0:
            while (self.etdn_list_TAB.rowCount() > 0):
                self.etdn_list_TAB.removeRow(0)
        else:
            grp_text = literal_eval(str(self.etdn_grp_rech_C.currentText()))

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            curs.execute("SELECT etudiant_id,nom,prenom,date_entree,exempter,paye,seances_restantes, presence,absence \
                FROM etudiant WHERE groupe_id = {id}".format(id = int(grp_text["رمز"])))
            d1 = curs.fetchall()

            while (self.etdn_list_TAB.rowCount() > 0):
                self.etdn_list_TAB.removeRow(0)
            
            self.etdn_list_TAB.setRowCount(0)
            self.etdn_list_TAB.insertRow(0)
            #verifier le contenu de la base de donnees puis remplir la table
            if d1:
                for row,form in enumerate(d1):
                    for column, item in enumerate(form):
                        self.etdn_list_TAB.setItem(row,column, QTableWidgetItem(str(item)))
                    row_position = self.etdn_list_TAB.rowCount()
                    self.etdn_list_TAB.insertRow(row_position)
            conn.commit()
            conn.close()    
   
    def etdn_mise_B_func(self):
        conn = sqlite3.connect("salam_school.db")
        curs = conn.cursor()
        if self.etdn_grp_rech_C.currentIndex() == 0:
            while (self.etdn_list_TAB.rowCount() > 0):
                self.etdn_list_TAB.removeRow(0)
            
            while (self.etdn_grp_C.count() > 0):
                self.etdn_grp_C.removeItem(0)
                self.etdn_grp_rech_C.removeItem(0)
            
            self.etdn_grp_C.addItem("غير محدد")
            self.etdn_grp_rech_C.addItem("غير محدد")
            curs.execute("SELECT groupe_id,num,phase,niveau,spec,matiere,prof_nom,nombre_seances FROM groupe")
            datas = curs.fetchall()
            for d1 in datas:
                data  ={
                        "رمز":d1[0],
                        "فوج":d1[1],
                        "طور":d1[2],
                        "مستوى":d1[3],
                        "تخصص":d1[4],
                        "مادة":d1[5]
                        }
                self.etdn_grp_C.addItem(str(data))
                self.etdn_grp_rech_C.addItem(str(data))
        else:
            grp_text = literal_eval(str(self.etdn_grp_rech_C.currentText()))

            curs.execute("SELECT etudiant_id,nom,prenom,date_entree,exempter,paye,seances_restantes, presence,absence \
                FROM etudiant WHERE groupe_id = {id}".format(id = int(grp_text["رمز"])))
            d1 = curs.fetchall()

            while (self.etdn_list_TAB.rowCount() > 0):
                self.etdn_list_TAB.removeRow(0)
            
            self.etdn_list_TAB.setRowCount(0)
            self.etdn_list_TAB.insertRow(0)
            #verifier le contenu de la base de donnees puis remplir la table
            if d1:
                for row,form in enumerate(d1):
                    for column, item in enumerate(form):
                        self.etdn_list_TAB.setItem(row,column, QTableWidgetItem(str(item)))
                    row_position = self.etdn_list_TAB.rowCount()
                    self.etdn_list_TAB.insertRow(row_position)
            conn.commit()
            conn.close()    

    def etdn_select_TAB_Func(self):
        ligne_select = self.etdn_list_TAB.currentRow()
        if self.etdn_list_TAB.rowCount() == 0:
            pass
        else:
           
            self.donnee = []
            self.etdnId = self.etdn_list_TAB.item(ligne_select,0).text()
            
            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            
            #effectuer une recherche des données

            curs.execute('SELECT nom,prenom,date_naissance,date_entree,sex,adresse,num_tel,num_telp,groupe_id,observation FROM etudiant WHERE \
                etudiant_id = (?)  LIMIT 1', self.etdnId)
            
            d1 = curs.fetchone() 
            self.donnee = list(d1)
            
            #envoyer les données vers les champs d'edition
            self.etdn_nom_E.setText( self.donnee[0])
            self.etdn_prnm_E.setText( self.donnee[1])
            self.etdn_dnaissance_DE.setDate(QDate().fromString(self.donnee[2],"yyyy/MM/dd"))
            self.etdn_dmois_DE.setDate(QDate().fromString(self.donnee[3],"yyyy/MM/dd")) #date d'entree

            self.etdn_sex_C.setCurrentIndex(self.etdn_sex_C.findText( self.donnee[4]))
            self.etdn_ads_E.setText( self.donnee[5])
            self.etdn_phn_E.setText( self.donnee[6])
            self.etdn_phnp_E.setText( self.donnee[7])
            self.etdn_grp_C.setCurrentIndex(self.etdn_grp_C.findText(self.etdn_grp_rech_C.currentText()))
            self.etdn_obsv_T.setPlainText( self.donnee[9])
            
            conn.commit()
            conn.close()

    def etdn_supp_B_func(self):
        
        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد التلميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            reponse = QMessageBox.question(self, "حذف تلميذ","هل تريد حذف التلميذ حقا؟",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            
            if reponse == QMessageBox.No:
                pass
            else:
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()
                donnee_rech = self.etdnId
                curs.execute('DELETE FROM etudiant WHERE etudiant_id = (?)', donnee_rech)            
                self.etdn_list_TAB.removeRow(select_ligne)
                
                conn.commit()
                conn.close()
    
    def etdn_edit_B_func(self):

        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد التلميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            donnee = self.etdn_tests_get()

            if donnee:
                #connection dans la base de donnee
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()
                donnee_rech = self.etdnId
                nom_donnee = str(('nom','prenom','date_naissance','sex','adresse','num_tel','num_telp','groupe_id','date_entree','observation','exempter','paye'))
                curs.execute("UPDATE etudiant SET {} = {} WHERE etudiant_id = (?)".format(nom_donnee,donnee[0:12]),donnee_rech)

                conn.commit()
                conn.close()    
    
    def etdn_prnt_B_func(self):
        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد التلميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            etudiant_select = self.etdnId

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            curs.execute("""UPDATE etudiant 
                            SET 
                                presence = presence + 1, 
                                seances_restantes =seances_restantes - 1 
                            WHERE 
                                etudiant_id = (?) AND seances_restantes > 0  AND seances_restantes <= 4""", etudiant_select)
            
            conn.commit()
            conn.close()
    
    def etdn_abst_B_func(self):
        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد التلميذ",QMessageBox.Close,QMessageBox.Close)

        else:
            etudiant_select = self.etdnId

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            curs.execute("""UPDATE etudiant 
                            SET 
                                absence = absence + 1, 
                                seances_restantes =seances_restantes - 1 
                            WHERE 
                                etudiant_id = (?) AND seances_restantes > 0  AND seances_restantes <= 4""", etudiant_select)
                        
            conn.commit()
            conn.close()
        
    def etdn_jabst_B_func(self):
        select_ligne = self.etdn_list_TAB.currentRow()

        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد التلميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            etudiant_select = self.etdnId

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            curs.execute("""UPDATE etudiant 
            SET 
                absence = absence - 1, 
                seances_restantes =seances_restantes + 1 
            WHERE 
                etudiant_id = (?) AND absence > 0  AND seances_restantes < 4""", etudiant_select)
            
            
            conn.commit()
            conn.close()

    def etdn_renouv_B_func(self):
        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد التلميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            etudiant_select = self.etdnId

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            
            curs.execute("SELECT nombre_seances FROM groupe WHERE groupe_id = {} LIMIT 1".format(etudiant_select[0]))
            seances_restantes = curs.fetchone()[0]
            
            curs.execute("""UPDATE etudiant 
                            SET 
                                presence = 0 ,
                                absence = 0, 
                                seances_restantes = {} 
                            WHERE 
                                etudiant_id = (?)""".format(seances_restantes), etudiant_select)
            
            conn.commit()
            conn.close()

    def etdn_st_B_func(self):
        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد قائمة التلاميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            grp_text = literal_eval(self.etdn_grp_rech_C.currentText())# pour convertir la chaine de caractere en dictionnaire
            etdn_grp_id = int(grp_text["رمز"])

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            curs.execute("""UPDATE etudiant 
                            SET 
                                presence = presence + 1,
                                seances_restantes = seances_restantes - 1 
                            WHERE groupe_id ={} AND seances_restantes > 0  AND seances_restantes <= 4""".format(etdn_grp_id))
            
            conn.commit()
            conn.close()

    def etdn_renouv_tout_B_func(self):
        select_ligne = self.etdn_list_TAB.currentRow()
        try: 
            if len(self.etdn_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            QMessageBox.warning(self,"جدولة فارغة","يرجى تحديد قائمة التلاميذ",QMessageBox.Close,QMessageBox.Close)
        else:
            grp_text = literal_eval(self.etdn_grp_rech_C.currentText())# pour convertir la chaine de caractere en dictionnaire
            etdn_grp_id = int(grp_text["رمز"])

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()
            curs.execute("SELECT nombre_seances FROM groupe WHERE groupe_id = {} LIMIT 1".format(etdn_grp_id))
            seances_restantes = curs.fetchone()[0]
    
            curs.execute("""UPDATE etudiant 
                            SET 
                                presence = 0,
                                absence = 0, 
                                seances_restantes = {} 
                            WHERE 
                                groupe_id = {}""".format(seances_restantes,etdn_grp_id))
            conn.commit()
            conn.close()
        
   # def etdn_grp_rech_E_func(self):

    

#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------espace prof----------------------------------------------------------------
    def prf_tests_get(self):
        self.conditions_prf_1 = str(self.prf_nom_E.text()) == "" or str(self.prf_prnm_E.text()) == "" or str(self.prf_ads_E.text()) == "" or str(self.prf_phn_E.text()) == ""
        self.conditions_prf_2 = str(self.prf_nom_E.text()).isdigit() or str(self.prf_prnm_E.text()).isdigit()
        

        if self.conditions_prf_1:
            QMessageBox.warning(self,"حقل فارغ", "أحد الحقول فارغة",QMessageBox.Ok,QMessageBox.Ok)
            
        elif self.conditions_prf_2:
            QMessageBox.warning(self,"قيمة غير مناسبة", "يرجى ادخال قيم مناسبة في الحقول!",QMessageBox.Ok,QMessageBox.Ok)
            self.prf_nom_E.clear(), self.prf_prnm_E.clear()

        else:
            prf_nom_E = str (self.prf_nom_E.text())
            prf_prnm_E = str(self.prf_prnm_E.text())
            prf_sex_C = str(self.prf_sex_C.currentText())
            prf_phn_E = str(self.prf_phn_E.text())
            prf_ads_E = str(self.prf_ads_E.text())
            prf_email_E = str(self.prf_email_E.text())
            prf_dmois_DE = str(self.prf_dmois_DE.text())
            prf_obsv_T = str(self.prf_obsv_T.toPlainText())
            #creation de la donnee complete
            donnee = (
                        prf_nom_E,
                        prf_prnm_E,
                        prf_sex_C,
                        prf_phn_E,
                        prf_ads_E,
                        prf_email_E,
                        prf_dmois_DE,
                        prf_obsv_T
                    )
            return donnee

    def prf_ajout_B_func(self):

        donnee = self.prf_tests_get()
        if donnee:
            #connection dans la base de donnee
            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()

            
            nom_donnee = str(('nom','prenom','sex','num_tel','adresse','email','date_entree','observation'))
            curs.execute("INSERT INTO prof {} VALUES {}".format(nom_donnee,donnee))

            curs.execute("SELECT prof_id,nom,prenom,num_tel,email,date_entree FROM prof ORDER BY rowid DESC LIMIT 1")
            d1 = curs.fetchone()
            conn.commit()

            data = str(d1[1] + " " + d1[2])
            self.grp_prof_C.addItem(data)

            if d1:
                row_position = self.prf_list_TAB.rowCount()-1
                self.prf_list_TAB.insertRow(row_position)
                for column,item in enumerate(d1):
                    self.prf_list_TAB.setItem(row_position,column, QTableWidgetItem(str(item)))

            conn.commit()
            conn.close()    
    
    def prf_select_TAB_Func(self):
        if self.prf_list_TAB.rowCount() == 0:
            pass
        else:
            ligne_select = self.prf_list_TAB.currentRow()
            self.donnee_p = str(self.prf_list_TAB.item(ligne_select,0).text())

            conn = sqlite3.connect("salam_school.db")
            curs = conn.cursor()

            curs.execute("SELECT * FROM prof WHERE prof_id = {id} LIMIT 1".format(id = self.donnee_p))
            d1 = curs.fetchone()

            self.prf_nom_E.setText(str(d1[1]))
            self.prf_prnm_E.setText(str(d1[2]))
            self.prf_sex_C.setCurrentIndex(self.prf_sex_C.findText(d1[3]))
            self.prf_phn_E.setText(str(d1[4]))
            self.prf_ads_E.setText(str(d1[5]))
            self.prf_email_E.setText(str(d1[6]))
            self.prf_dmois_DE.setDate(QDate().fromString(d1[7],"yyyy/MM/dd"))
            self.prf_obsv_T.setPlainText(str(d1[8]))
    
    def prf_supp_B_func(self):
        select_ligne = self.prf_list_TAB.currentRow()
        try: 
            if len(self.prf_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            pass
        else:
            reponse = QMessageBox.question(self, "حذف أستاذ","هل تريد حذف الأستاذ حقا؟",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if reponse == QMessageBox.No:
                pass
            else:
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()

                prf_id = int(self.prf_list_TAB.item(select_ligne,0).text())
                curs.execute("SELECT nom, prenom FROM prof WHERE prof_id = {id}".format(id = prf_id))
                d1 = curs.fetchone()
                curs.execute("DELETE FROM prof WHERE prof_id = {id}".format(id = prf_id))
                self.prf_list_TAB.removeRow(select_ligne)
                self.grp_prof_C.removeItem(self.grp_prof_C.findText(d1[0] + " " + d1[1]))

                conn.commit()
                conn.close()

    def prf_edit_B_func(self):
        select_ligne = self.prf_list_TAB.currentRow()
        try: 
            if len(self.prf_list_TAB.item(select_ligne,0).text()) == 0:
                pass
        except AttributeError:
            pass    
        else:
            donnee = self.prf_tests_get()
            if donnee:
                conn = sqlite3.connect("salam_school.db")
                curs = conn.cursor()

                #pour modefier le nom et prenom du prof dans le combobox dans groupe
                curs.execute("SELECT nom,prenom FROM prof WHERE prof_id = {} LIMIT 1".format(self.donnee_p))
                d1 = curs.fetchone()
                self.grp_prof_C.removeItem(self.grp_prof_C.findText(d1[0] + " " + d1[1]))

                nom_donnee = str(('nom','prenom','sex','num_tel','adresse','email','date_entree','observation'))
                curs.execute("UPDATE prof SET {} = {} WHERE prof_id = {}".format(nom_donnee,donnee, self.donnee_p))

                curs.execute("SELECT prof_id,nom,prenom,num_tel,email,date_entree FROM prof WHERE prof_id = {} LIMIT 1".format(self.donnee_p))
                d1 = curs.fetchone()

                data = str(d1[1] + " " + d1[2])
                self.grp_prof_C.addItem(data)

                if d1:  
                    for column,item in enumerate(d1):
                        self.prf_list_TAB.setItem(select_ligne,column, QTableWidgetItem(str(item)))

                conn.commit()
                conn.close()    
#---------------------------------------------------------------------------------------------------------------------

#----------------------------------------------Caisse--------------------------------------------------------
    def csAdmin_B_func(self):
        self.tabWidget_3.setCurrentIndex(0)
    def csProf_B_func(self):
        self.tabWidget_3.setCurrentIndex(1)
    def csEtdn_B_func(self):
        self.tabWidget_3.setCurrentIndex(2)
    
    
    def csetdn_imprim_B_func(self):
        imp = QPrinter(QPrinter.HighResolution)
        previewdialog = QPrintPreviewDialog(imp,self)
        previewdialog.paintRequested.connect(self.print_preview)
        previewdialog.exec_()
    def print_preview(self,imp):
        self.csetdn_bon_ET.print_(imp)

   

def main():
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    app.exec_()

if __name__=="__main__":
    main()




