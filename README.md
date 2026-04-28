# Crisiscore — Rapid Crisis Response Platform

> **Instantly detect, report, and synchronize emergency response across hospitality properties.**  
> Built for the *Rapid Crisis Response* hackathon challenge — eliminating fragmented communication between distressed guests, on-site staff, and emergency services.

---

## Table of Contents

1. [The Problem](#the-problem)
2. [Our Solution](#our-solution)
3. [Who Is This For?](#who-is-this-for)
4. [How It Works — User Journeys](#how-it-works--user-journeys)
5. [Key Features](#key-features)
6. [Architecture](#architecture)
7. [Tech Stack](#tech-stack)
8. [Project Structure](#project-structure)
9. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Backend (Docker — recommended)](#backend-docker--recommended)
   - [Backend (local)](#backend-local)
   - [Frontend (Flutter — mobile & web)](#frontend-flutter--mobile--web)
10. [Environment Variables](#environment-variables)
11. [API Reference](#api-reference)
12. [User Roles](#user-roles)
13. [Database Collections](#database-collections)
14. [Running Tests](#running-tests)
15. [Contributing](#contributing)

---

## The Problem

Hospitality venues — hotels, resorts, gated communities — face unpredictable, high-stakes emergencies (fires, medical crises, security threats, extreme weather). When disaster strikes:

- **Guests** are in unfamiliar surroundings, don't know who to call, and can't find the nearest exit.
- **Staff** receive fragmented information across radios, WhatsApp groups, and phone calls — no single source of truth.
- **Responders** (security, EMS, fire teams) arrive on scene without real-time situational awareness or accountability of who is where.
- **Property managers** have no live overview of the unfolding incident, making command decisions blindly.

The result: delayed response, miscommunication, and preventable harm.

---

## Our Solution

**Crisiscore** is a full-stack, real-time crisis coordination platform that unifies all four stakeholder groups on a single system. It replaces fragmented ad-hoc communication with a structured, role-specific, action-driven workflow — from the first SOS tap to the post-incident report.

| Without Crisiscore | With Crisiscore |
|---|---|
| Guests call the front desk or do nothing | One-tap SOS from a phone or browser triggers an immediate, geo-tagged alert |
| Staff coordinate over WhatsApp | Every responder receives a role-matched task with real-time status tracking |
| No-one knows who has evacuated | Accountability dashboard tracks each guest: Evacuated / Shelter-in-Place / Injured / Unknown |
| Managers get second-hand updates | Live incident map shows every responder, pin, CCTV feed, and status update in real time |
| Post-incident review is informal | Full timestamped timeline, SOP completion rate, and exportable analytics reports |

---

## Who Is This For?

| Stakeholder | Platform Surface | Core Need |
|---|---|---|
| **Hotel / Resort Guests** | Mobile app (iOS, Android) or web browser | Report an emergency in seconds; receive evacuation/shelter instructions |
| **On-site Staff** (Security, EMS, Wardens) | Mobile app | Receive task assignments, trigger incidents, run safety checks, complete drills |
| **Responders** (internal units or external services) | Mobile app | Accept dispatch, update unit status, log scene actions against an SOP checklist |
| **Property Administrators** | Web dashboard | Command-and-control view: live map, incident queue, staff directory, broadcast to all guests, post-incident analytics |

---

## How It Works — User Journeys

### 🔴 Crisis Starts — Guest SOS
```
Guest opens app / web → taps SOS button
  → selects incident type (Fire / Medical / Security / …)
  → geo-tagged alert pushed to FastAPI backend
  → alert fanned out to all relevant staff via Redis pub-sub
  → guest receives real-time safety instructions (Evacuate / Shelter-in-Place / Lockdown)
```

### 🟠 Staff Response
```
Staff member receives push notification with incident details
  → opens Active Incident screen
  → sees assigned SOP checklist (step-by-step actions)
  → marks steps complete; logs scene observations
  → silent panic button available for covert distress signals
```

### 🟡 Responder Coordination
```
Responder accepts dispatch assignment
  → updates unit status (Dispatched → En Route → On Scene)
  → logs actions against the live incident timeline
  → SOP step completion visible to all responders on the same incident
```

### 🟢 Admin Command View
```
Admin opens web dashboard
  → live map shows every incident pin, responder location, CCTV camera
  → incident queue with priority (P1 / P2 / P3) and live status
  → broadcasts targeted alerts to: all guests / affected floor / specific room
  → contacts external services (Fire Dept / Police / EMS) from the same interface
  → post-incident: full timeline, response times, SOP completion %, exportable report
```

---

## Key Features

| Feature | Description |
|---|---|
| **One-tap SOS** | Guests and staff trigger geo-tagged emergency alerts from mobile or web |
| **Role-based response routing** | Alerts auto-routed to the right responder type (Security, EMS, Warden) |
| **Live incident map** | Real-time pin map of active incidents, responder locations, and CCTV feeds |
| **Guest accountability tracker** | Check-in registry tracks each guest's status: Evacuated / Shelter-in-Place / Injured / Unknown |
| **SOP-driven response** | Step-by-step standard operating procedures enforce best-practice workflows |
| **Silent panic mode** | Staff can send a covert distress signal without alerting an aggressor |
| **Micro-training drills** | Timed, scored readiness drills keep staff prepared between incidents |
| **Safety checks** | Scheduled duty-status and perimeter-check workflows for on-site staff |
| **Multi-channel broadcasts** | Push notification, WhatsApp, and SMS broadcasts segmented by floor or room |
| **External service coordination** | Tracks dispatch status of fire department, police, and medical services |
| **Third-party integrations** | PMS, physical-security systems, sensors, and communication platforms |
| **Post-incident analytics** | Full incident timeline, response KPIs, and CDN-hosted exportable reports |

---

## Architecture

The platform is built as two independently deployable units: a **Flutter app** (runs on iOS, Android, and web browsers from a single codebase) and a **FastAPI backend** backed by MongoDB and Redis.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Frontend                                     │
│                                                                      │
│  ┌────────────────────┐          ┌─────────────────────────────┐     │
│  │   Mobile App       |          |                             |    
       (FLUTTER)        │          │        Web App              │     │
│  │  iOS  ·  Android   │          │      React +tailwind        │
│  └────────┬───────────┘          └──────────────┬──────────────┘    │
│           │                                     │                   |
│   ┌───────┴─────────────────────────────────────┴──────┐            │
│   │                                                    │            │
│   │  Guest App · Staff App · Responder · Admin Panel   │            │
│   │  Riverpod state · go_router · flutter_map          │            │
│   └───────────────────────────┬────────────────────────┘            │
└───────────────────────────────│─────────────────────────────────────┘
                                │  HTTPS / REST  (JWT Bearer token)
┌───────────────────────────────▼─────────────────────────────────────┐
│                     FastAPI  (Python 3.11)                          │
│                    /api/v1  ·  role-gated routes                    │
│                                                                      │
│   Guest ──▶ /guest/*       Staff ──▶ /staff/*                       │
│   Responder ──▶ /responder/*      Admin ──▶ /admin/*                │
├──────────────────────────────┬──────────────────────────────────────┤
│        MongoDB  (Motor)      │              Redis                   │
│     Primary data store       │   Session cache · SOS pub-sub        │
│     24 collections           │   Real-time broadcast channel        │
└──────────────────────────────┴──────────────────────────────────────┘
```

### Data flow for an SOS alert

```
Guest taps SOS
   │
   ▼
POST /api/v1/alert  ──▶  FastAPI validates + persists alert to MongoDB
                               │
                               ▼
                         Redis pub-sub channel (sos:broadcasts)
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
               Staff App           Admin Live Map
          (push notification)    (real-time pin update)
```

---

## Tech Stack

### Backend
| Layer | Technology |
|---|---|
| API framework | [FastAPI](https://fastapi.tiangolo.com/) 0.111 |
| Runtime | Python 3.11 |
| Database | [MongoDB](https://www.mongodb.com/) via [Motor](https://motor.readthedocs.io/) (async) |
| Cache / Pub-Sub | [Redis](https://redis.io/) 7 |
| Authentication | JWT (python-jose) + Argon2id password hashing (argon2-cffi) |
| Validation | [Pydantic v2](https://docs.pydantic.dev/latest/) |
| Linter | [Ruff](https://docs.astral.sh/ruff/) |
| Type-checker | [mypy](https://mypy.readthedocs.io/) (strict) |
| Tests | pytest + pytest-asyncio |
| Container | Docker + Docker Compose |

### Frontend
| Layer | Technology |
|---|---|
| Framework | [Flutter](https://flutter.dev/) (Dart SDK ^3.11.5) — builds iOS, Android, **and Web** from one codebase |
| State management | [Riverpod](https://riverpod.dev/) 3 |
| Navigation | [go_router](https://pub.dev/packages/go_router) 17 |
| Maps | google_maps_flutter · flutter_map · latlong2 |
| Fonts / animations | google_fonts · flutter_animate |
| Storage | shared_preferences |

---

## Project Structure

```
Crisiscore-platform/
├── backend/                    # FastAPI service
│   ├── app/
│   │   ├── api/v1/             # Route handlers, grouped by user role
│   │   │   ├── admin/          # Admin-only endpoints (overview, map, incident, staff, settings)
│   │   │   ├── guest/          # Guest endpoints (home, checkin, alert)
│   │   │   ├── responder/      # Responder endpoints (incident management)
│   │   │   ├── shared/         # Shared endpoints (app-init, SOS alert)
│   │   │   └── staff/          # Staff endpoints (auth, home, safety-check, incident, drill)
│   │   ├── core/               # Config, security (JWT + Argon2id), constants, error handlers
│   │   ├── db/
│   │   │   ├── models/         # MongoDB document models
│   │   │   └── repositories/   # Data-access layer (one repo per collection)
│   │   ├── schemas/            # Pydantic request/response models per role
│   │   ├── services/           # Business logic (one service per feature)
│   │   └── main.py             # App factory (CORS, lifespan, router mounting)
│   ├── scripts/
│   │   └── seed_db.py          # Database seeding with sample property data
│   ├── tests/                  # Unit and integration tests
│   ├── Dockerfile
│   ├── docker-compose.yaml     # MongoDB + Redis + API orchestration
│   └── pyproject.toml
│
└── frontend/
    └── app/                    # Flutter application (mobile + web)
        ├── lib/
        │   ├── core/
        │   │   ├── router/     # go_router config (staff + guest shell routes)
        │   │   ├── theme/      # App-wide theme and colours
        │   │   └── constants/  # Shared app constants
        │   ├── features/
        │   │   ├── auth/       # Splash, onboarding, staff login, guest check-in
        │   │   ├── staff/      # Home, map, alerts, guide, crisis trigger, drill, incident
        │   │   ├── guest/      # Home, alerts, guide, account, instructions
        │   │   └── shared/     # Components shared across roles
        │   ├── providers.dart  # Global Riverpod providers
        │   └── main.dart
        └── pubspec.yaml
```

---

## Getting Started

### Prerequisites

| Tool | Minimum version |
|---|---|
| Docker & Docker Compose | 24+ |
| Python | 3.11 |
| [Poetry](https://python-poetry.org/) | 1.8+ |
| Flutter SDK | 3.11.5 |
| Dart SDK | 3.11.5 |

---

### Backend (Docker — recommended)

```bash
cd backend

# 1. Create an environment file for the Docker containers
cp .env.docker.example .env.docker   # edit values as needed

# 2. Start MongoDB, Redis, and the API
docker compose up --build

# API will be available at:  http://localhost:8000
# Swagger UI (dev only):     http://localhost:8000/docs
# ReDoc (dev only):          http://localhost:8000/redoc
# Health check:              http://localhost:8000/health
```

> **Note**: Swagger UI and ReDoc are disabled when `APP_ENV=production`.

---

### Backend (local)

```bash
cd backend

# 1. Install dependencies
poetry install

# 2. Copy and configure environment variables
cp .env.example .env   # see Environment Variables section below

# 3. Start MongoDB and Redis via Docker
docker compose up mongodb redis -d

# 4. (Optional) Seed the database with sample data
poetry run python scripts/seed_db.py

# 5. Start the development server with hot-reload
poetry run uvicorn app.main:app --reload --port 8000
```

---

### Frontend (Flutter — mobile & web)

```bash
cd frontend/app

# Install dependencies
flutter pub get

# ── Mobile ────────────────────────────────────────────
# Run on a connected device or emulator
flutter run

# ── Web ───────────────────────────────────────────────
# Run in the browser (Chrome)
flutter run -d chrome

# Build a production web bundle
flutter build web
```

> **Google Maps API key**: add your key to `android/app/src/main/AndroidManifest.xml` (Android) and `ios/Runner/AppDelegate.swift` (iOS) before running on a physical device.

---

## Environment Variables

Create a `.env` file inside `backend/` (or `.env.docker` for the Compose stack).

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | `development` or `production` |
| `APP_VERSION` | `1.0.0` | Displayed in health check and API docs |
| `DEBUG` | `false` | Enable debug logging |
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGO_DB_NAME` | `rapid_response` | Database name |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `JWT_SECRET_KEY` | `CHANGE_ME` | ⚠️ **Must be changed in production** |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated CORS origins |
| `MAX_LOGIN_ATTEMPTS` | `5` | Failed logins before account lockout |
| `ACCOUNT_LOCK_DURATION_MINUTES` | `15` | Lockout duration |
| `FEATURE_BIOMETRICS_ENABLED` | `true` | Toggle biometric login |
| `FEATURE_MICRO_DRILL_ENABLED` | `true` | Toggle micro-training drills |
| `FEATURE_LIVE_MAP_ENABLED` | `true` | Toggle live incident map |
| `REPORT_EXPORT_BASE_URL` | `https://cdn.example.com/reports` | CDN base URL for report exports |
| `REPORT_EXPORT_EXPIRY_HOURS` | `24` | Signed URL expiry for exported reports |

---

## API Reference

All endpoints are versioned under `/api/v1`. Interactive Swagger UI is at `http://localhost:8000/docs` in development.

| Prefix | Caller Role | Description |
|---|---|---|
| `GET /health` | Public | Health check — `{"status":"ok","version":"..."}` |
| `/api/v1/app-init` | Shared | Bootstrap configuration for app startup |
| `/api/v1/alert` | Shared | SOS alert trigger (staff or guest) |
| `/api/v1/guest/home` | Guest | Home screen data and active alerts |
| `/api/v1/guest/checkin` | Guest | Guest check-in and emergency profile |
| `/api/v1/guest/alert` | Guest | Alert guides (Evacuate, Shelter, Lockdown, Medical) |
| `/api/v1/staff/auth/login` | Staff | Employee ID + PIN login → JWT access + refresh tokens |
| `/api/v1/staff/home` | Staff | Dashboard: tasks, active incidents, duty status |
| `/api/v1/staff/safety-check` | Staff | Duty-status and perimeter-check workflows |
| `/api/v1/staff/incident` | Staff | Create and manage incidents |
| `/api/v1/staff/drill` | Staff | Micro-training drill sessions and scoring |
| `/api/v1/responder/incident` | Responder | Accept assignments, update unit status, log SOP steps |
| `/api/v1/admin/overview` | Admin | KPI dashboard and prioritised incident queue |
| `/api/v1/admin/map` | Admin | Live map — incident pins, responder locations, CCTV |
| `/api/v1/admin/incident` | Admin | Full incident lifecycle + broadcast + external services |
| `/api/v1/admin/staff` | Admin | Staff directory, roles, and operational status |
| `/api/v1/admin/settings` | Admin | System settings, integrations, and danger-zone actions |

---

## User Roles

| Role | App Surface | Responsibilities |
|---|---|---|
| **Guest** | Mobile app · Web browser | Trigger SOS; receive evacuation / shelter-in-place instructions; view alert guides |
| **Staff — Security** | Mobile app | Respond to lockdown and security incidents; run perimeter safety checks |
| **Staff — EMS** | Mobile app | Respond to medical incidents; log patient observations |
| **Staff — Warden** | Mobile app | Coordinate floor evacuations; track guest accountability |
| **Staff — Admin** | Mobile app | Manage staff scheduling and on-site operations |
| **Responder** | Mobile app | Accept dispatches; update unit status (En Route → On Scene); complete SOP checklists |
| **Admin — Property Admin** | Web dashboard | Full incident management for one property; staff admin; reports |
| **Admin — Super Admin** | Web dashboard | Cross-property platform access |
| **Admin — Manager** | Web dashboard | Operational oversight without full admin privileges |

---

## Database Collections

| Collection | Description |
|---|---|
| `staff` | Staff accounts, roles, and biometric tokens |
| `guests` | Guest profiles and emergency information |
| `rooms` | Room / unit registry |
| `properties` | Property configuration |
| `incidents` | Active and historical incidents |
| `incident_logs` | Timestamped incident timeline entries |
| `alerts` | Triggered SOS alerts |
| `alert_types` | Configurable alert type definitions |
| `tasks` | Response tasks assigned to staff |
| `drills` | Drill configurations |
| `drill_sessions` | Completed staff drill attempts and scores |
| `drill_questions` | Question bank for drills |
| `safety_checks` | Safety check records |
| `guest_checkins` | Guest check-in and accountability records |
| `action_items` | SOP action items linked to incidents |
| `responder_assignments` | Responder dispatch records |
| `broadcasts` | Sent broadcast messages |
| `integrations` | External system integrations (PMS, CCTV, sensors) |
| `settings` | Per-property system settings |
| `protocols` / `sop_protocols` | Standard operating procedure templates |
| `cctv_cameras` | CCTV camera registry |
| `refresh_tokens` | Active JWT refresh tokens |
| `admin_users` | Admin-portal user accounts |

---

## Running Tests

```bash
cd backend

# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=app --cov-report=term-missing

# Lint
poetry run ruff check .

# Type-check
poetry run mypy app
```

---

## Contributing

1. Fork the repository and create a feature branch from `main`.
2. Follow the existing code style — `ruff` for linting, `mypy --strict` for types.
3. Add or update tests for any logic changes.
4. Open a pull request with a clear description of the changes.
