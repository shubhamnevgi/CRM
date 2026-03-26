from fastapi import APIRouter

router = APIRouter(tags=['Placeholders'])


def register_placeholder(prefix: str):
    sub = APIRouter(prefix=prefix, tags=[prefix.strip('/').title()])

    @sub.get('')
    def not_implemented_yet():
        return {'message': f'{prefix} endpoints scaffolded. Implementation in next phase.'}

    return sub
