extends HBoxContainer

@onready var upgrade_icon: PackedScene = preload("res://scenes/upgrade_hud.tscn")
@onready var arena = $"../.."

var img := {
	"fast_bullets": preload("res://art/fast_bullets.png"),
	"move_faster": preload("res://art/caffeine.png"),
	"double_shot": preload("res://art/moreshot-export.png"),
	"aoe_ring": preload("res://art/halo.png"),
	"regen": preload("res://art/vitality.png"),
	"max_health": preload("res://art/multivitamin.png"),
	"golden_apple": preload("res://art/goldenapple.png")
}

var UPGRADE_POOL := [
	{
		"id": "fast_bullets",
		"desc": "Increase bullet speed.",
	},
	{
		"id": "move_faster",
		"desc": "Increase movement speed.",
	},
	{
		"id": "double_shot",
		"desc": "Shoot an extra ball at once.",
	},
	{
		"id": "aoe_ring",
		"desc": "Periodic ring damage around you.",
	},
	{
		"id": "regen",
		"desc": "Recover health over time.",
	},
	{
		"id": "max_health",
		"desc": "Increase maximum health.",
	},
	{
		"id": "golden_apple",
		"desc": "Fully heal.",
	},
]

var upgrade_desc := {}

func _ready() -> void:
	for u in UPGRADE_POOL:
		upgrade_desc[u.id] = u.desc

	arena.update_upgrade_ui.connect(refresh_ui)
	refresh_ui()

func refresh_ui() -> void:
	for child in get_children():
		child.queue_free()

	for upgrade in global.upgrades:
		var level := int(global.upgrades[upgrade])
		if level > 0:
			var element = upgrade_icon.instantiate()

			var label: Label = element.get_node("Label")
			var sprite: Sprite2D = element.get_node("Sprite2D")

			label.text = str(level)
			sprite.texture = img.get(upgrade)
			element.scale = Vector2(2, 2)

			element.tooltip_text = "%s\nLevel: %d" % [
				upgrade_desc.get(upgrade, "Unknown upgrade"),
				level
			]

			add_child(element)
