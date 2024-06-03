import os
import xml.etree.ElementTree as ET

# Đường dẫn tệp và thư mục đầu ra
base_folder = os.environ.get('KRDICT_BASE_FOLDER', os.path.abspath(os.path.dirname(__file__)))
xml_folder = os.path.join(base_folder, "data", "xml_20240601", "1_5000_20240601.xml")
output_path = os.path.join(base_folder, "data", "result.txt")

# Kiểm tra sự tồn tại của tệp
if not os.path.exists(xml_folder):
    raise FileNotFoundError(f"Tệp không tồn tại: {xml_folder}")

# Từ loại tiếng Việt
pos_mapping = {
    "명사": "Danh từ",
    "대명사": "Đại từ",
    "수사": "Số từ",
    "조사": "Trợ từ",
    "동사": "Động từ",
    "형용사": "Tính từ",
    "관형사": "Định từ",
    "부사": "Phó từ",
    "감탄사": "Thán từ",
    "접사": "Phụ tố",
    "의존 명사": "Danh từ phụ thuộc",
    "보조 동사": "Động từ bổ trợ",
    "보조 형용사": "Tính từ bổ trợ",
    "어미": "Vĩ tố",
    "품사 없음": "Không có từ loại"
}

# Cấp độ từ vựng
vocabulary_level_mapping = {
    "초급": "☆☆☆",
    "중급": "☆☆",
    "고급": "☆",
    "없음": ""
}

def parse_lexical_entry(lexical_entry):
    result = []

    # Lấy các thông tin cơ bản từ LexicalEntry
    written_form = lexical_entry.find("Lemma/feat[@att='writtenForm']").get('val', '') if lexical_entry.find("Lemma/feat[@att='writtenForm']") is not None else ''
    homonym_number = lexical_entry.find("feat[@att='homonym_number']").get('val', '') if lexical_entry.find("feat[@att='homonym_number']") is not None else ''
    vocabulary_level = lexical_entry.find("feat[@att='vocabularyLevel']").get('val', '') if lexical_entry.find("feat[@att='vocabularyLevel']") is not None else ''
    vocabulary_level_star = vocabulary_level_mapping.get(vocabulary_level, '')
    part_of_speech = lexical_entry.find("feat[@att='partOfSpeech']").get('val', '') if lexical_entry.find("feat[@att='partOfSpeech']") is not None else ''
    pos_vietnamese = pos_mapping.get(part_of_speech, part_of_speech)

    # Xử lý origin
    origin_text = ""
    origin = lexical_entry.find("feat[@att='origin']")
    if origin is not None:
        origin_val = origin.get('val', '')
        if origin_val:
            origin_text = f" ({origin_val})"

    # Xây dựng chuỗi kết quả ban đầu
    result.append(f"{written_form}={written_form}{homonym_number}{origin_text} {vocabulary_level_star}")

    pronunciation = ""
    word_forms = lexical_entry.findall("WordForm")
    word_form_data = []
    if word_forms is not None:
        for word_form in word_forms:
            type_feat = word_form.find("feat[@att='type']")
            if type_feat is not None and type_feat.get('val') == '발음':
                pronunciation_feat = word_form.find("feat[@att='pronunciation']")
                pronunciation = pronunciation_feat.get('val', '') if pronunciation_feat is not None else ''
                if pronunciation:
                    result.append(f"\tPhát âm\t[{pronunciation}]")
            if type_feat is not None and type_feat.get('val') == '활용':
                written_form_val = word_form.find("feat[@att='writtenForm']").get('val', '') if word_form.find("feat[@att='writtenForm']") is not None else ''
                pronunciation_feat = word_form.find("feat[@att='pronunciation']")
                pronunciation_val = pronunciation_feat.get('val', '') if pronunciation_feat is not None else ''
                form_repr = word_form.find("FormRepresentation/feat[@att='writtenForm']")
                if form_repr is not None:
                    form_written_form = form_repr.get('val', '')
                    form_pronunciation_feat = word_form.find("FormRepresentation/feat[@att='pronunciation']")
                    form_pronunciation = form_pronunciation_feat.get('val', '') if form_pronunciation_feat is not None else ''
                    word_form_data.append(f"{written_form_val}[{pronunciation_val}]({form_written_form}[{form_pronunciation}])")
                else:
                    word_form_data.append(f"{written_form_val}[{pronunciation_val}]")

    if word_form_data:
        result.append(f"\tỨng dụng\t{', '.join(word_form_data)}")

    # Xử lý các phần tử annotation chung
    general_annotation = lexical_entry.find("feat[@att='annotation']")
    if general_annotation is not None:
        annotation_text = general_annotation.get('val', '')
        result.append(f"\tTham khảo toàn bộ\t{annotation_text}")

    # Xử lý RelatedForm
    related_forms = lexical_entry.findall("RelatedForm")
    related_form_data = []
    for related_form in related_forms:
        if related_form.find("feat[@att='type']").get('val') == '파생어':
            written_form = related_form.find("feat[@att='writtenForm']").get('val', '')
            related_form_data.append(written_form)
        elif related_form.find("feat[@att='type']").get('val') == '☞(가 보라)':
            written_form = related_form.find("feat[@att='writtenForm']").get('val', '')
            result.append(f"☞ {written_form}")

    if related_form_data:
        result.append(f"Từ phái sinh {', '.join(related_form_data)}")

    result.append(f"\tTừ loại\t「{part_of_speech}」 {pos_vietnamese}")

    # Duyệt qua các phần tử Sense
    sense_val = ""
    senses = lexical_entry.findall("Sense")
    for sense in senses:
        if len(senses) > 1:
            sense_val = sense.get('val', '')
            if sense_val:
                sense_val = f"{sense_val}. "

        vietnamese_equivalent = ""
        equivalent_elements = sense.findall("Equivalent")
        for equivalent in equivalent_elements:
            if equivalent.find("feat[@att='language']").get('val') == '베트남어':
                vietnamese_equivalent = equivalent.find("feat[@att='lemma']").get('val', '')

        sense_definition = sense.find("feat[@att='definition']").get('val', '') if sense.find("feat[@att='definition']") is not None else ''
        vietnamese_definition = ""
        for equivalent in equivalent_elements:
            if equivalent.find("feat[@att='language']").get('val') == '베트남어':
                vietnamese_definition = equivalent.find("feat[@att='definition']").get('val', '')

        result.append(f"{sense_val}{vietnamese_equivalent}")
        result.append(f"\t{sense_definition}")
        result.append(f"\t{vietnamese_definition}")

        # Duyệt qua các ví dụ trong Sense
        examples = sense.findall("SenseExample")
        for example in examples:
            example_text = example.find("feat[@att='example']").get('val', '') if example.find("feat[@att='example']") is not None else ''
            result.append(f"\t* {example_text}")

        # Xử lý Multimedia
        multimedia_elements = sense.findall("Multimedia")
        multimedia_data = []
        for i, multimedia in enumerate(multimedia_elements, start=1):
            label = multimedia.find("feat[@att='label']").get('val', '')
            multimedia_data.append(label)
        if multimedia_data:
            result.append(f"\nĐa truyền thông {len(multimedia_data)}\n" + "\t".join(multimedia_data))

        # Xử lý syntacticPattern
        syntactic_patterns = sense.findall("feat[@att='syntacticPattern']")
        if syntactic_patterns:
            patterns = [pattern.get('val', '') for pattern in syntactic_patterns]
            result.append(f"Cấu trúc ngữ pháp {', '.join(patterns)}")

        # Xử lý syntacticAnnotation
        syntactic_annotation = sense.find("feat[@att='syntacticAnnotation']")
        if syntactic_annotation is not None:
            annotation_text = syntactic_annotation.get('val', '')
            result.append(f"Tham khảo cấu trúc ngữ pháp {annotation_text}")

        # Xử lý các phần tử SenseRelation
        sense_relations = sense.findall("SenseRelation")
        for relation in sense_relations:
            relation_type = relation.find("feat[@att='type']").get('val', '')
            if relation_type == '참고어':
                lemma = relation.find("feat[@att='lemma']").get('val', '')
                homonym_number = relation.find("feat[@att='homonymNumber']").get('val', '') if relation.find("feat[@att='homonymNumber']") is not None else ''
                result.append(f"\tTừ tham khảo {lemma}{homonym_number}")
            elif relation_type == '동의어':
                lemma = relation.find("feat[@att='lemma']").get('val', '')
                result.append(f"\tTừ đồng nghĩa {lemma}")
            elif relation_type == '상위어':
                lemma = relation.find("feat[@att='lemma']").get('val', '')
                result.append(f"\tCấp trên {lemma}")
            elif relation_type == '하위어':
                lemma = relation.find("feat[@att='lemma']").get('val', '')
                result.append(f"\tCấp dưới {lemma}")
            elif relation_type == '유의어':
                lemma = relation.find("feat[@att='lemma']").get('val', '')
                result.append(f"\tTừ đồng nghĩa {lemma}")

        # Thêm chú thích nếu có
        annotation = sense.find("feat[@att='annotation']")
        if annotation is not None:
            annotation_text = annotation.get('val', '')
            result.append(f"\t* Tham khảo {annotation_text}")

    return '\n'.join(result)

# Đọc và phân tích tệp XML
tree = ET.parse(xml_folder)
root = tree.getroot()

# Duyệt qua từng LexicalEntry và ghi kết quả vào tệp
with open(output_path, 'w', encoding='utf-8') as f:
    for lexical_entry in root.findall(".//LexicalEntry"):
        entry_data = parse_lexical_entry(lexical_entry)
        f.write(entry_data + '\n')

print(f"Kết quả đã được lưu vào {output_path}")
