import os
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Draw
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

class ChemicalStructureGenerator:
    """化合物の構造式を生成するクラス"""
    def __init__(self):
        load_dotenv()
        self.genai_api_key = os.getenv('YOUR_API_KEY')
        
    def get_smiles_from_pubchem(self, compound_name):
        """PubChemからSMILES文字列を取得"""
        try:
            compounds = pcp.get_compounds(compound_name, 'name')
            if not compounds:
                raise ValueError("化合物が見つかりませんでした。")
            return compounds[0].isomeric_smiles
        except (IndexError, ValueError) as e:
            print(f"PubChem APIエラー: {e}")
            return None

    def get_smiles_from_gemini(self, compound_name):
        """GeminiからSMILES文字列を取得"""
        try:
            if not self.genai_api_key:
                raise ValueError("APIキーが設定されていません。")
            
            client = genai.Client(api_key=self.genai_api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[f"Generate a SMILES string for the compound:{compound_name}. Return only the SMILES string. If the compound is polymer, return only the SMILES of its monomer. Do not include any other text. If the compound is not found, return 'not found'."],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=100,
                ),
            )
            
            smiles = response.text.strip()
            if smiles == 'not found':
                print('化合物が見つかりませんでした。')
                return None
            return smiles
        except Exception as e:
            print(f"Gemini APIエラー: {e}")
            return None

    def generate_structure_image(self, smiles, compound_name, img_path=None, show_image=False): # img_pathとshow_image引数を追加
        """SMILES文字列から構造式画像を生成し、指定されたパスに保存"""
        try:
            mol = Chem.MolFromSmiles(str(smiles))
            if mol is None:
                mol = Chem.MolFromSmiles(str(smiles), sanitize=False)
                if mol is None:
                    raise ValueError("SMILESから分子を生成できませんでした。")

            if img_path is None:
                # デフォルトのパス設定（Fletアプリから呼ばれる場合はパスが指定される想定）
                os.makedirs('./img', exist_ok=True)
                img_path = f'./img/{compound_name.replace(" ", "_")}.png' # ファイル名にスペース等が含まれないように

            # ファイルに描画
            Draw.MolToFile(mol, img_path, legend=compound_name, imageType='png', size=(300, 300)) # sizeオプション追加も検討
            print(f'構造式画像を {img_path} に保存しました。')

            if show_image: # オプションで画像表示
                try:
                    img = Image.open(img_path)
                    img.show()
                except Exception as e:
                    print(f"画像表示エラー: {e}")

            return True # 成功したことを示す値を返す
        except ValueError as e:
            print(f"RDKitエラー: {e}")
        except FileNotFoundError as e: # これはMolToFileでは通常発生しないはず
            print(f"ファイル関連エラー: {e}")
        except Exception as e:
            print(f"構造式画像生成中の予期せぬエラー: {e}")
        return False # 失敗したことを示す値を返す
    
    def generate_smiles_from_image(self, image_path):
        """画像から構造式を生成"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError("指定された画像ファイルが見つかりません。")
            
            # 画像を読み込む
            img = Image.open(image_path)
            print("画像を読み込みました。")

            # Gemini APIを使用してSMILESを生成
            if not self.genai_api_key:
                raise ValueError("APIキーが設定されていません。")
            
            client = genai.Client(api_key=self.genai_api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[img, "Generate a SMILES string from the image of the compound. Return only the SMILES string. If the compound is polymer, return only the SMILES of its monomer. Do not include any other text. If the compound is not found, return 'not found'."],
                config=types.GenerateContentConfig(
                    temperature=0,
                    max_output_tokens=100,
                ),
            )
            
            smiles = response.text.strip()
            if smiles == 'not found':
                print('化合物が見つかりませんでした。')
                return None
            return smiles
        except Exception as e:
            print(f"Gemini APIエラー: {e}")
            return None
def main():
    """メイン関数"""
    generator = ChemicalStructureGenerator()
    input_method = input("入力方法を選択してください (名前: name, SMILES: smiles, 画像:image): ").lower()

    if input_method == "name":
        compound_name = input('化合物の名前: ')
        # PubChemで試行
        smiles = generator.get_smiles_from_pubchem(compound_name)
    
        # PubChemで失敗した場合、Geminiで試行
        if smiles is None:
            smiles = generator.get_smiles_from_gemini(compound_name)
        print(smiles)
        # SMILESが取得できた場合、構造式を生成
        if smiles:
            generator.generate_structure_image(smiles, compound_name)
    elif input_method == "smiles":
        smiles = input('SMILES文字列: ')
        compound_name = input('化合物の名前: ')
        print(smiles)
        generator.generate_structure_image(smiles, compound_name)
        
    elif input_method == "image":
        image_path = input('画像のパス: ')
        compound_name = input('化合物の名前: ')
        # 画像からSMILESを生成
        smiles = generator.generate_smiles_from_image(image_path)
        print(smiles)
        if smiles:
            # SMILESから構造式を生成
            generator.generate_structure_image(smiles, compound_name)
    else:
        print("無効な入力です。'name' または 'smiles' を選択してください。")
if __name__ == "__main__":
    pass