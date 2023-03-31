from fastapi import APIRouter, Depends
from redis import Redis

from quark.database import get_redis
from quark.schemas import UserResponse
from quark.utils import get_current_user

router = APIRouter(prefix="/users")


@router.get("/@me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.get("/one/{param}")
async def one(param, redis: Redis = Depends(get_redis)):
    await redis.publish("ch1", param)
    return "ok"
