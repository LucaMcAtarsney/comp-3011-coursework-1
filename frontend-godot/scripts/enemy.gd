extends CharacterBody2D

@export var speed := 50
@export var damage := 1
@export var xp := 1
var player = null
@export var health := 3
var inrange = false

var xp_drop: PackedScene = preload("res://scenes/xp.tscn")
var food: PackedScene = preload("res://scenes/food.tscn")


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var players = get_tree().get_nodes_in_group("player")
	if players.size() > 0:
		player = players[0]

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(_delta: float) -> void:
	if player:
		var direction = (player.global_position - global_position)
		
		# Optional: stop moving if too close
		if direction.length() < 8:
			$AnimatedSprite2D.play("walk")
			return

		direction = direction.normalized()
		velocity = direction * speed
		move_and_slide()

		# Flip sprite based on direction
		if direction.x != 0:
			$AnimatedSprite2D.flip_h = direction.x > 0

		$AnimatedSprite2D.play("walk")

func _on_hit(area):
	if area.name == "Bullet":  # Adjust if needed
		health -= 1
		print("Hit! Health now:", health)

	if health <= 0:
		die()


func die():
	var drop
	var rand = randi_range(1,20)
	if rand == 1:
		drop = food.instantiate()
		drop.global_position = global_position + Vector2(0,6)
	else:
		drop = xp_drop.instantiate()
		drop.xp_value = xp
		drop.global_position = global_position + Vector2(0,6)
	
	global.monsters_slain += 1
	
	print(global.level)
	
	get_tree().current_scene.add_child(drop)
	queue_free()
	
	

	
func _on_hitbox_area_entered(area: Area2D) -> void:
	if area.is_in_group("bullet"):
		area.queue_free()
		health -= 1

		if health <= 0:
			call_deferred("die")

signal attacked(damage:int)



func _on_attack_range_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		inrange = true
		attack_player()
		print("attacked player")
		$AttackTimer.start()


func _on_attack_range_body_exited(_body: Node2D) -> void:
	inrange = false
	
func attack_player():
	attacked.emit(damage)

func _on_attack_timer_timeout() -> void:
	if inrange:
		attack_player()
