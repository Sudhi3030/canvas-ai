from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class MetricScore(BaseModel):
    score: float = Field(..., ge=0.0, le=100.0)
    details: str = Field(default="")

class ScoreBreakdown(BaseModel):
    hierarchy: MetricScore
    alignment: MetricScore
    spacing: MetricScore
    balance: MetricScore
    contrast: MetricScore
    accessibility: MetricScore
    overall_score: float = Field(..., ge=0.0, le=100.0)
