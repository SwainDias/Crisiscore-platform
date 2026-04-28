# Crisiscore Platform

> **IoT-enabled crisis management platform for housing societies.**  
> One-tap SOS alerts · Role-based incident response · Live maps · Micro-training drills · Post-incident analytics

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Backend (Docker — recommended)](#backend-docker--recommended)
   - [Backend (local)](#backend-local)
   - [Frontend (Flutter)](#frontend-flutter)
7. [Environment Variables](#environment-variables)
8. [API Reference](#api-reference)
9. [User Roles](#user-roles)
10. [Database Collections](#database-collections)
11. [Running Tests](#running-tests)
12. [Contributing](#contributing)

---

## Overview

Crisiscore is a full-stack emergency-response platform designed for residential and hospitality properties (apartment complexes, hotels, gated communities). It connects guests, on-site staff, first responders, and property administrators through a single unified system, enabling faster detection, coordinated response, and detailed post-incident reporting.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Flutter Mobile App                  │
│        (Guest · Staff · Responder · Admin)          │
└────────────────────┬────────────────────────────────┘
                     │ HTTPS / REST
┌────────────────────▼────────────────────────────────┐
│             FastAPI  (Python 3.11)                  │
│         /api/v1  —  JWT-authenticated               │
├──────────────────────────┬──────────────────────────┤
│      MongoDB (Motor)     │      Redis               │
│   primary data store     │  caching / pub-sub       │
└──────────────────────────┴──────────────────────────┘
```

---

## Features

| Feature | Description |
|---|---|
| **One-tap SOS** | Guests and staff trigger emergency alerts instantly from the app |
| **Role-based response** | Alerts are routed to the right people (Security, EMS, Warden, Admin) |
| **Live incident map** | Real-time pin-based map showing active incidents, responder locations, and CCTV feeds |
| **Guest accountability** | Check-in registry tracks evacuation, shelter-in-place, and injury status |
| **Micro-training drills** | Timed, scored drills for staff with configurable question sets |
| **Safety checks** | Scheduled duty-status and perimeter-check workflows for on-site staff |
| **SOP enforcement** | Step-by-step standard operating procedures attached to incident types |
| **Broadcast notifications** | Push, WhatsApp, and SMS broadcasts to guests by floor or room |
| **External services** | Coordinate fire department, police, and medical response |
| **Integrations** | Connect physical-security systems, PMS, communication tools, and sensors |
| **Post-incident analytics** | Admin dashboard with incident timelines, response metrics, and exportable reports |

---

## Tech Stack

### Backend
| Layer | Technology |
|---|---|
| API framework | [FastAPI](https://fastapi.tiangolo.com/) 0.111 |
| Runtime | Python 3.11 |
| Database | [MongoDB](https://www.mongodb.com/) via [Motor](https://motor.readthedocs.io/) (async) |
| Cache / Pub-Sub | [Redis](https://redis.io/) 7 |
| Auth | JWT (python-jose) + Argon2id password hashing (argon2-cffi) |
| Validation | [Pydantic v2](https://docs.pydantic.dev/latest/) |
| Linter | [Ruff](https://docs.astral.sh/ruff/) |
| Type-checker | [mypy](https://mypy.readthedocs.io/) (strict) |
| Tests | pytest + pytest-asyncio |
| Container | Docker + Docker Compose |

### Frontend
| Layer | Technology |
|---|---|
| Framework | [Flutter](https://flutter.dev/) (Dart SDK ^3.11.5) |
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
│   │   │   ├── admin/          # Admin-only endpoints
│   │   │   ├── guest/          # Guest endpoints
│   │   │   ├── responder/      # Responder endpoints
│   │   │   ├── shared/         # Endpoints shared by multiple roles
│   │   │   └── staff/          # Staff endpoints
│   │   ├── core/               # Config, security, constants, error handlers
│   │   ├── db/
│   │   │   ├── models/         # MongoDB document models
│   │   │   └── repositories/   # Data-access layer
│   │   ├── schemas/            # Pydantic request/response models
│   │   ├── services/           # Business logic
│   │   └── main.py             # App factory
│   ├── scripts/
│   │   └── seed_db.py          # Database seeding script
│   ├── tests/                  # Unit and integration tests
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   └── pyproject.toml
│
└── frontend/
    └── app/                    # Flutter mobile/web application
        ├── lib/
        │   ├── core/           # Router, theme, constants
        │   ├── features/       # Screen/feature modules
        │   │   ├── auth/
        │   │   ├── guest/
        │   │   ├── shared/
        │   │   └── staff/
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

# API will be available at http://localhost:8000
# Swagger UI:  http://localhost:8000/docs
# ReDoc:       http://localhost:8000/redoc
```

> **Note**: Swagger UI and ReDoc are only served when `APP_ENV != production`.

---

### Backend (local)

```bash
cd backend

# 1. Install dependencies
poetry install

# 2. Copy and configure environment variables
cp .env.example .env   # see Environment Variables section

# 3. Start MongoDB and Redis (Docker is easiest)
docker compose up mongodb redis -d

# 4. (Optional) Seed the database with sample data
poetry run python scripts/seed_db.py

# 5. Start the development server
poetry run uvicorn app.main:app --reload --port 8000
```

---

### Frontend (Flutter)

```bash
cd frontend/app

# 1. Install Flutter dependencies
flutter pub get

# 2. Run on a connected device or emulator
flutter run

# Build a web release
flutter build web
```

> **Google Maps**: Set your Google Maps API key in `android/app/src/main/AndroidManifest.xml` (Android) and `ios/Runner/AppDelegate.swift` (iOS) before running on a physical device.

---

## Environment Variables

Create a `.env` file inside `backend/` (or `.env.docker` for the Compose stack). All keys and their defaults:

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | `development` or `production` |
| `APP_VERSION` | `1.0.0` | Displayed in health check and API docs |
| `DEBUG` | `false` | Enable debug logging |
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGO_DB_NAME` | `rapid_response` | Database name |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `JWT_SECRET_KEY` | `CHANGE_ME` | **Must be changed in production** |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated CORS origins |
| `MAX_LOGIN_ATTEMPTS` | `5` | Failed logins before lockout |
| `ACCOUNT_LOCK_DURATION_MINUTES` | `15` | Lockout duration |
| `FEATURE_BIOMETRICS_ENABLED` | `true` | Enable biometric login |
| `FEATURE_MICRO_DRILL_ENABLED` | `true` | Enable micro-training drills |
| `FEATURE_LIVE_MAP_ENABLED` | `true` | Enable live map |
| `REPORT_EXPORT_BASE_URL` | `https://cdn.example.com/reports` | CDN base URL for report exports |
| `REPORT_EXPORT_EXPIRY_HOURS` | `24` | Signed URL expiry for reports |

---

## API Reference

All endpoints are versioned under `/api/v1`. Interactive documentation (Swagger UI) is available at `http://localhost:8000/docs` in non-production mode.

### Endpoint Groups

| Prefix | Role | Description |
|---|---|---|
| `GET /health` | Public | Health check — returns `{"status":"ok","version":"..."}` |
| `/api/v1/app-init` | Shared | Bootstrap data for app startup |
| `/api/v1/alert` | Shared | Shared SOS alert trigger |
| `/api/v1/guest/home` | Guest | Guest home screen data |
| `/api/v1/guest/checkin` | Guest | Guest check-in / emergency profile |
| `/api/v1/guest/alert` | Guest | Guest alert guides and triggers |
| `/api/v1/staff/auth/login` | Staff | Employee ID + PIN login, returns JWT pair |
| `/api/v1/staff/home` | Staff | Staff dashboard and task list |
| `/api/v1/staff/safety-check` | Staff | Duty-status and perimeter checks |
| `/api/v1/staff/incident` | Staff | Create and update incidents |
| `/api/v1/staff/drill` | Staff | Micro-training drill sessions |
| `/api/v1/responder/incident` | Responder | Accept assignments, update unit status, log actions |
| `/api/v1/admin/overview` | Admin | KPI dashboard and incident queue |
| `/api/v1/admin/map` | Admin | Live map — incident pins, responder locations, CCTV |
| `/api/v1/admin/incident` | Admin | Full incident lifecycle management |
| `/api/v1/admin/staff` | Admin | Staff directory, roles, and operational status |
| `/api/v1/admin/settings` | Admin | System settings, integrations, and danger-zone actions |

---

## User Roles

| Role | Description |
|---|---|
| **Guest** | Residents or visitors who can trigger SOS alerts, check in, and receive broadcast notifications |
| **Staff — Security** | On-site security guards; handle lockdowns and perimeter safety checks |
| **Staff — EMS** | On-site medical personnel; respond to medical incidents |
| **Staff — Warden** | Floor/area wardens; coordinate evacuations and shelter-in-place |
| **Staff — Admin** | Property staff administrators |
| **Responder** | Dispatched units (internal or external) who update status and log scene actions |
| **Admin — Property Admin** | Manages a single property's settings, staff, and incident data |
| **Admin — Super Admin** | Full platform access across all properties |
| **Admin — Manager** | Operational oversight without full admin privileges |

---

## Database Collections

MongoDB collections used by the platform:

| Collection | Description |
|---|---|
| `staff` | Staff accounts, roles, and biometric tokens |
| `guests` | Guest profiles and emergency information |
| `rooms` | Room/unit registry |
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
