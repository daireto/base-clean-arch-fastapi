from dataclasses import dataclass

from pydantic_core import ErrorDetails


@dataclass
class ValidationErrorDetail:
    detail: str
    pointer: str

    @classmethod
    def from_pydantic_error_details(
        cls, errors: list[ErrorDetails]
    ) -> list['ValidationErrorDetail']:
        members = []

        for err in errors:
            pointer = cls.pydantic_loc_to_json_pointer(err['loc'])
            members.append(ValidationErrorDetail(detail=err['msg'], pointer=pointer))

        return members

    @classmethod
    def pydantic_loc_to_json_pointer(cls, loc: tuple[int | str, ...]) -> str:
        return f'#/{"/".join(str(step) for step in loc)}'


@dataclass
class Error(Exception):
    status: int
    title: str
    detail: str
    code: str
    type: str = 'about:blank'
    errors: list[ValidationErrorDetail] | None = None
    extra: dict[str, object] | None = None

    def __post_init__(self) -> None:
        super().__init__(self.detail)

    def to_rfc_9457_dict(self, instance: str | None = None) -> dict[str, object]:
        return {
            'type': self.type,
            'title': self.title,
            'status': self.status,
            'detail': self.detail,
            'instance': instance,
            'code': self.code,
            'errors': self.errors,
        }
