extends CanvasLayer


func _on_new_player_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/new_player.tscn")


func _on_returning_player_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/pre_run.tscn")


func _on_go_back_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
