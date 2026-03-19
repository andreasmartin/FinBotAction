# PROJECT.md

## Purpose

FinBotAction is a FastAPI application evolved from the existing BAIssue codebase.
Its current scope is to store account records through a POST API, return a created ID,
and provide a simple HTML page listing all stored entries.

---

## Architecture

Clean Architecture:
domain ← application ← interfaces ← infrastructure

Current baseline keeps the existing layered FastAPI + SQLAlchemy structure and will be
iteratively adapted use-case by use-case.

UC-001 minimal component design:

- Domain
  - `AccountRecord` entity with:
    - `KassierDate`
    - `KassierName`
    - `PraesidiumDate`
    - `PraesidiumName`
    - `VereinEmail`
    - generated `AntragsNr`
- Application
  - `AccountRecordService` use case:
    - create and store account record
    - return generated `AntragsNr`
    - list stored account records
- Interfaces
  - REST endpoint for `POST` account record submission
  - HTML endpoint/page to render a simple list of stored records
- Infrastructure
  - persistence model + repository adapter for account records
  - FastAPI wiring for API and HTML routes

---

## Structure

`src/app/domain`  
`src/app/application`  
`src/app/interfaces`  
`src/app/infrastructure`

`tests/unit`  
`tests/integration`  
`tests/e2e`

---

## Commands

Install

`pip install -r requirements.txt`

Test

`pytest -q`

Start

`PYTHONPATH=$PWD/src uvicorn app.main:app --reload`

---

## Dependencies

Declared in:

`requirements.txt`
