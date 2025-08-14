
### remover isso
def compare_dicts(dict1, dict2):
    for key in dict1.keys():
        if key not in dict2.keys() or dict1[key] != dict2[key]:
            return False
    return True


def generate_problemFile(items):
    lines = []
    # Parse the file into lines

    for keys in items:
        items[keys] = int(items[keys])

    n_box1 = items['cx1_peq_metal'] + items['cx1_med_metal'] + items['cx1_grd_metal'] + items['cx1_peq'] + items[
        'cx1_med'] + items['cx1_grd']
    n_box2 = items['cx2_peq_metal'] + items['cx2_med_metal'] + items['cx2_grd_metal'] + items['cx2_peq'] + items[
        'cx2_med'] + items['cx2_grd']
    n_box3 = items['cx3_peq_metal'] + items['cx3_med_metal'] + items['cx3_grd_metal'] + items['cx3_peq'] + items[
        'cx3_med'] + items['cx3_grd']

    n_peq_metal = items['cx1_peq_metal'] + items['cx2_peq_metal'] + items['cx3_peq_metal']
    n_med_metal = items['cx1_med_metal'] + items['cx2_med_metal'] + items['cx3_med_metal']
    n_grd_metal = items['cx1_grd_metal'] + items['cx2_grd_metal'] + items['cx3_grd_metal']

    n_peq = items['cx1_peq'] + items['cx2_peq'] + items['cx3_peq']
    n_med = items['cx1_med'] + items['cx2_med'] + items['cx3_med']
    n_grd = items['cx1_grd'] + items['cx2_grd'] + items['cx3_grd']

    n_items = sum(items.values())

    with open('problem-template.pddl', 'r') as f:
        for line in f:
            #if line.startswith('	##definir_itens'):
            #    line = '        '
            #    for x in range(n_items):
            #        line = line + 'item' + str(x) + ' '
            #    line += '- item'

            if line.startswith('	##definir_tipos'):
                line = '        '
                num = 0
                tipo_items = {}
                for x in range(n_peq_metal):
                    line = line + 'item' + str(num) + ' - peqmet)\n        '
                    tipo_items['item' + str(num)] = 'peqmet'
                    num += 1

                for x in range(n_med_metal):
                    line = line + 'item' + str(num) + ' - medmet)\n        '
                    tipo_items['item' + str(num)] = 'medmet'
                    num += 1

                for x in range(n_grd_metal):
                    line = line + 'item' + str(num) + ' - grdmet)\n        '
                    tipo_items['item' + str(num)] = 'grdmet'
                    num += 1

                for x in range(n_peq):
                    line = line + 'item' + str(num) + ' - peqnmet)\n        '
                    tipo_items['item' + str(num)] = 'peqnmet'
                    num += 1

                for x in range(n_med):
                    line = line + 'item' + str(num) + ' - mednmet)\n        '
                    tipo_items['item' + str(num)] = 'mednmet'
                    num += 1

                for x in range(n_grd):
                    line = line + ' item' + str(num) + ' - grdnmet)\n        '
                    tipo_items['item' + str(num)] = 'grdnmet'
                    num += 1

            #if line.startswith('	##definir_inicio'):
            #    if n_items > 0:
            #        line = '        (at inicio item0)'

            if line.startswith('	##definir_inicio'):
                for x in range(n_items - 1):
                    line = '        (at inicio item' + ')\n        '

            if line.startswith('	##definir_destino'):
                line = '        '

                key_list = list(tipo_items.keys())

                for keys in items:
                    match keys:
                        case 'cx1_peq_metal':
                            for x in range(items['cx1_peq_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('peqmet')
                                tipo_items[key_list[position]] = 'box1'

                        case 'cx1_med_metal':
                            for x in range(items['cx1_med_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('medmet')
                                tipo_items[key_list[position]] = 'box1'

                        case 'cx1_grd_metal':
                            for x in range(items['cx1_grd_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('grdmet')
                                tipo_items[key_list[position]] = 'box1'

                        case 'cx1_peq':
                            for x in range(items['cx1_peq']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('peqnmet')
                                tipo_items[key_list[position]] = 'box1'

                        case 'cx1_med':
                            for x in range(items['cx1_med']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('mednmet')
                                tipo_items[key_list[position]] = 'box1'

                        case 'cx1_grd':
                            for x in range(items['cx1_grd']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('grdnmet')
                                tipo_items[key_list[position]] = 'box1'

                        case 'cx2_peq_metal':
                            for x in range(items['cx2_peq_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('peqmet')
                                tipo_items[key_list[position]] = 'box2'

                        case 'cx2_med_metal':
                            for x in range(items['cx2_med_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('medmet')
                                tipo_items[key_list[position]] = 'box2'

                        case 'cx2_grd_metal':
                            for x in range(items['cx2_grd_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('grdmet')
                                tipo_items[key_list[position]] = 'box2'

                        case 'cx2_peq':
                            for x in range(items['cx2_peq']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('peqnmet')
                                tipo_items[key_list[position]] = 'box2'

                        case 'cx2_med':
                            for x in range(items['cx2_med']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('mednmet')
                                tipo_items[key_list[position]] = 'box2'

                        case 'cx2_grd':
                            for x in range(items['cx2_grd']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('grdnmet')
                                tipo_items[key_list[position]] = 'box2'

                        case 'cx3_peq_metal':
                            for x in range(items['cx3_peq_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('peqmet')
                                tipo_items[key_list[position]] = 'box3'

                        case 'cx3_med_metal':
                            for x in range(items['cx3_med_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('medmet')
                                tipo_items[key_list[position]] = 'box3'

                        case 'cx3_grd_metal':
                            for x in range(items['cx3_grd_metal']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('grdmet')
                                tipo_items[key_list[position]] = 'box3'

                        case 'cx3_peq':
                            for x in range(items['cx3_peq']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('peqnmet')
                                tipo_items[key_list[position]] = 'box3'

                        case 'cx3_med':
                            for x in range(items['cx3_med']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('mednmet')
                                tipo_items[key_list[position]] = 'box3'

                        case 'cx3_grd':
                            for x in range(items['cx3_grd']):
                                val_list = list(tipo_items.values())
                                position = val_list.index('grdnmet')
                                tipo_items[key_list[position]] = 'box3'

                # for x in range(n_box1):
                #   line += '(at box1 ' +
                for key, value in tipo_items.items():
                    line += '(at ' + value + ' ' + key + ')' + '\n        '

            lines.append(line)

    # Write them back to the file
    with open('problem.pddl', 'w') as f:
        f.writelines(lines)

