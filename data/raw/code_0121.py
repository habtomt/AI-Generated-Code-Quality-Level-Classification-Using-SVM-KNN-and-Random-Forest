from googletrans import Translator
import sys

translator = Translator()

def parse_srt(content):
    blocks = content.strip().split("\n\n")
    subtitles = []

    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            index = lines[0]
            timecode = lines[1]
            text = " ".join(lines[2:])
            subtitles.append((index, timecode, text))
    return subtitles

def translate_text(text, target_lang):
    try:
        return translator.translate(text, dest=target_lang).text
    except Exception:
        return text

def build_srt(subtitles, target_lang):
    output_blocks = []

    for index, timecode, text in subtitles:
        translated = translate_text(text, target_lang)
        block = f"{index}\n{timecode}\n{translated}"
        output_blocks.append(block)

    return "\n\n".join(output_blocks)

def translate_srt_file(input_path, output_path, target_lang):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    subtitles = parse_srt(content)
    translated_srt = build_srt(subtitles, target_lang)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated_srt)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py input.srt output.srt target_lang")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    lang = sys.argv[3]

    translate_srt_file(input_file, output_file, lang)