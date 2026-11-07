import logging
import os
import shutil

CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"],
}
SKIP_FILES = ["desktop.ini", "thumbs.db"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(SCRIPT_DIR, "organizer.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


def say(message):
    # prints and logs at the same time
    print(message)
    logging.info(message)


def get_category(ext):
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def unique_path(folder, name):
    # if file.txt already exists, use file (1).txt, file (2).txt ...
    base, ext = os.path.splitext(name)
    path = os.path.join(folder, name)
    count = 1
    while os.path.exists(path):
        path = os.path.join(folder, f"{base} ({count}){ext}")
        count += 1
    return path


def organize(folder, dry_run):
    summary = {}
    errors = 0

    with os.scandir(folder) as it:
        files = [e for e in it if e.is_file()]

    for entry in files:
        name = entry.name
        if name.startswith(".") or name.lower() in SKIP_FILES:
            continue
        if os.path.abspath(entry.path) == os.path.abspath(__file__):
            continue

        category = get_category(os.path.splitext(name)[1].lower())
        dest_folder = os.path.join(folder, category)

        if dry_run:
            say(f"[DRY RUN] {name} -> {category}/")
            summary[category] = summary.get(category, 0) + 1
            continue

        try:
            os.makedirs(dest_folder, exist_ok=True)
            dest = unique_path(dest_folder, name)
            shutil.move(entry.path, dest)
            say(f"Moved {name} -> {category}/{os.path.basename(dest)}")
            summary[category] = summary.get(category, 0) + 1
        except (FileExistsError, PermissionError) as e:
            errors += 1
            say(f"Skipped {name}: {e}")
        except OSError as e:
            errors += 1
            say(f"Error with {name}: {e}")

    return summary, errors


def main():
    folder = input("Folder to organize (e.g. C:\\Users\\DELL\\Downloads): ").strip().strip('"')
    if not os.path.isdir(folder):
        print("That folder does not exist")
        return

    dry_run = input("Dry run first? (y/n): ").strip().lower() == "y"
    summary, errors = organize(folder, dry_run)

    total = sum(summary.values())
    say("")
    say("----- Summary -----")
    for category, count in summary.items():
        say(f"{category}: {count}")
    say(f"Total files {'to move' if dry_run else 'moved'}: {total}")
    say(f"Errors: {errors}")


main()