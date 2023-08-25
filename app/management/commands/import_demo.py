import os
import json

from typing import Any
from django.core.management import BaseCommand
from app.models import (
    Application,
    Contract,
    Customership,
    Directory,
    Integration,
    License,
    Provider,
    Server,
    Service,
)


class Importer:
    help = 'This is an import class that imports default json data.'

    def __init__(self, json_keyword, class_name):
        self.script_dir = os.path.dirname(__file__)
        self.rel_path = f"import_data/{json_keyword}.json"
        self.abs_file_path = os.path.join(self.script_dir, self.rel_path)
        self.json_keyword = json_keyword
        self.class_name = class_name
        self.obj_data = {}

    def read_data(self) -> Any:
        """Fetches the json file and returns it in readable format."""
        with open(self.abs_file_path, "r") as json_file:
            data = json.load(json_file)
            return data

    def process_data(self) -> None:
        """Processes and creates the objects."""
        data = self.read_data()

        for json_pk, obj_values in data[self.json_keyword].items():
            class_obj = self.class_name()
            for field, field_value in obj_values.items():
                setattr(class_obj, field, field_value)

            class_obj.save()

            print(f"Created object: {json_pk} / {class_obj.base_id} / {class_obj.name}")

            json_template = {
                json_pk: {
                    'generated_id': class_obj.base_id,
                    'relations': getattr(class_obj, "relation_fields", {}),
                    'json_kw': self.json_keyword,
                }
            }

            self.obj_data.update(json_template)


class Command(BaseCommand):
    help = 'This importer runs everything.'

    def __init__(self):
        self.all_objs = {}
        self.references = {
            'applications': Application,
            'contracts': Contract,
            'customerships': Customership,
            'directories': Directory,
            'integrations': Integration,
            'licenses': License,
            'providers': Provider,
            'servers': Server,
            'services': Service,
        }

    def fetch_relation(self, obj_pk: str) -> Any:
        """Shared logic for fetching relation objects."""
        rel_pk = self.all_objs[obj_pk]
        return self.references[rel_pk['json_kw']].objects.get(pk=rel_pk['generated_id'])

    def relation_handler(self) -> None:
        """Core logic for establishing relations."""

        for json_pk, pk_data in self.all_objs.items():
            # Example: {'lcn_1': {'generated_id': 'lcn-9ss-3vSpN8w', 'relations': {'contract': 'con_1'}}}

            main_obj = self.references[pk_data['json_kw']].objects.get(
                pk=pk_data['generated_id']
            )
            for relation_field, relation_dt in pk_data['relations'].items():
                # Example: 'relations': {'contract': 'con_1'}

                if relation_dt:
                    # Ignore empty lists and null values.
                    if isinstance(relation_dt, list):
                        for obj_pk in relation_dt:
                            # Handle multiple objects. Example: ['ser_1', 'ser_2']
                            getattr(main_obj, relation_field).add(
                                self.fetch_relation(obj_pk)
                            )
                    else:
                        # Handle single objects. Example: 'srv_1'
                        setattr(
                            main_obj, relation_field, self.fetch_relation(relation_dt)
                        )
            main_obj.save()
            print(f"Successfully established all relations for {json_pk}")

    def handle(self, *args, **options) -> None:
        """Handle function. Called first when ran."""

        for json_reference, reference_model in self.references.items():
            import_class = Importer(
                json_keyword=json_reference, class_name=reference_model
            )
            import_class.process_data()

            self.all_objs.update(import_class.obj_data)

        self.relation_handler()
        print("Importer completed.")
