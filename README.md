# ISEZAKI YOTARO — /HAL/ サイト

**公開URL: https://yotaro2121.github.io/hal-site/**

## ふだんの運用(作品の追加・差し替え)

1. **Chrome** で `admin.html` をダブルクリックして開く
2. 「hal-site フォルダを開く」→ このフォルダを選択
3. 写真をドラッグして追加/差し替え(トップの壺=HERO・WORKS・COLOR DNA すべて対応)、作品名・色・表示位置を編集、↑↓で並べ替え
4. 「保存」を押す
5. このフォルダ内の **公開.command** をダブルクリック → 1〜2分で公開URLに反映

写真は自動で縮小・軽量化されるので、カメラの写真をそのまま入れて大丈夫です。
細かい変更(文章の書き換え・デザイン調整など)は Claude Code に「〇〇して」と頼めば対応できます。

**作品コンセプトの正本は `concept.md`。** サイト上のコンセプト文言(ヒーローのリード文・STATEMENT・OGP)を変えるときは、まず `concept.md` を更新し、それを正としてサイトに反映する。

---

# Handoff: ISEZAKI YOTARO — /HAL/ アーティストサイト

陶芸家・伊勢崎陽太郎さんのポートフォリオ／ブランドサイト。コンセプトは **「画像を、焼く（IMAGES, FIRED）」** — 詳細は正本 `concept.md` を参照(物と画像が溢れる時代に、AI生成画像=ニセモノを、人間の物語と工芸の技術=二つのホンモノで挟み、750℃で二度と取り消せない実在に変える)。

このバンドルは **Claude Code でそのまま開発を継続できる、フレームワーク非依存のスタティックサイト** です。ビルド不要・依存パッケージなしで `index.html` を開けば動きます。

---

## このバンドルについて

- `index.html` — 完成品のスタンドアロン HTML。全 CSS を `<head>` 内の `<style>` に、Color DNA の切り替えロジックを末尾の `<script>`（バニラ JS）に持ちます。**外部ライブラリ・ビルドツールは一切不要。**
- `assets/` — サイトで使用する作品写真（最適化済み JPEG）。
- フォントは Google Fonts（`Zen Kaku Gothic New` / `IBM Plex Mono`）を CDN 読み込み。

> ⚠️ プレビュー環境（サンドボックス）では相対パスの画像に認証トークンが付かず表示されないことがありますが、**ローカルで開けば正常に表示されます**。確認するには:
> ```bash
> cd design_handoff_hal_site
> python3 -m http.server 8000   # → http://localhost:8000
> ```

## Fidelity

**High-fidelity（ハイファイ）**。配色・タイポグラフィ・余白・インタラクションまで確定済みの実装です。React / Next.js / Astro 等の実コードベースへ移す場合は、この見た目をピクセル単位で再現しつつ、そのプロジェクトの既存パターン（コンポーネント分割・ルーティング・画像最適化）に載せ替えてください。単一ファイルのまま拡張しても構いません。

---

## 画面構成（1ページ・縦スクロール）

固定ヘッダー（ナビ）＋アンカースクロール。セクション順:

### 00 HERO
- 2カラムグリッド `minmax(340px,46fr) / minmax(320px,54fr)`、高さ `100vh - 60px`。
- 左：キッカー `IMAGES, FIRED — /HAL/`／特大見出し **画像を、焼く。**（「焼く」のみアクセント赤）／リード文／CTA 2つ（`ARCHIVE を見る`＝塗り、`CONTACT`＝アウトライン）／署名。
- 右：メインの壺写真（`isezaki_IY_3_-46d3d54d.jpg`）を `object-fit:cover` でフルブリード。四辺に背景色へのグラデーションを重ねて文字可読性を確保。左下に小さなモノスペースのキャプション。
- 背景に極薄のアウトライン文字 `/HAL/`（`-webkit-text-stroke`）。
- 各要素は `fadeUp` を段階ディレイで適用。

### （マーキー）
- 横スクロールする用語帯（`OVERGLAZE TRANSFER` / `750°C — 7H` / `REGEN: DISABLED` 等）。同一行を2つ並べ `translateX(-50%)` で無限ループ。

### 01 WORKS
- 6カラムグリッド、`gap:18px`。カードは `span 4` / `span 2` を混在させたモザイク。
- **キャラクターの顔がはっきり写った接写を優先**（作品全体像より視認性が高いという方針）。ホバーで `translateY(-5px)` ＋ボーダー赤。

### 02 COLOR DNA
- 「HALの人格は、色で分岐する」= **色ごとに異なる原画キャラクター**を切り替えて見せるインタラクティブ・セクション。
- 左：大きなステージ画像（白背景）。右：巨大な色名漢字＋コード、スペック表、下部にサムネイル・チップ（5色）。
- チップをクリックすると画像・漢字・色・コードが切り替わり、画像に `dnaLoad`（クリップ＋彩度）アニメーションが走る。
- データは `<script>` 内の `DNA` 配列（下記「State / データ」参照）。

### 03 STATEMENT
- ターミナル風パネル（`KILN_LOG.txt`）。各行頭に赤い `>`、末尾に点滅カーソル `▊`。アーティストステートメント。

### 04 EXHIBITIONS
- `130px 1fr auto` の3カラム行リスト（年月・会場・ステータス）。予定／終了で色分け。

### 05 PROFILE
- `<dl>` による `150px 1fr` の定義リスト（NAME / ORIGIN / BASE / METHOD / SERIES / KILN）。

### 06 CONTACT（フッター）
- 特大 `CONTACT_`、メールリンク、コラボ案内文、下部にコピーライト・Instagram・タグライン。

---

## インタラクション & アニメーション

- **Color DNA 切り替え**：`select(i)` が画像 `src`/`alt`/`object-position`、漢字テキストと色、コード、チップの `active` クラスを更新。`img.style.animation` を一旦 `none` にして reflow 後に再設定することで `dnaLoad` を毎回リスタート。
- **アニメーション**：`fadeUp` `fadeIn`（初期表示）、`marquee`（帯）、`rainFall`（背景の縦テキスト）、`flick`（走査線ちらつき）、`blink`（カーソル）、`dnaLoad`（DNA切替）。
- **アクセシビリティ**：`@media (prefers-reduced-motion:reduce)` で全アニメーション停止。
- **レスポンシブ**：`max-width:860px` でヘッダー縦積み、ヒーロー1カラム（画像を上に）、WORKS 2カラム、EXHIBITIONS 1カラム。

## State / データ

Color DNA のみ状態を持ちます。`index.html` 末尾の `DNA` 配列を編集すれば増減・差し替え可能:

```js
{ kanji:'赤', code:'HAL_01 / 緋', img:'assets/isezaki_IY_28_2.jpg', color:'#C8452B', pos:'center 62%' }
```
`kanji`=表示漢字 / `code`=識別コード / `img`=画像パス / `color`=漢字の色 / `pos`=`object-position`。

---

## Design Tokens（`:root` 変数）

| 用途 | 変数 | 値 |
|---|---|---|
| 背景（ベース） | `--bg` | `#0B0A09` |
| パネル | `--panel` / `--panel-2` | `#151210` / `#100E0C` |
| 文字（主） | `--ink` | `#EDE6D8` |
| 文字（副） | `--ink-2` | `#CFC7B8` |
| 文字（弱） | `--muted` / `--muted-2` | `#B8AE9C` / `#8A8478` |
| アクセント（緋） | `--accent` | `#C8452B` |
| 紫（グリッチ等） | `--violet` | `#7A68B5` |
| 罫線 | `--line` / `--line-soft` | `rgba(237,230,216,.12)` / `.08` |

Color DNA の色: 赤 `#C8452B` / 緑 `#4E8A5E` / 紫 `#7A68B5` / 桃 `#C86A8E` / 黄 `#C9A227`。

**タイポグラフィ**
- 見出し・本文：`Zen Kaku Gothic New`（500 / 700 / 900）
- ラベル・数値・コード：`IBM Plex Mono`（400 / 500 / 600）、`letter-spacing` 広め（.18〜.3em）
- ヒーロー見出し：`clamp(56px,7.2vw,124px)` / weight 900 / line-height 1.08
- セクション見出し：34px / weight 900 / `letter-spacing:.3em`

**レイアウト**：コンテンツ最大幅 `--max:1440px`、セクション上下 `90px`（先頭 `120px`）、左右 `40px`。

---

## Assets

`assets/` 内はすべて伊勢崎さんの作品写真（本人提供の元画像を長辺 1500〜2000px・JPEG q0.82〜0.84 に最適化したもの）。

- ヒーロー：`isezaki_IY_3_-46d3d54d.jpg`
- WORKS：`isezaki_IY_27_2 / 23_1 / 29_1 / 36_2_1 / 11_1 / 44_1 / 27_1`
- COLOR DNA：`isezaki_IY_28_2 / 32_2 / 9_2 / 23_3 / 30_2`

差し替え・追加時は元の高解像度から同程度に最適化してください。フォント2種は CDN 読み込みのため同梱なし。

---

## 移行のヒント（Claude Code）

1. まず `index.html` をローカルサーバーで開き、意図した見た目・挙動を確認。
2. React/Astro 等に載せる場合は、セクション単位（Hero / Works / ColorDna / Statement / Exhibitions / Profile / Contact）でコンポーネント分割し、`DNA` 配列はデータファイル化。
3. `:root` のトークンはそのまま CSS 変数 or テーマとして流用可能。
4. 画像は各フレームワークの最適化機構（`next/image` 等）へ。
5. アニメーションは CSS のまま移植可能。`prefers-reduced-motion` 対応を維持のこと。
