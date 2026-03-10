extends CanvasLayer


func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")


func _on_leaderboard_button_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/leaderboard.tscn")


func _on_dev_zone_button_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/admin_login.tscn")


func _on_player_stats_button_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/player_analytics.tscn")
