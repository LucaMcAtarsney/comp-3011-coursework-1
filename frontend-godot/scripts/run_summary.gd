extends CanvasLayer

@onready var time_surv = $TimeSurvived
@onready var monsters_slain = $MonstersSlain
@onready var bosses_slain = $BossesSlain
@onready var xp_level = $XPLevel

func _ready() -> void:
	Network.call_run_end()
	time_surv.text = "Time survived: " + global.time_survived_label
	monsters_slain.text = "Monsters slain: " + str(global.monsters_slain)
	xp_level.text = "XP level: " + str(global.level)
	
	


func _on_start_button_button_down() -> void:
	for upgrade in global.upgrades:
		global.upgrades[upgrade] = 0
		
	global.bullet_speed_increase = 0
	global.bullets_per_click = 1
	global.player_health = 20
	global.xp = 0
	global.level = 0
	global.base_xp_to_level_up = 30
	global.remaining_xp_to_level_up = 30
	global.monsters_slain = 0
	global.bosses_slain = 0
	global.player_name = null
	global.time_survived_label = null
	global.cause_of_death = "monster"
		
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
