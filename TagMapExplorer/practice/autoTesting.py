import subprocess


def run_tests():
    result = subprocess.run(['pytest', '--html=report.html', 'testingTrial.py'], capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    run_tests()