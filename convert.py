with open("google-10000-english-usa-no-swears-medium.txt", "r") as f:
    words = f.read().splitlines()
    with open("words.txt", "w") as f2:
        f2.write("words = [\n")
        for word in words:
            f2.write("\"" + word + "\",")
        f2.write("\n]\n")
