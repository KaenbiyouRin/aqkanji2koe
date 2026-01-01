/**************************************************************
	Kanji2KoeCmd - かな漢字混じりテキストを音声記号列に変換

	>Kanji2KoeCmd < in.txt(SJIS) > out.koe(SJIS)

	処理は改行単位

	■ビルド
	必要に応じて、
	  AqKanji2Koe.hのパスをインクルードファイル検索パスに追加
	  AqKanji2Koe.libのパスをライブラリ検索パスに追加

	■実行時の配置
	AqKanji2Koe.dllは、exeと同じディレクトリに配置
	辞書フォルダ(aq_dic)もexeと同じディレクトリに配置

		|- Kanji2KoeCmd.exe
		|- AqKanji2Koe.dll
		|- aq_dic/
			|- aqdic.bin 
			|- aq_user.dic (ユーザ辞書:任意)
			|- CREDITS

  
	2019/03/03	Ver.4用に一部修正

**************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Windows.h>
#include <AqKanji2Koe.h>	// インクルードパスの追加が必要
#pragma comment(lib, "AqKanji2Koe.lib")  // AqKanji2Koeライブラリをリンク
#pragma warning(disable : 4996) 

#define	NSTR	4096

void _AqGetExePath(char *path);

int main(int ac, char **av)
{
	int iret;
	char kanji[NSTR];
	char koe[NSTR];
	char dicDir[_MAX_PATH];

	// 開発ライセンスキーの指定(ライセンス証に記載)
	iret = AqKanji2Koe_SetDevKey("XXX-XXX-XXX");

	// 辞書データファイルのパスを求める
	_AqGetExePath(dicDir);
	strcat(dicDir, "aq_dic");
	
	// 言語処理ライブラリのインスタンス生成
	void *hAqKanji2Koe = AqKanji2Koe_Create(dicDir, &iret);
	if(hAqKanji2Koe==0)	// エラーの場合、0が返る エラーコードはiretに
		return iret;

	int i;
	for(i=0; ; i++){
		if(fgets(kanji, NSTR, stdin)==0) break;
		// 漢字かな交じりのテキストデータを音声記号列に変換
		iret = AqKanji2Koe_Convert_sjis(hAqKanji2Koe, kanji, koe, NSTR);
		if(iret!=0) break;	// エラーの場合、0以外が返る
		fprintf(stdout, "%s\n", koe);
	}


	// 言語処理ライブラリのインスタンス解放
	AqKanji2Koe_Release(hAqKanji2Koe);
	return iret;
}


/*------------------ 関数----------- ------------------------------
NAME
PARAM
	path[_MAX_PATH + 1 ]
RETURN
DESCRIPTION
	実行中のパス（ドライブ付き）を求める
NOTE
	最後には\が付く
--------------------------------------------------------------------*/
void _AqGetExePath(char *path)
{
	char 	str[ _MAX_PATH + 1 ];
	char	drive[_MAX_DRIVE];
	char	dir[_MAX_DIR];
	char	fname[_MAX_FNAME];
	char	ext[_MAX_EXT];

	GetModuleFileName(NULL, str, _MAX_PATH);
	_splitpath( str, drive, dir, fname, ext );
	strcpy(path,drive);
	strcat(path, dir);
	return ;
}
