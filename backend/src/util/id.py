import bson


def generate_test_id():
    return "test-" + str(bson.ObjectId())

def generate_test_step_id():
    return "step-" + str(bson.ObjectId())

def generate_test_sceenshot_id():
    return "screenshot-" + str(bson.ObjectId())

def generate_test_run_id():
    return "run-" + str(bson.ObjectId())

