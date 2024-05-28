import bson


def generate_test_id():
    return "test-" + str(bson.ObjectId())


def generate_test_step_id():
    return "step-" + str(bson.ObjectId())


def generate_test_sceenshot_id():
    return "screenshot-" + str(bson.ObjectId())


def generate_test_run_id():
    return "run-" + str(bson.ObjectId())


def get_user_test_id(user_id: str, test_id: str) -> str:
    return f"{user_id}_{test_id}"
