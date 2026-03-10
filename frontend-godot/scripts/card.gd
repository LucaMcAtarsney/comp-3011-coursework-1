extends ColorRect

@export var hover_scale := Vector2(1.1, 1.1)
@export var tween_time := 0.15

@onready var card = $"."

var tween: Tween
signal change_ui

func _ready():
	# Ensure the pivot is centered once size is known
	pivot_offset = size * 0.5

	# Keep pivot centered if the rect resizes (layout / text changes)
	resized.connect(_on_resized)
	
	gui_input.connect(_on_gui_input)

	mouse_entered.connect(_on_mouse_entered)
	mouse_exited.connect(_on_mouse_exited)

func _on_gui_input(event: InputEvent):
	if event is InputEventMouseButton \
			and event.button_index == MOUSE_BUTTON_LEFT \
			and event.pressed:
				if card.is_in_group("player_card"):
					change_ui.emit(int($PlayerID.text))
					
		
		
		
func _on_resized():
	pivot_offset = size * 0.5

func _on_mouse_entered():
	_scale_to(hover_scale)

func _on_mouse_exited():
	_scale_to(Vector2.ONE)

func _scale_to(target: Vector2):
	if tween:
		tween.kill()

	tween = create_tween()
	tween.tween_property(self, "scale", target, tween_time)\
		 .set_trans(Tween.TRANS_QUAD)\
		 .set_ease(Tween.EASE_OUT)
