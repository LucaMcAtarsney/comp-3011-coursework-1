extends CanvasLayer

@onready var player_name = $PlayerName
@onready var num_of_runs = $VBoxContainer/Row1/NumberOfRuns/Text
@onready var time_played = $VBoxContainer/Row1/TimePlayed/Text
@onready var avg_survival_time =$VBoxContainer/Row1/AvgTimeSurvived/Text
@onready var longest_run = $VBoxContainer/Row2/LongestRun/Text
@onready var fav_upgrade = $VBoxContainer/Row2/FavUpgrade/Text
@onready var monsters_slain = $VBoxContainer/Row2/MonstersSlain/Text

func _ready() -> void:
	Network.player_stats_received.connect(_visualise_stats)
	if global.view_player_id != null:
		Network.get_player_stats(global.view_player_id)
	

func _visualise_stats(stats_data):
	
	# Extract all the data
	player_name.text = stats_data["player_name"]
	num_of_runs.text = str(int(stats_data["number_of_runs"]))
	var t_time = stats_data["total_time_played"]
	var minutes = int(t_time) / 60
	var seconds = int(t_time) % 60
	var time_str = "%02d:%02d" % [minutes, seconds]
	
	time_played.text = time_str
		
	t_time = stats_data["average_time_survived"]
	minutes = int(t_time) / 60
	seconds = int(t_time) % 60
	time_str = "%02d:%02d" % [minutes, seconds]
	
	avg_survival_time.text = time_str
	
	t_time  = stats_data["longest_run"]
	minutes = int(t_time) / 60
	seconds = int(t_time) % 60
	time_str = "%02d:%02d" % [minutes, seconds]
	
	longest_run.text = time_str
	
	
	var upgrade = stats_data["favourite_upgrade"]
	
	if upgrade != null:
		fav_upgrade.text = upgrade
	else:
		fav_upgrade.text = "N/A"
	
	monsters_slain.text = str(int(stats_data["total_monsters_slain"]))
	

func _on_go_back_button_up() -> void:
	global.view_player_id = null
	get_tree().change_scene_to_file("res://scenes/player_analytics.tscn")
