extends CanvasLayer

@onready var cont = $VBoxContainer
@export var ldb_record: PackedScene= preload("res://scenes/leaderboard_record.tscn")
func _ready() -> void:
	Network.leaderboard_received.connect(_on_leaderboard_received)
	Network.get_leaderboard()
	


func _on_leaderboard_received(leaderboard_data):
	print("Updating UI with leaderboard data: ", leaderboard_data)
	# Here, you would loop through the leaderboard_data array
	# and create/update UI labels to display the scores.
	var rec
	var i = 0
	
	for run_data in leaderboard_data:
		i += 1
		var player_name = run_data["player_name"] # This line is corrected
		var survival_time = run_data["duration_seconds"]
		
		var minutes = int(survival_time) / 60
		var seconds = int(survival_time) % 60
		var time_str = "%02d:%02d" % [minutes, seconds]
		
		rec = ldb_record.instantiate()
		
		rec.get_node("Name").text = str(i) + ". " + player_name
		rec.get_node("RunLength").text = str(time_str)
		
		cont.add_child(rec)
		

func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/analytics.tscn")
