//////////////////////////////////////////////////////////////////////
/*!	@class	AqKanji2Koe

	@brief	AquesTalk用 言語処理エンジン (Win)

	漢字かな混じりテキスト->音声記号列（かな/ローマ字）

	author	AQUEST Corp.

	@date	2022/12/05	Ver.4.21
*/
//  COPYRIGHT (C) 2010 AQUEST CORP.
//////////////////////////////////////////////////////////////////////
#if !defined(_AQ_KANJI2KOE_H_)
#define _AQ_KANJI2KOE_H_
#ifdef __cplusplus
extern "C"{
#endif

/////////////////////////////////////////////
//!	言語処理インスタンス生成（初期化）[ファイル指定]
//! @param	pathDic[in]		辞書のディレクトリを指定(最後に/が有っても無くても良い）
//! @param	pErr[out]		エラー時にはエラーコードが入る 正常終了時は不定値
//!	@return	インスタンスハンドル エラーの時は０が返る
void * __stdcall AqKanji2Koe_Create(const char *pathDic, int *pErr);

/////////////////////////////////////////////
//!	言語処理インスタンス生成 （初期化）[アドレス指定]
//!   呼び出し側で辞書データ(バイナリ)をメモリに読み込んでから指定
//!   初期化を高速化するためのメモリマップトファイルなどが使える
//! @param	pSysDic[in]		システム辞書データ先頭アドレス(必須)
//! @param	pUserDic[in]	ユーザ辞書データ先頭アドレス（使用しないときは0を指定）
//! @param	pErr[out]		エラー時にはエラーコードが入る 正常終了時は不定値
//!	@return	インスタンスハンドル エラーの時は０が返る
void * __stdcall AqKanji2Koe_Create_Ptr(const void *pSysDic, const void *pUserDic, int *pErr);

/////////////////////////////////////////////
//!	インスタンス解放
//! @param	hAqKanji2Koe[in]	AqKanji2Koe_Create()で返されたインスタンスハンドル
void  __stdcall AqKanji2Koe_Release(void *hAqKanji2Koe);

/////////////////////////////////////////////
//!	言語処理 (漢字仮名交じりテキストを音声記号列に変換)
//! @param	hAqKanji2Koe[in]	AqKanji2Koe_Create()で返されたインスタンスハンドル
//! @param	kanji[in]	漢字かな混じり文テキスト
//! @param	koe[out]	音声記号列
//! @param	nBufKoe[in]	koeの配列サイズ
//!	@return	0:正常終了 それ以外：エラーコード
//! 入出力:UTF-8
int __stdcall AqKanji2Koe_Convert_utf8(void *hAqKanji2Koe, const char *kanji, char *koe, int nBufKoe);
//! 入出力:UTF-16LE
int __stdcall AqKanji2Koe_Convert_utf16(void *hAqKanji2Koe, const char16_t *kanji, char16_t *koe, int nBufKoe);
//! 入出力:Shift-JIS
int __stdcall AqKanji2Koe_Convert_sjis(void *hAqKanji2Koe, const char *kanji, char *koe, int nBufKoe);

/////////////////////////////////////////////
//!	言語処理 (漢字仮名交じりテキストを ローマ字音声記号列(AquesTalk pico用）に変換)
//! @param	hAqKanji2Koe[in]	AqKanji2Koe_Create()で返されたインスタンスハンドル
//! @param	kanji[in]	漢字かな混じり文テキスト
//! @param	koe[out]	音声記号列(ローマ字)
//! @param	nBufKoe[in]	koeの配列サイズ
//!	@return	0:正常終了 それ以外：エラーコード
//! 入力:UTF-8 出力：ASCII
int __stdcall AqKanji2Koe_ConvRoman_utf8(void *hAqKanji2Koe, const char *kanji, char *koe, int nBufKoe);
//! 入力:UTF-16LE 出力：ASCII
int __stdcall AqKanji2Koe_ConvRoman_utf16(void *hAqKanji2Koe, const char16_t *kanji, char *koe, int nBufKoe);
//! 入力:Shift-JIS 出力：ASCII
int __stdcall AqKanji2Koe_ConvRoman_sjis(void *hAqKanji2Koe, const char *kanji, char *koe, int nBufKoe);

/////////////////////////////////////////////
//!	開発ライセンスキー設定
//!	音声波形を生成する前に一度呼び出す。
//!	これにより評価版の制限がなくなる。
//!	@param  key[in]		開発ライセンスキーを指定
//!	@return	ライセンスキーが正しければ0、正しくなければ1が返る
//! *キーの解析を防ぐため不正なキーでも0を返す場合がある。このとき制限は解除されない。
int __stdcall AqKanji2Koe_SetDevKey(const char *devKey);


#ifdef __cplusplus
}
#endif
#endif // !defined(_AQ_KANJI2KOE_H_)
//  ----------------------------------------------------------------------
// !  Copyright AQUEST Corp. 2006- .  All Rights Reserved.                !
// !  An unpublished and CONFIDENTIAL work.  Reproduction, adaptation, or !
// !  translation without prior written permission is prohibited except   !
// !  as allowed under the copyright laws.                                !
//  ----------------------------------------------------------------------
