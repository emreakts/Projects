"""Türkçe sayı okuma/yazma yardımcıları."""

import re


def parse_number(text: str) -> float:
    """'1.250,50', '1250.5', '%12', '89 TL' gibi girdileri sayıya çevirir. Geçersizse ValueError."""
    s = text.strip().lower().replace("tl", "").replace("₺", "").replace("%", "").replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")  # 1.250 -> binlik ayraç
    value = float(s)
    if value < 0:
        raise ValueError("negatif değer")
    return value


def fmt_tl(value: float) -> str:
    s = f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{s} TL"


def fmt_pct(value: float) -> str:
    return f"%{value:.1f}".replace(".", ",")


def fmt_usd(value: float) -> str:
    s = f"{abs(value):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{'-' if value < 0 else ''}${s}"


def fmt_num(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")
