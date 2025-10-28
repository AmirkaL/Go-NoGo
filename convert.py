def convert_existing_stimuli(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = []
    stimuli = []

    in_stimuli = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("' Stimuli sequence") or stripped.startswith("'Stimuli sequence"):
            in_stimuli = True
            header.append(line.rstrip())
        elif in_stimuli and stripped and not stripped.startswith("'"):
            if stripped.endswith(','):
                stimuli.append(stripped)
        else:
            header.append(line.rstrip())

    print(f"Найдено стимулов: {len(stimuli)}")

    congruent_count = sum(1 for s in stimuli if s.endswith(',,1,'))
    incongruent_count = sum(1 for s in stimuli if s.endswith(',,2,'))
    print(f"Исходное распределение: конгруентных={congruent_count}, инконгруентных={incongruent_count}")

    congruent_by_color = {'white': [], 'red': [], 'yellow': [], 'blue': [], 'green': []}

    for i, stim in enumerate(stimuli):
        if stim.endswith(',,1,'):
            color = stim.split('_')[0]
            if color in congruent_by_color:
                congruent_by_color[color].append(i)

    positions_to_convert = []

    for color, indices in congruent_by_color.items():
        if len(indices) >= 8:
            step = len(indices) // 8
            selected_indices = [indices[i * step] for i in range(8)]
            positions_to_convert.extend(selected_indices)
        else:
            print(f"Недостаточно стимулов для цвета {color}: {len(indices)}")

    print(f"Выбрано для преобразования: {len(positions_to_convert)} стимулов")

    converted_count = 0
    for pos in positions_to_convert:
        if pos < len(stimuli) and stimuli[pos].endswith(',,1,'):
            stimuli[pos] = stimuli[pos].replace(',,1,', ',,2,')
            converted_count += 1
    i = 0
    while i < len(stimuli) - 1:
        current_stim = stimuli[i]
        next_stim = stimuli[i + 1]
        if (current_stim.endswith(',,1,') and
                next_stim.endswith(',,2,') and
                current_stim.split('_')[0] == next_stim.split('_')[0]):
            i += 2
        elif (current_stim.endswith(',,2,') and
              i > 0 and
              stimuli[i - 1].endswith(',,1,') and
              current_stim.split('_')[0] == stimuli[i - 1].split('_')[0]):
            i += 1
        elif (current_stim.endswith(',,2,') and
              current_stim.split('_')[0] in ['white', 'red', 'yellow', 'blue', 'green']):
            color = current_stim.split('_')[0]
            for j in range(len(stimuli)):
                if (j != i and
                        stimuli[j].endswith(',,1,') and
                        stimuli[j].split('_')[0] == color and
                        (j == len(stimuli) - 1 or not stimuli[j + 1].endswith(',,2,'))):
                    moved_stim = stimuli.pop(i)
                    stimuli.insert(j + 1, moved_stim)
                    break
            i += 1
        else:
            i += 1

    for i, line in enumerate(header):
        if line.startswith('StimulNumber='):
            header[i] = f'StimulNumber={len(stimuli)}'
            break

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(header))
        f.write('\n')
        for stim in stimuli:
            f.write(stim + '\n')

    final_congruent = sum(1 for s in stimuli if s.endswith(',,1,'))
    final_incongruent = sum(1 for s in stimuli if s.endswith(',,2,'))

    print(f"\nРезультат:")
    print(f"Всего стимулов: {len(stimuli)}")
    print(f"Конгруентных: {final_congruent}")
    print(f"Инконгруентных: {final_incongruent}")
    print(f"Преобразовано: {converted_count} стимулов")
    print(f"Файл сохранен как: {output_file}")

input_file = "stroop_25.seq"
output_file = "stroop_25_converted.seq"

convert_existing_stimuli(input_file, output_file)