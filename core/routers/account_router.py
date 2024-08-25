from fastapi import APIRouter


def get_account_router() -> APIRouter:
    """Generate a router with an account route"""
    router = APIRouter()

    @router.post("/account", status_code=201, response_model=NoteCreate)
    async def note_create(note_to_create: NoteCreate,
                          db_session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(fastapi_users.current_user(active=True))
                          ) -> NoteCreate:
        date_time_format = "%H:%M %d.%m.%Y"
        if not datetime.strptime(note_to_create.remind_time, date_time_format):
            raise HTTPException(status_code=406, detail="Wrong date-time data format")
        converted_remind_time = datetime.strptime(note_to_create.remind_time, "%H:%M %d.%m.%Y")
        if converted_remind_time < datetime.now():
            raise HTTPException(status_code=406, detail="Inappropriate time value")
        new_note = Note(user_id=user.id,
                        remind_time=converted_remind_time,
                        message=note_to_create.message,
                        important=note_to_create.important,
                        is_completed=False)
        db_session.add(new_note)
        await db_session.commit()
        return note_to_create


    @router.get("/account", response_model=list[NoteRead])
    async def get_notes(db_session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(fastapi_users.current_user(active=True))
                        ) -> list[NoteRead]:
        rows = await db_session.execute(
            select(NoteRead).where(Note.user_id == user.id and Note.is_completed==False)
        )
        rows = list(rows.scalars())
        return rows

    return router