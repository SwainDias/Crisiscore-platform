"""
app/core/constants.py
Single source of truth for all string constants, error codes, and enumerations.
"""

from enum import StrEnum


# ─── HTTP / API ──────────────────────────────────────────────────────────────

API_V1_PREFIX = "/api/v1"


# ─── Auth Error Codes ────────────────────────────────────────────────────────

class AuthErrorCode(StrEnum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    NETWORK_MISMATCH = "NETWORK_MISMATCH"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"


# ─── Alert Error Codes ───────────────────────────────────────────────────────

class AlertErrorCode(StrEnum):
    DUPLICATE_ALERT = "DUPLICATE_ALERT"
    LOCATION_REQUIRED = "LOCATION_REQUIRED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    ALERT_TYPE_NOT_FOUND = "ALERT_TYPE_NOT_FOUND"


# ─── Generic Error Codes ─────────────────────────────────────────────────────

class GenericErrorCode(StrEnum):
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    RATE_LIMITED = "RATE_LIMITED"


# ─── Staff Roles ─────────────────────────────────────────────────────────────

class StaffRole(StrEnum):
    SECURITY = "security"
    EMS = "ems"
    WARDEN = "warden"
    ADMIN = "admin"


# ─── Duty / Shift Status ─────────────────────────────────────────────────────

class DutyStatus(StrEnum):
    ON_DUTY = "on_duty"
    OFF_DUTY = "off_duty"
    STANDBY = "standby"


class ShiftStatus(StrEnum):
    ACTIVE = "active"
    BREAK = "break"
    ENDED = "ended"


# ─── Task ────────────────────────────────────────────────────────────────────

class TaskPriority(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    ROUTINE = "routine"


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ─── Incident / Alert ────────────────────────────────────────────────────────

class IncidentSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class IncidentStatus(StrEnum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    INVESTIGATING = "investigating"


class AlertUserType(StrEnum):
    STAFF = "staff"
    GUEST = "guest"


# ─── Device / Connectivity ───────────────────────────────────────────────────

class DeviceHealth(StrEnum):
    OPTIMAL = "optimal"
    DEGRADED = "degraded"
    CRITICAL = "critical"


class ConnectivityStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    LIMITED = "limited"


# ─── Service Status ──────────────────────────────────────────────────────────

class ServiceStatus(StrEnum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    SYNCED = "synced"


# ─── Timeline Event Icons ────────────────────────────────────────────────────

class TimelineIconType(StrEnum):
    ALERT = "alert"
    PERSON = "person"
    EMS = "ems"
    CHECK = "check"


# ─── Drill ───────────────────────────────────────────────────────────────────

DRILL_PASSING_PERCENT = 70.0        # minimum % to pass a micro-drill


# ─── SOS Broadcast ───────────────────────────────────────────────────────────

SOS_BROADCAST_CHANNEL = "sos:broadcasts"


# ─── Collections (MongoDB collection names) ──────────────────────────────────

class Collection(StrEnum):
    STAFF = "staff"
    PROPERTIES = "properties"
    INCIDENTS = "incidents"
    ALERTS = "alerts"
    ALERT_TYPES = "alert_types"
    TASKS = "tasks"
    LOGS = "logs"
    DRILLS = "drills"
    DRILL_SESSIONS = "drill_sessions"
    DRILL_QUESTIONS = "drill_questions"
    SAFETY_CHECKS = "safety_checks"
    ACTION_ITEMS = "action_items"
    REFRESH_TOKENS = "refresh_tokens"
