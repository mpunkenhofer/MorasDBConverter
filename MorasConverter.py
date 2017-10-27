# Author: Punkenhofer Mathias
# Mail: code.mpunkenhofer@gmail.com
# Date: 25.10.2017

import json


class MorasConverter:
    def __init__(self, metadata):
        self.moras_realm = {'All': 7, 'Alb': 1, 'Hib': 2, 'Mid': 4}

        if not metadata:
            raise ValueError('Need metadata file for conversion!')

        with open(metadata) as metadata_file:
            print("Loading '%s' ..." % metadata)
            self.metadata = json.load(metadata_file)

            if self.metadata:
                abilities = '' if 'abilities' not in self.metadata else self.metadata['abilities']
                self.positions = [] if 'position' not in abilities else abilities['position']
                self.magic_types = [] if 'magic_type' not in abilities else abilities['magic_type']
                self.spells = [] if 'spell' not in abilities else abilities['spell']
                req = '' if 'requirements' not in self.metadata else self.metadata['requirements']
                self.classes = [] if 'usable_by' not in req else req['usable_by']
                bonus_types = [] if 'bonus_types' not in self.metadata else self.metadata['bonus_types']
                self.stats = [] if '1' not in bonus_types and 'sub_types' not in bonus_types['1'] else bonus_types['1']['sub_types']
                self.skills = [] if '2' not in bonus_types and 'sub_types' not in bonus_types['2'] else bonus_types['2']['sub_types']
                self.resists = [] if '5' not in bonus_types and 'sub_types' not in bonus_types['5'] else bonus_types['5']['sub_types']
                self.focuses = [] if '6' not in bonus_types and 'sub_types' not in bonus_types['6'] else bonus_types['6']['sub_types']
                self.toa_arte = [] if '35' not in bonus_types and 'sub_types' not in bonus_types['35'] else bonus_types['35']['sub_types']
                # self.myth_resi_cap = [] if '57' not in bonus_types and 'sub_types' not in bonus_types['57'] else bonus_types['57']['sub_types']
                # self.myth_stat_cap = [] if '64' not in bonus_types and 'sub_types' not in bonus_types['64'] else bonus_types['64']['sub_types']
                # self.myth_reis_and_cap = [] if '68' not in bonus_types and 'sub_types' not in bonus_types['68'] else bonus_types['68']['sub_types']
                # self.myth_stat_and_cap = [] if '75' not in bonus_types and 'sub_types' not in bonus_types['75'] else bonus_types['75']['sub_types']

                print("Done loading '%s' ..." % metadata)

    @staticmethod
    def name(item):
        if not item or 'name' not in item:
            raise ValueError('Item has no name!')
        else:
            return item['name']

    @staticmethod
    def origin(item):
        if not item or 'sources' not in item:
            return ''
        else:
            sources = item['sources']
            origin = ''

            if 'monsters' in sources:
                origin += 'Dropped by:\n'
                monsters = sources['monsters']

                if 'normal_drop' in monsters:
                    origin += '\n'.join(monsters['normal_drop']) + '\n'

                if 'one_time_drop' in monsters:
                    origin += ' (OTD)\n'.join(monsters['one_time_drop']) + ' (OTD)\n'

            if 'quests' in sources:
                origin += 'Quests:\n'
                origin += '\n'.join(sources['quests']) + '\n'

            if 'stores' in sources:
                origin += 'Stores:\n'
                origin += '\n'.join(sources['stores']) + '\n'

            return origin

    @staticmethod
    def description(item):
        if not item:
            return ''

        description = ''

        '''
        if 'abilities' in item:
            description += 'Abilities:\n'

            abilities = item['abilities']
            
            for ability in abilities:
                if 'position' in ability and self.positions:
                    if str(ability['position']) in self.positions:
                        description += self.positions[str(ability['position'])] + ':\n'
                if 'spell' in ability and self.spells:
                    if str(ability['spell']) in self.spells:
                        description += self.spells[str(ability['spell'])] + '\n'
                if 'max_charges' in ability:
                    description += 'Max Charges: ' + str(ability['max_charges']) + '\n'
                if 'magic_type' in ability and self.magic_types:
                    if str(ability['magic_type']) in self.magic_types:
                        description += 'Effect: ' + self.magic_types[str(ability['magic_type'])] + '\n'
        '''

        if 'delve_text' in item:
            description += item['delve_text'] + '\n'

        return description

    def patch(self):
        return ''

    def class_restriction(self, item):
        if item and 'requirements' in item:
            if 'usable_by' in item['requirements']:
                classes = []

                if not self.classes:
                    return ''

                usable_by = item['requirements']['usable_by']

                for u in usable_by:
                    if str(u) in self.classes:
                        class_restriction = self.classes[str(u)].upper()
                        classes.append(class_restriction)

                return ';'.join(classes)

        return ''

    def bonuses(self, item):
        if item and 'bonuses' in item:
            item_stats = []
            bonuses = item['bonuses']

            stat_and_overcap = []

            for bonus in bonuses:
                if 'type' not in bonus or 'value' not in bonus:
                    raise ValueError('Item stats corrupt!')

                level_req = '0'

                if self.is_artifact(item):
                    if 'level_required' in bonus:
                        level_req = str(bonus['level_required'])

                stat_type = bonus['type']
                value = str(bonus['value'])
                stat_id = '' if 'id' not in bonus else str(bonus['id'])

                if not value:
                    raise ValueError('Item[%d] stat %d conversion error (stat without value)!' % (item['id'], stat_type))

                # STATS
                if stat_type == 1 and stat_id in self.stats:
                    item_stats.append(self.stats[stat_id].upper() + ':' + value + ':' + level_req)
                # SKILLS
                elif stat_type == 2 and stat_id in self.skills:
                    special_stats = {'300': 'ALL_MELEE_BONUS',
                                     '301': 'ALL_DUAL_WIELD_BONUS',
                                     '302': 'ALL_ARCHERY_BONUS',
                                     '303': 'ALL_MAGIC_BONUS'
                                     }

                    if stat_id in special_stats:
                        item_stats.append(special_stats[stat_id] + ':' + value + ':' + level_req)
                    else:
                        item_stats.append(self.skills[stat_id].replace(' ', '_').upper() + ':' + value + ':' + level_req)
                # HP
                elif stat_type == 4:
                    item_stats.append('HITPOINTS' + ':' + value + ':' + level_req)
                # RESITS
                elif stat_type == 5 and stat_id in self.resists:
                    item_stats.append('RES_' + self.resists[stat_id].upper() + ':' + value + ':' + level_req)
                # RESIST ID 0 issue (ignore resist)
                elif stat_type == 5 and stat_id == '0':
                    continue
                # FOCUSES
                elif stat_type == 6 and stat_id in self.focuses:
                    special_stats = {'303': 'ALL_MAGIC_FOCUS',  # All Casting
                                     '304': 'ALL_MAGIC_FOCUS'   # All Focus
                                     }

                    if stat_id in special_stats:
                        item_stats.append(special_stats[stat_id] + ':' + value + ':' + level_req)
                    else:
                        item_stats.append(self.focuses[stat_id].replace(' ', '_').upper() + '_FOCUS' + ':' + value + ':' + level_req)
                elif stat_type == 27:
                    item_stats.append('ARCHERY_SPELL_DAMAGE_BONUS' + ':' + value + ':' + level_req)
                # CAP STATS
                elif stat_type == 28 and stat_id in self.stats:
                    item_stats.append('CAP_' + self.stats[stat_id].upper() + ':' + value + ':' + level_req)
                # TOA ARTE
                elif stat_type == 35:
                    converted_stat = {'1': 'ARCANE_SIPHON',
                                      '2': '',  # Damage Conversion
                                      '3': '',  # Radiant Aura
                                      '4': '',  # XP Bonus
                                      '5': 'EXTRA_COINS',
                                      '6': 'REALM_POINT_BONUS',
                                      '7': ''  # BP Bonus
                                      }

                    if stat_id in converted_stat:
                        if not converted_stat[stat_id]:
                            continue
                        else:
                            item_stats.append(converted_stat[stat_id] + ':' + value + ':' + level_req)
                    else:
                        raise ValueError('Item Toa Arfifact stat %s conversion error (unknown stat)!' % stat_id)
                # OVERCAP RESITS
                elif stat_type == 57 and stat_id in self.resists:
                    item_stats.append('OVERCAP_RES_' + self.resists[stat_id].upper() + ':' + value + ':' + level_req)
                # OVERCAP STATS
                elif stat_type == 64 and stat_id in self.stats:
                    item_stats.append('OVERCAP_' + self.stats[stat_id].upper() + ':' + value + ':' + level_req)
                # OVERCAP RESITS AND CAP
                elif stat_type == 68 and stat_id in self.resists:
                    stat_and_overcap.append(('resist', self.resists[stat_id].upper(), value, level_req))
                # OVERCAP STATS AND CAP
                elif stat_type == 75 and stat_id in self.stats:
                    stat_and_overcap.append(('stat', self.stats[stat_id].upper(), value, level_req))
                # TOA
                else:
                    converted_stat = {8: 'MELEE_DAMAGE_BONUS',
                                      9: 'ARCHERY_SPELL_DAMAGE_BONUS',
                                      10: 'STYLE_DAMAGE_BONUS',
                                      11: 'ARCHERY_SPELL_RANGE_BONUS',
                                      12: 'ARCHERY_SPELL_RANGE_BONUS',
                                      13: 'SPELL_DURATION_BONUS',
                                      14: 'BUFF_BONUS',
                                      15: 'DEBUFF_BONUS',
                                      16: 'HEALING_BONUS',
                                      17: 'FATIGUE',
                                      19: 'MELEE_SPEED_BONUS',
                                      20: 'ARCHERY_CASTING_SPEED_BONUS',
                                      21: 'ARCHERY_CASTING_SPEED_BONUS',
                                      22: 'AF_BONUS',
                                      27: 'ARCHERY_SPELL_DAMAGE_BONUS',
                                      29: 'CAP_HITPOINTS',
                                      30: 'CAP_POWER_PERCENTAGE_BONUS',
                                      31: '',  # Toa Fatigue Cap
                                      32: 'REDUCE_MAGIC_RESISTS',
                                      34: 'POWER_PERCENTAGE_BONUS',
                                      37: 'SPELL_POWER_COST_REDUCTION',
                                      38: 'CONCENTRATION',
                                      40: 'HEALTH_REGEN',
                                      41: 'POWER_REGEN',
                                      42: 'PIERCE_ABLATIVE',
                                      44: 'DEATH_EXPIERIENCE_LOSS_REDUCTION',
                                      46: 'NEGATIVE_EFFECT_DURATION_REDUCTION',
                                      47: 'STYLE_COST_REDUCTION',
                                      48: 'TO_HIT_BONUS',
                                      49: 'DEFENSIVE_BONUS',
                                      50: 'BLADETURN_REINFORCEMENT',
                                      51: 'PARRY_BONUS',
                                      52: 'BLOCK_BONUS',
                                      53: 'EVADE_BONUS',
                                      54: 'REACTIONARY_STYLE_DAMAGE_BONUS',
                                      55: 'ENCUMBRANCE_INCREASE',  # mythical
                                      58: 'SIEGE_SPEED_BONUS',  # mythical
                                      60: 'PARRY_BONUS',  # mythical
                                      61: 'EVADE_BONUS',  # mythical
                                      62: 'BLOCK_BONUS',  # mythical
                                      63: 'EXTRA_COINS',  # mythical
                                      66: 'CROWD_CONTROL_REDUCTION',  # mythical
                                      67: 'ESSENCE_RESIST',  # mythical
                                      69: 'SIEGE_DAMAGE_REDUCTION',  # mythical
                                      71: 'DAMAGE_INCREASE',  # mythical
                                      72: 'REALM_POINT_BONUS',  # mythical
                                      73: '',  # Mythical Spell Focus
                                      74: '',  # Mythical Resurrection Sickness Reduction
                                      76: 'HEALTH_REGEN',  # mythical
                                      77: 'POWER_REGEN',  # mythical
                                      78: 'ENDURANCE_REGEN',  # mythical
                                      80: 'PHYSICAL_DAMAGE_DECREASE',  # mythical
                                      }

                    if stat_type in converted_stat:
                        if not converted_stat[stat_type]:
                            continue
                        else:
                            item_stats.append(converted_stat[stat_type] + ':' + value + ':' + level_req)
                    else:
                        raise ValueError('Item[%d] stat %d conversion error (unknown stat)!' % (item['id'], stat_type))

            for stat in stat_and_overcap:
                (stat_t, stat_n, stat_v, stat_lvl) = stat

                stat_name = ''
                stat_overcap_name = ''

                if stat_t == 'resist':
                    stat_name = 'RES_' + stat_n
                    stat_overcap_name = 'OVERCAP_RES_' + stat_n
                elif stat_t == 'stat':
                    stat_name = stat_n
                    stat_overcap_name = 'OVERCAP_' + stat_n
                else:
                    raise ValueError('Item[%d], Mythical stat %s conversion error!' % (item['id'], stat_t))

                # 1) look if the stat is already in item_stats
                # 2) if the stat is in there edit and add the value
                if not self.edit_stat(item_stats, stat_name, stat_v):
                    # 3) if it is not there add the stat
                    item_stats.append(stat_name + ':' + stat_v + ':' + stat_lvl)

                # 3) look if the over cap is already in item_stats
                # 4) if it is add the value
                if not self.edit_stat(item_stats, stat_overcap_name, stat_v):
                    # 5) if it is not there add the over cap
                    item_stats.append(stat_overcap_name + ':' + stat_v + ':' + stat_lvl)

            # in moras item only have 10 slots ... try to remove overcap res values
            if len(item_stats) > 10:
                while len(item_stats) > 10:
                    found = False

                    for s in item_stats:
                        if s.find("OVERCAP_RES") >= 0:
                            item_stats.remove(s)
                            found = True
                            break

                    if not found:
                        raise ValueError('Item[%d] has too many stats (could not fix)!' % item['id'])

            return ';'.join(item_stats)
        else:
            raise ValueError('Item[%d] has no stats!' % item['id'])

    @staticmethod
    def edit_stat(item_stats, stat_name, stat_value):
        for i, v in enumerate(item_stats):
            value_elements = v.split(':')
            if value_elements[0] == stat_name:
                new_value = str(int(value_elements[1]) + int(stat_value))
                item_stats[i] = value_elements[0] + ':' + new_value + ':' + value_elements[-1]
                return True
        return False

    def realm(self, item):
        if item and 'realm' in item:
            converted_realm = {0: self.moras_realm['All'],
                               1: self.moras_realm['Alb'],
                               2: self.moras_realm['Mid'],
                               3: self.moras_realm['Hib']}

            return converted_realm[item['realm']]
        else:
            raise ValueError('Item has no realm!')

    @staticmethod
    def level(item):
        if item and 'requirements' in item:
            if 'level_required' in item['requirements']:
                return item['requirements']['level_required']
        if item and 'bonus_level' in item:
            return item['bonus_level']

        return '0'  # default value

    @staticmethod
    def slot(item):
        if not item:
            return 0

        if 'slot' in item:
            '''  json file          moras (-1)
                "1": "Helm",        2
                "2": "Hands",       1
                "3": "Feet",        3
                "4": "Jewel",       13
                "5": "Torso",       6
                "6": "Cloak",       12
                "7": "Legs",        4
                "8": "Arms",        5
                "9": "Necklace",    11
                "12": "Belt",       14
                "13": "Bracer",     17
                "15": "Ring",       15
                "16": "Ring",       16
                "17": "Mythirian"   19
            '''
            converted_slot = {1: 1,
                              2: 0,
                              3: 2,
                              4: 12,
                              5: 5,
                              6: 11,
                              7: 3,
                              8: 4,
                              9: 10,
                              12: 13,
                              13: 16,
                              15: 14,
                              16: 15,
                              17: 18
                              }

            return converted_slot[item['slot']]

        if 'type_data' in item:
            return 6  # moras weapon

        if 'category' in item and item['category'] in [1, 4]:
            return 6  # identifying moras slot type via category (1: Weapon, 4: Instrument)

        return '0'

    @staticmethod
    def quality(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'base_quality' in type_data:
                return type_data['base_quality']

        return '100'  # default value

    @staticmethod
    def bonus(item):
        # TODO
        return '35'  # default value

    @staticmethod
    def dps(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'dps' in type_data:
                return type_data['dps']
            if 'clamped_dps' in type_data:
                return type_data['clamped_dps']

        return '0'  # default value

    @staticmethod
    def damage_type(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'damage_type' in type_data:
                # moras         daoc
                # 1 (slash)     2 (slash)
                # 2 (thrust)    3 (thrust)
                # 3 (crush)     1 (crush)
                #               10 (heat)
                #               5 (Crossbow of the Blackheart id: 41173)
                #               17 (Soul Flayer id: 58105)
                converted_damage_typ = {2: 1, 3: 2, 1: 3, 10: 1, 5: 3, 17: 3}

                if type_data['damage_type'] not in converted_damage_typ:
                    print(type_data['damage_type'])

                return converted_damage_typ[type_data['damage_type']]

        return '0'

    @staticmethod
    def speed(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'speed' in type_data:
                return type_data['speed']

        return '0'  # default value

    @staticmethod
    def armor_factor(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'armor_factor' in type_data:
                return type_data['armor_factor']
            if 'clamped_armor_factor' in type_data:
                return type_data['clamped_armor_factor']

        return '0'  # default value

    def item_class(self, item):
        if not item:
            return -1

        if 'type_data' in item:
            type_data = item['type_data']

            if 'shield_size' in type_data:
                # moras shield classes
                # small shield 6
                # med shield 7
                # large shield 8
                converted_shield_class = {1: 6, 2: 7, 3: 8}
                return converted_shield_class[type_data['shield_size']]

            if 'absorption' in type_data:
                # cloth, leather, studded, chain, plate
                converted_armor_class = {0: 0, 10: 1, 19: 2, 27: 3, 34: 4}
                return converted_armor_class[type_data['absorption']]

            converted_weapon_class = {
                'Staff':            5,
                'Slash':            14,
                'Slash Left':       15,
                'Crush':            16,
                'Crush Left':       17,
                'Thrust':           18,
                'Thrust Left':      19,
                'Polearm':          20,
                'Flexible':         21,
                'Two Handed':       22,
                'Longbow':          23,
                'Shortbow Alb':     24,
                'Crossbow':         25,
                # 'Quaterstaff':    26,
                'Flute Alb':        27,
                'Drum Alb':         28,
                'Lute Alb':         29,
                'Harp Alb':         30,
                'Fist Wraps Alb':   31,
                'Hand to Hand Alb': 32,  #
                'Mauler Staff Alb': 33,
                'Large Weaponry':   38,
                'Blades':           39,
                'Blades Left':      40,
                'Blunt':            41,
                'Blunt Left':       42,
                'Piercing':         43,
                'Piercing Left':    44,
                'Scythe':           45,
                'Celtic Spear':     46,
                'Shortbow Hib':     47,
                'Recurve Bow':      48,
                'Flute Hib':        49,
                'Drum Hib':         50,
                'Lute Hib':         51,
                'Harp Hib':         52,
                'Fist Wraps Hib':   53,
                'Hand to Hand Hib': 54,  #
                'Mauler Staff Hib': 55,
                'Sword':            60,
                'Sword 2h':         61,
                'Axe':              62,
                'Axe Left':         63,
                'Axe 2h':           64,
                'Hammer':           65,
                'Hammer 2h':        66,
                'Spear':            67,
                'Claw':             68,
                'Thrown Mid':       69,
                'Composite Bow':    70,
                'Fist Wraps Mid':   71,
                'Hand to Hand Mid': 72,  #
                'Mauler Staff Mid': 73,
                'Fist Wraps All':   53,
                'Hand to Hand All': 54,  #
                'Mauler Staff All': 55

            }

            skill_id = '' if 'skill_used' not in type_data else str(type_data['skill_used'])
            skill = '' if skill_id not in self.skills else self.skills[skill_id]

            '''
            if skill == 'Hand to Hand' and not self.left_handed(item):
                raise NotImplementedError("HAND TO HAND RIGHT")
            if skill == 'Fist Wraps' and not self.left_handed(item):
                raise NotImplementedError("FIST WRAPS RIGHT")
            '''

            if skill == 'Bow' and not self.two_handed(item):
                if self.albion(item):
                    skill = 'Shortbow Alb'
                elif self.hibernia(item):
                    skill = 'Shortbow Hib'

            if skill == 'Bow' and self.two_handed(item):
                if self.albion(item):
                    skill = 'Longbow'
                elif self.hibernia(item):
                    skill = 'Recurve Bow'
                elif self.midgard(item):
                    skill = 'Composite Bow'

            if self.two_handed(item) and not self.two_handed_skill(skill):
                skill += ' 2h'

            if self.left_handed(item) and skill not in ['Fist Wraps', 'Hand to Hand', 'Flexible']:
                # Workaround for left usable sword and hammers
                if skill in ['Sword', 'Hammer']:
                    skill = 'Axe'

                skill += ' Left'

            if skill == 'Thrown' and self.midgard(item):
                skill += ' Mid'

            if self.is_instrument(item):
                if self.midgard(item):
                    skill += ' Mid'
                elif self.hibernia(item):
                    skill += ' Hib'

            # Mauler stuff
            if skill in ['Fist Wraps', 'Hand to Hand', 'Mauler Staff']:
                if self.albion(item):
                    skill += ' Alb'
                elif self.hibernia(item):
                    skill += ' Hib'
                elif self.midgard(item):
                    skill += ' Mid'
                else:
                    skill += ' All'

            if skill not in converted_weapon_class:
                raise NotImplementedError('Item class [%s] for this type of item[%d] not implemented.' % (skill, item['id']))  # TODO
            else:
                weapon_item_class = converted_weapon_class[skill]
                return weapon_item_class

        # Instruments
        if 'category' in item and item['category'] == 4:
            item_name = '' if 'name' not in item else item['name']
            instrument_names = {
                'Drum': 'Drum',
                'Flute': 'Flute',
                'Pipe': 'Flute',
                'Lute': 'Lute',
                'Dirge': 'Harp',
                'Harp': 'Harp'
            }

            converted_instrument_class = {
                'Flute Alb':    27,
                'Drum Alb':     28,
                'Lute Alb':     29,
                'Harp Alb':     30,
                'Flute Hib':    49,
                'Drum Hib':     50,
                'Lute Hib':     51,
                'Harp Hib':     52
            }

            item_class_name = ''

            for n in instrument_names.keys():
                if item_name.find(n) != -1:
                    item_class_name = instrument_names[n]
                    break

            # Default Harp
            if not item_class_name:
                item_class_name = 'Harp'

            if self.albion(item):
                item_class_name += ' Alb'  # Harp Alb
            elif self.hibernia(item):
                item_class_name += ' Hib'  # Harp Hib
            else:
                item_class_name += ' Hib'  # Default Hib

            if item_class_name not in converted_instrument_class:
                raise NotImplementedError(
                    'Item class [%s] for this type of item[%d] not implemented.' % (item_class_name, item['id']))
            else:
                return converted_instrument_class[item_class_name]

        return -1

    def max_level(self, item):
        if self.is_artifact(item):
            return '10'

        return '0'

    @staticmethod
    def material(item):
        return '-1'

    @staticmethod
    def subclass(item):
        return '-1'

    @staticmethod
    def type(item):
        return '0'

    def all(self, item):
        return self.realm(item) == self.moras_realm['All']

    def albion(self, item):
        return self.realm(item) == self.moras_realm['Alb']

    def hibernia(self, item):
        return self.realm(item) == self.moras_realm['Hib']

    def midgard(self, item):
        return self.realm(item) == self.moras_realm['Mid']

    @staticmethod
    def two_handed_skill(skill):
        two_handed_skills = ['Staff',
                             'Mauler Staff',
                             'Large Weaponry',
                             'Celtic Spear',
                             'Spear',
                             'Composite Bow',
                             'Recurve Bow',
                             'Two Handed',
                             'Polearm',
                             'Longbow',
                             'Bow',
                             'Crossbow',
                             'Scythe'
                             ]

        return skill in two_handed_skills

    @staticmethod
    def two_handed(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'two_handed' in type_data:
                if type_data['two_handed'] == 1:
                    return True
        return False

    @staticmethod
    def left_handed(item):
        if item and 'type_data' in item:
            type_data = item['type_data']
            if 'left_handed' in type_data:
                if type_data['left_handed'] == 1:
                    return True
        return False

    def right_handed(self, item):
        return not self.two_handed(item) and not self.left_handed(item)

    @staticmethod
    def is_artifact(item):
        if item and 'artifact' in item:
            return item['artifact']

    @staticmethod
    def is_shield(item):
        if item and 'type_data' in item:
            type_data = item['tye_data']
            if 'shield_size' in type_data:
                return True
        return False

    @staticmethod
    def is_instrument(item):
        if item and 'category' in item:
            return item['category'] == 4
        return False

