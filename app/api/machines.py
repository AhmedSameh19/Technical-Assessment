from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db


from app.schemas.machines import MachineStatusUpdate
from app.services.machines import update_machine_status_service


router = APIRouter(prefix="/machines", tags=["machines"])


# endpoint path is http://localhost:8000/machines/{machine_id}/status
# body payload is {
#     "status": "Active" | "Broken" | "Maintenance" ,
#     "reason": "string"  # required if status is Broken
# }

# returns the updated machine details
#{  machine_id: int,
#   machine_name: str,
#   updated_status: "Active" | "Broken" | "Maintenance"
#}
@router.patch("/{machine_id}/status")
def update_machine_status(
    machine_id: int,
    payload: MachineStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        with db.begin():
            if payload.status == "Broken" and not payload.reason:
                raise HTTPException(400, "Reason is required when setting status to Broken")
            machine = update_machine_status_service(db, machine_id, payload.status, payload.reason)
        db.refresh(machine)
        return {"id": machine.id, "name": machine.name, "status": machine.status}
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(500, "Failed to update machine status safely")

