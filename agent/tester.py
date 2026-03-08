import subprocess


def run_tests():

    try:
        result = subprocess.run(
            ["pytest"],
            capture_output=True,
            text=True
        )

        return result.stdout + result.stderr

    except FileNotFoundError:
        return "pytest not found. No tests executed."