extends Node2D

@onready var clock: Timer = $Clock
@onready var time_survived_label: Label = $CanvasLayer/TimeSurvived
@onready var xp_bar = $CanvasLayer/xp
@onready var upgrade = $CanvasLayer/Upgrade

var time_survived := 0  # total seconds

func _ready() -> void:
	global.level_up.connect(_choose_upgrade)
	global.xp_changed.connect(_update_xp_ui)
	upgrade.upgrade_chosen.connect(_apply_upgrade)
	
	upgrade.visible = false
	clock.start()

func _on_clock_timeout() -> void:
	time_survived += 1
	global.time_survived = time_survived

	var minutes := time_survived / 60
	var seconds := time_survived % 60

	time_survived_label.text = "%d:%02d" % [minutes, seconds]

func _update_xp_ui() -> void:
	# XP progress in current level:
	var max_xp = global.base_xp_to_level_up
	var current = max_xp - global.remaining_xp_to_level_up

	xp_bar.max_value = max_xp
	xp_bar.value = current
	
func _choose_upgrade(level):
	get_tree().paused = true
	upgrade.visible = true

signal update_upgrade_ui

func _apply_upgrade(id: String):
	global.upgrades[id] = global.upgrades.get(id, 0) + 1

	match id:
		"fast_bullets":
			global.bullet_speed_increase += 0.15
		"move_faster":
			$player.speed += 20
		"double_shot":
			global.bullets_per_click += 1
		"aoe_ring":
			$player.enable_aoe_ring()
		"regen":
			$player.regen_per_second += 0.2
		"max_health":
			$player.max_health += 2
			$player.health += 2
		"golden_apple":
			$player.health  = $player.max_health
			$player.hp_bar.value = $player.health
			
	update_upgrade_ui.emit()
	get_tree().paused = false
	upgrade.visible = false
	upgrade.randomise()
	
	
	


func _on_audio_stream_player_2d_finished() -> void:
	$AudioStreamPlayer2D.play()
	


func _on__thiry_second_timer_timeout() -> void:
	$AudioStreamPlayer2D.pitch_scale += 0.1
	$"30 second timer".start()


func _on_api_update_run_timeout() -> void:
	global.time_survived = time_survived
	Network.call_run_update()
	
	
	$API_Update_Run.start()
