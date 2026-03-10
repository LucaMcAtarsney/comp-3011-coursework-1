extends Node

#const BASE_URL:String="https://comp-3011-coursework-1.onrender.com"
const BASE_URL:String="http://127.0.0.1:8000"
var _http:HTTPRequest=HTTPRequest.new()

# --- Player State ---
var current_player_id:int=-1
var current_player_name:String=""
var current_player_password:String=""
var current_run_id:int=-1
var last_request_type:String=""

# --- Admin State ---
var admin_user:String = ""
var admin_pass:String = ""

# --- Player Signals ---
signal password_received(player_name:String, password:String)
signal authentication_failed(error_message:String)
signal game_session_started(player_id:int, run_id:int)
signal leaderboard_received(leaderboard_data:Array)
signal all_runs_received(json_data:Array)
signal players_received(json_data:Array)
signal player_stats_received(stats_data:Dictionary)
signal name_check_received(exists:bool,message:String)
signal random_name_received(player_name:String)

# --- Admin Signals ---
signal admin_login_successful
signal admin_login_failed(error_message:String)

func _ready()->void:
	add_child(_http)
	_http.request_completed.connect(_on_request_completed)
	
func _request_json(path:String,method:int=HTTPClient.METHOD_GET,body:Dictionary={}, is_admin:bool=false)->void:
	var url:String=BASE_URL+path
	var headers:PackedStringArray=PackedStringArray(["Content-Type: application/json"])
	
	# Add Basic Auth header for admin requests
	if is_admin:
		if admin_user.is_empty() or admin_pass.is_empty():
			push_error("Admin credentials are not set for request to %s" % path)
			return
		var auth_string = "%s:%s" % [admin_user, admin_pass]
		var auth_base64 = Marshalls.utf8_to_base64(auth_string)
		headers.append("Authorization: Basic %s" % auth_base64)
		
	var json_body:String=""
	if method!=HTTPClient.METHOD_GET and method!=HTTPClient.METHOD_HEAD and not body.is_empty():
		json_body=JSON.stringify(body)
		
	var err:int=_http.request(url,headers,method,json_body)
	if err!=OK:
		push_error("HTTP request error (%s) for %s"%[str(err),url])

# --- Admin Functions ---

func check_admin_login(user: String, password: String):
	last_request_type = "admin_login"
	# Store credentials for subsequent admin requests
	admin_user = user
	admin_pass = password
	_request_json("/admin/login", HTTPClient.METHOD_GET, {}, true)

func admin_delete_run(run_id: int):
	last_request_type = "admin_delete"
	_request_json("/admin/runs/%s" % str(run_id), HTTPClient.METHOD_DELETE, {}, true)

func admin_delete_player(player_id: int):
	last_request_type = "admin_delete"
	_request_json("/admin/players/%s" % str(player_id), HTTPClient.METHOD_DELETE, {}, true)

func admin_update_player_name(player_id: int, new_name: String):
	last_request_type = "admin_update"
	var body_data: Dictionary = {"name": new_name}
	_request_json("/admin/players/%s" % str(player_id), HTTPClient.METHOD_PATCH, body_data, true)

# --- Player & Game Functions ---
			
func check_player_name(player_name:String)->void:
	last_request_type="check_name"
	var body_data:Dictionary={"player_name":player_name}
	_request_json("/players/check-name",HTTPClient.METHOD_POST,body_data)

func generate_random_name()->void:
	last_request_type="generate_name"
	_request_json("/players/generate-name",HTTPClient.METHOD_GET)

func start_game_session(player_name: String, password: String = "", is_new_player: bool = false) -> void:
	last_request_type = "start_run"
	current_player_name = player_name
	current_player_password = password

	var body_data: Dictionary = {
		"player_name": player_name,
		"map_id": "default_map",
		"create_new_player": is_new_player
	}

	if not password.is_empty():
		body_data["password"] = password

	_request_json("/runs/start", HTTPClient.METHOD_POST, body_data)

func call_run_update()->void:
	last_request_type="update_run"
	if current_run_id==-1:
		push_error("Invalid run_id. Cannot update run.")
		return
	var body_data:Dictionary={"time_survived":global.time_survived,"monsters_slain":global.monsters_slain,"xp":global.xp,"upgrades":global.upgrades,"level":global.level}
	_request_json("/runs/%s/update"%str(current_run_id),HTTPClient.METHOD_POST,body_data)

func call_run_end()->void:
	last_request_type="update_run"
	if current_run_id==-1:
		push_error("Invalid run_id. Cannot end run.")
		return
	var body_data:Dictionary={"time_survived":global.time_survived,"monsters_slain":global.monsters_slain,"xp":global.xp,"upgrades":global.upgrades,"level":global.level,"status":"completed","cause_of_death":global.cause_of_death}
	_request_json("/runs/%s/update"%str(current_run_id),HTTPClient.METHOD_POST,body_data)

func get_leaderboard(limit:int=10)->void:
	last_request_type="leaderboard"
	_request_json("/analytics/leaderboard?limit=%s"%str(limit),HTTPClient.METHOD_GET)

func get_players(search_term:String="")->void:
	last_request_type="players_summary"
	var path:String="/analytics/players-summary"
	if not search_term.is_empty():
		var encoded_search:String=search_term.uri_encode()
		path+="?search=%s"%encoded_search
	# NOTE: This now requires admin auth. We need to pass `true`.
	_request_json(path, HTTPClient.METHOD_GET, {}, false)

func get_runs()->void:
	last_request_type="all_runs"
	_request_json("/runs",HTTPClient.METHOD_GET)

func get_player_stats(player_id:int)->void:
	if player_id<=0:
		push_error("Invalid player ID provided.")
		return
	last_request_type="player_stats"
	_request_json("/analytics/view_player_stats/%s"%str(player_id),HTTPClient.METHOD_GET)
	
func delete_current_player()->void:
	if current_player_id > 0:
		last_request_type = "delete_player"
		_request_json("/players/%s" % str(current_player_id), HTTPClient.METHOD_DELETE)
		current_player_id = -1
		current_run_id = -1
		current_player_name = ""
		current_player_password = ""

# --- Response Handling ---

func _on_request_completed(result:int, response_code:int, headers:PackedStringArray, body:PackedByteArray) -> void:
	var completed_request_type = last_request_type
	last_request_type = ""

	# Handle failed requests
	if response_code < 200 or response_code >= 300:
		print("HTTP request failed with code: ", response_code)
		var response_text:String = body.get_string_from_utf8()
		print("Response body: ", response_text)
		
		if completed_request_type == "admin_login":
			admin_login_failed.emit("Invalid admin credentials.")
			return
		
		if response_code == 403 and completed_request_type == "start_run":
			var parsed:Variant = JSON.parse_string(response_text)
			if parsed is Dictionary:
				var error_msg:String = parsed.get("detail", "Invalid credentials.")
				authentication_failed.emit(error_msg)
		return

	# Handle successful but empty responses (like DELETE)
	if body.get_string_from_utf8().is_empty():
		if completed_request_type == "admin_delete" and response_code == 204:
			print("Admin delete successful.")
		return

	# Parse JSON response
	var parsed:Variant = JSON.parse_string(body.get_string_from_utf8())
	if parsed == null:
		print("Failed to parse JSON response. Raw: ", body.get_string_from_utf8())
		return

	# Process based on the completed request type
	match completed_request_type:
		"admin_login":
			if response_code == 200:
				admin_login_successful.emit()

		"admin_delete":
			# This case is now handled by the empty body check above, but we keep it for clarity
			pass

		"admin_update":
			if response_code == 200:
				print("Admin update successful: ", parsed)
			else:
				print("Admin update failed. Status: ", response_code)

		"check_name":
			if parsed is Dictionary:
				var exists:bool = parsed.get("exists", false)
				var message:String = parsed.get("message", "")
				name_check_received.emit(exists, message)

		"generate_name":
			if parsed is Dictionary:
				var player_name:String = parsed.get("player_name", "")
				random_name_received.emit(player_name)

		"start_run":
			if parsed is Dictionary:
				current_player_id = int(parsed["player_id"])
				current_run_id = int(parsed["run_id"])
				
				if parsed.has("password") and parsed["password"] != null:
					current_player_password = parsed["password"]
					password_received.emit(current_player_name, current_player_password)
				
				game_session_started.emit(current_player_id, current_run_id)
				print("Successfully started run! Player ID: %s, Run ID: %s" % [str(current_player_id), str(current_run_id)])

		"update_run":
			print("Run update successful. Server response: ", parsed)

		"player_stats":
			if parsed is Dictionary:
				player_stats_received.emit(parsed)

		"leaderboard":
			if parsed is Array:
				leaderboard_received.emit(parsed)

		"all_runs":
			if parsed is Array:
				all_runs_received.emit(parsed)

		"players_summary":
			if parsed is Array:
				players_received.emit(parsed)
				
		"delete_player":
			if response_code == 204:
				print("Player successfully deleted.")
			else:
				print("Player deletion might have failed. Status: ", response_code)

		_:
			print("Received an unhandled response for request type '%s': " % completed_request_type, parsed)
