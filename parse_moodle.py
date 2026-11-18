import re, html

with open('Course_ COS360 - Otimização (ECI) + COM361 - Introd. à Otimização (ECA) - 2026_2 _ Moodle PESC.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# remove script and style
text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)

# Let's extract the main region
main = re.search(r'<div[^>]*role="main"[^>]*>(.*?)</div>\s*</section>', text, re.DOTALL)
if not main:
    main_text = text
else:
    main_text = main.group(1)

clean = re.sub(r'<[^>]+>', '\n', main_text)
lines = [html.unescape(l.strip()) for l in clean.split('\n') if l.strip()]
# filter out UI clutter
filtered = []
for l in lines:
    if l in ['Topic outline', 'General', 'Home', 'Dashboard', 'My courses', 'Close course index', 'Open course index']:
        continue
    filtered.append(l)

print(f"Total lines: {len(filtered)}")
with open('moodle_clean_text.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(filtered))

print("Written to moodle_clean_text.txt. Let's see some key parts:")
for i, l in enumerate(filtered[:120]):
    print(f"{i}: {l}")
