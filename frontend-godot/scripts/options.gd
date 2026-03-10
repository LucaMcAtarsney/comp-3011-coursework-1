extends CanvasLayer


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	inputs()

func inputs():
	esc()
	
func esc():
	if Input.is_action_just_pressed("options"):
		global.in_options = false
		queue_free()

func _on_give_up_button_down() -> void:
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
