from qualite import analyser_ligne, analyser_lot, histogramme, verdict


def test_juste_sous_limite_basse():
    assert verdict(24.95) == "conforme"
    assert verdict(24.949) == "rebut"


def test_code_entoure_d_espaces():
    assert analyser_ligne("  AXE-0042  ; 25,03 mm") == ("AXE-0042", 25.03, "conforme")


def test_lot_entierement_invalide():
    resultats, erreurs = analyser_lot(["ERREUR", "AXE-1;25", "AXE-0001;abc"])
    assert resultats == []
    assert len(erreurs) == 3


def test_histogramme_sans_mesure():
    texte = histogramme([], debut=24.92, pas=0.02, nb_classes=3)
    assert len(texte.splitlines()) == 3
    assert "*" not in texte