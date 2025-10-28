from collections import defaultdict

def analyze_stroop_file(filename):
    count_1 = 0
    count_2 = 0
    pair_counts = defaultdict(int)
    stimulus_counts = defaultdict(int)
    right_1_counts = defaultdict(int)  # _right.jpg с индикатором 1
    right_2_counts = defaultdict(int)  # _right.jpg с индикатором 2
    color_counts = defaultdict(int)  # _color.jpg с индикатором 2

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("'"):
                continue

            parts = line.split(',,')
            if len(parts) >= 2:
                stimulus = parts[0].strip()
                indicator = parts[1].replace(',', '').strip()

                if indicator == '1':
                    count_1 += 1
                elif indicator == '2':
                    count_2 += 1

                full_stimulus = f"{stimulus},,{indicator},"
                stimulus_counts[full_stimulus] += 1

                if '_right.jpg' in stimulus:
                    if indicator == '1':
                        right_1_counts[stimulus] += 1
                    elif indicator == '2':
                        right_2_counts[stimulus] += 1
                else:
                    color_counts[stimulus] += 1

    stimuli_sequence = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("'"):
                continue
            stimuli_sequence.append(line)

    for i in range(len(stimuli_sequence) - 1):
        current_line = stimuli_sequence[i]
        next_line = stimuli_sequence[i + 1]

        current_parts = current_line.split(',,')
        next_parts = next_line.split(',,')

        if len(current_parts) >= 2 and len(next_parts) >= 2:
            current_stimulus = current_parts[0].strip()
            current_indicator = current_parts[1].replace(',', '').strip()
            next_stimulus = next_parts[0].strip()
            next_indicator = next_parts[1].replace(',', '').strip()

            if (current_stimulus == next_stimulus and
                    current_indicator == '1' and
                    next_indicator == '2'):
                pair_counts[current_stimulus] += 1

    print(f"\nОБЩАЯ СТАТИСТИКА:")
    print(f"Количество стимулов с индикатором 1: {count_1}")
    print(f"Количество стимулов с индикатором 2: {count_2}")
    print(f"Общее количество стимулов: {count_1 + count_2}")

    print(f"\nПОСЛЕДОВАТЕЛЬНЫЕ ПАРЫ (id:1, id:2):")
    if pair_counts:
        total_pairs = 0
        for stimulus, count in sorted(pair_counts.items()):
            print(f"  {stimulus} - пар: {count}")
            total_pairs += count
        print(f"Всего пар: {total_pairs}")
    else:
        print("  Последовательных пар (id:1, id:2) не найдено.")

    print(f"\nРАСПРЕДЕЛЕНИЕ СТИМУЛОВ ПО НАЗВАНИЯМ:")

    print(f"\nСтимулы _right.jpg с индикатором 1:")
    if right_1_counts:
        for stimulus, count in sorted(right_1_counts.items()):
            print(f"  {stimulus} - {count} шт.")
    else:
        print("  Не найдено")

    print(f"\nСтимулы _right.jpg с индикатором 2:")
    if right_2_counts:
        for stimulus, count in sorted(right_2_counts.items()):
            print(f"  {stimulus} - {count} шт.")
    else:
        print("  Не найдено")

    print(f"\nСтимулы _color.jpg с индикатором 2:")
    if color_counts:
        for stimulus, count in sorted(color_counts.items()):
            print(f"  {stimulus} - {count} шт.")
    else:
        print("  Не найдено")

    print(f"\nСВОДНАЯ СТАТИСТИКА ПО ТИПАМ:")
    total_right_1 = sum(right_1_counts.values())
    total_right_2 = sum(right_2_counts.values())
    total_color = sum(color_counts.values())

    print(f"Всего _right.jpg с индикатором 1: {total_right_1}")
    print(f"Всего _right.jpg с индикатором 2: {total_right_2}")
    print(f"Всего _color.jpg с индикатором 2: {total_color}")

filename = "stroop_25_random.seq"
analyze_stroop_file(filename)