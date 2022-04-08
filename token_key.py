import random
import string

print(
    f"Your token key: {''.join([random.choice(string.ascii_letters) for _ in range(50)])}"
)
