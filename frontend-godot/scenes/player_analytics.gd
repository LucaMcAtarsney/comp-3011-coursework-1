extends CanvasLayer

@onready var cont = $ScrollContainer/VBoxContainer
@export var p_record: PackedScene= preload("res://scenes/player_record.tscn")

func _ready() -> void:
	Network.players_received.connect(_on_players_recieved)
	Network.get_players()
	
func _on_players_recieved(json_data):
	for child in cont.get_children():
		child.queue_free()

	if not json_data is Array:
		print("Error: Data for populating players is not an array.")
		return

	for player_data in json_data:
		
		
		var player_name = player_data["name"]
		var player_id = player_data["id"]
		var total_runs = str(int(player_data["total_runs"]))
		var created_at_string = player_data["created_at"]
		var best_run_time_seconds = player_data["best_run_time"]

		var minutes = int(best_run_time_seconds) / 60
		var seconds = int(best_run_time_seconds) % 60
		var time_str = "%02d:%02d" % [minutes, seconds]
		
		# --- Normalize datetime string for Godot ---
		var s = created_at_string.replace(" ", "T")
		if s.contains("."):
			s = s.split(".")[0]

		# --- Convert to datetime dict ---
		var unix_time = Time.get_unix_time_from_datetime_string(s)
		var datetime_dict = Time.get_datetime_dict_from_unix_time(unix_time)

		var day = datetime_dict["day"]
		var month = datetime_dict["month"]
		var year = datetime_dict["year"]
		var formatted_date = "%02d/%02d/%02d" % [day, month, year % 100]

		var rec = p_record.instantiate()
		rec.get_node("Row").change_ui.connect(_view_player_stats)

		rec.get_node("Row/Name").text = player_name
		rec.get_node("Row/PlayerID").text = str(player_id)
		rec.get_node("Row/Runs").text = str(total_runs)
		rec.get_node("Row/CreatedAt").text = formatted_date
		rec.get_node("Row/Best Run Time").text = time_str

		rec.name = "run_" + str(player_id)

		cont.add_child(rec)
		
	var rec = p_record.instantiate()
	cont.add_child(rec)

func _view_player_stats(player_id: int):
	global.view_player_id = player_id
	get_tree().change_scene_to_file("res://scenes/view_player.tscn")
func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/analytics.tscn")


func _on_line_edit_text_changed(new_text: String) -> void:
	Network.get_players(new_text)
