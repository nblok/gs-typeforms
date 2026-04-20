import typing as t

from typeforms_domain.core.entity.form import Form
from typeforms_domain.core.valueobject.form_id import FormId


class FormRepository(t.Protocol):
    async def get(self, form_id: FormId) -> t.Optional[Form]: ...

    async def find_all(self) -> list[Form]: ...

    async def save(self, form: t.Any) -> FormId: ...
