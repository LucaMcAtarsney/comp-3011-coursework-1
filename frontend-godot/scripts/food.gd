extends Area2D

@export var heal_val: int = 5

func _ready() -> void:
	pass

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		global.heal(heal_val)
		queue_free()
