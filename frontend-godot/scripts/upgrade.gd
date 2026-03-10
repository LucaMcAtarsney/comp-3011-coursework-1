extends Control

signal upgrade_chosen(id: String)

var _pulse_tween: Tween

@onready var card_buttons: Array[Button] = [
	$HBoxContainer/Option1/Button,
	$HBoxContainer/Option2/Button,
	$HBoxContainer/Option3/Button,
]

@onready var card_bg_color: Array[ColorRect] = [
	$HBoxContainer/Option1,
	$HBoxContainer/Option2,
	$HBoxContainer/Option3,
]

@onready var card_sprite: Array[Sprite2D] = [
	$HBoxContainer/Option1/ImgBG/Sprite,
	$HBoxContainer/Option2/ImgBG/Sprite,
	$HBoxContainer/Option3/ImgBG/Sprite,
]

@onready var card_name: Array[Label] = [
	$HBoxContainer/Option1/Option1DescriptionBox/Option1Name,
	$HBoxContainer/Option2/Option2DescriptionBox/Option2Name,
	$HBoxContainer/Option3/Option3DescriptionBox/Option3Name
]

@onready var card_desc: Array[Label] = [
	$HBoxContainer/Option1/Option1DescriptionBox/Option1DescriptionLabel,
	$HBoxContainer/Option2/Option2DescriptionBox/Option2DescriptionLabel,
	$HBoxContainer/Option3/Option3DescriptionBox/Option3DescriptionLabel
]



var UPGRADE_POOL := [
	{
		"id": "fast_bullets",
		"title": "Trigger Happy",
		"desc": "Increase bullet speed.",
		"color": Color.PURPLE,
		"image": preload("res://art/fast_bullets.png")
	},
	{
		"id": "move_faster",
		"title": "Caffeine",
		"desc": "Increase movement speed.",
		"color": Color.BLUE,
		"image": preload("res://art/caffeine.png")
	},
	{
		"id": "double_shot",
		"title": "More bullets",
		"desc": "Shoot an extra ball at once.",
		"color": Color.ORANGE_RED,
		"image": preload("res://art/moreshot-export.png")
	},
	{
		"id": "aoe_ring",
		"title": "Halo",
		"desc": "Periodic ring damage around you.",
		"one_time": true,
		"color": Color.YELLOW,
		"image": preload("res://art/halo.png")
	},
	{
		"id": "regen",
		"title": "Vitality",
		"desc": "Recover health over time.",
		"color": Color.HOT_PINK,
		"image": preload("res://art/vitality.png")
	},
	{
		"id": "max_health",
		"title": "Multivitamin",
		"desc": "Increase maximum health.",
		"color": Color.RED,
		"image": preload("res://art/multivitamin.png")
	},
	{
		"id": "golden_apple",
		"title": "Gold Apple",
		"desc": "Fully heal",
		"color": Color.DARK_GOLDENROD,
		"image": preload("res://art/goldenapple.png")
	},
]
var picks

func randomise():
	set_up_cards()
	
func _ready() -> void:
	
	set_up_cards()
	start_pulse()
	
func start_pulse() -> void:
	# If you reopen the menu, avoid stacking tweens
	if _pulse_tween and _pulse_tween.is_running():
		_pulse_tween.kill()

	_pulse_tween = create_tween()
	_pulse_tween.set_loops() # infinite
	_pulse_tween.set_trans(Tween.TRANS_SINE)
	_pulse_tween.set_ease(Tween.EASE_IN_OUT)

	# Start from normal size
	scale = Vector2.ONE

	# Slightly bigger, then back
	_pulse_tween.tween_property(self, "scale", Vector2(2.03, 2.03), 0.45)
	_pulse_tween.tween_property(self, "scale", Vector2(2, 2), 0.45)


func set_up_cards():
	picks = _pick_random_upgrades(3)

	for i in range(card_buttons.size()):
		var btn = card_buttons[i]
		var upg = picks[i]
		
		card_name[i].text = upg["title"]
		card_desc[i].text = upg["desc"]
		card_bg_color[i].color = upg["color"]
		card_sprite[i].texture = upg["image"]
		
		# Store the upgrade id on the button
		btn.set_meta("upgrade_id", upg.id)

		# Connect click (avoid double-connecting if reused)
		if btn.pressed.is_connected(_on_card_pressed) == false:
			btn.pressed.connect(_on_card_pressed.bind(btn))
	
func _on_card_pressed(btn: Button) -> void:
	var id: String = btn.get_meta("upgrade_id")
	upgrade_chosen.emit(id)

func _pick_random_upgrades(count: int) -> Array:
	# Filter out one-time upgrades the player already has
	var available: Array = []
	for u in UPGRADE_POOL:
		var id: String = u.id
		var one_time = u.has("one_time") and u.one_time == true

		if one_time and global.upgrades.get(id, 0) >= 1:
			continue

		available.append(u)

	# If fewer than needed, just return what we can
	available.shuffle()
	return available.slice(0, min(count, available.size()))
