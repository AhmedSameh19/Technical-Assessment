from __future__ import annotations

from typing import  List

from sqlalchemy import Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import MachineStatus

from app.models.work_order import WorkOrder
from app.models.maintenance_ticket import MaintenanceTicket
from app.models.downtime_log import DowntimeLog


class Machine(Base):
    __tablename__ = "machine"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[MachineStatus] = mapped_column(
        Enum(MachineStatus, name="machine_status"),
        nullable=False,
        default=MachineStatus.Active,
    )

 

 