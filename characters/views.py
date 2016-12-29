from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models

import json


@login_required
def monster_detail(request, monster_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    monsters = sorted(models.Monster.objects.filter(user=user),
        key=lambda monster: monster.name.lower()
        )
    if monster_pk:
        this_monster = get_object_or_404(models.Monster, pk=monster_pk)
        if this_monster.user == request.user:
            return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})
        else:
            raise Http404
    elif len(monsters) > 0:
        this_monster = monsters[0]
        if this_monster.user == request.user:
            return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})
        else:
            raise Http404
    else:
        this_monster = None
    return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})

@login_required
def npc_detail(request, npc_pk=''):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    npcs = sorted(models.NPC.objects.filter(user=user),
        key=lambda npc: npc.name.lower()
        )
    if npc_pk:
        this_npc = get_object_or_404(models.NPC, pk=npc_pk)
        if this_npc.user == request.user:
            return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})
        else:
            raise Http404
    elif len(npcs) > 0:
        this_npc = npcs[0]
        if this_npc.user == request.user:
            return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})
        else:
            raise Http404
    else:
        this_npc = None
    return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})

@login_required
def player_detail(request, player_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    players = sorted(models.Player.objects.filter(user=user),
        key=lambda player: player.player_name.lower()
        )
    if player_pk:
        this_player = get_object_or_404(models.Player, pk=player_pk)
        if this_player.user == request.user:
            return render(request, 'characters/player_detail.html', {'this_player': this_player, 'players': players})
        else:
            raise Http404
    elif len(players) > 0:
        this_player = players[0]
        if this_player.user == request.user:
            return render(request, 'characters/player_detail.html', {'this_player': this_player, 'players': players})
        else:
            raise Http404
    else:
        this_player = None
    return render(request, 'characters/player_detail.html', {'this_player': this_player, 'players': players})

@login_required
def monster_create(request):
    form = forms.MonsterForm()
    if request.method == 'POST':
        form = forms.MonsterForm(request.POST)
        if form.is_valid():
            monster = form.save(commit=False)
            monster.user = request.user
            monster.save()
            messages.add_message(request, messages.SUCCESS, "Monster created!")
            return HttpResponseRedirect(monster.get_absolute_url())
    return render(request, 'characters/monster_form.html', {'form': form})

@login_required
def npc_create(request):
    form = forms.NPCForm()
    if request.method == 'POST':
        form = forms.NPCForm(request.POST)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.user = request.user
            npc.save()
            messages.add_message(request, messages.SUCCESS, "NPC created!")
            return HttpResponseRedirect(npc.get_absolute_url())
    return render(request, 'characters/npc_form.html', {'form': form})

@login_required
def player_create(request):
    form = forms.PlayerForm()
    if request.method == 'POST':
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            messages.add_message(request, messages.SUCCESS, "Player created!")
            return HttpResponseRedirect(player.get_absolute_url())
    return render(request, 'characters/player_form.html', {'form': form})

@login_required
def monster_update(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.MonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.MonsterForm(instance=monster, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated monster: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(monster.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/monster_form.html', {'form': form, 'monster': monster})

@login_required
def npc_update(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.NPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.NPCForm(instance=npc, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated NPC: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(npc.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/npc_form.html', {'form': form, 'npc': npc})

@login_required
def player_update(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.PlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.PlayerForm(instance=player, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated player: {}".format(form.cleaned_data['player_name']))
                return HttpResponseRedirect(player.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/player_form.html', {'form': form, 'player': player})

@login_required
def monster_delete(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.DeleteMonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.DeleteMonsterForm(request.POST, instance=monster)
            if monster.user.pk == request.user.pk:
                monster.delete()
                messages.add_message(request, messages.SUCCESS, "Monster deleted!")
                return HttpResponseRedirect(reverse('characters:monster_detail'))
    else:
        raise Http404
    return render(request, 'characters/monster_delete.html', {'form': form, 'monster': monster})

@login_required
def npc_delete(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.DeleteNPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.DeleteNPCForm(request.POST, instance=npc)
            if npc.user.pk == request.user.pk:
                npc.delete()
                messages.add_message(request, messages.SUCCESS, "NPC deleted!")
                return HttpResponseRedirect(reverse('characters:npc_detail'))
    else:
        raise Http404
    return render(request, 'characters/npc_delete.html', {'form': form, 'npc': npc})

@login_required
def player_delete(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.DeletePlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.DeletePlayerForm(request.POST, instance=player)
            if player.user.pk == request.user.pk:
                player.delete()
                messages.add_message(request, messages.SUCCESS, "Player deleted!")
                return HttpResponseRedirect(reverse('characters:player_detail'))
    else:
        raise Http404
    return render(request, 'characters/player_delete.html', {'form': form, 'player': player})

@login_required
def monster_copy(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.CopyMonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.CopyMonsterForm(request.POST, instance=monster)
            if monster.user.pk == request.user.pk:
                monster.pk = None
                monster.name = monster.name + "_Copy"
                monster.save()
                messages.add_message(request, messages.SUCCESS, "Monster Copied!")
                return HttpResponseRedirect(monster.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/monster_copy.html', {'form': form, 'monster': monster})


@login_required
def npc_copy(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.CopyNPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.CopyNPCForm(request.POST, instance=npc)
            if npc.user.pk == request.user.pk:
                npc.pk = None
                npc.name = npc.name + "_Copy"
                npc.save()
                messages.add_message(request, messages.SUCCESS, "NPC copied!")
                return HttpResponseRedirect(npc.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/npc_copy.html', {'form': form, 'npc': npc})


@login_required
def player_copy(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.CopyPlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.CopyPlayerForm(request.POST, instance=player)
            if player.user.pk == request.user.pk:
                player.pk = None
                player.player_name = player.player_name + "_Copy"
                player.save()
                messages.add_message(request, messages.SUCCESS, "Player copied!")
                return HttpResponseRedirect(player.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/player_copy.html', {'form': form, 'player': player})

@login_required
def monster_import(request):
    user_import = None
    form = forms.ImportMonsterForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return Http404
        form = forms.ImportMonsterForm(request.POST)
        if "monsters" in user_import: 
            for monster, monster_attributes in user_import["monsters"].items():
                new_monster = models.Monster(
                    user=request.user,
                    name=monster,
                    alignment=monster_attributes["alignment"],
                    size=monster_attributes["size"],
                    languages=monster_attributes["languages"],
                    strength=monster_attributes["strength"],
                    dexterity=monster_attributes["dexterity"],
                    constitution=monster_attributes["constitution"],
                    intelligence=monster_attributes["intelligence"],
                    wisdom=monster_attributes["wisdom"],
                    charisma=monster_attributes["charisma"],
                    armor_class=monster_attributes["armor_class"],
                    hit_points=monster_attributes["hit_points"],
                    speed=monster_attributes["speed"],
                    saving_throws=monster_attributes["saving_throws"],
                    skills=monster_attributes["skills"],
                    creature_type=monster_attributes["creature_type"],
                    damage_vulnerabilities=monster_attributes["damage_vulnerabilities"],
                    damage_immunities=monster_attributes["damage_immunities"],
                    damage_resistances=monster_attributes["damage_resistances"],
                    condition_immunities=monster_attributes["condition_immunities"],
                    senses=monster_attributes["senses"],
                    challenge_rating=monster_attributes["challenge_rating"],
                    traits=monster_attributes["traits"],
                    actions=monster_attributes["actions"]
                )
                new_monster.save()
            return HttpResponseRedirect('characters:monster_detail')
    return render(request, 'characters/monster_import.html', {'form': form, 'user_import': user_import})

@login_required
def npc_import(request):
    user_import = None
    form = forms.ImportNPCForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return Http404
        form = forms.ImportNPCForm(request.POST)
        if form.is_valid():
            if "npcs" in user_import:
                for npc, npc_attributes in user_import["npcs"].items():
                    new_npc = models.NPC(
                        user=request.user,
                        name=npc,
                        alignment=npc_attributes["alignment"],
                        size=npc_attributes["size"],
                        languages=npc_attributes["languages"],
                        strength=npc_attributes["strength"],
                        dexterity=npc_attributes["dexterity"],
                        constitution=npc_attributes["constitution"],
                        intelligence=npc_attributes["intelligence"],
                        wisdom=npc_attributes["wisdom"],
                        charisma=npc_attributes["charisma"],
                        armor_class=npc_attributes["armor_class"],
                        hit_points=npc_attributes["hit_points"],
                        speed=npc_attributes["speed"],
                        saving_throws=npc_attributes["saving_throws"],
                        skills=npc_attributes["skills"],
                        npc_class=npc_attributes["npc_class"],
                        age=npc_attributes["age"],
                        height=npc_attributes["height"],
                        weight=npc_attributes["weight"],
                        creature_type=npc_attributes["creature_type"],
                        damage_vulnerabilities=npc_attributes["damage_vulnerabilities"],
                        damage_immunities=npc_attributes["damage_immunities"],
                        damage_resistances=npc_attributes["damage_resistances"],
                        condition_immunities=npc_attributes["condition_immunities"],
                        senses=npc_attributes["senses"],
                        challenge_rating=npc_attributes["challenge_rating"],
                        traits=npc_attributes["traits"],
                        actions=npc_attributes["actions"],
                        notes=npc_attributes["notes"]
                    )
                    new_npc.save()
            return HttpResponseRedirect('characters:npc_detail')
    return render(request, 'characters/npc_import.html', {'form': form, 'user_import': user_import})

@login_required
def monster_export(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    monsters = sorted(models.Monster.objects.filter(user=user),
        key=lambda monster: monster.name.lower()
        )
    if monsters:
        for monster in monsters:
            monster.traits = json.dumps(monster.traits)
            monster.actions = json.dumps(monster.actions)
        return render(request, 'characters/monster_export.html', {'monsters': monsters})
    else:
        raise Http404

@login_required
def npc_export(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    npcs = sorted(models.NPC.objects.filter(user=user),
        key=lambda npc: npc.name.lower()
        )
    if npcs:
        for npc in npcs:
            npc.traits = json.dumps(npc.traits)
            npc.actions = json.dumps(npc.actions)
            npc.notes = json.dumps(npc.notes)
        return render(request, 'characters/npc_export.html', {'npcs': npcs})
    else:
        raise Http404