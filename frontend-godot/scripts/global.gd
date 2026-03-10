extends Node
var bullet_direction = "left"
var player_health = 20
var xp = 0
var level = 0
var base_xp_to_level_up = 30
var remaining_xp_to_level_up = 30
var player_name
var view_player_id

var player_password

var in_options = false

signal xp_changed
signal level_up(new_level: int)

func add_xp(amount: int) -> void:
	xp += amount

	var gained := amount
	var leveled := false

	while gained > 0:
		if gained >= remaining_xp_to_level_up:
			gained -= remaining_xp_to_level_up
			level += 1
			base_xp_to_level_up = int(ceil(base_xp_to_level_up * 1.2))
			remaining_xp_to_level_up = base_xp_to_level_up
			leveled = true
		else:
			remaining_xp_to_level_up -= gained
			gained = 0

	xp_changed.emit()

	if leveled:
		level_up.emit(level)

signal heal_player(amount:int)

func heal(amount: int) -> void:
	heal_player.emit(amount)
		
		
var time_survived
var time_survived_label
var cause_of_death = "monster"
var monsters_slain = 0
var bosses_slain = 0

var bullet_speed_increase = 0
var bullets_per_click = 1
# upgrades
var upgrades := {
	"fast_bullets": 0,
	"move_faster": 0,
	"more_shot": 0,      
	"aoe_ring": 0,         
	"regen": 0,
	"max_health": 0,
	"golden_apple": 0
}
