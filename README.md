# python-saol

Python-paketering av den senaste SAOL-utgåvan som är fritt tillgänglig, SAOL 14 från 2015[^1].

SAOL 14 är licensierad under Creative Commons Attribution 4.0 International (CC-BY-4.0).

Mer information om SAOL som datakälla: https://spraakbanken.gu.se/resurser/historiska-saol

Jag som gjort det här pythonpaketet har ingen koppling till SAOL, Språkbanken eller Göteborgs universitet.

## Användning

Ordlistan exponeras som en enkel lista med ord, ordklass och böjningar. Ett exempel på användning:

```python
from saol import all_upos_by_word, saol14

print(f"Ordlistan innehåller {len(saol14)} ord.")
print("Första ordet i listan:")
print(saol14[0])
print()

part_of_speech_by_word = all_upos_by_word(saol14)

for word in "en putslustig talgoxe äter sin finfördelade goja".split():
    upos = part_of_speech_by_word.get(word, None)
    if upos:
        print(
            f'"{word}" finns i ordlistan och är märkt med ordklass(er)'
            f' {", ".join(upos)}.'
        )
    else:
        print(f'"{word}" finns inte i ordlistan.')
```

Exemplet ger följande utskrift:

```
Ordlistan innehåller 126900 ord.
Första ordet i listan:
SaolEntry(word='a', upos='NOUN', conj='a:et; pl. a:n el. a, best. pl. a:na')

"en" finns i ordlistan och är märkt med ordklass(er) PRON, X, NOUN.
"putslustig" finns i ordlistan och är märkt med ordklass(er) ADJ.
"talgoxe" finns i ordlistan och är märkt med ordklass(er) NOUN.
"äter" finns inte i ordlistan.
"sin" finns i ordlistan och är märkt med ordklass(er) PRON, X, NOUN.
"finfördelade" finns inte i ordlistan.
"goja" finns i ordlistan och är märkt med ordklass(er) NOUN.
```

Notera att endast ord i grundform förekommer i listan: `finfördela` finns med, men inte `finfördelad`.
Likaså `äta` men inte `äter`.

Det finns också ett antal "ord" (2432 stycken) som består av flera ord, till exempel `haka på`, `fylla i` samt `ruska av sig`.

## Framtida arbete

- Tillgänggliggör böjningar av ord. Här bör man kunna använda `conj`-fältet (motsvarande `conj` i faksimilfilen)
  för att härleda hur andra former ser ut.

## Om indataformatet

Här följer lite anteckningar kring indatan i faksimilfilen, som laddas ner från Språkbanken då paketet byggs.

- Ordklasser i `upos`-fältet är taggade enligt [Universal Dependencies](https://universaldependencies.org/).
- Ordklasser i `ordkl`-fältet är taggade på svenska, och ibland även med böjningssuffix i en `<i></i>`-tagg.
- `normaliserat_ord` är normalt det ord man vill använda, då det är rensat från betoningsmarkeringar och liknande.
- `text`-fältet verkar innehålla  samma sak som böjningssuffixen i `ordkl`-fältet.

[^1]: Svenska Akademien (2025). SAOL 14 (2015) - faksimil (uppdaterad: 2025-12-11). [Data set]. Språkbanken Text. https://doi.org/10.23695/fqh2-af42
