from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = Flask(__name__)

# Load the NLLB-200 model
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

@app.route("/")
def home():
    return jsonify({"status": "✅ NLLB Translator is running!"})

@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()
        text = data.get("text")
        source_lang = data.get("source_lang")
        target_lang = data.get("target_lang")

        if not text or not source_lang or not target_lang:
            return jsonify({
                "error": "Please provide 'text', 'source_lang', and 'target_lang'."
            }), 400

        tokenizer.src_lang = source_lang
        encoded = tokenizer(text, return_tensors="pt").to(device)
        generated = model.generate(
            **encoded,
            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
            max_length=512
        )
        translation = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

        return jsonify({
            "input": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "translation": translation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
