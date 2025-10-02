from fastapi import APIRouter

from src.router import user, plan, day_schedule, schedule_slot

router = APIRouter("/api/v1")

router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(plan.router, prefix="/plans", tags=["Plans"])
router.include_router(day_schedule.router, prefix="/day-schedules", tags=["Day Schedules"])
router.include_router(schedule_slot.router, prefix="/schedule-slots", tags=["Schedule Slots"])
