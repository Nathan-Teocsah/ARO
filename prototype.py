import numpy as np
import copy
import subprocess
import random as rd

# On ne peut relier plusieurs proposition qu'à une démonstration ou une remarque mais à rien d'autres

class note:
    nb = 0
    def __init__(self, file, Note=None): # file peut être soit un nom de fichier soit un nouvel élément à ajouter
        if Note==None :
            try : self.num = int(file.readline())
            except : raise ValueError("Le fichier est fini")
            self.type = file.readline().rstrip('\n')
            self.complet = int(file.readline())
            file.readline()
            self.__line_prec = file.readline()
            self.__line_suiv = file.readline()
            self.__line = self.__line_prec if self.__line_suiv != "}\n" else self.__line_prec.rstrip('\n')
            while self.__line_suiv != "}\n":
                self.__line_prec = self.__line_suiv
                self.__line_suiv = file.readline()
                self.__line += self.__line_prec if self.__line_suiv != "}\n" else self.__line_prec.rstrip('\n')
            self.contenu = self.__line
            try : self.entre = [int(numero) for numero in file.readline().split()]
            except : self.entre = []
            try : self.sortie = [int(numero) for numero in file.readline().split()]
            except : self.sortie = []
            note.nb = self.num
        else :
             self.num = note.nb
             self.type = Note[0]
             self.complet = Note[1]
             self.contenu = Note[2]
             self.entre = Note[3]
             self.sortie = Note[4]
             with open(file,"a") as fichier :
                ligne3 = " ".join(map(str,self.entre)) if self.entre!=[] else "_"
                ligne4 = " ".join(map(str,self.sortie)) if self.sortie!=[] else "_"
                bloc = f"------ Note {self.num} ------\n" + str(self.num) + "\n" + self.type + "\n" + str(self.complet) +"\n" +"{\n" + self.contenu + "\n}\n" + ligne3 + "\n" + ligne4 + "\n"
                fichier.write(bloc)

        self.nature = "note"
        note.nb = note.nb + 1
        print(f"---> creation d'un objet de type Note numéro {self.num}")

    def liste(self):
        return [self.num,self.type,self.complet,self.contenu,self.entre,self.sortie]
    
    def montre(self,path_pdf_note):
        self.__proc = subprocess.Popen(["xpdf", "-geometry 600x200+100+100", "-z 250" , path_pdf_note + f"{self.num}" + ".pdf"])

    def stop_montre(self):
        self.__proc.terminate()

    def sup(self,path_pdf,path_pdf_rel,path_note,filename_note,filename_relation,liste_note,liste_relation): 
        filename = f"{self.num}"
        num = self.num
        rang = 0
        while self.num != liste_note[rang].num:
            rang += 1
        def conversion(Note):
             Note[0] = str(Note[0])
             Note[2] = str(Note[2])
             i=3
             Note[i] = "{\n" + Note[i] + "\n}"
             Note[i+1] = " ".join(map(str,Note[i+1])) if Note[i+1]!=[] else "_"
             Note[i+2] = " ".join(map(str,Note[i+2])) if Note[i+2]!=[] else "_"
        def trouve_rel(liste_relation,num):
            L = []
            for k in range(len(liste_relation)):
                if num in liste_relation[k].extremite :
                    L.append(k)
            return L

        Liste_rel_a_supprimer = trouve_rel(liste_relation,self.num)
        liste_relation_copy = copy.copy(liste_relation)
        for k in Liste_rel_a_supprimer :
            liste_relation_copy[k].sup(path_pdf_rel,filename_relation,liste_relation,liste_note)

        del liste_note[rang]

        for Note in liste_note :
            if num in Note.entre :
                Note.entre.remove(num)
            if num in Note.sortie :
                Note.sortie.remove(num)

        self.__Liste = [line.liste() for line in liste_note]
        for i in range(len(self.__Liste)) : 
             Num = self.__Liste[i][0]
             conversion(self.__Liste[i])
             self.__Liste[i] = f"----- Note {Num} ------\n" + "\n".join(self.__Liste[i])+"\n"
        with open(path_note+filename_note, "w", encoding="utf-8") as file:
            for Note in self.__Liste :
                file.writelines(Note)
        subprocess.Popen(["rm", "-rf", path_pdf+filename+".pdf"])

        print(f"---> suppression de-l'objet Note numéro {self.num} et des relations associées")



class relation:
    nb = 0
    def __init__(self, file, Relation=None): # file peut être soit un nom de fichier soit un nouvel élément à ajouter
        if Relation==None :
            try : self.extremite = [int(Note) for Note in file.readline().split()] 
            except : raise ValueError("Le fichier est fini")
            self.claire = int(file.readline())
            self.type = file.readline().rstrip('\n')
            file.readline()
            self.__line_prec = file.readline()
            self.__line_suiv = file.readline()
            self.__line = self.__line_prec if self.__line_suiv != "}\n" else self.__line_prec.rstrip('\n')
            while self.__line_suiv != "}\n":
                self.__line_prec = self.__line_suiv
                self.__line_suiv = file.readline()
                self.__line += self.__line_prec if self.__line_suiv != "}\n" else self.__line_prec.rstrip('\n')
            self.contenu = self.__line
        else :
             self.extremite = Relation[0]
             self.claire = Relation[1]
             self.type = Relation[2]
             self.contenu = Relation[3]
             with open(file,"a") as fichier :
                bloc = f"--- Relation {relation.nb} ---\n" + " ".join(map(str,self.extremite)) + "\n" + str(self.claire) +"\n" + self.type + "\n" +"{\n" + self.contenu + "\n}\n"
                fichier.write(bloc)

        self.nature = "relation"
        self.num = relation.nb
        relation.nb = relation.nb + 1
        print(f"---> creation d'un objet de type Relation numéro {self.nb-1}")
         
    def liste(self):
        return [self.num, self.extremite,self.claire,self.type,self.contenu]
    
    def montre(self,path_pdf_rel):
        if self.contenu=="" : 
            print("--> Il n'y a pas de description")
        else :
            self.__proc = subprocess.Popen(["xpdf", "-geometry 600x200+100+100", "-z 250" , path_pdf_rel + f"{self.extremite[0]},{self.extremite[1]}" + ".pdf"])

    def stop_montre(self):
        if self.contenu!="":
            self.__proc.terminate()

    def sup(self,path_pdf,filename_relation,liste,liste_note): 
        num = 0
        filename = f"{self.extremite[0]},{self.extremite[1]}"
        while liste[num].extremite != self.extremite : num += 1
        def conversion(Rel):
             Rel[0] = str(Rel[0])
             Rel[1] = " ".join(map(str,Rel[1]))
             Rel[2] = str(Rel[2])
             Rel[4] = "{\n" + Rel[4] + "\n}"
        del liste[num]
        for k in range(len(liste_note)):
            for i in range(len(liste_note)):
                if self.extremite[0] == liste_note[k].num and self.extremite[1] == liste_note[i].num :
                    liste_note[k].sortie.remove(self.extremite[1])
                    liste_note[i].entre.remove(self.extremite[0])

        self.__Liste = [line.liste() for line in liste]
        for i in range(len(self.__Liste)) : 
             conversion(self.__Liste[i])
             self.__Liste[i] = f"-----  Relation {liste[i].num} ------\n" + "\n".join(self.__Liste[i][1:len(self.__Liste[i])])+"\n"
        with open(filename_relation, "w", encoding="utf-8") as file:
            for Rel in self.__Liste :
                file.writelines(Rel)
        subprocess.Popen(["rm", "-rf", path_pdf+filename+".pdf"])
        print(f"---> suppression de l'objet Relation numéro {num}")









'''******************************************************************************************************************
        Fonction nescaire à la compilation et la création des pdf et de la récupération des donnée utilisateur 
*********************************************************************************************************************'''

def mise_a_jour(liste_note,path_note,filename_note):
    def conversion(Note):
        Note[0] = str(Note[0])
        Note[2] = str(Note[2])
        i=3
        Note[i] = "{\n" + Note[i] + "\n}"
        Note[i+1] = " ".join(map(str,Note[i+1])) if Note[i+1]!=[] else "_"
        Note[i+2] = " ".join(map(str,Note[i+2])) if Note[i+2]!=[] else "_"
    Liste = [line.liste() for line in liste_note]
    for i in range(len(Liste)) : 
            Num = Liste[i][0]
            conversion(Liste[i])
            Liste[i] = f"----- Note {Num} ------\n" + "\n".join(Liste[i])+"\n"
    with open(path_note+filename_note, "w", encoding="utf-8") as file:
        file.writelines("".join(Liste))
    print("---> Mise à jour terminé du fichier : ",path_note+filename_note)

def mise_a_jour_rel(liste_relation,path_note,filename_relation):
    def conversion(Rel):
                 Rel[0] = str(Rel[0])
                 Rel[1] = " ".join(map(str,Rel[1]))
                 Rel[2] = str(Rel[2])
                 Rel[4] = "{\n" + Rel[4] + "\n}"
    Liste = [line.liste() for line in liste_relation]
    for i in range(len(Liste)) : 
            Num = Liste[i][0]
            conversion(Liste[i])
            Liste[i] = f"-----  Relation {liste_relation[i].num} ------\n" + "\n".join(Liste[i][1:len(Liste[i])])+"\n"
    with open(path_note+filename_relation, "w", encoding="utf-8") as file:
        file.writelines("".join(Liste))
    print("---> Mise à jour terminé du fichier : ",path_note+filename_relation)


def trouve_note(liste_note,num):
    for i in range(len(liste_note)):
        if liste_note[i].num == num :
            return i
    raise ValueError(f"Note numéro {num} de type {type(num)} introuvable dans : ",[liste_note[i].num for i in range(len(liste_note))])


def compile(path,filename,latex):
    print("Compilation en cours...")
    
    subprocess.run(["touch", path+filename+".tex"])
    latex_entete = r"""\documentclass[12pt,a4paper]{article}
\usepackage{package_affichage}

\begin{document}
"""

    latex = latex_entete + latex + r"""
\end{document}"""

    with open(path+filename+".tex", "w", encoding="utf-8") as f:
                f.write(latex)

    subprocess.run(["pdflatex", "-output-directory=" + path, path + filename + ".tex"],
        stdout=subprocess.DEVNULL
    )
    proc = subprocess.Popen(["xpdf", "-geometry 600x200+100+100", "-z 250" , path + filename + ".pdf"])
    
    subprocess.run(["rm", "-rf", path+filename+".aux", path+filename+".log", path+filename+".fls", path+filename+".out",path+filename+".fdb_latexmk",path+filename+".thm",path+filename+".fdb_latexmk"])

    return proc


def compile_tmp(path_tmp,editeur_latex,latex):
    print("Compilation en cours...")

    subprocess.run(["touch", path_tmp+"tmp.tex"])
    latex_entete = r"""\documentclass[12pt,a4paper]{article}
\usepackage{package_affichage}

% Ne rien écrire ici

\begin{document}
"""

    latex = latex_entete + latex + r"""
\end{document}"""

    print("--> Ouverture de "+editeur_latex+"...")
    with open(path_tmp+"tmp.tex", "w", encoding="utf-8") as f:
                f.write(latex)

    proc = subprocess.Popen([editeur_latex, path_tmp + "tmp.tex"],
        stdout=subprocess.DEVNULL
    )
    input("Si vous avez terminé l'édition, appuyer sur entrée pour valider les modification.")
    proc.terminate()


def compile_maitre(path,filename,latex):
    print("Compilation en cours...")
    subprocess.run(["touch", path+filename+".tex"])
    latex_entete = r"""\documentclass[12pt,a4paper]{article}
\usepackage{package_perso}

\begin{document}
"""

    latex = latex_entete + latex + r"""
\end{document}"""

    with open(path+filename+".tex", "w", encoding="utf-8") as f:
                f.write(latex)

    subprocess.run(["pdflatex", "-output-directory=" + path, path + filename + ".tex"],
        stdout=subprocess.DEVNULL
    )

    subprocess.run(["pdflatex", "-halt-on-error", "-output-directory=" + path, path + filename + ".tex"],
        stdout=subprocess.DEVNULL
    )
    
    #subprocess.run(["rm", "-rf", path+filename+".aux", path+filename+".log", path+filename+".fls", path+filename+".out",path+filename+".fdb_latexmk",path+filename+".thm",path+filename+".fdb_latexmk"])


def detect_note_loc_glob(texte,liste_note):
    liste_mot = texte.split()
    nv_texte = " "
    provisoire = ""
    for n in range(len(liste_mot)):
        mot = liste_mot[n]
        if "::" in mot :
            if provisoire != "" :
                nv_texte += provisoire
            provisoire = ""
            start = False
            compte = 0
            k = ""
            k_complet = False
            end = False
            for i in range(len(mot)) :
                if not start :
                    provisoire += mot[i]
                    if mot[i] == ":" :
                        compte += 1
                    else : 
                        nv_texte += provisoire
                        provisoire = ""
                        break
                    if compte == 2 :
                        compte = 0
                        start = True
                elif mot[i].isdigit() and not k_complet :
                    k += mot[i]
                    provisoire += mot[i]
                elif not end :
                    k_complet = True
                    if mot[i] == ":" :
                        compte += 1
                    elif compte<2 :
                        nv_texte += provisoire
                        provisoire = ""
                        break
                    if compte == 2 :
                        end = True
                else :
                    if k != "" :
                        nv_texte += f"::{liste_note[int(k)].num}::"
                        k = ""
                        provisoire = ""
                    nv_texte += mot[i]
            if k != "" and start and end :
                nv_texte += f"::{liste_note[int(k)].num}::"
                provisoire = ""
        else :
            nv_texte += liste_mot[n] + " "
    return nv_texte


def detect_note_glob_loc(texte,liste_note):
    liste_mot = texte.split()
    nv_texte = " "
    provisoire = ""
    for n in range(len(liste_mot)):
        mot = liste_mot[n]
        if "::" in mot :
            if provisoire != "" :
                nv_texte += provisoire
            provisoire = ""
            start = False
            compte = 0
            k = ""
            k_complet = False
            end = False
            for i in range(len(mot)) :
                if not start :
                    provisoire += mot[i]
                    if mot[i] == ":" :
                        compte += 1
                    else : 
                        nv_texte += provisoire
                        provisoire = ""
                        break
                    if compte == 2 :
                        compte = 0
                        start = True
                elif mot[i].isdigit() and not k_complet :
                    k += mot[i]
                    provisoire += mot[i]
                elif not end :
                    k_complet = True
                    if mot[i] == ":" :
                        compte += 1
                    elif compte<2 :
                        nv_texte += provisoire
                        provisoire = ""
                        break
                    if compte == 2 :
                        end = True
                else :
                    if k != "" :
                        nv_texte += f"::{trouve_note(liste_note,int(k))}::"
                        k = ""
                        provisoire = ""
                    nv_texte += mot[i]
            if k != "" and start and end :
                nv_texte += f"::{trouve_note(liste_note,int(k))}::"
                provisoire = ""
        else :
            nv_texte += liste_mot[n] + " "
    return nv_texte


def determinant(Type,liste_determinant,Choix_note):
    for i in range(len(Choix_note)):
        if Type == Choix_note[i]:
            return liste_determinant[i]
    raise ValueError(f"determinant pour {Type} introuvable")


def detect_note(texte,liste_note,liste_determinant,Choix_note):
    liste_mot = texte.split()
    nv_texte = " "
    provisoire = ""
    prec = ""
    for n in range(len(liste_mot)):
        mot = liste_mot[n]
        if "::" in mot :
            if provisoire != "" :
                nv_texte += provisoire
            provisoire = ""
            start = False
            compte = 0
            k = ""
            k_complet = False
            end = False
            for i in range(len(mot)) :
                if not start :
                    provisoire += mot[i]
                    if mot[i] == ":" :
                        compte += 1
                    else : 
                        nv_texte += provisoire
                        provisoire = ""
                        break
                    if compte == 2 :
                        compte = 0
                        start = True
                elif mot[i].isdigit() and not k_complet :
                    k += mot[i]
                    provisoire += mot[i]
                elif not end :
                    k_complet = True
                    if mot[i] == ":" :
                        compte += 1
                    elif compte<2 :
                        nv_texte += provisoire
                        provisoire = ""
                        break
                    if compte == 2 :
                        end = True
                else :
                    if k != "" :
                        k0 = trouve_note(liste_note,int(k))
                        Note = liste_note[k0] 
                        if Note.type != "équation":
                            nv_texte += (determinant(Note.type,liste_determinant,Choix_note).capitalize() if (prec=="" or prec ==".") else determinant(Note.type,liste_determinant,Choix_note)) + Note.type + r" \ref{"+Note.nature+f":{Note.num}"+r"} "
                        else :
                            nv_texte += (determinant(Note.type,liste_determinant,Choix_note).capitalize() if (prec=="" or prec ==".") else determinant(Note.type,liste_determinant,Choix_note)) + Note.type + r" \eqref{"+Note.nature+f":{Note.num}"+r"} "
                        k = ""
                        provisoire = ""
                    nv_texte += mot[i]
                prec = mot[i]
            if k != "" and start and end :
                k0 = trouve_note(liste_note,int(k))
                Note = liste_note[k0] 
                if Note.type != "équation":
                    nv_texte += (determinant(Note.type,liste_determinant,Choix_note).capitalize() if (prec=="" or prec ==".") else determinant(Note.type,liste_determinant,Choix_note)) + Note.type + r" \ref{"+Note.nature+f":{Note.num}"+r"} "
                else :
                    nv_texte += (determinant(Note.type,liste_determinant,Choix_note).capitalize() if (prec=="" or prec ==".") else determinant(Note.type,liste_determinant,Choix_note)) + Note.type + r" \eqref{"+Note.nature+f":{Note.num}"+r"} "
                k = ""
                provisoire = ""
        else :
            nv_texte += liste_mot[n] + " "
        prec = mot[len(mot)-1]
    return nv_texte


def edit_contenu_note(liste_note,num_note,path_tmp,path_note,filename_note,editeur_latex):
    def trouve(liste_note,num):
        for k in range(len(liste_note)):
            if liste_note[k].num == num :
                return k
        raise ValueError(f"trouve pour num = {num} dans edit_contenu_note")

    k0 = trouve(liste_note,num_note)
    latex = liste_note[k0].contenu
    compile_tmp(path_tmp,editeur_latex,latex)
    print("---> Récupération du nouveau texte...")
    latex = ""
    with open(path_tmp+"tmp.tex","r") as file :
        ligne = file.readline()
        while r"\end{document}" not in ligne :
            if r"\begin{document}" in ligne :
                latex = ""
            else:
                latex += ligne
            ligne = file.readline()
    liste_note[k0].contenu = latex
    print("---> Texte récupéré !")
    print("---> Mise à jour en cours... ")
    mise_a_jour(liste_note,path_note,filename_note)

def edit_relation(rel,Note1,Note2,Choix_rel,liste_relation,path_tmp,path_note,filename_relation,editeur_latex):
    while True :
        print("Que voulez vous modifier ?")
        if rel.type!="Equivalence":
            print("1) Le statut de la relation (justifié ou non).")
            print("2) Le type de la relation.")
            print("3) Son contenu.")
            continuer = True
            while continuer :
                rep = int(input("Réponse : "))
                if rep>=1 and rep <=3 :
                    continuer = False
                else : 
                    print("--- Choix invalide ---")
        else :
            print("1) Le statut de la relation (justifié ou non).")
            print("2) Le type de la relation.")
            continuer = True
            while continuer :
                rep = int(input("Réponse : "))
                if rep>=1 and rep <=2 :
                    continuer = False
                else : 
                    print("--- Choix invalide ---")
        if rep == 1 :
            if input("Etes-vous capable de justifier cette relation ? (o/n) ")=="n":
                rel.claire = 0
            else :
                rel.claire = 1
        if rep == 2:
            Choix = Choix_rel.copy()
            if Note1.type == "équation" and Note2.type == "équation":
                protege_équation=True
            if not protege_équation :
                Choix.remove("Equivalence")
            rel.type = choix_type(Choix)
            if rel.type=="Equivalence":
                rel.contenu = ""

        if rep == 3 :
            latex = rel.contenu
            compile_tmp(path_tmp,editeur_latex,latex)
            print("---> Récupération du nouveau texte...")
            latex = ""
            with open(path_tmp+"tmp.tex","r") as file :
                ligne = file.readline()
                while r"\end{document}" not in ligne :
                    if r"\begin{document}" in ligne :
                        latex = ""
                    else:
                        latex += ligne
                    ligne = file.readline()
            rel.contenu = latex
            print("---> Texte récupéré !")
        print("---> Mise à jour en cours... ")
        mise_a_jour_rel(liste_relation,path_note,filename_relation)

        if input("Voulez vous continuer à éditer cette relation  ? (o/n) ")!="o" :
            break

    

def choix_type(Choix):
    New_Choix = Choix.copy()
    New_Choix.append("Arrêt du programme")
    print("\n--------------------------------")
    print("Choix possible :")
    for i in range(len(New_Choix)):
        print(f"{i})",New_Choix[i])
    continuer = 1
    while continuer==1 :
        continuer = 0
        try : 
            type = New_Choix[int(input("\nType : "))]
        except : 
            continuer = 1
            print("--- Choix invalide ---")
    print("---------------------------------\n")
    if type==New_Choix[-1]: raise ValueError("Arrêt du programme")
    return type


def choix_description(path_tmp):
    print("---- Descrition ----")
    reponse = input("Voulez vous écrire dans l'invite de commande ou dans l'éditeur (i/e) ? ")
    if reponse=="e":
        print("--> Ouverture de "+editeur_latex+"...")
        proc = subprocess.Popen([editeur_latex, path_tmp + "tmp.tex"],
                stdout=subprocess.DEVNULL
            )
        input("Si vous avez terminé l'édition, appuyer sur entrée pour valider les modification.")
        proc.terminate()
        latex = ""
        with open(path_tmp+"tmp.tex","r") as file :
            ligne = file.readline()
            while r"\end{document}" not in ligne :
                if r"\begin{document}" in ligne :
                    latex = ""
                else:
                    latex += ligne
                ligne = file.readline()
    else:
        reponse = input("\npour quitte appuyer sur 'entrer' puis ':q'\nDescription :\n")
        repondu = 0
        latex = ""
        while reponse != ":q" or repondu == 0:
            latex += reponse 
            reponse = input()
            if reponse !=":q":
                latex += "\n"
            repondu = 1
    return latex


def creer_relation_pour_note(Note1,Note2,type_Note,liste_note,path_pdf_lien,path_tmp,path_Note,filename_relation,Choix_rel):
    Choix = copy.deepcopy(Choix_rel)
    def trouve(liste_note,num):
        for k in range(len(liste_note)):
            if liste_note[k].num == num :
                return k
        return k+1
    extremite = [Note1,Note2]
    claire = 0 if input(f"\nLa relation de la note {trouve(liste_note,Note1)} vers la note {trouve(liste_note,Note2)} est elle bien définie (justifé) ? (o/n) ")=="n" else 1
    protege_équation=False
    k1 = trouve(liste_note,Note1)
    k2 = trouve(liste_note,Note2)
    if k1 == len(liste_note):
        type1 = type_Note
    else :
        type1 = liste_note[k1].num
    if k2 == len(liste_note):
        type2 = type_Note
    else :
        type2 = liste_note[k2].num
    if type1 == "équation" and type2 == "équation":
        protege_équation=True
    if protege_équation :
        Choix.remove("Equivalence")
    type = choix_type(Choix)
    contenu = choix_description(path_tmp)
    if contenu != "" and contenu != "\n":
        proc = compile(path_pdf_lien,f"{Note1},{Note2}",contenu)
    else : 
        contenu = ""
    while True :
        reponse = input("\nVoulez-vous modifier vos réponses ? (o/n) ")
        if reponse!="o": break
        print("\n-------- Relation -----------")
        print("Claire ? ","oui" if claire else "non")
        print("Type : ",type)
        print("Description :\n")
        print(contenu)
        print("-------- Fin Relation -----------")
        if input("Voulez vous modifier le statut de cette relation (définie ou pas) ? (o/n) ")=="o": claire = 0 if input("\nLa relation entre ces 2 noeuds est elle bien définie (justifé) ? (o/n) ")=="n" else 1
        if input("Voulez vous modifier le type ? (o/n) ")=="o": type = choix_type(Choix)
        if type!=Choix[0]:
            if input("Voulez vous modifier la description ? (o/n) ")=="o": contenu = choix_description(path_tmp)
            proc.terminate()
            if contenu != "" or contenu != "\n" :
                proc = compile(path_pdf_lien,f"{Note1},{Note2}",contenu)
        else : 
            contenu = ""
    if contenu!="":
        proc.terminate()
    return relation(path_Note+filename_relation,[extremite,claire,type,detect_note_loc_glob(contenu,liste_note)])


def creer_Note(path_pdf_Note,path_pdf_Lien,path_Note,path_tmp,filename_note,liste_note,liste_relation,Choix_note,Choix_rel,Protege,filename_relation):

    print(f"-------------------- CREATION DE LA NOTE {note.nb} -------------------")

    filename = str(note.nb)
    Choix = copy.deepcopy(Choix_note)

    if len(liste_note)!= 0:
        entre_loc = input("Impliquation de qui ? ").split()
        entre_glob = [liste_note[int(e)].num for e in entre_loc]
        entre = " ".join(map(str,entre_glob))

        sortie_loc = input("Implique qui ? ").split()
        sortie_glob = [liste_note[int(s)].num for s in sortie_loc]
        sortie = " ".join(map(str,sortie_glob))
    else :
        entre = ""
        sortie = ""
    protege_active = False
    for num in (entre+" "+sortie).split():
        k_num = trouve_note(liste_note,int(num))
        if liste_note[k_num].type in Protege :
            protege_active = True
            break
    if protege_active :
        for type in Protege:
            Choix.remove(type)
    ok=False
    while not ok :
        type = choix_type(Choix)
        if protege_active and type in Protege :
            print("---> "+type+" ne peut à être associé à une Note parmi les types suivants :\n"+", ".join(Protege))
        else :
            ok=True
    latex = choix_description(path_tmp)
    complet = 0 if input("La description est-elle complète ? (o/n) ")=="n" else 1
    if latex != "" or latex != "\n":
        print("---> Visualisation de la description...")
        proc = compile(path_pdf_Note,filename,latex)
    while True :
        reponse = input("\nVoulez-vous modifier vos réponses ? (o/n) ")
        if reponse!="o": break
        print("\n-------- Note -----------")
        print("Type : ",type)
        print("Description :\n")
        print(latex)
        print("Complet ? "+"oui" if complet else "non")
        print("Implication de qui ? ",entre_loc)
        print("Implique qui ? ",sortie_loc)
        print("-------- Fin Note -----------")
        if input("Voulez vous modifier le type ? (o/n) ")=="o": type = choix_type(Choix)
        if input("Voulez vous modifier la description ? (o/n) ")=="o": latex = choix_description(path_tmp)
        if input("Voulez vous le statut de la description (complet ou pas) ? (o/n) ")=="o": complet = 0 if input("La description est-elle complète ? (o/n) ")=="n" else 1
        if input("Voulez vous modifier de qui est-ce impliqué ? (o/n) ")=="o": entre_loc = input("Impliquation de qui ? ").split()
        if input("Voulez vous modifier qui ça implique ? (o/n) ")=="o": sortie_loc = input("Implique qui ? ").split()
        entre_glob = [liste_note[int(e)].num for e in entre_loc]
        entre = " ".join(map(str,entre_glob))
        sortie_glob = [liste_note[int(s)].num for s in sortie_loc]
        sortie = " ".join(map(str,sortie_glob))
        proc.terminate()
        if latex != "" or latex != "\n":
            print("---> Visualisation de la description...")
            proc = compile(path_pdf_Note,filename,latex)
    proc.terminate()
    rel = []
    if entre != "":
        print("\n-------------------- relations entrantes --------------------------")
        depart = [int(x) for x in entre.split()]
        Note_arrive = note.nb
        for Note_depart in depart :
            rel.append(creer_relation_pour_note(Note_depart,Note_arrive,type,liste_note,path_pdf_Lien,path_tmp,path_Note,filename_relation,Choix_rel))
            liste_note[trouve_note(liste_note,Note_depart)].sortie += [Note_arrive]
    if sortie != "":
        print("\n-------------------- relations sortantes --------------------------")
        arrive = [int(x) for x in sortie.split()]
        Note_depart = note.nb
        for Note_arrive in arrive :
            rel.append(creer_relation_pour_note(Note_depart,Note_arrive,type,liste_note,path_pdf_Lien,path_tmp,path_Note,filename_relation,Choix_rel))
            liste_note[trouve_note(liste_note,Note_arrive)].entre += [Note_depart]
    if sortie != "" or entre != "":
        mise_a_jour(liste_note,path_Note,filename_note)
    liste_note.append(note(path_Note+filename_note,[type,complet,detect_note_loc_glob(latex,liste_note),[int(x) for x in entre.split()],[int(x) for x in sortie.split()]]))
    liste_relation += rel


def composante_connexe(liste_note):
    def union(A,B):
        stop="non"
        for a in A :
            for b in B :
                if a == b :
                    stop="oui"
                    break
            if stop=="oui" :
                break
        if stop=="non" :
            return []
        return A+B
    
    def insertion(liste,B):
        inserer="non"
        for n in range(len(liste)) :
            if len(union(liste[n],B)) > 0 :
                liste[n] = union(liste[n],B)
                inserer="oui"
                break
        if len(liste)==0 or inserer=="non":
            liste.append(B)
        
    def nettoyage_doublon(liste):
        for i in range(len(liste)) :
            B = []
            for a in liste[i] :
                if a not in B :
                    B.append(a)
            liste[i] = B

    n = len(liste_note)
    Graphe1 = []
    Graphe = []
    for note in liste_note :
        B = [note.num]+note.entre+note.sortie
        insertion(Graphe1,B)

    for i in range(len(Graphe1)):
        dernier_inserer="non"
        for j in range(i+1,len(Graphe1)):
            if len(union(Graphe1[i],Graphe1[j])) > 0:
                Graphe.append(union(Graphe1[i],Graphe1[j]))
                if j == len(Graphe1)-1:
                    dernier_inserer="oui"
            else :
                Graphe.append(Graphe1[i])
    if dernier_inserer=="non":
        Graphe.append(Graphe1[-1])

    nettoyage_doublon(Graphe)

    return Graphe


def niveau(liste_note):
    def trouve(num,liste_note):
        k=0
        for liste in liste_note:
            if num==liste.num :
                return k
            k=k+1
        raise ValueError(f"trouve pour num = {num} dans niveau")
    
    def niveau_max(C0,liste_note,niv):
        for num in C0 :
            k = trouve(num,liste_note)
            sortie = liste_note[k].sortie
            if len(sortie) != 0:
                niv = max(niv,niveau_max(sortie,liste_note,niv+1))
        return niv
    
    def niveau_elt(niv_max,C0,liste_note,Niv):
        for num in C0:
            k = trouve(num,liste_note)
            if len(liste_note[k].sortie)==0:
                Niv[k] = niv_max
            else :
                for num_sortie in liste_note[k].sortie:
                    k_sortie = trouve(num_sortie,liste_note)
                    Niv[k_sortie] += 1
                C_sortie = liste_note[k].sortie
                niveau_elt(niv_max,C_sortie,liste_note,Niv)
            
    Comp = composante_connexe(liste_note)
    Niv=[0 for i in range(len(liste_note))]
    Niv_comp=[[0 for i in range(len(Comp[k]))] for k in range(len(Comp))]
    for c in range(len(Comp)):
        C0=[] #Niveau 0
        for num in Comp[c]:
            k = trouve(num,liste_note)
            if len(liste_note[k].entre)==0:
                C0.append(num)

        niv_max=niveau_max(C0,liste_note,0)
        niveau_elt(niv_max,C0,liste_note,Niv)

        for i in range(len(Comp[c])):
            num = Comp[c][i]
            k = trouve(num,liste_note)
            Niv_comp[c][i] = Niv[k]

    return Niv,Niv_comp


def max_depth(liste_note):
    def trouve(num,liste_note):
            k=0
            for liste in liste_note:
                if num==liste.num :
                    return k
                k=k+1
            raise ValueError(f"trouve pour num = {num} dans max_depth")

    def raisonnement(liste_note,num_debut,num_debut_init,num_fin,Chemin,Liste_Chemin):
        k = trouve(num_debut,liste_note)
        sortie = liste_note[k].sortie
        Chemin.append(num_debut)
        if num_debut!=num_fin:
            for num_sortie in sortie :
                raisonnement(liste_note,num_sortie,num_debut_init,num_fin,Chemin,Liste_Chemin)
                if num_fin in Chemin and num_debut_init==num_debut:
                    Liste_Chemin.append(Chemin)
                Chemin = [num_debut_init]

    def test_presence(Liste,elem):
        for L in Liste:
            if elem in L :
                return True
        return False

    def doublon(Chemin):
        nv_Chemin = copy.deepcopy(Chemin)
        def extrem(C):
            return [C[0],C[-1]]
        extremite = []
        def ajoute(Liste,elem):
            if elem not in Liste :
                Liste.append(elem)
                return True
            return False
        for C in nv_Chemin :
            if not ajoute(extremite,extrem(C)):
                Chemin.remove(C)


    Comp_connexe = composante_connexe(liste_note)
    C0 = [[] for i in range(len(Comp_connexe))]
    Liste_Chemin=[[] for i in range(len(Comp_connexe))]
    Fin = [[] for i in range(len(Comp_connexe))]
    for c in range(len(Comp_connexe)):
        ElemL0 = []
        Liste_Chemin0=[]
        for i in range(len(Comp_connexe[c])):
            k = trouve(Comp_connexe[c][i],liste_note)
            if len(liste_note[k].sortie) == 0 :
                Fin[c].append(Comp_connexe[c][i])
                ElemL00 = []
                Chemin = []
                for k in range(len(Comp_connexe[c])) :
                    k0 = trouve(Comp_connexe[c][k],liste_note)
                    if len(liste_note[k0].entre)==0:
                        raisonnement(liste_note,Comp_connexe[c][k],Comp_connexe[c][k],Fin[c][-1],[],Chemin)
                        if test_presence(Chemin,Fin[c][-1]) :
                            ElemL00.append(Comp_connexe[c][k])
                doublon(Chemin)
                Liste_Chemin0.append(Chemin)
                ElemL0.append(ElemL00)
        if Liste_Chemin0 == [[]] :
            C0[c] = [[Fin[c][-1]]]
            Liste_Chemin[c] = [[Fin[c][-1],Fin[c][-1]]]
        else :
            min_prof = [min([len(Liste_Chemin0[i][j]) for j in range(len(Liste_Chemin0[i]))])  for i in range(len(Liste_Chemin0))]
            C0[c] = [[] for i in range(len(ElemL0))]
            for i in range(len(Liste_Chemin0)):
                for j in range(len(Liste_Chemin0[i])):
                    if len(Liste_Chemin0[i][j])==min_prof[i]:
                        C0[c][i].append(ElemL0[i][j])
                        Liste_Chemin[c].append(Liste_Chemin0[i][j])
    return C0,Liste_Chemin,Fin


def pre_requis(liste_note,num,liste_prerequis):
    def trouve(liste_note,num):
        for k in range(len(liste_note)):
            if liste_note[k].num==num:
                return k
        raise ValueError(f"trouve pour num = {num} dans pre_requis")
    def ajoute(Liste,liste_a_ajouter):
        for elem in liste_a_ajouter:
            if elem not in Liste :
                Liste.append(elem)

    k0 = trouve(liste_note,num)
    ajoute(liste_prerequis,liste_note[k0].entre)
    for num_entre in liste_note[k0].entre :
        pre_requis(liste_note,num_entre,liste_prerequis)


def indentation(texte):
    indent = "    "
    nv_texte = indent + texte[0]
    for i in range(1,len(texte)):
        if texte[i-1]=="\n" :
            nv_texte += indent
        nv_texte += texte[i]
    return nv_texte

def generate_doc(liste_note,liste_relation,path_document_maitre,liste_transition,liste_determinant,Choix_note,environnement):
    print("--------------- Création du document maitre --------------")
    def trouve_rel(num,num_implique,liste_relation):
        for k in range(len(liste_relation)):
            if num in liste_relation[k].extremite and num_implique in liste_relation[k].extremite :
                return k
        raise ValueError(f"trouve_rel pour num = {num} et num_implique = {num_implique} dans generate_doc")

    def presence_rel(num,num_implique,liste_relation):
        for k in range(len(liste_relation)):
            if num in liste_relation[k].extremite and num_implique in liste_relation[k].extremite :
                return True
        return False

    def Latex(dernier,Chemin,Num_utilise,liste_note,liste_relation,liste_transition,liste_determinant,Choix_note,environnement):
        latex=""
        def retire_dollar(texte):
            nouv_texte = ""
            for i in range(len(texte)) :
                if texte[i] != "$":
                    nouv_texte += texte[i]
            return nouv_texte

        def label_env(Note):
            return r"\label{"+Note.nature+f":{Note.num}"+r"}"

        def ref_env(Note):
            if Note.type != "équation":
                return r"\ref{"+Note.nature+f":{Note.num}"+r"}"
            return r"\eqref{"+Note.nature+f":{Note.num}"+r"}"

        def categorisation(liste_prerequis,Num_utilise,Num_utilise_prerequis,Num_pas_utilise_prerequis,existe_prec,num_prec):
            for num_prerequis in liste_prerequis :
                if ajoute(Num_utilise,num_prerequis) :
                    Num_pas_utilise_prerequis.append(num_prerequis)
                elif not existe_prec or num_prec != num_prerequis :
                    Num_utilise_prerequis.append(num_prerequis)

        def creer_env(Note):
            latex=""
            protege = False
            pres_note = True
            if Note.nature == "relation" :
                pres_note = False
                [n1,n2] = Note.extremite
                [k1,k2] = [trouve_note(liste_note,n1),trouve_note(liste_note,n2)]
                if liste_note[k1].type == "équation" and liste_note[k2].type == "équation":
                    protege = True
            for i in range(len(environnement)):
                if environnement[i][0]==Note.type :
                    if environnement[i][1] != "" and (pres_note or protege) :
                        env = environnement[i][1].split()
                        if (environnement[i][2] == "" and (Note.contenu == "" or Note.contenu == "\n")) or protege :
                            latex += env[0] + label_env(Note) + ("\n" + "\n".join(env[1:len(env)]) if len(env[1:len(env)]) != 0 else "")
                        else :
                            latex += env[0] + label_env(Note) + ("\n" + "\n".join(env[1:len(env)]) if len(env[1:len(env)]) != 0 else "") + "\n"

                    if Note.contenu.strip("\n") != "" and (pres_note or not protege) :
                        if Note.type == "équation" :
                            latex += indentation(retire_dollar(Note.contenu))
                        else :
                            latex += detect_note(Note.contenu,liste_note,liste_determinant,Choix_note)
                        if environnement[i][2] != "" :
                            latex += "\n"

                    if environnement[i][2] != "" and (pres_note or not protege) :
                        if not pres_note :
                            latex += determinant(liste_note[k1].type,liste_determinant,Choix_note).capitalize() + liste_note[k1].type + ref_env(liste_note[k1]) + environnement[i][2] + determinant(liste_note[k2].type,liste_determinant,Choix_note) + liste_note[k2].type + ref_env(liste_note[k2]) 
                            latex += r"\\"  + "\n"
                        else :
                            latex += environnement[i][2]
            return latex

        def ajoute(Num_utilise,num):
            if num not in Num_utilise :
                Num_utilise.append(num)
                return True
            return False

        def texte_justification(liste_relation,liste_note,liste_determinant,Choix_note,liste_transition,Liste_num_prerequis,num):
            latex = ""
            if presence_rel(Liste_num_prerequis[0],num,liste_relation) :
                k_rel0 = trouve_rel(Liste_num_prerequis[0],num,liste_relation)
            else :
                k_rel0 = -1
            if len(Liste_num_prerequis) >= 2 or (len(Liste_num_prerequis)==1 and ((k_rel0 == -1) or liste_relation[k_rel0].type != "Equivalence")) :
                latex += r"\noindent D'après " 
                for n in range(len(Liste_num_prerequis)) :
                    num_prerequis = Liste_num_prerequis[-n-1]
                    k1=trouve_note(liste_note,num_prerequis)
                    if n==len(Liste_num_prerequis)-1 and len(Liste_num_prerequis)>1 :
                        latex += " et "
                    elif n!=0 and len(Liste_num_prerequis)>1 :
                        latex += ", "
                    latex += determinant(liste_note[k1].type,liste_determinant,Choix_note) + liste_note[k1].type + " " + ref_env(liste_note[k1])
                    if n==len(Liste_num_prerequis)-1 :
                        latex += ", "+liste_transition[rd.randint(0,len(liste_transition)-1)]
            else :
                k1=trouve_note(liste_note,Num_utilise_prerequis[0])
                latex += r"\noindent L'équation "+ref_env(liste_note[k1])+" est équivalente à "
            k_num = trouve_note(liste_note,num)
            latex += determinant(liste_note[k_num].type,liste_determinant,Choix_note) + liste_note[k_num].type + ref_env(liste_note[k_num]) + ".\n"
            return latex
        
        k_prec=-1
        dernier_num=-1
        pres_preuve = False
        for m in range(len(Chemin)):
            num = Chemin[m]
            if ajoute(Num_utilise,num) : 
                k0=trouve_note(liste_note,num)
                if m>0 and dernier_num == -1 :
                    dernier_num = max(liste_note[k0].entre)+1
                if k_prec != -1 and [dernier_num] == liste_note[k0].entre :
                    k_rel = trouve_rel(num,liste_note[k_prec].num,liste_relation)
                    latex += creer_env(liste_relation[k_rel]) + "\n"
                liste_prerequis=[]
                pre_requis(liste_note,num,liste_prerequis)
                Num_utilise_prerequis = []
                Num_pas_utilise_prerequis = []
                categorisation(liste_prerequis,Num_utilise,Num_utilise_prerequis,Num_pas_utilise_prerequis,k_prec!=-1,liste_note[k_prec].num)
                num0 = num
                num1 = num
                utilise = []
                for n in range(len(Num_pas_utilise_prerequis)) :
                    if len(Num_pas_utilise_prerequis)-n-1 not in utilise:
                        utilise.append(len(Num_pas_utilise_prerequis)-n-1)
                        num_prerequis = Num_pas_utilise_prerequis[-n-1]
                        k1=trouve_note(liste_note,num_prerequis)
                        if presence_rel(num_prerequis,num0,liste_relation):
                            k_rel = trouve_rel(num_prerequis,num0,liste_relation)
                            Note = liste_note[k1]
                            if dernier_num not in Note.entre :
                                latex += texte_justification(liste_relation,liste_note,liste_determinant,Choix_note,liste_transition,Note.entre,num_prerequis)
                            if Note.type != "démonstration" and not pres_preuve and n!=len(Num_pas_utilise_prerequis)-1 :
                                latex += creer_env(Note) + "\n" + creer_env(liste_relation[k_rel]) 
                            elif not pres_preuve and n!=len(Num_pas_utilise_prerequis)-1 :
                                preuve = creer_env(Note) + "\n"
                                pres_preuve = True
                            else  :
                                if Note.type != "démonstration" and n!=len(Num_pas_utilise_prerequis)-1 :
                                    latex += creer_env(Note) + preuve
                                    preuve = ""
                                    pres_preuve = False
                                elif n == len(Num_pas_utilise_prerequis)-1 :
                                    latex += creer_env(Note) + "\n"
                                else :
                                    preuve += creer_env(Note) + "\n"
                            dernier_num = num_prerequis
                        else :
                            if dernier_num not in liste_note[k1].entre and liste_note[k1].entre != [] :
                                latex += texte_justification(liste_relation,liste_note,liste_determinant,Choix_note,liste_transition,liste_note[k1].entre,liste_note[k1].num)
                            Note = liste_note[k1]
                            if Note.type != "démonstration" and not pres_preuve and n != len(Num_pas_utilise_prerequis)-1 :
                                latex += creer_env(Note) + "\n"
                            elif not pres_preuve and n == len(Num_pas_utilise_prerequis)-1 :
                                preuve = creer_env(Note) + "\n"
                                pres_preuve = True
                            elif n == len(Num_pas_utilise_prerequis)-1 :
                                latex += creer_env(Note) + "\n"
                            else :
                                if Note.type != "démonstration" :
                                    latex += creer_env(Note) + preuve
                                    preuve = ""
                                    pres_preuve = False
                                else :
                                    preuve += creer_env(Note)

                            dernier_num = liste_note[k1].num
                            for n in range(len(Num_pas_utilise_prerequis)):
                                num1 = Num_pas_utilise_prerequis[n]
                                pres = presence_rel(num_prerequis,num1,liste_relation)
                                if pres and n not in utilise:
                                    k_rel = trouve_rel(num_prerequis,num1,liste_relation)
                                    k2 = trouve_note(liste_note,num1)
                                    if dernier_num not in liste_note[k2].entre :
                                        latex += texte_justification(liste_relation,liste_note,liste_determinant,Choix_note,liste_transition,liste_note[k2].entre,num1)
                                    latex += creer_env(liste_relation[k_rel]) + "\n" + creer_env(liste_note[k2])
                                    dernier_num = num1
                                    utilise.append(n)

                                    
                if len(liste_note[k0].entre) > 1 or (dernier_num not in liste_note[k0].entre and liste_note[k0].entre != []):
                    latex += texte_justification(liste_relation,liste_note,liste_determinant,Choix_note,liste_transition,liste_note[k0].entre,num)

                Note = liste_note[k0]
                if m==len(Chemin)-1 and dernier :
                    if not pres_preuve :
                        latex += creer_env(Note) + "\n"
                    else :
                        latex += creer_env(Note) + preuve + "\n"
                        pres_preuve = False
                        preuve = ""
                else :
                    if Note.type != "démonstration" and not pres_preuve :
                        latex += creer_env(Note) + "\n"
                    elif not pres_preuve :
                        preuve = creer_env(Note) + "\n"
                        pres_preuve = True
                    else :
                        if Note.type != "démonstration" :
                            latex += creer_env(Note) + preuve
                            preuve = ""
                            pres_preuve = False
                        else :
                            preuve += creer_env(Note)
                k_prec = k0
                dernier_num = liste_note[k0].num
        return latex
        
    debut,Liste_chemin,fin = max_depth(liste_note)
    latex=""
    Num_utilise=[]

    for C in Liste_chemin:
        if latex != "" :
            latex += r"\newpage" + "\n"
        latex+=r"\part{}" + "\n"
        for n in range(len(C)) :
            Chemin = C[n]
            print("--> Ecriture du chemin : ",[trouve_note(liste_note,Chemin[n]) for n in range(len(Chemin))])
            if n==len(C)-1:
                dernier = True
            else :
                dernier = False
            latex+=Latex(dernier,Chemin,Num_utilise,liste_note,liste_relation,liste_transition,liste_determinant,Choix_note,environnement)
            latex += "\n"

    compile_maitre(path_document_maitre, "document_maitre", latex)
    print("---> Document maitre créé !")

def generate_doc_chrono(liste_note,path_Note_chrono):
    print("----------- Création du document chronologique -----------")
    print("---> Ecriture du texte...")
    latex = ""
    k=0
    for note in liste_note :
        latex += r"\noindent\textbf{" + f" Note {k}" + r"}" + "\n"
        latex += r"\begin{enumerate}[label=$-$]" + "\n"
        latex += r"\item" + " Type : " + note.type + "\n"
        latex += r"\item" + " Contenu complet ? " + ("Oui" if note.complet==1 else "Non") + "\n"
        latex += r"\item" + " Contenu :" + r"\\" + "\n" + r"\hspace*{.5cm}\begin{minipage}{20cm}" + "\n" + indentation(detect_note_glob_loc(note.contenu,liste_note)) + "\n" + r"\end{minipage}" + "\n"
        latex += r"\item" + " Note(s) qui l'implique : " 
        latex += ", ".join(map(str,[trouve_note(liste_note,num) for num in note.entre])) if note.entre!=[] else "-"
        latex += "\n" + r"\item" + " Note(s) qu'elle implique : " 
        latex += ", ".join(map(str,[trouve_note(liste_note,num) for num in note.sortie])) if note.sortie!=[] else "-"
        latex += "\n" + r"\end{enumerate}" + "\n"
        latex += r"\vspace{.2cm}"
        latex += "\n" + r"\hrule" + "\n\n"

        k += 1
    print("---> Création du document...")
    compile_maitre(path_Note_chrono, "document_chronologique", latex)
    print("---> Document chronologique créé !")

def read_env(path_Note,Choix_note,liste_determinant,Choix_rel,environnement):
    with open(path_Note+"environnement","r") as file :
        ligne = file.readline()
        while ligne != "" :
            num_ligne = 0
            type = ""
            determinant = ""
            nature = ""
            debut = ""
            fin = ""
            while ligne=="\n" :
                ligne = file.readline()
            while num_ligne <= 4:
                if num_ligne == 0 :
                    if type!="":
                        type += "_"
                    type += (ligne.rstrip('\n')).replace("*","")
                if num_ligne == 1 :
                    determinant = (ligne.rstrip('\n')).replace("*","")
                if num_ligne == 2 :
                    nature = (ligne.rstrip('\n')).replace("*","")
                if num_ligne == 3 :
                    if debut == "" :
                        debut = (ligne.rstrip('\n')).replace("*","")
                    else : 
                        debut += "\n" + (ligne.rstrip('\n')).replace("*","")
                if num_ligne == 4 :
                    if fin == "" :
                        fin = (ligne.rstrip('\n')).replace("*","")
                    else : 
                        fin += "\n" + (ligne.rstrip('\n')).replace("*","")

                if (ligne.rstrip('\n'))[-1]=="*":
                    num_ligne += 1  
                    
                ligne = file.readline() 

            if nature == "note":
                Choix_note.append(type)
            else : 
                Choix_rel.append(type)
            liste_determinant.append(determinant)
            environnement.append([type, debut, fin]) 


def MENU(path_pdf_Note,path_pdf_Lien,path_Note,path_tmp,filename_note,filename_relation,liste_note,liste_relation,Choix_note,Choix_rel,Protege,editeur_latex):
    def trouve_rel(liste_relation,num1,num2):
        for k in range(len(liste_relation)):
            if [num1,num2] == liste_relation[k].extremite :
                return True
        return False
    ancien_choix = True
    while True :
        Choix_menu = ["Ajouter une Note.","Ajouter une relation.","Editer/Supprimer une Note.","Editer/Supprimer une relation.","Générer le document maitre.","Afficher les notes avec contenu incomplet."]
        if len(liste_note) == 0 :
            Choix_menu = ["Ajouter une Note."]
        elif len(liste_note) == 1 :
            Choix_menu = ["Ajouter une Note.","Editer/Supprimer une Note.","Générer le document de maitre."]
        elif len(liste_relation) == 0 :
            Choix_menu = ["Ajouter une Note.","Ajouter une relation.","Editer/Supprimer une Note.","Générer le document de maitre.","Afficher les notes avec contenu incomplet."]
        if len(liste_note)>=1 and ancien_choix :
            generate_doc_chrono(liste_note,path_document_chrono)
        ancien_choix = True

        print("\n------- MENU -------")
        nb_choix = len(Choix_menu)
        for i in range(len(Choix_menu)):
            print(f"{i+1}) {Choix_menu[i]}")
        continuer = 1
        while continuer==1 :
            continuer = 0
            num_choix = int(input("\nChoix : "))
            if num_choix < 1 or num_choix> nb_choix :
                continuer = 1
                print("--- Choix invalide ---")
        if Choix_menu[num_choix-1] == "Ajouter une Note." :
            creer_Note(path_pdf_Note,path_pdf_Lien,path_Note,path_tmp,filename_note,liste_note,liste_relation,Choix_note,Choix_rel,Protege,filename_relation)
        if Choix_menu[num_choix-1] == "Ajouter une relation.":
            print("Note_1 --> Note_2")
            k1 = int(input("numéro Note_1 : "))
            k2 = int(input("numéro Note_2 : "))
            Note1 = liste_note[k1]
            Note2 = liste_note[k2]
            if trouve_rel(liste_relation,Note1.num,Note2.num) :
                print(f"---> Il existe déjà une relation Note {k1} --> Note {k2}")
            else :
                liste_relation.append(creer_relation_pour_note(Note1.num,Note2.num,Note1.type,liste_note,path_pdf_Lien,path_tmp,path_Note,filename_relation,Choix_rel))
                Note1.sortie += [Note2.num]
                Note2.entre += [Note1.num]  
                mise_a_jour(liste_note,path_Note,filename_note)
        if Choix_menu[num_choix-1] == "Editer/Supprimer une Note." :
            k = int(input("Choisissez le numéro d'une note : "))
            Note = liste_note[k]
            rep = input("Voulez-vous éditer (e) ou supprimer (s) une note ? ")
            if rep == "s":
                if input("Etes vous sûr de vouloir supprimer cette note ? ")=="o":
                    Note.sup(path_pdf_Note,path_pdf_Lien,path_Note,filename_note,filename_relation,liste_note,liste_relation)
                    mise_a_jour(liste_note,path_Note,filename_note)
                    mise_a_jour_rel(liste_relation,path_Note,filename_relation)
            else :
                edit_contenu_note(liste_note,Note.num,path_tmp,path_Note,filename_note,editeur_latex)
        if Choix_menu[num_choix-1] == "Editer/Supprimer une relation." :
            print("Choisir une relation Note_1 --> Note_2")
            k1 = int(input("Numéro de Note_1 : "))
            k2 = int(input("Numéro de Note_2 : "))
            Note1 = liste_note[k1]
            Note2 = liste_note[k2]
            matching_relation = []
            i = 0
            for rel in liste_relation :
                if [Note1.num,Note2.num] == rel.extremite :
                    matching_relation.append(rel)
                    print(f"- relation {i} de type {rel.type}")
                i += 1
            if len(matching_relation) == 0 :
                print("\n---> Aucune relation détectée...")
            else :
                rel = matching_relation[0]
                if len(matching_relation)>1 :
                    continuer=True
                    while continuer:
                        k = int(input("Choix de la relation : "))
                        if k<0 or k>=len(matching_relation):
                            print("--- Choix invalide ---")
                        else :
                            continuer = False
                    rel = matching_relation[k]
                rep = input("Voulez-vous éditer (e) ou supprimer (s) cette relation ? ")
                if rep == "s":
                    if input("Etes vous sûr de vouloir supprimer cette relation ? ")=="o":
                        rel.sup(path_pdf_Lien,filename_relation,liste_relation,liste_note)
                        mise_a_jour_rel(liste_relation,path_Note,filename_relation)
                        mise_a_jour(liste_note,path_Note,filename_note)
                else :
                    edit_relation(rel,Note1,Note2,Choix_rel,liste_relation,path_tmp,path_Note,filename_relation,editeur_latex)
        if Choix_menu[num_choix-1] == "Générer le document maitre." :
            generate_doc(liste_note,liste_relation,path_document_maitre,liste_transition,liste_determinant,Choix_note,environnement)
            ancien_choix = False
        if Choix_menu[num_choix-1] == "Afficher les notes avec contenu incomplet." :
            presence = False
            print("\nNote(s) incomplète(s) :")
            for k in range(len(liste_note)):
                if liste_note[k].complet == 0 :
                    presence = True
                    print(f"- Note {k}")
            if not presence :
                print("-->Toutes les notes sont complètes")
            ancien_choix = False



'''********************************************************************************************************
                                            Zone de TEST
********************************************************************************************************'''

filename_note = "notes"
filename_relation = "relations"
path_pdf_Note = "Notes/pdfNote/"
path_pdf_Lien = "Notes/pdfLien/"
path_Note = "Notes/"
path_tmp = "Notes/tmp/"
path_document_maitre = "Notes/doc_maitre/"
path_document_chrono = "Notes/doc_chronologique/"
editeur_latex = "texstudio"

Choix_note = []
liste_determinant = []
Choix_rel = []
environnement = []

read_env(path_Note,Choix_note,liste_determinant,Choix_rel,environnement)

Protege = ["théorème", "corolaire", "proposition"]
liste_transition = ["il suit ", "il vient "]

liste_note = []
liste_relation = []

print("-------------------- RECUPERATION des NOTES ---------------------------")
with open(path_Note+filename_note,"r") as file :
    ligne = file.readline()
    while ligne != "" and ligne !="\n" :
        liste_note.append(note(file))
        ligne = file.readline()
print("-------------------- RECUPERATION des RELATIONS ---------------------------")
with open(path_Note+filename_relation,"r") as file :
    ligne = file.readline()
    while ligne != "" and ligne !="\n" :
        liste_relation.append(relation(file))
        ligne = file.readline()

MENU(path_pdf_Note,path_pdf_Lien,path_Note,path_tmp,filename_note,filename_relation,liste_note,liste_relation,Choix_note,Choix_rel,Protege,editeur_latex)