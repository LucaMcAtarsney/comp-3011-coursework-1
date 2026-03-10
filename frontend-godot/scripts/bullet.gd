extends Area2D
@export var speed = 200
var direction = Vector2.LEFT  # default direction

func _ready() -> void:
	speed += global.bullet_speed_increase
	match global.bullet_direction:
		"left":
			direction = Vector2.LEFT
		"right":
			direction = Vector2.RIGHT
		"up":
			direction = Vector2.UP
		"down":
			direction = Vector2.DOWN
			
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	position += direction.normalized() * speed * delta


func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("wall"):
		queue_free()
