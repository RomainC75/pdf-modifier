## specifications

*** pdf de la même entreprise


** default date : last day of the current month

** nom des fichiers après traitement :
ARE-nom-prenom-dateDuDebutDeContrat.pdf


*** organisation des fichiers
D :Société_AER_Mois_Annee
    
    --> D: 00_AER_combine
        F: NomDeLaSociété_AER_ MoisAnnee.pdf
    
    --> D: nom_prénom
        F: NomDeLaSociété_AER_Nom_Prénom_ dateDuDebutDeContrat.pdf 


*** insertions en PDF
page1: secu + nom + prénom 

*** if (SECU cannot be extracted)
 => not pdf 
 => report at the end




Report must contain :
 number of entries
 number of extracted files with no errors
 number of errors
 list of unextracted file names
 => creation of a folder with no extracted pdfs (copy)
 

## date_choice.txt 

```
today => t
manual => yyyy-mm-dd
last day of month => default
```


```
cd ..../project
docker build -t la-bellevilloise .

docker run -v "${PWD}/data":/app/data --name labellevilloise la-bellevilloise
```