import asyncio
from datetime import datetime
from typing import Optional

from telethon import events
from telethon.tl import types

from .logger import ActivityLogger, format_dt

STABLE_STATUS_SECONDS = 60


class PresenceMonitor:
    def __init__(self, client, target_user_id: int, logger: ActivityLogger):
        self.client = client
        self.target_user_id = target_user_id
        self.logger = logger
        self._pending_task: Optional[asyncio.Task] = None
        self._pending_state: Optional[str] = None
        self._last_confirmed_state: Optional[str] = None
        self._last_unavailable_status: Optional[str] = None

    def register(self) -> None:
        @self.client.on(events.UserUpdate)
        async def handler(event):
            if event.user_id != self.target_user_id or event.status is None:
                return

            await self.handle_status(event.status)

    async def handle_status(self, status) -> None:
        state = self._status_state(status)

        if state is None:
            self._cancel_pending()
            label = self._status_label(status)
            if label != self._last_unavailable_status:
                self._last_unavailable_status = label
                self.logger.event(
                    "Presence",
                    f"Модуль недоступен: Telegram показывает '{label}', точное время в сети недоступно.",
                )
            return

        self._last_unavailable_status = None
        if state == self._pending_state:
            return

        self._cancel_pending()
        self._pending_state = state
        self._pending_task = asyncio.create_task(self._confirm_stable_status(status, state))

    async def _confirm_stable_status(self, status, state: str) -> None:
        try:
            await asyncio.sleep(STABLE_STATUS_SECONDS)
            if state == self._last_confirmed_state:
                return

            event_time = self._status_event_time(status)
            if state == "online":
                self.logger.event(
                    "Presence",
                    f"Человек находится в сети. Время: {format_dt(event_time)}",
                    event_time,
                )
            else:
                self.logger.event(
                    "Presence",
                    f"Человек вышел из сети. Время: {format_dt(event_time)}",
                    event_time,
                )
            self._last_confirmed_state = state
        except asyncio.CancelledError:
            raise
        finally:
            if self._pending_state == state:
                self._pending_state = None
                self._pending_task = None

    def _cancel_pending(self) -> None:
        if self._pending_task and not self._pending_task.done():
            self._pending_task.cancel()
        self._pending_task = None
        self._pending_state = None

    @staticmethod
    def _status_state(status) -> Optional[str]:
        if isinstance(status, types.UserStatusOnline):
            return "online"
        if isinstance(status, types.UserStatusOffline):
            return "offline"
        return None

    @staticmethod
    def _status_event_time(status) -> datetime:
        if isinstance(status, types.UserStatusOffline) and status.was_online:
            return status.was_online
        return datetime.now().astimezone()

    @staticmethod
    def _status_label(status) -> str:
        if isinstance(status, types.UserStatusRecently):
            return "был недавно"
        if isinstance(status, types.UserStatusLastWeek):
            return "был(а) на этой неделе"
        if isinstance(status, types.UserStatusLastMonth):
            return "был(а) давно"
        if isinstance(status, types.UserStatusEmpty):
            return "время скрыто"
        return status.__class__.__name__
