import json
import sys


class InputDefinition:

    def build(self, filepath=None):
        store = self.build_language_map("languages.txt")
        definition = {}
        definition["frames"] = [{
            "name": "language",
            "options": {
                "timeQuantum": "YMD",
                "inverseEnabled": True,
                "cacheType": "ranked"
            }
        },
            {
                "name": "stargazer",
                "options": {
                    "timeQuantum": "YMD",
                    "inverseEnabled": True,
                    "cacheType": "ranked"
                }

            }]

        definition["fields"] = [
            {
                "name": "repo_id",
                "primaryKey": True
            },
            {
                "name": "language_id",
                "actions": [
                    {
                        "frame": "language",
                        "valueDestination": "mapping",
                        "valueMap": store
                    }
                ]
            },
            {
                "name": "stargazer_id",
                "actions": [
                    {
                        "frame": "stargazer",
                        "valueDestination": "value-to-row"
                    }
                ]
            }
        ]
        input_def = json.dumps(definition, indent=4, sort_keys=True)
        if filepath:
            inputDef_file = open(filepath, "w")
            inputDef_file.write(input_def)
        else:
            print(input_def)


    def build_language_map(cls, fname):
        store = {}
        with open(fname) as f:
            content = f.readlines()
        for i, x in enumerate(content):
            store[x.strip()] = i
        return store

def main():
    st = InputDefinition()
    if len(sys.argv) == 2:
        st.build(sys.argv[1])
    else:
        st.build()

if __name__ == '__main__':
    main()
