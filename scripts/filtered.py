import os
import shutil


def main():
    resumes_path = "./resumes/original/"
    destination = "./resumes/filtered/"

    files_name = os.listdir(resumes_path)

    if os.path.isdir(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    for txt in files_name:
        if not txt.endswith(".txt"):
            continue

        lab = txt.replace(".txt", ".lab")

        with open(
            os.path.join(resumes_path, txt), "r", encoding="windows-1252"
        ) as file:
            content = file.read().replace("\n", ",")

        with open(
            os.path.join(resumes_path, lab), "r", encoding="windows-1252"
        ) as file:
            label = file.read().replace("\n", ",")

        if len(content) <= 0 or len(label) <= 0:
            continue

        with open(os.path.join(destination, txt), "w", encoding="utf-8") as file:
            file.write(content)

        with open(os.path.join(destination, lab), "w", encoding="utf-8") as file:
            file.write(label)


if __name__ == "__main__":
    main()
