extends CharacterBody2D

@export var speed = 100
@onready var animator = $AnimatedSprite2D
@onready var hp_bar = $health
@onready var time_survived_label = $"../CanvasLayer/TimeSurvived"
@onready var halo = $Powers/Halo
@onready var halo_timer = $Powers/Halo/Timer

@export var options_menu: PackedScene = preload("res://scenes/options.tscn")
@onready var lava: TileMapLayer = get_parent().get_node("walls")

var bullet_scene = preload("res://scenes/bullet.tscn")
var direction = "left"
var directionLR = "left"
var doing
var health = 15
var max_health
var regen_per_second
var halo_active
var options_open = false
var base_color

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	base_color = animator.modulate
	hp_bar.max_value = health
	hp_bar.value = health
	global.heal_player.connect(_heal_player)
	max_health = health
	regen_per_second = 0
	halo_active = false
	halo.visible = false
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	inputs()
	play_animation()

func inputs():
	movement()
	attack()
	esc()

func _toggle_options_menu():
	if options_open:
		return

	options_open = true
	get_tree().paused = true

	var menu = options_menu.instantiate()
	get_tree().current_scene.add_child(menu)

	menu.tree_exited.connect(func():
		get_tree().paused = false
		options_open = false
	)
	
func esc():
	if Input.is_action_just_pressed("options"):
		#global.in_options = true
		#get_tree().change_scene_to_file("res://scenes/options.tscn")
		_toggle_options_menu()

func _get_tile_speed() -> float:

	var cell: Vector2i = lava.local_to_map(lava.to_local(global_position))

	# Get tile data from this layer
	var tile_data: TileData = lava.get_cell_tile_data(cell)

	if tile_data == null:
		return 1.0

	if tile_data.has_custom_data("slow_multiplier"):
		return tile_data.get_custom_data("slow_multiplier")

	return 1.0
	
func movement():
	velocity = Vector2.ZERO
	doing = "idle"  # Reset every frame

	if Input.is_action_pressed("right"):
		velocity.x += 1
		direction = "right"
		directionLR = "right"
		doing = "walk"
	elif Input.is_action_pressed("left"):
		velocity.x -= 1
		direction = "left"
		directionLR = "left"
		doing = "walk"

	if Input.is_action_pressed("down"):
		velocity.y += 1
		direction = "down"
		doing = "walk"
	elif Input.is_action_pressed("up"):
		velocity.y -= 1
		direction = "up"
		doing = "walk"

	if velocity.length() > 0:
		var speed_multiplier := _get_tile_speed()
		velocity = velocity.normalized() * (speed * speed_multiplier)

	move_and_slide()

func attack():
	var bullet
	if Input.is_action_just_pressed("atkleft"):
		for i in range(global.bullets_per_click):
			bullet = bullet_scene.instantiate()
			bullet.position = global_position
			global.bullet_direction = "left"
			bullet.position.x -= 7
			get_parent().add_child(bullet)
			await get_tree().create_timer(0.06).timeout
		
	elif Input.is_action_just_pressed("atkright"):
		for i in range(global.bullets_per_click):
			bullet = bullet_scene.instantiate()
			bullet.position = global_position
			global.bullet_direction = "right"
			bullet.position.x += 7 
			get_parent().add_child(bullet)
			await get_tree().create_timer(0.06).timeout
		
	elif Input.is_action_just_pressed("atkdown"):
		for i in range(global.bullets_per_click):
			bullet = bullet_scene.instantiate()
			bullet.position = global_position
			global.bullet_direction = "down"
			bullet.position.y += 7
			get_parent().add_child(bullet)
			await get_tree().create_timer(0.06).timeout
			
	elif Input.is_action_just_pressed("atkup"):
		for i in range(global.bullets_per_click):
			bullet = bullet_scene.instantiate()
			bullet.position = global_position
			global.bullet_direction = "up"
			bullet.position.y -= 7 
			get_parent().add_child(bullet)
			await get_tree().create_timer(0.06).timeout
	

		
func play_animation():
	match doing:
		"walk":
			if directionLR == "left":
				animator.flip_h = false
				animator.play("walk")
			else:
				animator.flip_h = true
				animator.play("walk")
			
		"idle":
			animator.play("idle")


func _on_player_attacked(damage: int) -> void:
	health -= damage
	global.player_health = health
	
	hp_bar.value = health
	
	if health <= 0:
		die()

func die():
	global.time_survived_label = time_survived_label.text
	for enemy in get_tree().get_nodes_in_group("enemy"):
		enemy.queue_free()
		print("freed")
		
	queue_free()
	get_tree().change_scene_to_file("res://scenes/run_summary.tscn")
	
func _heal_player(amount:int):
	health += amount
	
	if health > max_health:
		health = max_health
		
	hp_bar.value = health
	


func _on_regen_timeout() -> void:
	if regen_per_second > 0 and health != max_health:
		if health + regen_per_second > max_health:
			health = max_health
		else:
			health += regen_per_second
			
		hp_bar.value = health
		
func enable_aoe_ring():
	halo.visible = true
	halo_active = true
	
	
var can_halo_do_damage = true

func _on_area_2d_body_entered(body: Node2D) -> void:
	if halo_active:
		if body.is_in_group("enemy"):
			if can_halo_do_damage:
				halo_timer.start()
				can_halo_do_damage = false
				body.health -= 2
				print("halo damage")
				if body.health < 0:
					body.call_deferred("die")
					print("halo kill")
				
			


func _on_halo_timer_timeout() -> void:
	can_halo_do_damage = true

func _get_tile_dps() -> float:
	var cell: Vector2i = lava.local_to_map(lava.to_local(global_position))
	var tile_data: TileData = lava.get_cell_tile_data(cell)

	if tile_data == null:
		return 0.0

	if tile_data.has_custom_data("dps"):
		return float(tile_data.get_custom_data("dps"))

	return 0.0
	
func _on_lava_dmg_timeout() -> void:
	$LavaDmg.start()
	var dps := _get_tile_dps()
	
	if dps <= 0.0:
		animator.modulate = base_color
		return

	animator.modulate = Color(1.5, 0, 0.3)
	health -= dps
	hp_bar.value = health
	if health < 0:
		global.cause_of_death = "lava"
		die()
