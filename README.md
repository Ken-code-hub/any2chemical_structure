# 🧪 any2structure_chemistry ⚛️

## 🌟 概要

**Chemical Structure Generator** は、化学の世界をもっと身近にするためのツールです！🧪

化合物の **名前**、**SMILES文字列**、さらには **画像** から、美しい化学構造式を **瞬時に生成** します。

PubChemや最新のGemini API、そして強力なRDKitライブラリを活用し、直感的なGUI（Flet製）で誰でも簡単に操作できます。

## ✨ 主な特徴

*   **🧠 化合物名から自動生成:**
    *   一般的な名称やIUPAC名を入力するだけで、PubChem ([`ChemicalStructureGenerator.get_smiles_from_pubchem`](any2structure.py)) や Gemini ([`ChemicalStructureGenerator.get_smiles_from_gemini`](any2structure.py)) がSMILESを検索し、構造式を生成します。
*   **📝 SMILESから構造式を生成:**
    *   お手持ちのSMILES文字列を直接入力して、対応する構造式を画像化 ([`ChemicalStructureGenerator.generate_structure_image`](any2structure.py)) できます。
*   **🖼️ 画像から構造式を生成 (実験的機能):**
    *   手書きや既存の構造式画像からSMILESを抽出し、構造式を再生成 ([`ChemicalStructureGenerator.generate_smiles_from_image`](any2structure.py)) します。（⚠️ 現在、精度は不安定です）
*   **💾 GUI表示 & ファイル保存:**
    *   生成された構造式はアプリ画面に表示され、同時に画像ファイルとして保存 ([`ChemicalStructureGenerator.generate_structure_image`](any2structure.py)) されるため、レポート作成などにも便利です。

## 💻 必要な環境

*   🐍 **Python:** 3.13 (動作確認済み)
*   📚 **ライブラリ:** ([requirements.txt](requirements.txt) を参照)
    ```
    pubchempy>=1.0.4
    rdkit>=2024.9.5
    google-genai>=1.5.0
    Pillow>=11.1.0
    python-dotenv>=1.1.0
    flet>=0.27.6
    ```

## 🚀 インストール

1.  **リポジトリをクローン:** 
    ```bash
    git clone https://github.com/Ken-code-hub/any2structure_chemistry.git
    cd any2structure_chemistry
    ```
2.  **仮想環境の作成と有効化:**
    ```bash
    python -m venv venv
    # macOS / Linux
    source venv/bin/activate
    # Windows (Command Prompt or PowerShell)
    # .\venv\Scripts\activate
    ```
3.  **必要なライブラリをインストール:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **APIキーの設定:**
    *   プロジェクトルートに `.env` ファイルを作成します。
    *   以下の内容を記述し、`your-genai-api-key` をご自身のGemini APIキーに置き換えます。
        ```dotenv
        YOUR_API_KEY=your-genai-api-key
        ```
    *   APIキーは [Google AI Studio](https://aistudio.google.com) で無料で取得できます。

## ▶️ 使い方

1.  **アプリケーションを起動:**
    ```bash
    python main.py
    ```
2.  **入力タイプを選択:**
    *   ドロップダウンメニューから「化合物名」「SMILES」「画像ファイル」のいずれかを選びます。
3.  **情報を入力:**
    *   **化合物名:** テキストフィールドに化合物名（例: "Aspirin", "アスピリン"）を入力します。
    *   **SMILES:** テキストフィールドにSMILES文字列（例: `CC(=O)OC1=CC=CC=C1C(=O)O`）を入力します。
    *   **画像ファイル:** 「画像を選択...」ボタンをクリックし、構造式が描かれた画像ファイル（PNG, JPGなど）を選択します。
4.  **構造式を生成:**
    *   「構造式を生成」ボタンをクリックします。
5.  **結果を確認:**
    *   処理が完了すると、SMILES文字列と構造式画像が画面に表示されます。
    *   画像は `./img_flet/` ディレクトリにも自動で保存されます。

## ⚠️ 注意点

*   **🧪 GUIの安定性:** GUI部分は開発途上であり、予期せぬ動作をする可能性があります。
*   **💾 ファイル上書き:** SMILESや画像から生成した場合、ファイル名が `generated_structure.png` に固定されるため、連続して実行すると **前の画像が上書きされます**。ご注意ください。
*   **🔑 APIキー:** Gemini APIを利用するには、`.env` ファイルに有効なAPIキーを設定する必要があります。
*   **💰 API利用料金:** Gemini APIには無料枠がありますが、利用状況によっては料金が発生する可能性があります。詳細はGoogleの料金体系をご確認ください。
*   **🔬 生成精度:**
    *   生成される構造は、PubChemやGemini APIから得られる情報に依存します。特に **錯体** や複雑な構造では、期待通りの結果にならない場合があります。
    *   **画像からの生成 ([`ChemicalStructureGenerator.generate_smiles_from_image`](any2structure.py)) は特に実験的な機能であり、精度は保証されません。** 可能な限り、化合物名やSMILESでの入力を推奨します。
*   **⚡ 処理速度:** IUPAC名で入力すると、PubChemからの検索がヒットしやすく、高速に処理できる傾向があります。
*   **🌐 言語:** 日本語での化合物名入力も可能ですが、英語名の方が精度が高い場合があります。
*   **📜 ライセンス:**
    *   依存ライブラリのライセンスについては、[Notice.md](Notice.md) および `licences/` ディレクトリ内のファイルをご確認ください。
    *   本ソフトウェアの使用によって生じたいかなる損害についても、開発者は責任を負いません。詳細は [LICENSE](LICENSE) をご確認ください。

## 📄 ライセンス

[LICENSE](LICENSE) (BSD 3-Clause License)
