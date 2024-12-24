import inflect

p = inflect.engine()

word = "economists"
singular_word = p.singular_noun(word)
print(singular_word)
if singular_word:
    print(f"The singular form of '{word}' is '{singular_word}'.")
else:
    print(f"'{word}' is already in singular form or not recognized.")

