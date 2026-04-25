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


# ─── Guest Error Codes ───────────────────────────────────────────────────────

class GuestErrorCode(StrEnum):
    GUEST_NOT_FOUND = "GUEST_NOT_FOUND"
    CHECKIN_NOT_FOUND = "CHECKIN_NOT_FOUND"
    INVALID_EMERGENCY_PROFILE = "INVALID_EMERGENCY_PROFILE"
    ALERT_GUIDE_NOT_FOUND = "ALERT_GUIDE_NOT_FOUND"


# ─── Incident / Responder Error Codes ───────────────────────────────────────

class IncidentErrorCode(StrEnum):
    INCIDENT_NOT_FOUND = "INCIDENT_NOT_FOUND"
    INCIDENT_ALREADY_RESOLVED = "INCIDENT_ALREADY_RESOLVED"
    INVALID_INCIDENT_STATE = "INVALID_INCIDENT_STATE"
    ASSIGNMENT_FAILED = "ASSIGNMENT_FAILED"
    INCIDENT_LOG_FAILED = "INCIDENT_LOG_FAILED"


# ─── Admin Error Codes ───────────────────────────────────────────────────────

class AdminErrorCode(StrEnum):
    STAFF_NOT_FOUND = "STAFF_NOT_FOUND"
    INTEGRATION_NOT_FOUND = "INTEGRATION_NOT_FOUND"
    SETTING_NOT_FOUND = "SETTING_NOT_FOUND"
    DANGER_ACTION_NOT_ALLOWED = "DANGER_ACTION_NOT_ALLOWED"
    INVALID_BROADCAST_AUDIENCE = "INVALID_BROADCAST_AUDIENCE"


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
    CONTAINED = "contained"
    RESOLVED = "resolved"
    INVESTIGATING = "investigating"


class IncidentType(StrEnum):
    MEDICAL = "medical"
    FIRE = "fire"
    SECURITY = "security"
    WEATHER = "weather"
    HAZMAT = "hazmat"
    CUSTOM = "custom"


class AlertGuideType(StrEnum):
    SHELTER_IN_PLACE = "shelter_in_place"
    EVACUATE = "evacuate"
    LOCKDOWN = "lockdown"
    MEDICAL = "medical"
    CUSTOM = "custom"


class CrisisPriority(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class IncidentPinType(StrEnum):
    FIRE = "fire"
    MEDICAL = "medical"
    SECURITY = "security"


class AlertUserType(StrEnum):
    STAFF = "staff"
    GUEST = "guest"


class BloodType(StrEnum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "unknown"


class MobilityNeed(StrEnum):
    WHEELCHAIR_ACCESS = "wheelchair_access"
    HEARING_IMPAIRED = "hearing_impaired"
    VISUALLY_IMPAIRED = "visually_impaired"
    SERVICE_ANIMAL = "service_animal"


class InfoHubCategory(StrEnum):
    PROTOCOL = "protocol"
    RESOURCE = "resource"
    NOTICE = "notice"


class ResponderUnitStatus(StrEnum):
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    DISPATCHED = "dispatched"
    STANDBY = "standby"


class SOPStepStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class StaffDirectoryStatus(StrEnum):
    AVAILABLE = "available"
    RESPONDING = "responding"
    UNRESPONSIVE = "unresponsive"
    OFF_DUTY = "off_duty"


class IncidentQueueStatus(StrEnum):
    RESOLVED = "resolved"
    INVESTIGATING = "investigating"
    ACTIVE = "active"


class GuestAccountabilityStatus(StrEnum):
    EVACUATED = "evacuated"
    UNKNOWN = "unknown"
    SHELTER_IN_PLACE = "shelter_in_place"
    INJURED = "injured"


class BroadcastAudience(StrEnum):
    ALL_GUESTS = "all_guests"
    AFFECTED_FLOOR = "affected_floor"
    SPECIFIC_ROOM = "specific_room"


class BroadcastChannel(StrEnum):
    APP_PUSH = "app_push"
    WHATSAPP = "whatsapp"
    SMS = "sms"


class ExternalService(StrEnum):
    FIRE_DEPARTMENT = "fire_department"
    POLICE = "police"
    MEDICAL = "medical"


class ExternalServiceStatus(StrEnum):
    ON_SCENE = "on_scene"
    EN_ROUTE = "en_route"
    STANDBY = "standby"
    NOT_NOTIFIED = "not_notified"


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


class IntegrationCategory(StrEnum):
    PHYSICAL_SECURITY = "physical_security"
    PMS = "pms"
    COMMUNICATION = "communication"
    SENSOR = "sensor"


class IntegrationStatus(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class SyncSchedule(StrEnum):
    REAL_TIME_WEBHOOK = "real_time_webhook"
    INTERVAL = "interval"
    MANUAL = "manual"


class AdminUserRole(StrEnum):
    SUPER_ADMIN = "super_admin"
    PROPERTY_ADMIN = "property_admin"
    MANAGER = "manager"
    RESPONDER = "responder"


class DangerZoneAction(StrEnum):
    RESET_ALL_INCIDENTS = "reset_all_incidents"
    CLEAR_GUEST_REGISTRY = "clear_guest_registry"
    FACTORY_RESET = "factory_reset"


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


# ─── Guest / Resident ────────────────────────────────────────────────────────

class BloodType(StrEnum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"
    UNKNOWN = "unknown"


class MobilityNeed(StrEnum):
    WHEELCHAIR_ACCESS = "wheelchair_access"
    HEARING_IMPAIRED = "hearing_impaired"
    VISUALLY_IMPAIRED = "visually_impaired"
    SERVICE_ANIMAL = "service_animal"


class GuestAlertType(StrEnum):
    SHELTER_IN_PLACE = "shelter_in_place"
    EVACUATE = "evacuate"
    LOCKDOWN = "lockdown"
    MEDICAL = "medical"
    CUSTOM = "custom"


class GuestAccountabilityStatus(StrEnum):
    EVACUATED = "evacuated"
    UNKNOWN = "unknown"
    SHELTER_IN_PLACE = "shelter_in_place"
    INJURED = "injured"


# ─── Responder ───────────────────────────────────────────────────────────────

class ResponderStatus(StrEnum):
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    DISPATCHED = "dispatched"
    STANDBY = "standby"


class SOPStepStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class IncidentType(StrEnum):
    MEDICAL = "medical"
    FIRE = "fire"
    SECURITY = "security"
    WEATHER = "weather"
    HAZMAT = "hazmat"
    CUSTOM = "custom"


class IncidentContainmentStatus(StrEnum):
    ACTIVE = "active"
    CONTAINED = "contained"
    RESOLVED = "resolved"


# ─── Admin ───────────────────────────────────────────────────────────────────

class IncidentPriority(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class StaffOperationalStatus(StrEnum):
    AVAILABLE = "available"
    RESPONDING = "responding"
    UNRESPONSIVE = "unresponsive"
    OFF_DUTY = "off_duty"


class BroadcastAudience(StrEnum):
    ALL_GUESTS = "all_guests"
    AFFECTED_FLOOR = "affected_floor"
    SPECIFIC_ROOM = "specific_room"


class BroadcastChannel(StrEnum):
    APP_PUSH = "app_push"
    WHATSAPP = "whatsapp"
    SMS = "sms"


class IntegrationCategory(StrEnum):
    PHYSICAL_SECURITY = "physical_security"
    PMS = "pms"
    COMMUNICATION = "communication"
    SENSOR = "sensor"


class IntegrationStatus(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class SyncSchedule(StrEnum):
    REAL_TIME_WEBHOOK = "real_time_webhook"
    INTERVAL = "interval"
    MANUAL = "manual"


class AdminRole(StrEnum):
    SUPER_ADMIN = "super_admin"
    PROPERTY_ADMIN = "property_admin"
    MANAGER = "manager"
    RESPONDER = "responder"


class ExternalService(StrEnum):
    FIRE_DEPARTMENT = "fire_department"
    POLICE = "police"
    MEDICAL = "medical"


class ExternalServiceStatus(StrEnum):
    ON_SCENE = "on_scene"
    EN_ROUTE = "en_route"
    STANDBY = "standby"
    NOT_NOTIFIED = "not_notified"


class DangerZoneAction(StrEnum):
    RESET_ALL_INCIDENTS = "reset_all_incidents"
    CLEAR_GUEST_REGISTRY = "clear_guest_registry"
    FACTORY_RESET = "factory_reset"


class InfoHubCategory(StrEnum):
    PROTOCOL = "protocol"
    RESOURCE = "resource"
    NOTICE = "notice"


# ─── Admin Error Codes ────────────────────────────────────────────────────────

class AdminErrorCode(StrEnum):
    INVALID_CONFIRMATION_TOKEN = "INVALID_CONFIRMATION_TOKEN"
    STAFF_NOT_FOUND = "STAFF_NOT_FOUND"
    INCIDENT_NOT_ACTIVE = "INCIDENT_NOT_ACTIVE"
    INTEGRATION_NOT_FOUND = "INTEGRATION_NOT_FOUND"
    IMPORT_FAILED = "IMPORT_FAILED"
    BROADCAST_FAILED = "BROADCAST_FAILED"
    INVALID_DANGER_ACTION = "INVALID_DANGER_ACTION"


# ─── WebSocket channels ───────────────────────────────────────────────────────

WS_ADMIN_MAP_CHANNEL = "ws:admin:map"
WS_INCIDENT_CHANNEL_PREFIX = "ws:incident:"      # + incident_id


# ─── Collections (MongoDB collection names) ──────────────────────────────────

class Collection(StrEnum):
    STAFF = "staff"
    GUESTS = "guests"
    ROOMS = "rooms"
    PROPERTIES = "properties"
    INCIDENTS = "incidents"
    INCIDENT_LOGS = "incident_logs"
    ALERTS = "alerts"
    ALERT_TYPES = "alert_types"
    TASKS = "tasks"
    LOGS = "logs"
    DRILLS = "drills"
    DRILL_SESSIONS = "drill_sessions"
    DRILL_QUESTIONS = "drill_questions"
    SAFETY_CHECKS = "safety_checks"
    GUEST_CHECKINS = "guest_checkins"
    ACTION_ITEMS = "action_items"
    RESPONDER_ASSIGNMENTS = "responder_assignments"
    BROADCASTS = "broadcasts"
    INTEGRATIONS = "integrations"
    SETTINGS = "settings"
    USER_ROLES = "user_roles"
    PROTOCOLS = "protocols"
    CCTV_CAMERAS = "cctv_cameras"
    REFRESH_TOKENS = "refresh_tokens"
    # New
    GUESTS = "guests"
    CHECKINS = "checkins"
    ROOMS = "rooms"
    SOP_PROTOCOLS = "sop_protocols"
    RESPONDER_LOGS = "responder_logs"
    BROADCASTS = "broadcasts"
    INTEGRATIONS = "integrations"
    ADMIN_USERS = "admin_users"
    CCTV_CAMERAS = "cctv_cameras"