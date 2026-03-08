import difflib


def show_diff(old_code, new_code):

    diff = difflib.unified_diff(
        old_code.splitlines(),
        new_code.splitlines(),
        lineterm=""
    )

    for line in diff:
        print(line)


def apply_patch(file_path, new_code):

    confirm = input("\nApply this change? (y/n): ")

    if confirm.lower() == "y":
        with open(file_path, "w") as f:
            f.write(new_code)

        print("Change applied.")

    else:
        print("Change rejected.")