"""Dal (dropshipping modeli) ve dala bağlı form araçlarının tanımları."""

from collections.abc import Callable
from dataclasses import dataclass, field

from .roadmap import Stage
from .scoring import Criterion


@dataclass(frozen=True)
class Field:
    name: str
    question: str
    default: float | None = None  # boş geçilirse ("-") kullanılacak değer; None = zorunlu
    kind: str = "num"  # num: >= 0, positive: > 0, pct: 0-100 arası (100 hariç)


@dataclass(frozen=True)
class FormTool:
    """Kullanıcıya sırayla sayı soran ve sonunda rapor üreten araç (kâr hesabı, reklam testi vb.)."""

    id: str
    button: str  # menüdeki buton etiketi
    title: str
    fields: tuple[Field, ...]
    report: Callable[[dict[str, float]], str]  # alan değerleri -> HTML rapor


@dataclass(frozen=True)
class Branch:
    id: str
    title: str
    summary: str  # dalın ana sayfasında gösterilen HTML açıklama
    ready: bool
    stages: tuple[Stage, ...] = ()
    criteria: tuple[Criterion, ...] = ()
    tools: tuple[FormTool, ...] = field(default_factory=tuple)

    def tool(self, tool_id: str) -> FormTool:
        for t in self.tools:
            if t.id == tool_id:
                return t
        raise KeyError(tool_id)
