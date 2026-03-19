# UC-001-ACCOUNT-RECORD-SUBMISSION

## Intent
Allow users to submit an account record and receive a generated `AntragsNr`, then view all submitted records in a simple HTML list.

## Actors

Primary  
User

Secondary  
FinBotAction system

## Preconditions

- REST API is available.
- Storage is available.

## Flow

1. User sends a `POST` request with:
   - `KassierDate`
   - `KassierName`
   - `PraesidiumDate`
   - `PraesidiumName`
   - `VereinEmail`
2. System stores the submitted record.
3. System returns:
   - `AntragsNr`
4. User opens the HTML page.
5. System shows a simple list of all submitted records.

## Errors

- Input does not contain the required fields.

## Acceptance

Given  
the user submits:
```json
{
  "KassierDate": "20.05.1980",
  "KassierName": "Monika Meier",
  "PraesidiumDate": "15.02.1980",
  "PraesidiumName": "Hans Muster",
  "VereinEmail": "info@shindokan.ch"
}
```
When  
the system accepts the `POST` request  
Then  
the system stores the record and returns:
```json
{
  "AntragsNr": "a0ba8e16ef8f"
}
```

Given  
records were submitted  
When  
the user opens the HTML page  
Then  
the system shows a simple list containing all submitted records.

## Tests

Unit  
record creation returns a generated `AntragsNr`

Integration  
`POST` stores the record and returns `AntragsNr`

E2E  
submit a record, then verify the HTML page lists submitted records
