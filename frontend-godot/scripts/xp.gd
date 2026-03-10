extends Area2D

@export var xp_value: int = 5
@export var pickup_y_offset: float = 0.0 # optional if you want a little pop effect later

func _ready() -> void:
	pass



func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		# Give XP to the global leveling system
		global.add_xp(xp_value)
		print("picked up xp")

		# Remove the orb
		queue_free()
