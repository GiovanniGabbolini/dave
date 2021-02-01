from src.data import data

df = data.the_chain()

# df = df.head(200).tail(100)
s = ""
count = 1
for t, a, l in zip(df.track_name, df.artist_name, df.links[1:]):
    s += f"\n\n {count}) {t} by {a} \n\n   link: {l}"
    count += 1
print(s)
