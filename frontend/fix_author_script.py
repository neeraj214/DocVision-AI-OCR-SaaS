import os
import subprocess

# Define the email and name
CORRECT_NAME = "Neeraj Negi"
CORRECT_EMAIL = "neerajnegi108333@gmail.com"

# The command to run in the shell
# We use simple quotes for the shell command part
env_filter = (
    f"GIT_AUTHOR_NAME='{CORRECT_NAME}'; "
    f"GIT_AUTHOR_EMAIL='{CORRECT_EMAIL}'; "
    f"GIT_COMMITTER_NAME='{CORRECT_NAME}'; "
    f"GIT_COMMITTER_EMAIL='{CORRECT_EMAIL}';"
)

command = [
    "git", "filter-branch", "--force",
    "--env-filter", env_filter,
    "--tag-name-filter", "cat",
    "--", "origin/main..HEAD"
]

print(f"Running: {' '.join(command)}")
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
if result.returncode != 0:
    print("Error executing filter-branch")
