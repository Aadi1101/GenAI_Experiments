import streamlit as st
import random
import json
import string
from faker import Faker
import re

fake = Faker()

st.set_page_config(page_title="Multi-Object Swagger Mock Generator", layout="wide")
st.title("🧱 Multi-Object Swagger Mock Data Generator")

st.markdown("Define **multiple object types** like `User`, `Product`, etc., with fields, conditional logic, and custom formatting. Optionally, upload an existing JSON to auto-fill field structure.")

FIELD_TYPES = [
    "String", "Full Name", "Email", "Username", "Integer",
    "Float", "Boolean", "UUID", "DateTime",
    "Custom Choice", "Custom Format"
]

# Function to generate values based on custom format pattern
def custom_format_generator(pattern: str):
    def gen():
        result = ""
        regex_range = re.compile(r"{range:(\\d+)-(\\d+)}")
        regex_varnum = re.compile(r"{varnum:(\\d+)-(\\d+)}")

        i = 0
        while i < len(pattern):
            if pattern[i:i+7] == "{digit}":
                result += str(random.randint(0, 9))
                i += 7
            elif pattern[i:i+7] == "{alpha}":
                result += random.choice(string.ascii_uppercase)
                i += 7
            elif pattern[i:i+6] == "{word}":
                result += fake.word()
                i += 6
            elif pattern[i:i+6] == "{uuid}":
                result += fake.uuid4()
                i += 6
            elif match := regex_range.match(pattern[i:]):
                min_val, max_val = map(int, match.groups())
                result += str(random.randint(min_val, max_val))
                i += match.end()
            elif match := regex_varnum.match(pattern[i:]):
                min_len, max_len = map(int, match.groups())
                length = random.randint(min_len, max_len)
                result += ''.join(random.choices(string.digits, k=length))
                i += match.end()
            else:
                result += pattern[i]
                i += 1
        return result
    return gen

# Function to parse conditional rules
def parse_rules(text):
    parsed = []
    for line in text.strip().splitlines():
        if "then" in line:
            condition, result = line.split("then", 1)
            condition = condition.strip().removeprefix("if").strip()
            if "=" in result:
                field, val = result.split("=", 1)
                parsed.append((condition, field.strip(), val.strip().strip("'\"")))
    return parsed

# File upload and session state setup
if "parsed_objects" not in st.session_state:
    st.session_state.parsed_objects = {}
if "object_names" not in st.session_state:
    st.session_state.object_names = []

uploaded_json = st.file_uploader("📁 Upload a JSON file to infer fields", type=["json"])

if uploaded_json:
    if st.button("Process Uploaded JSON"):
        try:
            loaded_data = json.load(uploaded_json)
            parsed_objects = {}
            object_names = []
            for obj, entries in loaded_data.items():
                object_names.append(obj)
                if isinstance(entries, list) and entries:
                    sample = entries[0]
                    inferred_fields = {}
                    for k, v in sample.items():
                        if isinstance(v, str) and re.match(r"\d{3}-\d{4,15}", v):
                            inferred_fields[k] = "Custom Format"
                        elif isinstance(v, str) and "@" in v:
                            inferred_fields[k] = "Email"
                        elif isinstance(v, str):
                            inferred_fields[k] = "String"
                        elif isinstance(v, int):
                            inferred_fields[k] = "Integer"
                        elif isinstance(v, float):
                            inferred_fields[k] = "Float"
                        elif isinstance(v, bool):
                            inferred_fields[k] = "Boolean"
                        else:
                            inferred_fields[k] = "String"
                    parsed_objects[obj] = inferred_fields
            st.session_state.parsed_objects = parsed_objects
            st.session_state.object_names = object_names
            st.success("✅ JSON processed and fields inferred.")
        except Exception as e:
            st.error(f"Failed to parse uploaded JSON: {e}")

parsed_objects = st.session_state.get("parsed_objects", {})
object_names = st.session_state.get("object_names", [])

num_objects = st.number_input("How many object types do you want to define?", 1, 5, value=len(object_names) if object_names else 1)
final_data = {}

for obj_index in range(num_objects):
    st.markdown("---")
    suggested_name = object_names[obj_index] if obj_index < len(object_names) else f"Object{obj_index+1}"
    obj_name = st.text_input(f"🔹 Object #{obj_index + 1} name", value=suggested_name, key=f"obj_name_{obj_index}")
    num_records = st.slider(f"Number of records for `{obj_name}`", 1, 20, 5, key=f"num_records_{obj_index}")

    prefill_fields = list(parsed_objects.get(obj_name, {}).items()) if parsed_objects else []
    num_fields = st.selectbox(f"How many fields in `{obj_name}`?", range(1, 11), key=f"num_fields_{obj_index}", index=len(prefill_fields) if prefill_fields else 0)

    custom_fields = []

    st.markdown(f"### ✏️ Fields for `{obj_name}`")
    for i in range(num_fields):
        st.markdown(f"**Field #{i+1}**")
        col1, col2 = st.columns(2)

        prefill_name, prefill_type = prefill_fields[i] if i < len(prefill_fields) else (f"field{i+1}", "")

        with col1:
            key_name = st.text_input("Field name", value=prefill_name, key=f"{obj_index}_key_{i}")
        with col2:
            key_type = st.selectbox("Type", ["", *FIELD_TYPES], index=FIELD_TYPES.index(prefill_type) + 1 if prefill_type in FIELD_TYPES else 0, key=f"{obj_index}_type_{i}")

        field_generator = lambda: None

        if not key_name:
            continue

        if not key_type:
            custom_fields.append((key_name, key_type, lambda: None))
            continue

        if key_type == "Integer":
            min_val = st.number_input(f"Min for `{key_name}`", 0, 1000, 0, key=f"{obj_index}_min_{i}")
            max_val = st.number_input(f"Max for `{key_name}`", 0, 1000, 100, key=f"{obj_index}_max_{i}")
            field_generator = lambda a=min_val, b=max_val: random.randint(int(a), int(b))

        elif key_type == "Custom Choice":
            choices_raw = st.text_input(f"Choices (comma-separated)", key=f"{obj_index}_choices_{i}")
            choices = [c.strip() for c in choices_raw.split(",") if c.strip()]
            if choices:
                field_generator = lambda c=choices: random.choice(c)

        elif key_type == "Custom Format":
            pattern = st.text_input("Pattern", key=f"{obj_index}_pattern_{i}")
            if pattern:
                field_generator = custom_format_generator(pattern)

        elif key_type in FIELD_TYPES:
            field_mapping = {
                "String": lambda: fake.word(),
                "Full Name": lambda: fake.name(),
                "Email": lambda: fake.email(),
                "Username": lambda: fake.user_name(),
                "Float": lambda: round(random.uniform(1.0, 100.0), 2),
                "Boolean": lambda: random.choice([True, False]),
                "UUID": lambda: fake.uuid4(),
                "DateTime": lambda: fake.iso8601()
            }
            field_generator = field_mapping.get(key_type, lambda: None)

        custom_fields.append((key_name, key_type, field_generator))

    st.markdown(f"### ⚙️ Conditional Fields for `{obj_name}`")
    use_conditional = st.checkbox(f"Add conditional fields to `{obj_name}`?", key=f"{obj_index}_cond_toggle")
    conditional_rules = []
    dynamic_type_rules = []

    if use_conditional:
        st.markdown("#### Field Value Rules")
        raw_rules = st.text_area("Rules (e.g. `if age < 18 then category = minor`)", height=120, key=f"{obj_index}_cond_rules")
        conditional_rules = parse_rules(raw_rules)

        st.markdown("#### Field Type Rules")
        num_type_rules = st.number_input("How many type override rules?", 0, 5, 0, key=f"type_rule_count_{obj_index}")
        for tr in range(num_type_rules):
            col1, col2 = st.columns(2)
            with col1:
                field_name = st.text_input("Field Name", key=f"type_field_{obj_index}_{tr}")
            with col2:
                override_type = st.selectbox("Override Type", FIELD_TYPES, key=f"type_override_{obj_index}_{tr}")
            if field_name and override_type:
                condition = ""
                for cond_line in raw_rules.strip().splitlines():
                    if f"{field_name} =" in cond_line:
                        condition_part = cond_line.split("then")[0].replace("if", "").strip()
                        condition = condition_part
                        break
                if condition:
                    dynamic_type_rules.append((field_name, condition, override_type))

    def generate_field_by_type(field_type, key):
        if field_type == "Integer":
            return random.randint(0, 100)
        elif field_type == "String":
            return fake.word()
        elif field_type == "Full Name":
            return fake.name()
        elif field_type == "Email":
            return fake.email()
        elif field_type == "Username":
            return fake.user_name()
        elif field_type == "Float":
            return round(random.uniform(1.0, 100.0), 2)
        elif field_type == "Boolean":
            return random.choice([True, False])
        elif field_type == "UUID":
            return fake.uuid4()
        elif field_type == "DateTime":
            return fake.iso8601()
        elif field_type == "Custom Format":
            pattern = "{range:100-400}-{varnum:4-15}"
            return custom_format_generator(pattern)()
        elif field_type == "Custom Choice":
            return random.choice(["A", "B", "C"])
        return None

    def generate_record(fields, rules, type_rules):
        rec = {}

        # Initial generation
        for k, t, gen in fields:
            val = gen() if gen else None
            rec[k] = val

        # Override type logic
        for field, cond, new_type in type_rules:
            try:
                if eval(cond, {}, rec):
                    rec[field] = generate_field_by_type(new_type, field)
            except:
                pass

        for condition, field, value in rules:
            try:
                if eval(condition, {}, rec):
                    rec[field] = value
            except:
                rec[field] = None

        return rec

    if st.button(f"Generate `{obj_name}` Data", key=f"generate_btn_{obj_index}"):
        records = [generate_record(custom_fields, conditional_rules, dynamic_type_rules) for _ in range(num_records)]
        final_data[obj_name] = records

if final_data:
    st.success("🎉 All objects generated successfully!")
    st.subheader("📆 Final Output")
    st.json(final_data)

    st.download_button("📅 Download Full JSON", json.dumps(final_data, indent=2), "mock_schema.json", "application/json")
