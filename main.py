import flet as ft
from any2structure import ChemicalStructureGenerator # 既存のバックエンドクラスをインポート
import os
import base64 # 画像をBase64エンコードするために追加

# 画像をBase64にエンコードするヘルパー関数
def image_to_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

def main(page: ft.Page):
    page.title = "Chemical Structure Generator"
    page.vertical_alignment = ft.MainAxisAlignment.START

    generator = ChemicalStructureGenerator() # バックエンドクラスのインスタンス化

    # --- UI要素 ---
    input_type = ft.Dropdown(
        label="入力タイプ",
        options=[
            ft.dropdown.Option("name", "化合物名"),
            ft.dropdown.Option("smiles", "SMILES"),
            ft.dropdown.Option("image", "画像ファイル"),
        ],
        value="name", # 初期値
    )

    compound_input = ft.TextField(label="化合物名", expand=True)
    image_path_input = ft.TextField(label="画像ファイルのパス", visible=False, expand=True) # 初期状態では非表示
    pick_files_dialog = ft.FilePicker(on_result=lambda e: pick_files_result(e))
    page.overlay.append(pick_files_dialog) # FilePickerをページに追加

    output_smiles = ft.TextField(
        label="SMILES",
        value="",
        read_only=True,
        expand=True,
        border="underline",  # デザイン調整（任意）
    )
    structure_image = ft.Image(
        # src="path/to/placeholder.png", # 初期画像やプレースホルダー
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        visible=False, # 初期状態では非表示
    )
    status_text = ft.Text("")

    # --- イベントハンドラ ---
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            image_path_input.value = e.files[0].path
            image_path_input.update()

    def change_input_type(e):
        """入力タイプに応じて表示を切り替える"""
        selected_type = input_type.value
        if selected_type == "name":
            compound_input.label = "化合物名"
            compound_input.visible = True
            image_path_input.visible = False
            browse_button.visible = False
        elif selected_type == "smiles":
            compound_input.label = "SMILES"
            compound_input.visible = True
            image_path_input.visible = False
            browse_button.visible = False
        elif selected_type == "image":
            compound_input.visible = False # 化合物名入力は不要かも？（必要なら表示）
            image_path_input.visible = True
            browse_button.visible = True
        page.update()

    input_type.on_change = change_input_type # ドロップダウン変更時のイベントハンドラを設定

    browse_button = ft.ElevatedButton(
        "画像を選択...",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "gif"] # 必要に応じて拡張子を追加
        ),
        visible=False, # 初期状態では非表示
    )

    def generate_structure(e):
        """構造式生成ボタンが押されたときの処理"""
        selected_type = input_type.value
        smiles = None
        compound_name = "generated_structure" # デフォルト名
        img_path = None # 画像パスを初期化

        # UIをリセット
        status_text.value = "処理中..."
        output_smiles.value = ""
        structure_image.src_base64 = None # Base64を使う場合
        structure_image.visible = False
        page.update()

        try:
            if selected_type == "name":
                name = compound_input.value
                if not name:
                    status_text.value = "化合物名を入力してください。"
                    page.update()
                    return
                compound_name = name
                status_text.value = f"{name} のSMILESを検索中 (PubChem)..."
                page.update()
                smiles = generator.get_smiles_from_pubchem(name)
                if smiles is None:
                    status_text.value = f"{name} のSMILESを検索中 (Gemini)..."
                    page.update()
                    smiles = generator.get_smiles_from_gemini(name)

            elif selected_type == "smiles":
                smiles = compound_input.value
                if not smiles:
                    status_text.value = "SMILESを入力してください。"
                    page.update()
                    return
                # SMILESから化合物名を推定するのは難しいので、固定名か別途入力させる
                # compound_name = "from_smiles" # 必要ならユーザー入力フィールドを追加

            elif selected_type == "image":
                path = image_path_input.value
                if not path or not os.path.exists(path):
                    status_text.value = "有効な画像ファイルを選択してください。"
                    page.update()
                    return
                # compound_name = "from_image" # 必要ならユーザー入力フィールドを追加
                status_text.value = "画像からSMILESを生成中 (Gemini)..."
                page.update()
                smiles = generator.generate_smiles_from_image(path)

            if smiles and smiles != 'not found':
                output_smiles.value = smiles 
                status_text.value = "構造式画像を生成中..."
                page.update()

                # 画像生成 (ファイルに保存し、それを表示)
                # 一時ファイルを使うか、Base64エンコードして直接表示する
                img_dir = './img_flet' # Fletアプリ用の画像保存ディレクトリ
                os.makedirs(img_dir, exist_ok=True)
                # ファイル名が衝突しないように工夫が必要な場合がある
                img_path = os.path.join(img_dir, f'{compound_name.replace(" ", "_")}.png')

                success = generator.generate_structure_image(smiles, compound_name, img_path=img_path) # 保存パスを渡すように変更が必要

                if success and os.path.exists(img_path):
                     # Base64エンコードして表示
                    img_base64 = image_to_base64(img_path)
                    if img_base64:
                        structure_image.src_base64 = img_base64
                        structure_image.visible = True
                        status_text.value = "構造式を生成しました。"
                    else:
                        status_text.value = "画像の読み込みに失敗しました。"
                    # os.remove(img_path) # 不要なら一時ファイルを削除
                else:
                    status_text.value = "構造式画像の生成に失敗しました。"
            elif smiles == 'not found':
                 status_text.value = "指定された入力から化合物情報が見つかりませんでした。"
            else:
                status_text.value = "SMILESの取得に失敗しました。"

        except Exception as ex:
            status_text.value = f"エラーが発生しました: {ex}"

        page.update()

    # --- レイアウト ---
    page.add(
        ft.Row([input_type]),
        ft.Row(
            [
                compound_input,
                image_path_input, # TextField自体はRow内に配置
                browse_button,    # ButtonもRow内に配置
            ],
            # alignment=ft.MainAxisAlignment.START, # 必要に応じて調整
        ),
        ft.ElevatedButton("構造式を生成", on_click=generate_structure),
        ft.Divider(),
        output_smiles,
        structure_image,
        status_text,
    )

# アプリケーションの実行
ft.app(target=main)