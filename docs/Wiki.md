# Návrh riešenia

## Sťahovač (crawler)
Z centrálneho registra zmluv pomocou sťahovača (crawlera) stiahnem údaje o zmluvách. 
Prehľadávanie prebieha do šírky (FIFO), rešpektujúc podmienky CRZ.
Sťahovač si ukladá hashe navštívených URL aby zabránil duplikátnemu navštíveniu tej istej URL. Hashe sú perzistentne ukladané a načíané aj medzi jednotlivými behmi.
S využitím regulárnych výrazov sú extrahované atribúty zmluvy. Parsovanie zmluv je pokryté automatizovanými testami pre zaistenie čo najpresnejšej extrakcie atribútov.
Záznamy sú zapísané na disk vo forme csv súboru.
Na sťahovanie bol použitý framework `scrapy`.

### Pseudokód
```

```

##  Indexovanie
Zo záznamov je vytvorená neorientovaná grafová štruktúra. Uzol reprezentuje fyzickú/právnicku osobu a hrana reprezentuje uzatvorenie zmluvy. Hrana obsahuje aj atribúty uzatvorenej zmluvy.

## Vyhľadávanie
Pomocou prehľadávania do šírky je prehľadaný graf. Ak existuje cesta medzi dvoma zadanými entitami, vyhľadávač vráti túto cestu.
Na vyhľadanie a indexovanie použijem vstavané moduly jazyka Python 3.10.

## Ukážka datasetu
