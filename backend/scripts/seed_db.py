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

    client.close()
    print("\n✅  Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed())
