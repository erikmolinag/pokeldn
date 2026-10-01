"""The casino-coins gift: Game Corner coins from the delivery man, through the script's own addcoins.

How it could fail. The amount emitted is not the one asked for; a refusal at the cap (VAR_RESULT TRUE)
read as a success, so the player hears the fanfare and gets nothing; the card spent after one visit
when it is meant to repeat; an address somewhere, which would tie the card to one language.
"""

import dataclasses
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin"))

from pokeldn.frlg.gift import gift_artifact, gift_registry  # noqa: E402
from pokeldn.frlg.gift import gift_composer as gc  # noqa: E402
from pokeldn.frlg.gift import wonder_card_events as wce  # noqa: E402
from pokeldn.frlg.rom import scrcmd  # noqa: E402
from pokeldn.frlg.text import charmap  # noqa: E402
from test_gift_composer import ScriptVM  # noqa: E402


def _ram_script(gift=wce.CASINO_COINS_GIFT):
    return gc.compile_definition(gift, flag_id=wce.CASINO_COINS_FLAG_ID).ram_script


def _said(vm):
    return [charmap.decode_message(message) for message in vm.messages]


def test_the_delivery_man_hands_over_the_coins_with_the_fanfare():
    vm = ScriptVM(_ram_script(), coins=0).run()
    assert vm.ended and vm.coins == 9999
    assert vm.fanfares == [gc.MUS_OBTAIN_ITEM]
    assert any("9999 COINS" in text for text in _said(vm))


def test_the_player_is_released_only_after_the_fanfare():
    # Released mid-fanfare, stairs reset Task_Fanfare and leave the BGM paused; the next warp to
    # other music then never finishes fading and the screen stays black. Seen on a retail FireRed.
    vm = ScriptVM(_ram_script(), coins=0).run()
    assert vm.release_count == 1 and vm.releases_during_fanfare == 0
    lines = scrcmd.disassemble(_ram_script(), scrcmd.RAM_SCRIPT_VIRTUAL_BASE, limit=80)
    ops = [line.split()[2] for line in lines]
    assert ops[ops.index("playfanfare") + 1] == "waitfanfare"


def test_below_the_cap_the_coins_top_up_to_it():
    assert ScriptVM(_ram_script(), coins=4321).run().coins == 9999


def test_at_the_cap_the_player_is_told_and_nothing_changes():
    vm = ScriptVM(_ram_script(), coins=9999).run()
    assert vm.coins == 9999 and vm.fanfares == []
    assert gc.DEFAULT_COINS_FULL_MESSAGE in _said(vm)


def test_the_card_gives_again_on_the_next_visit():
    first = ScriptVM(_ram_script(), coins=0).run()
    second = ScriptVM(_ram_script(), variables=first.vars, flags=first.flags, coins=150).run()
    assert second.coins == 9999 and second.fanfares == [gc.MUS_OBTAIN_ITEM]


def test_the_script_emits_addcoins_with_the_amount_and_disassembles():
    script = _ram_script()
    assert bytes([scrcmd.OP_ADDCOINS]) + (9999).to_bytes(2, "little") in script
    lines = scrcmd.disassemble(script, scrcmd.RAM_SCRIPT_VIRTUAL_BASE, limit=80)
    assert any("addcoins 0x270F" in line for line in lines)


@pytest.mark.parametrize("amount", [0, gc.MAX_COINS + 1])
def test_an_amount_outside_1_to_9999_is_refused(amount):
    gift = dataclasses.replace(wce.CASINO_COINS_GIFT, delivery=gc.DeliveryPlan(delivery=(
        gc.DeliveryStage(gc.GiveCoins(amount)),)))
    with pytest.raises(gc.GiftValidationError, match="amount"):
        _ram_script(gift)


def test_a_stage_carries_one_fallible_reward_coins_included():
    gift = dataclasses.replace(wce.CASINO_COINS_GIFT, delivery=gc.DeliveryPlan(delivery=(
        gc.DeliveryStage(gc.GiveCoins(10), gc.GiveItem(1)),)))
    with pytest.raises(gc.GiftValidationError, match="fallible"):
        _ram_script(gift)


def test_the_gift_is_registered_repeatable_and_the_same_for_every_cartridge():
    assert wce.GIFT_CASINO_COINS in gift_registry.GIFT_REGISTRY.live_choices
    assert gift_registry.GIFT_REGISTRY.default_flag_id(wce.GIFT_CASINO_COINS) == 1010
    assert wce.CASINO_COINS_GIFT.event.repeatable
    assert wce.CASINO_COINS_GIFT.for_build is None


def test_the_command_line_serves_it():
    import frlg_mg_host
    parser = frlg_mg_host.build_parser()
    run = frlg_mg_host.build_run_config(parser, parser.parse_args(["--gift", "casino-coins"]))
    assert run.payload.build_distribution().ram_script == _ram_script()


def test_the_artifact_names_the_action():
    assert gift_artifact._action_summary(gc.GiveCoins(25)) == "GiveCoins(amount=25)"
