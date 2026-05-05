# Prosjektbeskrivelse – IT-utviklingsprosjekt (2IMI)
## Neglesalong

### Deltakere
- Helen  
- Mila  

---

## 1. Prosjektbeskrivelse

### Hva er prosjektet?
Prosjektet er en nettside/nettbutikk der kunder kan bestille negletime direkte hos salongen.  
Nettsiden skal samle timebestilling på ett sted og gjøre prosessen enkel og oversiktlig.

### Hvilket problem løser det?
I dag må mange kunder bestille time ved å sende DM på Instagram.  
Dette kan føre til lang ventetid, misforståelser og tapte henvendelser, både for kunden og negleteknikeren.

### Hvorfor er løsningen nyttig?
Løsningen gjør timebestilling raskere, mer effektiv og mer oversiktlig.  
Kundene kan bestille time når det passer dem, og negleteknikeren får bedre kontroll over timeplanen sin.

### Målgruppe
Målgruppen er personer som liker negler, som regelmessig tar manikyr eller andre neglbehandlinger.

### Hvem er løsningen laget for?
Løsningen er laget for både kunder og negleteknikere, siden den forenkler kommunikasjon, sparer tid og gir en bedre opplevelse for begge parter.


## 2. Funksjonelle krav
Systemet skal minst ha følgende funksjoner:

1. Vise tilgjengelige timer
2. Bestille negletime
3. Lagre kundeinformasjon
4. Administrere timeplan for negletekniker


## 3. Teknologivalg
Programmeringsspråk:
Python / JavaScript / C# / Flask 

Database:
MariaDB

Verktøy:
GitHub,
GitHub Projects (Kanban)

## 4. Datamodell
### Oversikt over tabeller

**Tabell 1**
- Navn: User  
- Beskrivelse: Lagrer informasjon om kunder og negleteknikere

**Tabell 2**
- Navn: Appointment  
- Beskrivelse: Lagrer informasjon om bookede timer

**Tabell 3**
- Navn: Service  
- Beskrivelse: Lagrer informasjon om ulike neglbehandlinger

---

### Eksempel på tabellstruktur

```sql
CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE Appointment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    date DATE,
    time TIME,
    FOREIGN KEY (user_id) REFERENCES User(id)
);
