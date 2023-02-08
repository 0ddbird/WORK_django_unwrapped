import json

from controller import extract_from_folder
from encoder import ClassDataEncoder


def export_to_json(extracted_classes):
    with open("exports/extracted_classes.json", "w") as f:
        json.dump(extracted_classes, f, cls=ClassDataEncoder)


def main():
    extracted_classes = extract_from_folder()
    extracted_classes_to_dict = {
        k: [v.to_dict() for v in v] for k, v in extracted_classes.items()
    }
    export_to_json(extracted_classes_to_dict)


if __name__ == "__main__":
    main()
