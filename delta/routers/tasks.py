from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from quark.database import get_db
from quark.models import Task as DbTask, Customer, Performer
from quark.schemas import UserResponse, TaskResponse
from quark.utils import get_current_user

router = APIRouter(prefix="/tasks")


@router.put("/create")
async def create_task(user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db), task: TaskResponse = None):
    # user type 2 - customer
    if user.type != 2:
        raise HTTPException(401, "Only customers maybe create task")

    if not task:
        raise HTTPException(400, "Body is empty")

    customer: Customer = db.query(Customer).filter(Customer.user_id == user.id).first()

    if not customer:
        raise HTTPException(404, "Customer not found")

    db_task = DbTask(
        number=0,
        workplace=task.workplace,
        customer_id=customer.user_id,
        description=task.description,
        files=";;".join(task.files) if task.files else None,
        state_id=1,
        org_id=customer.user.org_id
    )

    db.add(db_task)
    db.commit()

    return "Task created"


@router.put("/accept/{task_id}")
async def accept_task(user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db), task_id: int = None):
    # user type 1 - performer
    if user.type != 1:
        raise HTTPException(401, "Only performers maybe accept task")

    if not task_id:
        raise HTTPException(400, "Task ID is empty")

    task = db.query(DbTask).filter(DbTask.id == task_id)
    obj_task: DbTask = task.first()

    if not obj_task:
        raise HTTPException(404, "Task not found")

    if not obj_task.performer_id or obj_task.state_id != 1:
        raise HTTPException(400, "Task already accepted by other performer or state id not valid")

    performer: Performer = db.query(Performer).filter(Performer.user_id == user.id).first()

    if not performer:
        raise HTTPException(404, "Performer not found")

    task.update({"performer_id": performer.user_id, "state_id": 2})

    return "Task accepted"
