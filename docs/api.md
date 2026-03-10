---
title: Player and Run Tracker API v1.0.0
language_tabs:
  - shell: Shell
  - python: Python
language_clients:
  - shell: ""
  - python: ""
toc_footers: []
includes: []
search: false
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="player-and-run-tracker-api">Player and Run Tracker API v1.0.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

An API for tracking player data and game runs.

# Authentication

- HTTP Authentication, scheme: basic 

<h1 id="player-and-run-tracker-api-default">Default</h1>

## Check Name

<a id="opIdcheck_name_players_check_name_post"></a>

> Code samples

```shell
# You can also use wget
curl -X POST /players/check-name \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/players/check-name', headers = headers)

print(r.json())

```

`POST /players/check-name`

Checks if a player name is already taken. This is useful for
real-time validation in the user interface.

> Body parameter

```json
{
  "player_name": "string"
}
```

<h3 id="check-name-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[NameCheckRequest](#schemanamecheckrequest)|true|none|

> Example responses

> 200 Response

```json
{
  "exists": true,
  "message": "string"
}
```

<h3 id="check-name-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[NameCheckResponse](#schemanamecheckresponse)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Generate Name

<a id="opIdgenerate_name_players_generate_name_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /players/generate-name \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/players/generate-name', headers = headers)

print(r.json())

```

`GET /players/generate-name`

Generates a unique, random player name that is not already in use.

> Example responses

> 200 Response

```json
{
  "player_name": "string"
}
```

<h3 id="generate-name-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[GenerateNameResponse](#schemageneratenameresponse)|

<aside class="success">
This operation does not require authentication
</aside>

## Start Run

<a id="opIdstart_run_runs_start_post"></a>

> Code samples

```shell
# You can also use wget
curl -X POST /runs/start \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/runs/start', headers = headers)

print(r.json())

```

`POST /runs/start`

Starts a new game run. This endpoint handles both new and existing players.
If `create_new_player` is true, a new player is created. Otherwise,
the existing player is authenticated.

> Body parameter

```json
{
  "player_name": "string",
  "password": "string",
  "map_id": "string",
  "create_new_player": false
}
```

<h3 id="start-run-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[RunStart](#schemarunstart)|true|none|

> Example responses

> 200 Response

```json
{
  "player_id": 0,
  "run_id": 0
}
```

<h3 id="start-run-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[RunStartResponse](#schemarunstartresponse)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Get Players

<a id="opIdget_players_players_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /players \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/players', headers = headers)

print(r.json())

```

`GET /players`

Retrieves a list of all players with pagination.

<h3 id="get-players-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|skip|query|integer|false|none|
|limit|query|integer|false|none|

> Example responses

> 200 Response

```json
[
  {
    "name": "string",
    "id": 0,
    "created_at": "2019-08-24T14:15:22Z"
  }
]
```

<h3 id="get-players-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-players-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Players Players Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Players Players Get|[[Player](#schemaplayer)]|false|none|[Schema for representing a player, including their ID and creation date.]|
|» Player|[Player](#schemaplayer)|false|none|Schema for representing a player, including their ID and creation date.|
|»» name|string|true|none|none|
|»» id|integer|true|none|none|
|»» created_at|string(date-time)|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Create Player

<a id="opIdcreate_player_players_post"></a>

> Code samples

```shell
# You can also use wget
curl -X POST /players \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/players', headers = headers)

print(r.json())

```

`POST /players`

Creates a new player with a randomly generated password.
Returns the new player's details, including the password.

> Body parameter

```json
{
  "name": "string"
}
```

<h3 id="create-player-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[PlayerCreate](#schemaplayercreate)|true|none|

> Example responses

> 201 Response

```json
{
  "name": "string",
  "id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "password": "string"
}
```

<h3 id="create-player-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Successful Response|[PlayerCreateResponse](#schemaplayercreateresponse)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Read Player

<a id="opIdread_player_players__player_id__get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /players/{player_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/players/{player_id}', headers = headers)

print(r.json())

```

`GET /players/{player_id}`

Retrieves a single player by their ID.

<h3 id="read-player-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|player_id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "name": "string",
  "id": 0,
  "created_at": "2019-08-24T14:15:22Z"
}
```

<h3 id="read-player-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Player](#schemaplayer)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Delete Player

<a id="opIddelete_player_players__player_id__delete"></a>

> Code samples

```shell
# You can also use wget
curl -X DELETE /players/{player_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.delete('/players/{player_id}', headers = headers)

print(r.json())

```

`DELETE /players/{player_id}`

Deletes a player and all of their associated data.

<h3 id="delete-player-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|player_id|path|integer|true|none|

> Example responses

> 422 Response

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

<h3 id="delete-player-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|Successful Response|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Get Runs

<a id="opIdget_runs_runs_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /runs \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/runs', headers = headers)

print(r.json())

```

`GET /runs`

Retrieves a list of all runs with pagination.

<h3 id="get-runs-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|skip|query|integer|false|none|
|limit|query|integer|false|none|

> Example responses

> 200 Response

```json
[
  {
    "player_id": 0,
    "map_id": "string",
    "id": 0,
    "player": {
      "name": "string",
      "id": 0,
      "created_at": "2019-08-24T14:15:22Z"
    },
    "started_at": "2019-08-24T14:15:22Z",
    "status": "in_progress",
    "duration_seconds": 0,
    "level": 0,
    "xp": 0,
    "kills_total": 0,
    "upgrades": {
      "property1": 0,
      "property2": 0
    },
    "ended_at": "2019-08-24T14:15:22Z",
    "cause_of_death": "string"
  }
]
```

<h3 id="get-runs-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-runs-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Runs Runs Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Runs Runs Get|[[Run](#schemarun)]|false|none|[Schema for representing a run, including all its details.]|
|» Run|[Run](#schemarun)|false|none|Schema for representing a run, including all its details.|
|»» player_id|integer|true|none|none|
|»» map_id|string|true|none|none|
|»» id|integer|true|none|none|
|»» player|[Player](#schemaplayer)|true|none|Schema for representing a player, including their ID and creation date.|
|»»» name|string|true|none|none|
|»»» id|integer|true|none|none|
|»»» created_at|string(date-time)|true|none|none|
|»» started_at|string(date-time)|true|none|none|
|»» status|[RunStatus](#schemarunstatus)|true|none|An enumeration for the possible statuses of a run.|
|»» duration_seconds|integer|true|none|none|
|»» level|integer|true|none|none|
|»» xp|integer|true|none|none|
|»» kills_total|integer|true|none|none|
|»» upgrades|any|false|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|object|false|none|none|
|»»»» **additionalProperties**|integer|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» ended_at|any|true|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|string(date-time)|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» cause_of_death|any|true|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|string|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|status|in_progress|
|status|died|
|status|completed|

<aside class="success">
This operation does not require authentication
</aside>

## Get Run

<a id="opIdget_run_runs__run_id__get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /runs/{run_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/runs/{run_id}', headers = headers)

print(r.json())

```

`GET /runs/{run_id}`

Retrieves a single run by its ID.

<h3 id="get-run-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "player_id": 0,
  "map_id": "string",
  "id": 0,
  "player": {
    "name": "string",
    "id": 0,
    "created_at": "2019-08-24T14:15:22Z"
  },
  "started_at": "2019-08-24T14:15:22Z",
  "status": "in_progress",
  "duration_seconds": 0,
  "level": 0,
  "xp": 0,
  "kills_total": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}
```

<h3 id="get-run-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Run](#schemarun)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Update Run

<a id="opIdupdate_run_runs__run_id__patch"></a>

> Code samples

```shell
# You can also use wget
curl -X PATCH /runs/{run_id} \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.patch('/runs/{run_id}', headers = headers)

print(r.json())

```

`PATCH /runs/{run_id}`

Updates the details of a specific run, such as duration, kills, and status.
This is the primary endpoint for updating a run's progress.

> Body parameter

```json
{
  "duration_seconds": 0,
  "kills_total": 0,
  "level": 0,
  "xp": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "status": "in_progress",
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}
```

<h3 id="update-run-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|
|body|body|[RunUpdate](#schemarunupdate)|true|none|

> Example responses

> 200 Response

```json
{
  "player_id": 0,
  "map_id": "string",
  "id": 0,
  "player": {
    "name": "string",
    "id": 0,
    "created_at": "2019-08-24T14:15:22Z"
  },
  "started_at": "2019-08-24T14:15:22Z",
  "status": "in_progress",
  "duration_seconds": 0,
  "level": 0,
  "xp": 0,
  "kills_total": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}
```

<h3 id="update-run-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Run](#schemarun)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Delete Run

<a id="opIddelete_run_runs__run_id__delete"></a>

> Code samples

```shell
# You can also use wget
curl -X DELETE /runs/{run_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.delete('/runs/{run_id}', headers = headers)

print(r.json())

```

`DELETE /runs/{run_id}`

Deletes a single run and its associated events.

<h3 id="delete-run-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete-run-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete-run-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Create Run Event

<a id="opIdcreate_run_event_runs__run_id__events_post"></a>

> Code samples

```shell
# You can also use wget
curl -X POST /runs/{run_id}/events \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/runs/{run_id}/events', headers = headers)

print(r.json())

```

`POST /runs/{run_id}/events`

Creates a new event associated with a specific run.

> Body parameter

```json
{
  "event_type": "string",
  "value": "string"
}
```

<h3 id="create-run-event-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|
|body|body|[RunEventCreate](#schemaruneventcreate)|true|none|

> Example responses

> 200 Response

```json
{
  "event_type": "string",
  "value": "string",
  "id": 0,
  "run_id": 0,
  "timestamp": "2019-08-24T14:15:22Z"
}
```

<h3 id="create-run-event-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[RunEvent](#schemarunevent)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Get Run Events

<a id="opIdget_run_events_runs__run_id__events_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /runs/{run_id}/events \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/runs/{run_id}/events', headers = headers)

print(r.json())

```

`GET /runs/{run_id}/events`

Retrieves all events for a specific run.

<h3 id="get-run-events-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|

> Example responses

> 200 Response

```json
[
  {
    "event_type": "string",
    "value": "string",
    "id": 0,
    "run_id": 0,
    "timestamp": "2019-08-24T14:15:22Z"
  }
]
```

<h3 id="get-run-events-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-run-events-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Run Events Runs  Run Id  Events Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Run Events Runs  Run Id  Events Get|[[RunEvent](#schemarunevent)]|false|none|[Schema for representing a run event, including its ID and timestamp.]|
|» RunEvent|[RunEvent](#schemarunevent)|false|none|Schema for representing a run event, including its ID and timestamp.|
|»» event_type|string|true|none|none|
|»» value|any|false|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|string|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» id|integer|true|none|none|
|»» run_id|integer|true|none|none|
|»» timestamp|string(date-time)|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Get Leaderboard

<a id="opIdget_leaderboard_analytics_leaderboard_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /analytics/leaderboard \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/analytics/leaderboard', headers = headers)

print(r.json())

```

`GET /analytics/leaderboard`

Retrieves the top 10 runs for the leaderboard, sorted by duration.

> Example responses

> 200 Response

```json
[
  {
    "player_id": 0,
    "run_id": 0,
    "player_name": "string",
    "duration_seconds": 0,
    "total_kills": 0
  }
]
```

<h3 id="get-leaderboard-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get-leaderboard-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Leaderboard Analytics Leaderboard Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Leaderboard Analytics Leaderboard Get|[[RunLeaderboard](#schemarunleaderboard)]|false|none|[Schema for a single entry in the leaderboard.]|
|» RunLeaderboard|[RunLeaderboard](#schemarunleaderboard)|false|none|Schema for a single entry in the leaderboard.|
|»» player_id|integer|true|none|none|
|»» run_id|integer|true|none|none|
|»» player_name|string|true|none|none|
|»» duration_seconds|integer|true|none|none|
|»» total_kills|integer|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Get Players Summary

<a id="opIdget_players_summary_analytics_players_summary_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /analytics/players-summary \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/analytics/players-summary', headers = headers)

print(r.json())

```

`GET /analytics/players-summary`

Provides a summary of all players, including their total number of runs
and best run time. Can be filtered by a search term.

<h3 id="get-players-summary-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|search|query|any|false|none|

> Example responses

> 200 Response

```json
[
  {
    "name": "string",
    "id": 0,
    "created_at": "2019-08-24T14:15:22Z",
    "total_runs": 0,
    "best_run_time": 0
  }
]
```

<h3 id="get-players-summary-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-players-summary-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Players Summary Analytics Players Summary Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Players Summary Analytics Players Summary Get|[[PlayerSummary](#schemaplayersummary)]|false|none|[Schema for a player summary, which includes their total number of runs<br>and their best run time.]|
|» PlayerSummary|[PlayerSummary](#schemaplayersummary)|false|none|Schema for a player summary, which includes their total number of runs<br>and their best run time.|
|»» name|string|true|none|none|
|»» id|integer|true|none|none|
|»» created_at|string(date-time)|true|none|none|
|»» total_runs|integer|true|none|none|
|»» best_run_time|any|false|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|integer|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## View Player Stats

<a id="opIdview_player_stats_analytics_view_player_stats__player_id__get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /analytics/view_player_stats/{player_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/analytics/view_player_stats/{player_id}', headers = headers)

print(r.json())

```

`GET /analytics/view_player_stats/{player_id}`

Retrieves detailed statistics for a single player, such as total runs,
average survival time, and total kills.

<h3 id="view-player-stats-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|player_id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "player_name": "string",
  "number_of_runs": 0,
  "total_time_played": 0,
  "average_time_survived": 0,
  "longest_run": 0,
  "favourite_upgrade": "string",
  "total_monsters_slain": 0
}
```

<h3 id="view-player-stats-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[PlayerStats](#schemaplayerstats)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Get Player Runs

<a id="opIdget_player_runs_players__player_id__runs_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /players/{player_id}/runs \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/players/{player_id}/runs', headers = headers)

print(r.json())

```

`GET /players/{player_id}/runs`

Retrieves all runs for a specific player.

<h3 id="get-player-runs-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|player_id|path|integer|true|none|

> Example responses

> 200 Response

```json
[
  {
    "player_id": 0,
    "map_id": "string",
    "id": 0,
    "player": {
      "name": "string",
      "id": 0,
      "created_at": "2019-08-24T14:15:22Z"
    },
    "started_at": "2019-08-24T14:15:22Z",
    "status": "in_progress",
    "duration_seconds": 0,
    "level": 0,
    "xp": 0,
    "kills_total": 0,
    "upgrades": {
      "property1": 0,
      "property2": 0
    },
    "ended_at": "2019-08-24T14:15:22Z",
    "cause_of_death": "string"
  }
]
```

<h3 id="get-player-runs-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-player-runs-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Player Runs Players  Player Id  Runs Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Player Runs Players  Player Id  Runs Get|[[Run](#schemarun)]|false|none|[Schema for representing a run, including all its details.]|
|» Run|[Run](#schemarun)|false|none|Schema for representing a run, including all its details.|
|»» player_id|integer|true|none|none|
|»» map_id|string|true|none|none|
|»» id|integer|true|none|none|
|»» player|[Player](#schemaplayer)|true|none|Schema for representing a player, including their ID and creation date.|
|»»» name|string|true|none|none|
|»»» id|integer|true|none|none|
|»»» created_at|string(date-time)|true|none|none|
|»» started_at|string(date-time)|true|none|none|
|»» status|[RunStatus](#schemarunstatus)|true|none|An enumeration for the possible statuses of a run.|
|»» duration_seconds|integer|true|none|none|
|»» level|integer|true|none|none|
|»» xp|integer|true|none|none|
|»» kills_total|integer|true|none|none|
|»» upgrades|any|false|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|object|false|none|none|
|»»»» **additionalProperties**|integer|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» ended_at|any|true|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|string(date-time)|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» cause_of_death|any|true|none|none|

*anyOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|string|false|none|none|

*or*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|null|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|status|in_progress|
|status|died|
|status|completed|

<aside class="success">
This operation does not require authentication
</aside>

## Admin Login

<a id="opIdadmin_login_admin_login_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /admin/login \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/admin/login', headers = headers)

print(r.json())

```

`GET /admin/login`

Verifies admin credentials. This endpoint is protected and requires
Basic Authentication.

> Example responses

> 200 Response

```json
null
```

<h3 id="admin-login-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="admin-login-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
HTTPBasic
</aside>

## Admin Update Player Name

<a id="opIdadmin_update_player_name_admin_players__player_id__patch"></a>

> Code samples

```shell
# You can also use wget
curl -X PATCH /admin/players/{player_id} \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.patch('/admin/players/{player_id}', headers = headers)

print(r.json())

```

`PATCH /admin/players/{player_id}`

Admin-only endpoint to update a player's name.

> Body parameter

```json
{
  "name": "string"
}
```

<h3 id="admin-update-player-name-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|player_id|path|integer|true|none|
|body|body|[PlayerNameUpdate](#schemaplayernameupdate)|true|none|

> Example responses

> 200 Response

```json
{
  "name": "string",
  "id": 0,
  "created_at": "2019-08-24T14:15:22Z"
}
```

<h3 id="admin-update-player-name-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Player](#schemaplayer)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
HTTPBasic
</aside>

## Admin Delete Player

<a id="opIdadmin_delete_player_admin_players__player_id__delete"></a>

> Code samples

```shell
# You can also use wget
curl -X DELETE /admin/players/{player_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.delete('/admin/players/{player_id}', headers = headers)

print(r.json())

```

`DELETE /admin/players/{player_id}`

Admin-only endpoint to delete a player and all their associated runs.

<h3 id="admin-delete-player-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|player_id|path|integer|true|none|

> Example responses

> 422 Response

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

<h3 id="admin-delete-player-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|Successful Response|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
HTTPBasic
</aside>

## Admin Delete Run

<a id="opIdadmin_delete_run_admin_runs__run_id__delete"></a>

> Code samples

```shell
# You can also use wget
curl -X DELETE /admin/runs/{run_id} \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.delete('/admin/runs/{run_id}', headers = headers)

print(r.json())

```

`DELETE /admin/runs/{run_id}`

Admin-only endpoint to delete a specific run.

<h3 id="admin-delete-run-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|

> Example responses

> 422 Response

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

<h3 id="admin-delete-run-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|Successful Response|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
HTTPBasic
</aside>

## Update Run From Game

<a id="opIdupdate_run_from_game_runs__run_id__update_patch"></a>

> Code samples

```shell
# You can also use wget
curl -X PATCH /runs/{run_id}/update \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.patch('/runs/{run_id}/update', headers = headers)

print(r.json())

```

`PATCH /runs/{run_id}/update`

> Body parameter

```json
{
  "duration_seconds": 0,
  "kills_total": 0,
  "level": 0,
  "xp": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "status": "in_progress",
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}
```

<h3 id="update-run-from-game-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|run_id|path|integer|true|none|
|body|body|[RunUpdate](#schemarunupdate)|true|none|

> Example responses

> 200 Response

```json
{
  "player_id": 0,
  "map_id": "string",
  "id": 0,
  "player": {
    "name": "string",
    "id": 0,
    "created_at": "2019-08-24T14:15:22Z"
  },
  "started_at": "2019-08-24T14:15:22Z",
  "status": "in_progress",
  "duration_seconds": 0,
  "level": 0,
  "xp": 0,
  "kills_total": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}
```

<h3 id="update-run-from-game-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Run](#schemarun)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Test Endpoint One

<a id="opIdtest_endpoint_one_test1_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /test1 \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/test1', headers = headers)

print(r.json())

```

`GET /test1`

> Example responses

> 200 Response

```json
null
```

<h3 id="test-endpoint-one-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="test-endpoint-one-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Test Endpoint Two

<a id="opIdtest_endpoint_two_test2_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /test2 \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/test2', headers = headers)

print(r.json())

```

`GET /test2`

> Example responses

> 200 Response

```json
null
```

<h3 id="test-endpoint-two-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="test-endpoint-two-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## Test Endpoint Three

<a id="opIdtest_endpoint_three_test3_get"></a>

> Code samples

```shell
# You can also use wget
curl -X GET /test3 \
  -H 'Accept: application/json'

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/test3', headers = headers)

print(r.json())

```

`GET /test3`

> Example responses

> 200 Response

```json
null
```

<h3 id="test-endpoint-three-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="test-endpoint-three-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_GenerateNameResponse">GenerateNameResponse</h2>
<!-- backwards compatibility -->
<a id="schemageneratenameresponse"></a>
<a id="schema_GenerateNameResponse"></a>
<a id="tocSgeneratenameresponse"></a>
<a id="tocsgeneratenameresponse"></a>

```json
{
  "player_name": "string"
}

```

GenerateNameResponse

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_name|string|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_NameCheckRequest">NameCheckRequest</h2>
<!-- backwards compatibility -->
<a id="schemanamecheckrequest"></a>
<a id="schema_NameCheckRequest"></a>
<a id="tocSnamecheckrequest"></a>
<a id="tocsnamecheckrequest"></a>

```json
{
  "player_name": "string"
}

```

NameCheckRequest

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_name|string|true|none|none|

<h2 id="tocS_NameCheckResponse">NameCheckResponse</h2>
<!-- backwards compatibility -->
<a id="schemanamecheckresponse"></a>
<a id="schema_NameCheckResponse"></a>
<a id="tocSnamecheckresponse"></a>
<a id="tocsnamecheckresponse"></a>

```json
{
  "exists": true,
  "message": "string"
}

```

NameCheckResponse

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|exists|boolean|true|none|none|
|message|string|true|none|none|

<h2 id="tocS_Player">Player</h2>
<!-- backwards compatibility -->
<a id="schemaplayer"></a>
<a id="schema_Player"></a>
<a id="tocSplayer"></a>
<a id="tocsplayer"></a>

```json
{
  "name": "string",
  "id": 0,
  "created_at": "2019-08-24T14:15:22Z"
}

```

Player

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|id|integer|true|none|none|
|created_at|string(date-time)|true|none|none|

<h2 id="tocS_PlayerCreate">PlayerCreate</h2>
<!-- backwards compatibility -->
<a id="schemaplayercreate"></a>
<a id="schema_PlayerCreate"></a>
<a id="tocSplayercreate"></a>
<a id="tocsplayercreate"></a>

```json
{
  "name": "string"
}

```

PlayerCreate

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|

<h2 id="tocS_PlayerCreateResponse">PlayerCreateResponse</h2>
<!-- backwards compatibility -->
<a id="schemaplayercreateresponse"></a>
<a id="schema_PlayerCreateResponse"></a>
<a id="tocSplayercreateresponse"></a>
<a id="tocsplayercreateresponse"></a>

```json
{
  "name": "string",
  "id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "password": "string"
}

```

PlayerCreateResponse

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|id|integer|true|none|none|
|created_at|string(date-time)|true|none|none|
|password|string|true|none|none|

<h2 id="tocS_PlayerNameUpdate">PlayerNameUpdate</h2>
<!-- backwards compatibility -->
<a id="schemaplayernameupdate"></a>
<a id="schema_PlayerNameUpdate"></a>
<a id="tocSplayernameupdate"></a>
<a id="tocsplayernameupdate"></a>

```json
{
  "name": "string"
}

```

PlayerNameUpdate

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|

<h2 id="tocS_PlayerStats">PlayerStats</h2>
<!-- backwards compatibility -->
<a id="schemaplayerstats"></a>
<a id="schema_PlayerStats"></a>
<a id="tocSplayerstats"></a>
<a id="tocsplayerstats"></a>

```json
{
  "player_name": "string",
  "number_of_runs": 0,
  "total_time_played": 0,
  "average_time_survived": 0,
  "longest_run": 0,
  "favourite_upgrade": "string",
  "total_monsters_slain": 0
}

```

PlayerStats

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_name|string|true|none|none|
|number_of_runs|integer|true|none|none|
|total_time_played|integer|true|none|none|
|average_time_survived|number|true|none|none|
|longest_run|integer|true|none|none|
|favourite_upgrade|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|total_monsters_slain|integer|true|none|none|

<h2 id="tocS_PlayerSummary">PlayerSummary</h2>
<!-- backwards compatibility -->
<a id="schemaplayersummary"></a>
<a id="schema_PlayerSummary"></a>
<a id="tocSplayersummary"></a>
<a id="tocsplayersummary"></a>

```json
{
  "name": "string",
  "id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "total_runs": 0,
  "best_run_time": 0
}

```

PlayerSummary

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|id|integer|true|none|none|
|created_at|string(date-time)|true|none|none|
|total_runs|integer|true|none|none|
|best_run_time|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

<h2 id="tocS_Run">Run</h2>
<!-- backwards compatibility -->
<a id="schemarun"></a>
<a id="schema_Run"></a>
<a id="tocSrun"></a>
<a id="tocsrun"></a>

```json
{
  "player_id": 0,
  "map_id": "string",
  "id": 0,
  "player": {
    "name": "string",
    "id": 0,
    "created_at": "2019-08-24T14:15:22Z"
  },
  "started_at": "2019-08-24T14:15:22Z",
  "status": "in_progress",
  "duration_seconds": 0,
  "level": 0,
  "xp": 0,
  "kills_total": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}

```

Run

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_id|integer|true|none|none|
|map_id|string|true|none|none|
|id|integer|true|none|none|
|player|[Player](#schemaplayer)|true|none|Schema for representing a player, including their ID and creation date.|
|started_at|string(date-time)|true|none|none|
|status|[RunStatus](#schemarunstatus)|true|none|An enumeration for the possible statuses of a run.|
|duration_seconds|integer|true|none|none|
|level|integer|true|none|none|
|xp|integer|true|none|none|
|kills_total|integer|true|none|none|
|upgrades|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|object|false|none|none|
|»» **additionalProperties**|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ended_at|any|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string(date-time)|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|cause_of_death|any|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

<h2 id="tocS_RunEvent">RunEvent</h2>
<!-- backwards compatibility -->
<a id="schemarunevent"></a>
<a id="schema_RunEvent"></a>
<a id="tocSrunevent"></a>
<a id="tocsrunevent"></a>

```json
{
  "event_type": "string",
  "value": "string",
  "id": 0,
  "run_id": 0,
  "timestamp": "2019-08-24T14:15:22Z"
}

```

RunEvent

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|event_type|string|true|none|none|
|value|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|none|none|
|run_id|integer|true|none|none|
|timestamp|string(date-time)|true|none|none|

<h2 id="tocS_RunEventCreate">RunEventCreate</h2>
<!-- backwards compatibility -->
<a id="schemaruneventcreate"></a>
<a id="schema_RunEventCreate"></a>
<a id="tocSruneventcreate"></a>
<a id="tocsruneventcreate"></a>

```json
{
  "event_type": "string",
  "value": "string"
}

```

RunEventCreate

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|event_type|string|true|none|none|
|value|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

<h2 id="tocS_RunLeaderboard">RunLeaderboard</h2>
<!-- backwards compatibility -->
<a id="schemarunleaderboard"></a>
<a id="schema_RunLeaderboard"></a>
<a id="tocSrunleaderboard"></a>
<a id="tocsrunleaderboard"></a>

```json
{
  "player_id": 0,
  "run_id": 0,
  "player_name": "string",
  "duration_seconds": 0,
  "total_kills": 0
}

```

RunLeaderboard

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_id|integer|true|none|none|
|run_id|integer|true|none|none|
|player_name|string|true|none|none|
|duration_seconds|integer|true|none|none|
|total_kills|integer|true|none|none|

<h2 id="tocS_RunStart">RunStart</h2>
<!-- backwards compatibility -->
<a id="schemarunstart"></a>
<a id="schema_RunStart"></a>
<a id="tocSrunstart"></a>
<a id="tocsrunstart"></a>

```json
{
  "player_name": "string",
  "password": "string",
  "map_id": "string",
  "create_new_player": false
}

```

RunStart

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_name|string|true|none|none|
|password|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|map_id|string|true|none|none|
|create_new_player|boolean|false|none|none|

<h2 id="tocS_RunStartResponse">RunStartResponse</h2>
<!-- backwards compatibility -->
<a id="schemarunstartresponse"></a>
<a id="schema_RunStartResponse"></a>
<a id="tocSrunstartresponse"></a>
<a id="tocsrunstartresponse"></a>

```json
{
  "player_id": 0,
  "run_id": 0
}

```

RunStartResponse

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|player_id|integer|true|none|none|
|run_id|integer|true|none|none|

<h2 id="tocS_RunStatus">RunStatus</h2>
<!-- backwards compatibility -->
<a id="schemarunstatus"></a>
<a id="schema_RunStatus"></a>
<a id="tocSrunstatus"></a>
<a id="tocsrunstatus"></a>

```json
"in_progress"

```

RunStatus

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|RunStatus|string|false|none|An enumeration for the possible statuses of a run.|

#### Enumerated Values

|Property|Value|
|---|---|
|RunStatus|in_progress|
|RunStatus|died|
|RunStatus|completed|

<h2 id="tocS_RunUpdate">RunUpdate</h2>
<!-- backwards compatibility -->
<a id="schemarunupdate"></a>
<a id="schema_RunUpdate"></a>
<a id="tocSrunupdate"></a>
<a id="tocsrunupdate"></a>

```json
{
  "duration_seconds": 0,
  "kills_total": 0,
  "level": 0,
  "xp": 0,
  "upgrades": {
    "property1": 0,
    "property2": 0
  },
  "status": "in_progress",
  "ended_at": "2019-08-24T14:15:22Z",
  "cause_of_death": "string"
}

```

RunUpdate

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|duration_seconds|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|kills_total|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|level|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|xp|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|upgrades|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|object|false|none|none|
|»» **additionalProperties**|integer|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|status|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[RunStatus](#schemarunstatus)|false|none|An enumeration for the possible statuses of a run.|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ended_at|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string(date-time)|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|cause_of_death|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|

