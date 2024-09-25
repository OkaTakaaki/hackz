from django.shortcuts import render
from .forms import ThemeForm
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# モデルとトークナイザーをグローバルにロード
model_name = 'gpt2'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # GPU 使用可能なら使用
model = GPT2LMHeadModel.from_pretrained(model_name).to(device)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_motivational_text(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.cleaned_data['text']

            try:
                # テーマをトークナイズし、モデルで生成
                inputs = tokenizer.encode(theme, return_tensors='pt').to(device)
                outputs = model.generate(
                    inputs, 
                    max_length=150, 
                    num_return_sequences=1, 
                    no_repeat_ngram_size=2, 
                    early_stopping=True, 
                    temperature=0.7,  # ランダム性を抑える
                    top_k=50,         # トップ50単語から選択
                    top_p=0.9         # 確率質量の90%以内で選択
                )

                motivational_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            except Exception as e:
                motivational_text = f"エラーが発生しました: {str(e)}"

            # 結果をテンプレートに渡す
            return render(request, 'app/result.html', {'motivational_text': motivational_text})

    else:
        form = ThemeForm()

    return render(request, 'app/generate.html', {'form': form})
