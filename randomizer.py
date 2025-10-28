from collections import defaultdict
import random

def distribute_randomly_no_repeats(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    header_lines = []
    data_lines = []
    in_header = True
    found_stimuli_sequence = False

    for line in all_lines:
        if in_header:
            if "' Stimuli sequence" in line:
                found_stimuli_sequence = True
                header_lines.append(line)
            elif found_stimuli_sequence and line.strip() == "'":
                header_lines.append(line)
                in_header = False
            else:
                header_lines.append(line)
        else:
            data_lines.append(line.strip())

    lines = [line for line in data_lines if line.strip() and not line.strip().startswith("'")]

    # три типа строк
    right_pairs = []  # пары color_right (1 и 2) - как единый блок
    single_rights = []  # Одиночные color_right
    color_lines = []  # color_color строки

    i = 0
    while i < len(lines):
        line = lines[i]

        if '_right.jpg' in line:
            if (i + 1 < len(lines) and
                    '_right.jpg' in lines[i + 1] and
                    line.split('_')[0] == lines[i + 1].split('_')[0] and
                    line.endswith(',1,') and
                    lines[i + 1].endswith(',2,')):

                right_pairs.append([line, lines[i + 1]])
                i += 2
            else:
                single_rights.append(line)
                i += 1
        else:
            color_lines.append(line)
            i += 1

    print(f"Найдено пар color_right: {len(right_pairs)}")
    print(f"Найдено одиночных color_right: {len(single_rights)}")
    print(f"Найдено color_color: {len(color_lines)}")

    all_items = []

    for pair in right_pairs:
        all_items.append(('pair_block', pair))

    for single in single_rights:
        all_items.append(('single_right', single))

    for color in color_lines:
        all_items.append(('color_color', color))

    def can_insert(sequence, item, position):
        if position > 0:
            left_neighbor = sequence[position - 1]
            if get_content(left_neighbor) == get_content(item):
                return False

        if position < len(sequence):
            right_neighbor = sequence[position]
            if get_content(right_neighbor) == get_content(item):
                return False

        return True

    def get_content(item):
        if isinstance(item, tuple):
            item_type, content = item
            if item_type == 'pair_block':
                return content[0]
            return content
        return item

    def flatten_sequence(sequence):
        result = []
        for item in sequence:
            if isinstance(item, tuple):
                item_type, content = item
                if item_type == 'pair_block':
                    result.extend(content)
                else:
                    result.append(content)
            else:
                result.append(item)
        return result

    final_sequence = []
    random.shuffle(all_items)

    for item in all_items:
        if not final_sequence:
            final_sequence.append(item)
            continue

        possible_positions = []

        for pos in range(len(final_sequence) + 1):
            if can_insert(final_sequence, item, pos):
                possible_positions.append(pos)

        if possible_positions:
            pos = random.choice(possible_positions)
            final_sequence.insert(pos, item)
        else:
            best_pos = 0
            min_conflicts = float('inf')

            for pos in range(len(final_sequence) + 1):
                conflicts = 0

                if pos > 0:
                    left_neighbor = final_sequence[pos - 1]
                    if get_content(left_neighbor) == get_content(item):
                        conflicts += 1

                if pos < len(final_sequence):
                    right_neighbor = final_sequence[pos]
                    if get_content(right_neighbor) == get_content(item):
                        conflicts += 1

                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_pos = pos
            final_sequence.insert(best_pos, item)
    final_lines = flatten_sequence(final_sequence)

    def is_part_of_pair(index, lines):
        if index < 0 or index >= len(lines) - 1:
            return False

        current_line = lines[index]
        next_line = lines[index + 1]

        return ('_right.jpg,,1,' in current_line and
                '_right.jpg,,2,' in next_line and
                current_line.split('_')[0] == next_line.split('_')[0])
    i = 1
    max_attempts = len(final_lines) * 2
    attempt = 0

    while i < len(final_lines) and attempt < max_attempts:
        attempt += 1

        if final_lines[i] == final_lines[i - 1]:
            current_in_pair = is_part_of_pair(i, final_lines)
            prev_in_pair = is_part_of_pair(i - 1, final_lines)

            if not current_in_pair and not prev_in_pair:
                found_swap = False
                for j in range(i + 1, len(final_lines)):
                    j_in_pair = is_part_of_pair(j, final_lines)
                    j_prev_in_pair = is_part_of_pair(j - 1, final_lines) if j > 0 else False

                    if (not j_in_pair and not j_prev_in_pair and
                            final_lines[j] != final_lines[i - 1] and
                            (j == len(final_lines) - 1 or final_lines[j] != final_lines[j + 1]) and
                            (j == 0 or final_lines[j - 1] != final_lines[i])):
                        final_lines[i], final_lines[j] = final_lines[j], final_lines[i]
                        found_swap = True
                        break

                if not found_swap:
                    for j in range(i + 1, len(final_lines)):
                        j_in_pair = is_part_of_pair(j, final_lines)
                        j_prev_in_pair = is_part_of_pair(j - 1, final_lines) if j > 0 else False

                        if not j_in_pair and not j_prev_in_pair and final_lines[j] != final_lines[i - 1]:
                            final_lines[i], final_lines[j] = final_lines[j], final_lines[i]
                            found_swap = True
                            break
        i += 1
    repeat_count = 0
    for i in range(1, len(final_lines)):
        if final_lines[i] == final_lines[i - 1]:
            repeat_count += 1

    print(f"Финальное количество повторений: {repeat_count}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in header_lines:
            f.write(line)

        for line in final_lines:
            f.write(line + '\n')

    return final_lines

input_file = 'stroop_25_converted.seq'
output_file = 'stroop_25_random.seq'

result = distribute_randomly_no_repeats(input_file, output_file)
print(f"Рандомизация завершена. Результат сохранен в {output_file}")
print(f"Всего строк в результате: {len(result)}")

print("\nПодробная проверка пар:")
pair_count = 0
for i in range(len(result) - 1):
    if ('_right.jpg,,1,' in result[i] and '_right.jpg,,2,' in result[i + 1] and
            result[i].split('_')[0] == result[i + 1].split('_')[0]):
        pair_count += 1
        print(f"Пара {pair_count}: {result[i]} -> {result[i + 1]}")

print(f"\nИтого найдено пар: {pair_count}")
print(f"Ожидалось пар: 40")

if pair_count == 40:
    print("✓ Все пары сохранены!")
else:
    print(f"⚠ Проблема: потеряно {40 - pair_count} пар!")

repeats = 0
for i in range(1, len(result)):
    if result[i] == result[i - 1]:
        repeats += 1

if repeats == 0:
    print("✓ Повторений нет!")
else:
    print(f"⚠ Осталось повторений: {repeats}")