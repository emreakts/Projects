"""Ürün puanlama motoru.

Kullanıcı her kriter için bir seçenek seçer, her seçeneğin 1-5 arası puanı vardır.
Kriter ağırlıklarına göre 0-100 arası skor ve karar üretilir.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Criterion:
    key: str
    question: str
    options: tuple[tuple[str, int], ...]  # (etiket, puan 1-5)
    weight: int
    tip: str  # puan düşükse verilecek tavsiye
    hard_flag: bool = False  # en düşük puan alırsa toplam skordan bağımsız "girme" kararı


@dataclass
class ScoreResult:
    score: int  # 0-100
    verdict: str
    red_flags: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)


def evaluate(criteria: Sequence[Criterion], answers: dict[str, int]) -> ScoreResult:
    """answers: kriter anahtarı -> seçilen puan (1-5). Tüm kriterler cevaplanmış olmalı."""
    missing = [c.key for c in criteria if c.key not in answers]
    if missing:
        raise ValueError(f"Eksik kriterler: {', '.join(missing)}")

    total_weight = sum(c.weight for c in criteria)
    weighted = sum(c.weight * (answers[c.key] - 1) / 4 for c in criteria)
    score = round(weighted / total_weight * 100)

    red_flags = [c.tip for c in criteria if c.hard_flag and answers[c.key] == 1]
    weaknesses = [c.tip for c in criteria if not c.hard_flag and answers[c.key] <= 2]

    if red_flags or score < 50:
        verdict = "❌ Girme. Bu ürün şu haliyle riskli."
    elif score < 70:
        verdict = "⚠️ Dikkatli test et. Düşük bütçeyle dene."
    else:
        verdict = "✅ Gir. Güçlü bir aday, teste al."

    return ScoreResult(score=score, verdict=verdict, red_flags=red_flags, weaknesses=weaknesses)
