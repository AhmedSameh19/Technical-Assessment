from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session


from app.models import (
    DowntimeLog,
    Machine,
    MachineStatus,
    MaintenanceTicket,
    WorkOrder,
    WorkOrderStatus,
)

from app.schemas.machines import MachineStatusUpdate


# This is the endpoint which firstly check if this machine is a vaild machine
# then it will check if thre is a maintenance ticket is open for this machine
# then it will update the status of the machine to active 

#if the status is changed to broken it will pause all work orders in progress
# and create a downtime log entry with the provided reason and start time

# if the status is changed from broken to active it will close any open downtime log and updtate its endtime

#if any database operation fails it will rollback the transaction and return an error response

def update_machine_status_service(db: Session, machine_id: int, new_status: MachineStatus, reason: str | None = None) -> Machine:
    machine = db.get(Machine, machine_id)
    if not machine:
        raise ValueError("Machine not found")

    old_status = machine.status

    if new_status == MachineStatus.Active:
        guard_machine_activation(db, machine_id)

    machine.status = new_status

    if old_status != MachineStatus.Broken and new_status == MachineStatus.Broken:
        handle_broken_transition(db, machine_id, reason)

    if old_status == MachineStatus.Broken and new_status == MachineStatus.Active:
        close_open_downtime_log(db, machine_id)

    return machine
#it checks if there is any open maintenance ticket for the machine
# if there is it raises an http exception with status code 400
def guard_machine_activation(db: Session, machine_id: int):
    has_open_ticket = db.execute(
        select(MaintenanceTicket.id).where(
            MaintenanceTicket.machine_id == machine_id,
            MaintenanceTicket.is_open.is_(True),
        )
    ).first()

    if has_open_ticket:
        raise HTTPException(
            status_code=400,
            detail="Cannot set Machine to Active while an open Maintenance Ticket exists",
        )

#if the machine is broken it pauses all work orders in progress
# and creates a downtime log entry with the provided reason and start time
def handle_broken_transition(
    db: Session,
    machine_id: int,
    reason: str | None,
):
    now = datetime.utcnow()
    db.execute(
        update(WorkOrder)
        .where(
            WorkOrder.machine_id == machine_id,
            WorkOrder.status == WorkOrderStatus.InProgress,
        )
        .values(status=WorkOrderStatus.Paused)
    )

    db.add(
        DowntimeLog(
            machine_id=machine_id,
            reason=reason,
            start_time=now,
            end_time=None,
        )
    )

# it closes any open downtime log for the machine by setting its end time
def close_open_downtime_log(db: Session, machine_id: int):
    now = datetime.utcnow()
    open_log = db.execute(
        select(DowntimeLog)
        .where(
            DowntimeLog.machine_id == machine_id,
            DowntimeLog.end_time.is_(None),
        )
    ).scalars().first()

    if open_log:
        open_log.end_time = now

