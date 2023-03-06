s = input("Enter a string: ")
choice = int(input("Enter a number to find the nth most repeated element in the string: "))
if choice < 1:
    print("Invalid choice. Please enter a number greater than or equal to 1.")
else:
    counts = {c: s.count(c) for c in set(s)}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    if choice > len(sorted_counts):
        print(f"There are only {len(sorted_counts)} unique elements in the string.")
    else:
        nth_most_repeated = sorted_counts[choice - 1][0]
        count = sorted_counts[choice - 1][1]
        print(f"The {choice}nd most repeated element in the string is '{nth_most_repeated}' \
        with a count of {count}.")
