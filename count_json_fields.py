import os
import ijson
from collections import defaultdict

base_folder = os.environ.get('KRDICT_BASE_FOLDER', os.path.abspath(os.path.dirname(__file__)))
json_folder = os.path.join(base_folder, "data", "json_20240319")
json_file_path = os.path.join(json_folder, "1_5000_20240319.json")
output_path = os.path.join(base_folder, "data", "static", "fields.txt")
type_value_stats_path = os.path.join(base_folder, "data", "static", "type_value_stats.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)


#Hàm đếm tần suất trường mà không quan tâm vị trí
def print_keys_recursively(prefix, obj, output_file, stats):
    if isinstance(obj, dict):
        for key, value in obj.items():
            stats[key] += 1
            if key == 'att':
                stats[f"{key}.{value}"] += 1
            if isinstance(value, dict) or isinstance(value, list):
                print_keys_recursively(f"{prefix}.{key}", value, output_file, stats)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            print_keys_recursively(f"{prefix}.{i}", item, output_file, stats)


#Hàm đếm tần suất giá trị của trường val cùng cấp với trường att có giá trị type mà không quan tâm vị trí
def count_type_values(prefix, obj, type_value_stats):
    if isinstance(obj, dict):
        if "att" in obj and obj["att"] == "type" and "val" in obj:
            type_value_stats[obj['val']] += 1
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict) or isinstance(value, list):
                count_type_values(new_prefix, value, type_value_stats)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            count_type_values(f"{prefix}.{i}", item, type_value_stats)


with open(json_file_path, 'rb') as f, open(output_path, 'w', encoding='utf-8') as output_file:
    objects = ijson.items(f, '')
    stats = defaultdict(int)
    for obj in objects:
        print_keys_recursively('', obj, output_file, stats)
    output_file.write("\nThống kê:\n\n")
    max_key_length = max(len(key) for key in stats.keys())
    for key, count in stats.items():
        output_file.write(f"{key.ljust(max_key_length)} Tần suất: {count}\n")


with open(json_file_path, 'rb') as f, open(type_value_stats_path, 'w', encoding='utf-8') as type_value_stats_file:
    objects = ijson.items(f, '')
    type_value_stats = defaultdict(int)
    for obj in objects:
        count_type_values('', obj, type_value_stats)
    type_value_stats_file.write("\nThống kê giá trị:\n\n")
    for key, count in type_value_stats.items():
        type_value_stats_file.write(f"{key.ljust(max_key_length)} Tuần suất: {count}\n")