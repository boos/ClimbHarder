import datetime
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from pymongo.errors import DuplicateKeyError
from models.physiobiometrics import Sleep, SleepUpdate, SleepOnDB
from misc import security, nosql
from bson import ObjectId

router = APIRouter(dependencies=[Depends(security.oauth2_scheme)])

@router.post("/physiobiometrics/sleep/{date}",
             response_model=Sleep,
             response_model_exclude_none=True,
             response_model_exclude_unset=True,
             response_model_exclude_defaults=True,
             status_code=status.HTTP_201_CREATED,
             tags=["physio biometrics", "sleep"])
async def create_sleep_entry(date: datetime.date, sleep_data: Sleep,
                             current_user: dict = Depends(security.get_current_user)):
    """Insert a sleep record for a specific date."""

    if date != sleep_data.date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Date in URL does not match date in payload.")

    # Create the sleep data dictionary and add username before creating SleepOnDB instance
    sleep_dict = sleep_data.dict(exclude_unset=True, exclude_none=True)
    sleep_dict["username"] = current_user["username"]

    record = SleepOnDB(**sleep_dict)
    record.date = datetime.datetime.combine(date, datetime.datetime.min.time())

    try:
        await nosql.sleep_collection.insert_one(record.model_dump(exclude_unset=True, exclude_none=True))
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"A sleep entry already exists for {date}")

    return Sleep(**record.model_dump(exclude={"username"}))




@router.get("/physiobiometrics/sleep/{date}",
            response_model=Sleep,
            response_model_exclude_none=True,
            response_model_exclude_unset=True,
            response_model_exclude_defaults=True,
            status_code=status.HTTP_200_OK,
            tags=["physio biometrics", "sleep"])
async def read_sleep_entry(date: datetime.date, current_user: dict = Depends(security.get_current_user)):
    """Retrieve a sleep record for a specific date."""

    date_time_min = datetime.datetime.combine(date, datetime.datetime.min.time())
    sleep_entry = await nosql.sleep_collection.find_one({"date": date_time_min, "username": current_user["username"]})

    if not sleep_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No physiological biometric sleep data entry "
                                                                         f"found for {date}")

    sleep_entry.pop("_id")
    sleep_entry.pop("username")
    return Sleep(**sleep_entry)


@router.patch("/physiobiometrics/sleep/{date}",
              response_model=Sleep,
              response_model_exclude_none=True,
              response_model_exclude_unset=True,
              response_model_exclude_defaults=True,
              status_code=status.HTTP_200_OK,
              tags=["physio biometrics", "sleep"])
async def update_sleep_entry(date: datetime.date, sleep_data: SleepUpdate,
                             current_user: dict = Depends(security.get_current_user)):
    """Partially update a sleep record for a specific date and return the updated document."""

    update_fields = {k: v for k, v in updates.dict(exclude_unset=True, exclude_none=True).items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No fields provided for update.")

    result = await nosql.sleep_collection.update_one({"date": date, "username": current_user["username"]},
                                                     {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No sleep entry found to update for {date}")

    updated_entry = await nosql.sleep_collection.find_one({"date": date,"username": current_user["username"]})

    updated_entry["_id"] = str(updated_entry["_id"])
    return updated_entry



@router.delete("/physiobiometrics/sleep/{date}",
               response_model_exclude_none=True,
               response_model_exclude_unset=True,
               response_model_exclude_defaults=True,
               status_code=status.HTTP_200_OK,
               tags=["physio biometrics", "sleep"])
async def delete_sleep_entry(date: datetime.date, current_user: dict = Depends(security.get_current_user)):
    """Delete a sleep record for a specific date."""

    result = await nosql.sleep_collection.delete_one({
        "date": datetime.datetime.combine(date, datetime.datetime.min.time()),
        "username": current_user["username"]})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No sleep entry found to delete for {date}"
        )

    return {"message": f"Sleep entry for {date} deleted successfully."}
