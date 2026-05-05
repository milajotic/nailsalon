# Prosjektbeskrivelse – IT-utviklingsprosjekt (2IMI)
## Neglesalong

### Deltakere
- Mila
- Helen

---

## 1. Prosjektbeskrivelse

### Hva er prosjektet?
Prosjektet er en nettside der kunder kan bestille negletime direkte hos salongen.
Nettsiden samler timebestilling på ett sted og gjør prosessen enkel for både kunde og negletekniker.

### Hvilket problem løser det?
Mange kunder bestiller i dag time via Instagram DM, noe som kan føre til misforståelser, lang ventetid og tapte henvendelser.
Et eget bookingsystem løser dette ved å gjøre kommunikasjonen mer strukturert.

### Hvorfor er løsningen nyttig?
Løsningen gjør timebestilling raskere og mer oversiktlig.
Kundene kan bestille når det passer dem, og negleteknikeren får bedre kontroll over sin egen timeplan.

### Målgruppe
Målgruppen er personer som jevnlig tar manikyr eller andre neglbehandlinger.

### Hvem er løsningen laget for?
Løsningen er laget for både kunder og negleteknikere – den forenkler bookingprosessen og sparer tid for begge parter.


## 2. Funksjonelle krav
Systemet skal minst ha følgende funksjoner:

1. Vise tilgjengelige tjenester
2. Bestille negletime
3. Lagre kundeinformasjon
4. Gi negleteknikeren en adminside for å administrere bestillinger


## 3. Teknologivalg
Programmeringsspråk:
Python, Flask

Database:
MariaDB

Verktøy:
GitHub,
GitHub Projects (Kanban)

## 4. Datamodell
### Oversikt over tabeller

**Tabell 1**
- Navn: users
- Beskrivelse: Lagrer informasjon om kunder og negleteknikere, inkludert rolle (admin/user)

**Tabell 2**
- Navn: appointment
- Beskrivelse: Lagrer informasjon om bookede timer, koblet til bruker og tjeneste

**Tabell 3**
- Navn: service
- Beskrivelse: Lagrer informasjon om tilgjengelige neglbehandlinger og priser

---

### Eksempel på tabellstruktur

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE service (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(6,2) NOT NULL
);

CREATE TABLE appointment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    service_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES service(id)
);
```