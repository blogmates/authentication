import argparse
import subprocess

def build_image():
    print("Building Docker image...")
    subprocess.run(["docker", "build", "-t", "my-flask-app", "."])

def run_container():
    print("Running Docker container...")
    subprocess.run(["docker", "run", "-p", "5000:5000", "my-flask-app"])

def main():
    parser = argparse.ArgumentParser(description="Build and run Docker image for Flask app")
    parser.add_argument("-b", "--build", action="store_true", help="Build Docker image")
    parser.add_argument("-r", "--run", action="store_true", help="Run Docker container")
    args = parser.parse_args()

    if args.build:
        build_image()

    if args.run:
        run_container()

    if not args.build and not args.run:
        print("Please provide at least one of the following arguments: -b, -r")

if __name__ == "__main__":
    main()
