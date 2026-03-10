extends CanvasLayer


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


func _on_start_button_button_down() -> void:
	get_tree().change_scene_to_file("res://scenes/second_screen.tscn")


func _on_analytics_button_button_up() -> void:
	get_tree().change_scene_to_file("res://scenes/analytics.tscn")

		
