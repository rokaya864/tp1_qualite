"""Contrôle qualité d'une ligne d'usinage : lecture des mesures, verdicts, statistiques, rapport."""
import math

NOMINAL = 25.0     # diamètre nominal des axes, en mm
TOLERANCE = 0.05   # tolérance admise : 25,00 ± 0,05 mm


# --- Étape 1 : lire les données -----------------------------------------------------------------
import math

# --- Étape 1 : nettoyage et validation des entrées ------------------------------------------------
def lire_mesure(texte: str) -> float:
    """Enlève les espaces, passe en minuscules, retire le suffixe 'mm',
    remplace la virgule par un point, puis convertit en float.
    Lève ValueError pour toute valeur invalide, nulle/négative, nan ou inf.
    """
    texte_nettoye = texte.strip().lower()
    texte_nettoye = texte_nettoye.removesuffix("mm").strip()
    texte_nettoye = texte_nettoye.replace(",", ".")

    try:
        valeur = float(texte_nettoye)
    except ValueError:
        raise ValueError(f"mesure invalide : {texte.strip()!r}")

    if not math.isfinite(valeur) or valeur <= 0:
        raise ValueError(f"mesure invalide : {texte.strip()!r}")

    return valeur


def valider_code(code: str) -> bool:
    """Vérifie le format d'un code pièce (ex. 'AXE-0001').

    Exactement 8 caractères : 3 lettres majuscules ASCII, un tiret, 4 chiffres.
    """
    if len(code) != 8:
        return False

    prefixe = code[:3]
    separateur = code[3]
    chiffres = code[4:]

    return (
        prefixe.isalpha()
        and prefixe.isupper()
        and prefixe.isascii()
        and separateur == "-"
        and chiffres.isdigit()
    )
# --- Étape 2 : décider ----------------------------------------------------------------------------
def ecart(mesure: float, nominal: float = NOMINAL) -> float:
    """Écart à la cote nominale, arrondi à 3 décimales."""
    return round(mesure - nominal, 3)


def verdict(mesure: float, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> str:
    """Renvoie "conforme", "à reprendre" ou "rebut"."""
    if tolerance <= 0:
        raise ValueError("La tolérance doit être strictement positive.")

    e = ecart(mesure, nominal)
    if abs(e) <= tolerance:
        return "conforme"
    elif e > 0:
        return "à reprendre"
    else:
        return "rebut"

# --- Étape 3 : analyser une ligne -----------------------------------------------------------------
def analyser_ligne(ligne: str, *, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> tuple[str, float, str]:
    champs = ligne.split(";")
    if len(champs) != 2:
        raise ValueError(f"2 champs attendus, {len(champs)} trouvé(s)")

    code = champs[0].strip().upper()
    if not valider_code(code):
        raise ValueError(f"code invalide : {code!r}")

    mesure = lire_mesure(champs[1])
    v = verdict(mesure, nominal=nominal, tolerance=tolerance)

    return (code, mesure, v)
# --- Étape 4 : analyser un lot --------------------------------------------------------------------
def analyser_lot(lignes: list[str], **reglages) -> tuple[list[tuple[str, float, str]], list[str]]:
    resultats = []
    erreurs = []

    for numero, ligne in enumerate(lignes, start=1):
        ligne_epuree = ligne.strip()
        if not ligne_epuree or ligne_epuree.startswith("#"):
            continue

        try:
            res = analyser_ligne(ligne, **reglages)
            resultats.append(res)
        except ValueError as err:
            erreurs.append(f"ligne {numero} : {err}")

    return resultats, erreurs


def compter_verdicts(resultats: list[tuple[str, float, str]]) -> tuple[int, int, int]:
    conformes = 0
    a_reprendre = 0
    rebuts = 0

    for _, _, v in resultats:
        if v == "conforme":
            conformes += 1
        elif v == "à reprendre":
            a_reprendre += 1
        elif v == "rebut":
            rebuts += 1

    return conformes, a_reprendre, rebuts

# --- Étape 5 : statistiques et capabilité ---------------------------------------------------------
def moyenne(*valeurs: float) -> float:
    """Moyenne d'un nombre quelconque de valeurs. Lève ValueError s'il n'y en a aucune."""
    raise NotImplementedError("à compléter")


def ecart_type(*valeurs: float) -> float:
    """Écart type d'échantillon (division par n - 1). Lève ValueError avec moins de deux valeurs."""
    raise NotImplementedError("à compléter")


def capabilite(mesures: list[float], *, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> tuple[float, float]:
    """Indices de capabilité (Cp, Cpk), arrondis à 2 décimales.

    Cp  = largeur de la tolérance / (6 sigma)                  : le procédé est-il assez précis ?
    Cpk = distance de la moyenne à la limite la plus proche / (3 sigma) : est-il bien centré ?
    """
    raise NotImplementedError("à compléter")


# --- Étape 6 : le rapport -------------------------------------------------------------------------
def rapport(lignes: list[str], *, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> str:
    """Construit le rapport de contrôle d'un lot, sous forme d'une seule chaîne (une ligne par pièce)."""
    raise NotImplementedError("à compléter")


# --- Étape 8 (à la maison) : histogramme ----------------------------------------------------------
def histogramme(mesures: list[float], *, debut: float, pas: float, nb_classes: int) -> str:
    """Histogramme texte : une ligne par classe [borne, borne + pas[, une étoile par mesure.

    Les mesures hors de [debut, debut + nb_classes * pas[ sont ignorées.
    """
    raise NotImplementedError("à compléter")
