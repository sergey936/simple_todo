from fastapi import APIRouter


router = APIRouter(tags=['user'])


@router.get('/register')
async def register():
    return {'response': 'working'}
