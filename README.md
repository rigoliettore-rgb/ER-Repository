# Sincronizzazione degli orologi di Tempora

Applicazione da console in Python che confronta l'ora di quattro orologi con
quella della Torre dell'Orologio, impostata alle **15:00**. Per ciascun
orologio mostra lo scarto in minuti e un quadrante ASCII.

## Requisiti

- Python 3.10 o successivo
- Nessuna dipendenza esterna

## Struttura del progetto

```text
tempora_clock_sync/
├── main.py       # Applicazione, calcoli e disegno dei quadranti
├── test_main.py  # Test automatici con unittest
└── README.md     # Documentazione
```

## Avvio

Apri il terminale nella cartella del progetto ed esegui:

```text
python main.py
```

Il programma chiede l'orario di ciascuno dei quattro orologi. Inserisci un
orario alla volta nel formato 24 ore `HH:MM`, per esempio `14:30`. Se il
formato o l'orario non sono validi, viene mostrato un messaggio e puoi
inserirlo nuovamente.

Il programma visualizza quindi l'orario della torre e quello di ogni
orologio, il relativo scarto e il suo quadrante. Nel quadrante `H` indica la
lancetta delle ore, `M` quella dei minuti e `+` il centro. Alla fine indica
quanti orologi devono essere regolati, cioè quanti non segnano la stessa ora
della torre. Segnala come urgenti gli orologi il cui scarto assoluto supera
la soglia fissa di **120 minuti**. Uno scarto esattamente pari a 120 minuti
non supera la soglia e quindi non viene segnalato come urgente. Per ogni
orologio urgente indica di quanti minuti e in quale direzione regolarlo per
sincronizzarlo con la torre. Un riepilogo finale elenca tutti gli orologi con
lo scarto, la correzione suggerita e la classificazione:

- **High priority**: scarto assoluto maggiore di 120 minuti.
- **In line**: nessuno scarto; l'orologio è sincronizzato.
- **Low priority**: scarto diverso da zero, ma non superiore a 120 minuti.

## Come viene calcolato lo scarto

Gli orari vengono convertiti in minuti trascorsi dalla mezzanotte. Lo scarto è:

```text
minuti dell'orologio - minuti della Torre dell'Orologio
```

Per esempio, per un orologio che segna `14:30` rispetto alla torre alle
`15:00`:

```text
14 × 60 + 30 = 870
15 × 60      = 900
870 - 900    = -30 minuti
```

Un valore positivo indica che l'orologio è avanti; un valore negativo indica
che è indietro; zero significa che è sincronizzato. Con `14:30`, `15:05`,
`15:00` e `14:40` gli scarti sono rispettivamente `-30`, `+5`, `0` e `-20`
minuti.

## Controllo degli orari ed errori

Sono accettati solo orari da `00:00` a `23:59`, sempre con due cifre per ore e
minuti. Per esempio, `03:05` è valido, mentre `3:05`, `24:00` e `12:70` non
lo sono. Gli inserimenti non validi vengono rifiutati e richiesti di nuovo.
Se l'input termina prima di aver inserito tutti e quattro gli orari, il
programma mostra un errore e termina con un codice di uscita diverso da zero.

## Test automatici

Per eseguire i test dalla cartella del progetto:

```text
python -m unittest -v
```

I test verificano la conversione e la validazione degli orari, il calcolo
separato dello scarto per ciascun orologio, la formattazione dei risultati,
il disegno del quadrante e la gestione dell'input non valido.
