"""
scripts/seed_db.py
Seeds the MongoDB database with sample data for local development and testing.

Usage:
    python scripts/seed_db.py
"""

import asyncio
from datetime import UTC, datetime

from motor.motor_asyncio import AsyncIOMotorClient
from argon2 import PasswordHasher

MONGO_URI = "mongodb://mongodb:27017"
DB_NAME = "rapid_response"

_ph = PasswordHasher()


async def seed() -> None:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    print("🌱  Seeding database …")

    # ── Staff ─────────────────────────────────────────────────────────────────
    await db.staff.delete_many({})
    await db.staff.insert_many(
        [
            {
                "employee_id": "EMP001",
                "name": "Rajesh Kumar",
                "pin_hash": _ph.hash("1234"),
                "role": "security",
                "property_id": "PROP-HSG-001",
                "duty_status": "on_duty",
                "assignment_id": "ZONE-MAIN",
                "assignment_label": "Main Gate",
                "checkin_time": datetime.now(UTC).isoformat(),
                "failed_attempts": 0,
                "locked_until": None,
                "avatar_url": None,
            },
            {
                "employee_id": "EMP002",
                "name": "Priya Sharma",
                "pin_hash": _ph.hash("5678"),
                "role": "warden",
                "property_id": "PROP-HSG-001",
                "duty_status": "on_duty",
                "assignment_id": "ZONE-A",
                "assignment_label": "Block A Warden",
                "checkin_time": datetime.now(UTC).isoformat(),
                "failed_attempts": 0,
                "locked_until": None,
                "avatar_url": None,
            },
            {
                "employee_id": "ADM001",
                "name": "Anita Desai",
                "pin_hash": _ph.hash("0000"),
                "role": "admin",
                "property_id": "PROP-HSG-001",
                "duty_status": "on_duty",
                "assignment_id": "OFFICE",
                "assignment_label": "Society Office",
                "checkin_time": datetime.now(UTC).isoformat(),
                "failed_attempts": 0,
                "locked_until": None,
                "avatar_url": None,
            },
        ]
    )
    print("  ✓  Staff seeded (EMP001/1234, EMP002/5678, ADM001/0000)")

    # ── Alert Types ───────────────────────────────────────────────────────────
    await db.alert_types.delete_many({})
    await db.alert_types.insert_many(
        [
            {
                "type_id": "FIRE",
                "label": "Fire",
                "description": "Smoke or fire detected in the building",
                "icon": "flame",
                "color_hex": "#FF4500",
                "severity_default": "critical",
                "active": True,
            },
            {
                "type_id": "MEDICAL",
                "label": "Medical Emergency",
                "description": "Someone needs immediate medical attention",
                "icon": "heart-pulse",
                "color_hex": "#E91E63",
                "severity_default": "critical",
                "active": True,
            },
            {
                "type_id": "SECURITY",
                "label": "Security Threat",
                "description": "Suspicious activity or security breach",
                "icon": "shield-alert",
                "color_hex": "#FF6F00",
                "severity_default": "warning",
                "active": True,
            },
            {
                "type_id": "GAS_LEAK",
                "label": "Gas Leak",
                "description": "Gas smell or suspected leak",
                "icon": "wind",
                "color_hex": "#9C27B0",
                "severity_default": "critical",
                "active": True,
            },
            {
                "type_id": "FLOOD",
                "label": "Water / Flooding",
                "description": "Water damage, burst pipe, or flooding",
                "icon": "droplets",
                "color_hex": "#2196F3",
                "severity_default": "warning",
                "active": True,
            },
            {
                "type_id": "POWER",
                "label": "Power Failure",
                "description": "Electricity outage in the building",
                "icon": "zap-off",
                "color_hex": "#607D8B",
                "severity_default": "info",
                "active": True,
            },
        ]
    )
    print("  ✓  Alert types seeded (6 types)")

    # ── Drills ────────────────────────────────────────────────────────────────
    await db.drills.delete_many({})
    await db.drill_questions.delete_many({})

    await db.drills.insert_one(
        {
            "drill_id": "DRILL-FIRE-001",
            "title": "Fire Evacuation Basics",
            "description": "Quick 60-second fire safety refresher",
            "active": True,
        }
    )

    await db.drill_questions.insert_many(
        [
            {
                "drill_id": "DRILL-FIRE-001",
                "question_id": "Q001",
                "index": 0,
                "category": "Evacuation",
                "scenario_text": "You smell smoke on the 4th floor.",
                "prompt": "What is your FIRST action?",
                "image_url": None,
                "options": [
                    {"option_id": "A", "text": "Use the elevator to evacuate"},
                    {"option_id": "B", "text": "Activate the nearest fire alarm pull station"},
                    {"option_id": "C", "text": "Call a colleague first"},
                    {"option_id": "D", "text": "Look for the fire source"},
                ],
                "correct_option_id": "B",
                "feedback_correct": "Correct! Always activate the alarm first to alert all occupants.",
                "feedback_incorrect": "Never use elevators in a fire. Activate the alarm pull station immediately.",
            },
            {
                "drill_id": "DRILL-FIRE-001",
                "question_id": "Q002",
                "index": 1,
                "category": "Evacuation",
                "scenario_text": "The fire alarm is sounding.",
                "prompt": "Which route should residents use to evacuate?",
                "image_url": None,
                "options": [
                    {"option_id": "A", "text": "The fastest route regardless of smoke"},
                    {"option_id": "B", "text": "Designated stairwell — check door for heat first"},
                    {"option_id": "C", "text": "The elevator"},
                    {"option_id": "D", "text": "Wait for fire department instructions"},
                ],
                "correct_option_id": "B",
                "feedback_correct": "Correct! Use the designated stairwell and always check the door for heat before opening.",
                "feedback_incorrect": "Always use the designated stairwell. Check the door for heat — never use elevators.",
            },
            {
                "drill_id": "DRILL-FIRE-001",
                "question_id": "Q003",
                "index": 2,
                "category": "Equipment",
                "scenario_text": "A small wastepaper bin is on fire in an office.",
                "prompt": "Which fire extinguisher class should you use?",
                "image_url": None,
                "options": [
                    {"option_id": "A", "text": "Class A — ordinary combustibles"},
                    {"option_id": "B", "text": "Class B — flammable liquids"},
                    {"option_id": "C", "text": "Class C — electrical fires"},
                    {"option_id": "D", "text": "Class D — metal fires"},
                ],
                "correct_option_id": "A",
                "feedback_correct": "Correct! Class A extinguishers handle ordinary combustibles like paper and wood.",
                "feedback_incorrect": "Paper fires are Class A — ordinary combustibles. Use a Class A extinguisher.",
            },
        ]
    )
    print("  ✓  Drill 'DRILL-FIRE-001' seeded with 3 questions")

    # ── Properties ────────────────────────────────────────────────────────────
    await db.properties.delete_many({})
    await db.properties.insert_one(
        {
            "property_id": "PROP-HSG-001",
            "name": "Sunrise Heights",
            "address": "Plot 42, Andheri West, Mumbai 400058",
            "network_id": "PROP-HSG-001",
            "total_units": 120,
            "blocks": ["A", "B", "C"],
        }
    )
    print("  ✓  Property 'Sunrise Heights' seeded")

    # ── Rooms ─────────────────────────────────────────────────────────────────
    await db.rooms.delete_many({})
    await db.rooms.insert_many(
        [
            {
                "room_id": "ROOM-A-302",
                "property_id": "PROP-HSG-001",
                "room_number": "A-302",
                "wing": "A",
                "floor": 3,
                "zone_id": "ZONE-A3",
                "zone_label": "Block A Floor 3",
                "is_safe_zone": False,
                "safe_zone_note": None,
            },
            {
                "room_id": "ROOM-B-201",
                "property_id": "PROP-HSG-001",
                "room_number": "B-201",
                "wing": "B",
                "floor": 2,
                "zone_id": "ZONE-B2",
                "zone_label": "Block B Floor 2",
                "is_safe_zone": True,
                "safe_zone_note": "Designated shelter room with emergency kit.",
            },
            {
                "room_id": "ROOM-C-105",
                "property_id": "PROP-HSG-001",
                "room_number": "C-105",
                "wing": "C",
                "floor": 1,
                "zone_id": "ZONE-C1",
                "zone_label": "Block C Floor 1",
                "is_safe_zone": False,
                "safe_zone_note": None,
            },
        ]
    )
    print("  ✓  Rooms seeded (3 rooms)")

    # ── Guests ────────────────────────────────────────────────────────────────
    await db.guests.delete_many({})
    await db.guests.insert_many(
        [
            {
                "guest_id": "GST001",
                "name": "Aarav Mehta",
                "property_id": "PROP-HSG-001",
                "room_id": "ROOM-A-302",
                "room_number": "A-302",
                "wing": "A",
                "floor": 3,
                "status": "checked_in",
                "zone_id": "ZONE-A3",
                "lat": 19.0730,
                "lng": 72.8801,
                "emergency_profile": {
                    "blood_type": "O+",
                    "mobility_needs": ["hearing_impaired"],
                    "medical_notes": "Mild asthma",
                    "share_with_responders": True,
                },
            },
            {
                "guest_id": "GST002",
                "name": "Sara Khan",
                "property_id": "PROP-HSG-001",
                "room_id": "ROOM-B-201",
                "room_number": "B-201",
                "wing": "B",
                "floor": 2,
                "status": "checked_in",
                "zone_id": "ZONE-B2",
                "lat": 19.0728,
                "lng": 72.8797,
                "emergency_profile": {
                    "blood_type": "A+",
                    "mobility_needs": ["wheelchair_access"],
                    "medical_notes": None,
                    "share_with_responders": True,
                },
            },
            {
                "guest_id": "GST003",
                "name": "David Roy",
                "property_id": "PROP-HSG-001",
                "room_id": "ROOM-C-105",
                "room_number": "C-105",
                "wing": "C",
                "floor": 1,
                "status": "checked_in",
                "zone_id": "ZONE-C1",
                "lat": 19.0724,
                "lng": 72.8792,
                "emergency_profile": {
                    "blood_type": "unknown",
                    "mobility_needs": [],
                    "medical_notes": None,
                    "share_with_responders": False,
                },
            },
        ]
    )
    print("  ✓  Guests seeded (3 guests)")

    # ── Tasks ─────────────────────────────────────────────────────────────────
    await db.tasks.delete_many({})
    await db.tasks.insert_many(
        [
            {
                "task_id": "TSK-001",
                "assigned_to": "EMP001",
                "title": "Check fire panel status",
                "priority": "high",
                "priority_order": 1,
                "status": "pending",
                "due_at": datetime.now(UTC).isoformat(),
            },
            {
                "task_id": "TSK-002",
                "assigned_to": "EMP001",
                "title": "Verify emergency exits",
                "priority": "medium",
                "priority_order": 2,
                "status": "in_progress",
                "due_at": datetime.now(UTC).isoformat(),
            },
            {
                "task_id": "TSK-003",
                "assigned_to": "EMP002",
                "title": "Update occupancy log",
                "priority": "routine",
                "priority_order": 3,
                "status": "pending",
                "due_at": datetime.now(UTC).isoformat(),
            },
        ]
    )
    print("  ✓  Tasks seeded (3 tasks)")

    # ── Incidents & Alerts ───────────────────────────────────────────────────
    await db.incidents.delete_many({})
    await db.alerts.delete_many({})

    active_incident_id = "INC-2026-0001"
    resolved_incident_id = "INC-2026-0000"

    await db.incidents.insert_many(
        [
            {
                "incident_id": active_incident_id,
                "incident_code": "INC-ACT-0001",
                "event_code": "EVT-FIRE-001",
                "property_id": "PROP-HSG-001",
                "type": "fire",
                "status": "active",
                "severity": "P2",
                "title": "Smoke detected near Block A utility room",
                "description": "Smoke sensor triggered and manual confirmation pending.",
                "auto_triggered": True,
                "created_at": datetime.now(UTC),
                "started_at": datetime.now(UTC),
                "location": {
                    "building": "Block A",
                    "zone": "Utility Corridor",
                    "sector": "A3",
                    "room": "A-Utility-03",
                    "floor": 3,
                    "coordinates": {"lat": 19.0732, "lng": 72.8804},
                },
                "sensor_status": True,
                "responder_assignments": [
                    {
                        "employee_id": "EMP001",
                        "name": "Rajesh Kumar",
                        "role": "security",
                        "team": "Alpha",
                        "status": "on_scene",
                        "eta_seconds": 0,
                        "unit_label": "Unit-1",
                    },
                    {
                        "employee_id": "EMP002",
                        "name": "Priya Sharma",
                        "role": "warden",
                        "team": "Bravo",
                        "status": "en_route",
                        "eta_seconds": 90,
                        "unit_label": "Unit-2",
                    },
                ],
                "guest_accountability": [
                    {
                        "guest_id": "GST001",
                        "room": "A-302",
                        "name": "Aarav Mehta",
                        "status": "evacuated",
                    },
                    {
                        "guest_id": "GST002",
                        "room": "B-201",
                        "name": "Sara Khan",
                        "status": "unknown",
                    },
                ],
                "services_notified": ["fire", "medical"],
                "external_services": [
                    {"service": "fire_department", "status": "en_route", "eta_seconds": 300},
                    {"service": "medical", "status": "standby", "eta_seconds": None},
                ],
                "sop": {
                    "protocol_name": "Fire First Response",
                    "total_steps": 4,
                    "completed_steps": 2,
                    "steps": [
                        {
                            "step_id": "S1",
                            "order": 1,
                            "title": "Verify alarm source",
                            "description": "Confirm false positive vs active smoke.",
                            "status": "completed",
                            "completed_at": datetime.now(UTC).isoformat(),
                        },
                        {
                            "step_id": "S2",
                            "order": 2,
                            "title": "Dispatch nearest responders",
                            "description": "Send security and warden team.",
                            "status": "completed",
                            "completed_at": datetime.now(UTC).isoformat(),
                        },
                        {
                            "step_id": "S3",
                            "order": 3,
                            "title": "Prepare evacuation",
                            "description": "Broadcast advisory to guests.",
                            "status": "pending",
                            "completed_at": None,
                        },
                        {
                            "step_id": "S4",
                            "order": 4,
                            "title": "Escalate if smoke spreads",
                            "description": "Trigger full evacuation if required.",
                            "status": "pending",
                            "completed_at": None,
                        },
                    ],
                },
                "timeline": [
                    {
                        "event_id": "evt-1",
                        "timestamp": datetime.now(UTC).isoformat(),
                        "title": "Sensor trigger",
                        "description": "Smoke sensor triggered on floor 3.",
                        "icon_type": "alert",
                    },
                    {
                        "event_id": "evt-2",
                        "timestamp": datetime.now(UTC).isoformat(),
                        "title": "Responders dispatched",
                        "description": "Security and warden teams dispatched.",
                        "icon_type": "person",
                    },
                ],
                "kpis": {
                    "response_time_seconds": 74,
                    "sla_delta_seconds": -26,
                    "personnel_accounted": 2,
                    "personnel_total": 3,
                    "sop_compliance_percent": 68.0,
                    "deviations_logged": 0,
                },
            },
            {
                "incident_id": resolved_incident_id,
                "incident_code": "INC-RES-0000",
                "event_code": "EVT-MED-000",
                "property_id": "PROP-HSG-001",
                "type": "medical",
                "status": "resolved",
                "severity": "P3",
                "title": "Minor medical incident in lobby",
                "description": "First aid provided and incident closed.",
                "created_at": datetime.now(UTC),
                "concluded_at": datetime.now(UTC),
                "location": {
                    "building": "Lobby",
                    "zone": "Reception",
                    "sector": "L1",
                    "room": "LOBBY",
                    "floor": 1,
                    "coordinates": {"lat": 19.0725, "lng": 72.8795},
                },
                "timeline": [],
                "improvement_opportunities": [],
                "kpis": {"response_time_seconds": 120},
            },
        ]
    )

    await db.alerts.insert_many(
        [
            {
                "alert_id": "ALT-0001",
                "type_id": "FIRE",
                "incident_id": active_incident_id,
                "additional_details": "Smoke smell near electrical panel.",
                "location": {"lat": 19.0732, "lng": 72.8804, "manual_label": "Block A Floor 3"},
                "raised_by": {"user_id": "EMP001", "user_type": "staff"},
                "severity": "warning",
                "status": "active",
                "device_id": "DEV-SEC-1",
                "created_at": datetime.now(UTC),
            }
        ]
    )
    print("  ✓  Incidents and alerts seeded")

    # ── Responder assignments / logs ─────────────────────────────────────────
    await db.responder_assignments.delete_many({})
    await db.responder_assignments.insert_many(
        [
            {
                "assignment_id": "ASG-0001",
                "incident_id": active_incident_id,
                "employee_id": "EMP001",
                "assigned_by": "ADM001",
                "status": "on_scene",
                "eta_seconds": 0,
            },
            {
                "assignment_id": "ASG-0002",
                "incident_id": active_incident_id,
                "employee_id": "EMP002",
                "assigned_by": "ADM001",
                "status": "en_route",
                "eta_seconds": 90,
            },
        ]
    )

    await db.incident_logs.delete_many({})
    await db.incident_logs.insert_many(
        [
            {
                "incident_id": active_incident_id,
                "log_id": "LOG-0001",
                "actor_id": "ADM001",
                "note": "Initial command center established.",
                "timestamp": datetime.now(UTC).isoformat(),
            },
            {
                "incident_id": active_incident_id,
                "log_id": "LOG-0002",
                "actor_id": "EMP001",
                "note": "Smoke level moderate, no flame visible.",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        ]
    )
    print("  ✓  Responder assignments and incident logs seeded")

    # ── Broadcasts ────────────────────────────────────────────────────────────
    await db.broadcasts.delete_many({})
    await db.broadcasts.insert_one(
        {
            "broadcast_id": "BRD-0001",
            "incident_id": active_incident_id,
            "property_id": "PROP-HSG-001",
            "audience": "affected_floor",
            "message": "Please remain calm and await instructions.",
            "channels": ["app_push", "whatsapp"],
            "sent_by": "ADM001",
            "recipients": 2,
            "created_at": datetime.now(UTC),
        }
    )
    print("  ✓  Broadcast history seeded")

    # ── CCTV cameras ──────────────────────────────────────────────────────────
    await db.cctv_cameras.delete_many({})
    await db.cctv_cameras.insert_many(
        [
            {
                "camera_id": "CAM-A3-01",
                "property_id": "PROP-HSG-001",
                "floor": 3,
                "lat": 19.0731,
                "lng": 72.8802,
                "stream_url": None,
                "status": "active",
            },
            {
                "camera_id": "CAM-B2-01",
                "property_id": "PROP-HSG-001",
                "floor": 2,
                "lat": 19.0728,
                "lng": 72.8798,
                "stream_url": None,
                "status": "offline",
            },
        ]
    )
    print("  ✓  CCTV cameras seeded")

    # ── Integrations / settings / users / protocols ──────────────────────────
    await db.integrations.delete_many({})
    await db.integrations.insert_many(
        [
            {
                "integration_id": "int-whatsapp",
                "name": "WhatsApp Business",
                "category": "communication",
                "description": "Guest and resident outbound messaging",
                "logo_url": None,
                "status": "connected",
                "auto_sync": True,
                "api_status": {
                    "latency_ms": 118,
                    "last_synced_at": datetime.now(UTC).isoformat(),
                    "sync_schedule": "real_time_webhook",
                    "sync_interval_seconds": None,
                },
                "metadata": {"provider": "Meta", "region": "ap-south-1"},
            },
            {
                "integration_id": "int-locks",
                "name": "Smart Lock Controller",
                "category": "physical_security",
                "description": "Emergency unlock orchestration",
                "logo_url": None,
                "status": "disconnected",
                "auto_sync": False,
                "api_status": {
                    "latency_ms": 0,
                    "last_synced_at": datetime.now(UTC).isoformat(),
                    "sync_schedule": "manual",
                    "sync_interval_seconds": None,
                },
                "metadata": {"controller": "v2"},
            },
        ]
    )

    await db.settings.delete_many({})
    await db.settings.insert_one(
        {
            "key": "general",
            "settings": {
                "auto_dispatch_enabled": True,
                "default_language": "en",
                "guest_tracking_opt_in": True,
                "drill_frequency_days": 7,
                "panic_mode_silent_default": True,
            },
        }
    )

    await db.user_roles.delete_many({})
    await db.user_roles.insert_many(
        [
            {
                "user_id": "USR-ADM-001",
                "name": "Anita Desai",
                "email": "anita@example.com",
                "role": "property_admin",
                "last_login_at": datetime.now(UTC).isoformat(),
                "active": True,
            },
            {
                "user_id": "USR-MGR-001",
                "name": "Karan Joshi",
                "email": "karan@example.com",
                "role": "manager",
                "last_login_at": datetime.now(UTC).isoformat(),
                "active": True,
            },
        ]
    )

    await db.protocols.delete_many({})
    await db.protocols.insert_many(
        [
            {
                "protocol_id": "PROT-FIRE-01",
                "name": "Fire Evacuation SOP",
                "incident_type": "fire",
                "steps_count": 12,
                "last_updated_at": datetime.now(UTC).isoformat(),
                "active": True,
            },
            {
                "protocol_id": "PROT-MED-01",
                "name": "Medical First Response SOP",
                "incident_type": "medical",
                "steps_count": 9,
                "last_updated_at": datetime.now(UTC).isoformat(),
                "active": True,
            },
        ]
    )
    print("  ✓  Integrations, settings, users, and protocols seeded")

    client.close()
    print("\n✅  Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed())
