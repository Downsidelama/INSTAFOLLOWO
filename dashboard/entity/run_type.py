class RunType:
    run_types = {"hashtag": "Hashtag", "other_profile": "Other Profile"}

    @staticmethod
    def get_run_types():
        return RunType.run_types.keys()

    @staticmethod
    def get_run_types_description():
        return RunType.run_types.values()

    @staticmethod
    def get_types_and_descriptions():
        return RunType.run_types

    @staticmethod
    def get_run_type_description(run_type):
        if run_type in RunType.run_types.keys():
            return RunType.run_types.get(run_type)
        else:
            return None
