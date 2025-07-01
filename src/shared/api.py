from fastapi import APIRouter

router = APIRouter()


@router.get('/health')
def read_root() -> dict[str, str]:
    return {'detail': 'ok'}
