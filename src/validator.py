import json


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def no_empty(value):
    return isinstance(value, str) and value.strip() != ""
def enum(value,allowed_values):
    return value in allowed_values

VALIDATION_FUNCTIONS = {
    "non_empty_string": no_empty,
    "enum": enum
}


def validate_rule(rule, submission):
    field = rule["field"]
    value = submission.get(field)
    rule_type = rule["type"]
    func = VALIDATION_FUNCTIONS.get(rule_type)


    if rule_type == "enum":
     passed = func(value, rule.get("allowed_values", []))

    else: 
      passed = func(value)


    return {
        "rule_id": rule["id"],
        "field": field,
        "description": rule["description"],
        "value": value,
        "passed": passed,
        "color": rule["color"]  
    }


def validate_submission(rules, submission):
    return [validate_rule(rule, submission) for rule in rules]


if __name__ == "__main__":
    rules = load_json("rules/rules.json")
    submission = load_json("tests/valid_submission.json")

    results = validate_submission(rules, submission)

    for r in results:
        status = "PASSED" if r["passed"] else "FAILED"
        print(f"{r['rule_id']} → {status} (value={r['value']}, color={r['color']})")
