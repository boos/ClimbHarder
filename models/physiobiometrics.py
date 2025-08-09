from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime

class Sleep(BaseModel):

    # Mandatory fields for core recovery and training load evaluation (based on sleep quantity and autonomic status)
    date: datetime.date = Field(title="Physiological sleep date.")

    # Micro, Microcycle, Meso, Macro parameters 
    avg_hrv: int = Field(gt=0, title="Average HRV in milliseconds")
    avg_hrv_7d: int = Field(None, gt=0, title="7-day average HRV in milliseconds")

    avg_sleep_hr: int = Field(gt=0, title="Average heart rate during sleep")
    avg_sleep_hr_7d: int = Field(None, gt=0, title="7-day average of sleep HR")

    # subjective_rating is a meta-parameter
    subjective_rating: Optional[int] = Field(None, ge=1, le=9, title="Subjective sleep rating (1–9)") 
    skin_temp_offset: float = Field(None, title="Skin temperature offset from baseline")

    sleep_score: int = Field(None, ge=0, le=100, title="Sleep score provided by the device")
    
    sleep_duration_minutes: int = Field(gt=0, title="Total sleep duration in minutes")
    sleep_efficiency_percent: float = Field(None, ge=0, le=100, title="Sleep efficiency in percent")

    # Micro, Microcycle, Meso parameters 
    awake_duration_min: int = Field(None, gt=0, title="Awake time during sleep in minutes")
    deep_duration_min: int = Field(None, gt=0, title="Deep sleep duration in minutes")
    rem_duration_min: int = Field(None, gt=0, title="REM sleep duration in minutes")

    # avg respiratory rate is a Microcycle, Meso, Macro and Meta parameter
    avg_respiratory_rate: Optional[float] = Field(None, ge=0, title="Respiratory rate (breaths per minute)")
    skin_temp_baseline: float = Field(None, gt=0, title="Baseline skin temperature")

    spo2_avg: float = Field(None, ge=0, le=100, title="Average SpO₂ (%) during sleep")
    spo2_avg_7d: float = Field(None, ge=0, le=100, title="7-day average SpO₂ (%)")

    
    avg_respiratory_rate_7d: float = Field(None, ge=0, title="7-day average respiratory rate")
    min_respiratory_rate: float = Field(None, ge=0, title="Minimum respiratory rate during sleep")
    max_respiratory_rate: float = Field(None, ge=0, title="Maximum respiratory rate during sleep")

    note: Optional[str] = Field(None, title="Optional note")

    model_config = ConfigDict(extra="forbid")

class SleepUpdate(BaseModel):
    """Fields that can be partially updated in a sleep entry."""

    # Mandatory fields for core recovery and training load evaluation (based on sleep quantity and autonomic status)
    date: datetime.date = Field(title="Physiological sleep date.")

    # Micro, Microcycle, Meso, Macro parameters 
    avg_hrv: Optional[int] = Field(None, gt=0, title="Average HRV in milliseconds")
    avg_hrv_7d: Optional[int] = Field(None, gt=0, title="7-day average HRV in milliseconds")

    avg_sleep_hr: Optional[int] = Field(None, gt=0, title="Average heart rate during sleep")
    avg_sleep_hr_7d: Optional[int] = Field(None, gt=0, title="7-day average of sleep HR")

    # subjective_rating is a meta-parameter
    subjective_rating: Optional[int] = Field(None, ge=1, le=9, title="Subjective sleep rating (1–9)")
    skin_temp_offset: Optional[float] = Field(None, title="Skin temperature offset from baseline")

    sleep_score: Optional[int] = Field(None, ge=0, le=100, title="Sleep score provided by the device")

    sleep_duration_minutes: Optional[int] = Field(None, gt=0, title="Total sleep duration in minutes")
    sleep_efficiency_percent: Optional[float] = Field(None, ge=0, le=100, title="Sleep efficiency in percent")

    # Micro, Microcycle, Meso parameters 
    awake_duration_min: Optional[int] = Field(None, gt=0, title="Awake time during sleep in minutes")
    deep_duration_min: Optional[int] = Field(None, gt=0, title="Deep sleep duration in minutes")
    rem_duration_min: Optional[int] = Field(None, gt=0, title="REM sleep duration in minutes")

    # avg respiratory rate is a Microcycle, Meso, Macro and Meta parameter
    avg_respiratory_rate: Optional[float] = Field(None, ge=0, title="Respiratory rate (breaths per minute)")
    skin_temp_baseline: Optional[float] = Field(None, gt=0, title="Baseline skin temperature")

    spo2_avg: Optional[float] = Field(None, ge=0, le=100, title="Average SpO₂ (%) during sleep")
    spo2_avg_7d: Optional[float] = Field(None, ge=0, le=100, title="7-day average SpO₂ (%)")

    avg_respiratory_rate_7d: Optional[float] = Field(None, ge=0, title="7-day average respiratory rate")
    min_respiratory_rate: Optional[float] = Field(None, ge=0, title="Minimum respiratory rate during sleep")
    max_respiratory_rate: Optional[float] = Field(None, ge=0, title="Maximum respiratory rate during sleep")

    note: Optional[str] = Field(None, title="Optional note")


class SleepOnDB(Sleep):
    """Sleep model used for persistence in the database, with username as identifier."""
    username: str = Field(..., title="Username of the data owner")
