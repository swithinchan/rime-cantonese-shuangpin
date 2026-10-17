# 粵語雙拼（自然碼兼容版）

一套以香港語言學學會粵語拼音方案（Jyutping，下稱「粵拼」）為基礎的粵語雙拼輸入法。每個粵語音節固定使用兩鍵：第一鍵輸入聲母，第二鍵輸入韻母。方案運行於 Rime（中州韻），聲母鍵位盡量兼容內地自然碼雙拼的肌肉記憶，韻母則按粵語音系壓縮到 26 個字母鍵及 `;` 鍵。

本倉庫目前以 Linux + Fcitx5 + Rime 為主要驗證環境；Rime 本身是跨平台引擎，因此同一套 schema 也可在其他 Rime 前端使用，但安裝路徑會不同。

## 設計理念

粵拼有 20 個聲母（含零聲母）和 56 個韻母。全拼輸入時，一個音節往往要打 3 至 5 鍵；雙拼則把每個音節固定壓縮為 2 鍵。林語堂很早便提出以聲母、韻母作為漢字記音的基本骨架；雙拼正是取其精要，去掉拼寫中的冗餘，做到「我手寫我口」。

本方案不改變粵拼本身的聲韻分析，只在鍵盤層面做映射：

- 聲母大多與字母同鍵。
- 粵拼特有的 `gw`、`kw`、`ng`、`j` 分別映射到 `I`、`U`、`V`、`Y`。
- 零聲母以 `O` 起首。
- 長短元音、鼻音韻尾與相應入聲韻尾，按發音位置合併到同一鍵。

## 快速上手

### 單字打法

| 字詞 | 粵拼 | 聲母 | 韻母 | 雙拼碼 |
| --- | --- | --- | --- | --- |
| 我 | `ngo` | `ng` → `V` | `o` → `O` | `VO` |
| 你 | `nei` | `n` | `ei` → `Z` | `NZ` |
| 好 | `hou` | `h` | `ou` → `B` | `HB` |
| 佢 | `keoi` | `k` | `eoi` → `Y` | `KY` |
| 靚 | `leng` | `l` | `eng` → `G` | `LG` |
| 廣 | `gwong` | `gw` → `I` | `ong` → `S` | `IS` |
| 關 | `gwaan` | `gw` → `I` | `aan` → `J` | `IJ` |
| 愛 | `oi` | 零聲母 → `O` | `oi` → `O` | `OO` |
| 唔 | `m` | 零聲母 → `O` | `m` → `M` | `OM` |
| 五 | `ng` | 零聲母 → `O` | `ng` → `V` | `OV` |

### 詞組打法

連續輸入每個音節的雙拼碼即可，詞庫和整句引擎會自動分詞：

| 詞組 | 粵拼 | 雙拼碼 |
| --- | --- | --- |
| 香港 | `hoeng gong` | `HXGS` |
| 你好 | `nei hou` | `NZHB` |
| 鐵路 | `tit lou` | `TTLB` |
| 我手寫我口 | `ngo sau se ngo hau` | `VOSKSEVOHK` |

## 鍵位表

### 聲母

| 粵拼聲母 | 按鍵 | 說明／例子 |
| --- | --- | --- |
| `b p m f d t n l g k h z c s w` | 同字母 | 與全拼相同 |
| `gw` | `I` | `gwong`（廣） → `IS` |
| `kw` | `U` | `kwaa`（誇） → `UA` |
| `ng` | `V` | `ngo`（我） → `VO` |
| `j` | `Y` | `jaa`（也） → `YA` |
| 零聲母 | `O` | `oi`（愛） → `OO` |

### 韻母

| 按鍵 | 粵拼韻母 | 例子 |
| --- | --- | --- |
| `A` | `a`、`aa` | `faa`（花） → `FA` |
| `B` | `ou` | `gou`（高） → `GB` |
| `C` | `aam`、`aap` | `zaam`（站） → `ZC` |
| `D` | `am`、`ap` | `gap`（急） → `GD` |
| `E` | `e` | `se`（些） → `SE` |
| `F` | `an`、`at` | `san`（新） → `SF` |
| `G` | `ang`、`ak` | `hak`（黑） → `HG` |
| `H` | `aang`、`aak` | `haak`（客） → `HH` |
| `I` | `i` | `ji`（衣） → `YI` |
| `J` | `aan`、`aat` | `saan`（山） → `SJ` |
| `K` | `aau`、`au` | `gaau`（交） → `GK` |
| `L` | `aai`、`ai` | `gaai`（街） → `GL` |
| `M` | `im`、`ip` | `tip`（貼） → `TM` |
| `N` | `in` | `jin`（煙） → `YN` |
| `O` | `o`、`oi` | `hoi`（海） → `HO` |
| `P` | `un`、`ut` | `wun`（碗） → `WP` |
| `Q` | `iu` | `jiu`（要） → `YQ` |
| `R` | `yun`、`yut` | `syut`（雪） → `SR` |
| `S` | `on`、`ong`、`ok`、`ung`、`uk` | `hung`（紅） → `HS` |
| `T` | `it` | `bit`（必） → `BT` |
| `U` | `u` | `fu`（夫） → `FU` |
| `V` | `yu`、`ui` | `zyu`（豬） → `ZV` |
| `W` | `oe` | `hoe`（靴） → `HW` |
| `X` | `oeng`、`oek` | `hoeng`（香） → `HX` |
| `Y` | `eoi`、`eon`、`eot` | `seoi`（需） → `SY` |
| `Z` | `ei` | `fei`（非） → `FZ` |
| `;` | `ing`、`ik` | `ming`（名） → `M;` |

獨立成音節的鼻音另外處理：

| 音節 | 雙拼碼 |
| --- | --- |
| `m`（唔） | `OM` |
| `ng`（五、吳） | `OV` |

> 在手機虛擬鍵盤上，如果沒有 `;` 鍵，可使用支援符號鍵的 Rime 前端，或由前端另行映射 `ing/ik`。

## 安裝

### Linux：Fcitx5 + Rime

1. 安裝 Fcitx5 與 Rime。

   - Fedora：

     ```bash
     sudo dnf install fcitx5 fcitx5-rime
     ```

   - Debian／Ubuntu：

     ```bash
     sudo apt install fcitx5 fcitx5-rime
     ```

   - Arch Linux：

     ```bash
     sudo pacman -S fcitx5 fcitx5-rime
     ```

2. 取得本倉庫，並複製必要檔案到 Rime 用戶目錄。

   ```bash
   git clone https://github.com/swithinchan/rime-cantonese-shuangpin.git /tmp/jyutping-nc
   mkdir -p ~/.local/share/fcitx5/rime
   cd /tmp/jyutping-nc
   cp jyutping_nc.schema.yaml jyutping_nc.dict.yaml default.custom.yaml \
     ~/.local/share/fcitx5/rime/
   ```

   如果系統 Rime 資料目錄尚未提供 `jyutping.dict.yaml`，可從 rime-cantonese 下載：

   ```bash
   curl -fLo ~/.local/share/fcitx5/rime/jyutping.dict.yaml \
     https://raw.githubusercontent.com/rime/rime-cantonese/master/jyutping.dict.yaml
   ```

3. 確認 `default.custom.yaml` 已啟用本方案。

   ```yaml
   patch:
     schema_list:
       - schema: jyutping_nc
   ```

4. 重新部署並重啟 Fcitx5。

   ```bash
   cd ~/.local/share/fcitx5/rime
   rime_deployer --build "$PWD" /usr/share/rime-data "$PWD/build"
   fcitx5-remote -r
   ```

5. 在 Fcitx5 設定中加入 Rime 輸入法，然後選擇「粵語雙拼（自然碼兼容版）」。

### 其他平台

Rime 是跨平台引擎，本 schema 理論上可移植到以下前端：

| 平台 | Rime 前端 | 用戶目錄 |
| --- | --- | --- |
| Linux（IBus） | ibus-rime | `~/.config/ibus/rime` |
| macOS | Squirrel（鼠鬚管） | `~/Library/Rime` |
| Windows | Weasel（小狼毫） | `%APPDATA%\Rime` |
| Android | Trime | 依 App 指定目錄 |

本倉庫目前只驗證 Linux／Fcitx5 的安裝流程；其他平台使用時，可能需要按前端習慣調整部署方式。

## 碰撞率

### 統計口徑

- 詞庫：本機 Rime 自帶 `jyutping.dict.yaml`（version `2013.12.07`），再加上本倉庫 `jyutping_nc.dict.yaml` 的本地覆蓋詞條。
- 單位：以「字頭／詞條 + 粵拼碼」去重後計算。
- 重碼率定義：

  ```text
  重碼率 = (1 - 唯一碼數 / 詞條數) × 100%
  ```

- 雙拼統計只納入目前已有雙拼碼的詞條；少數未編碼的罕用讀音會另外標示。

### 計算程式

本倉庫附有 `collision_stats.py`，可重現上述數字。公式如下：

```text
重碼率 = (1 - 唯一碼數 / 詞條數) × 100%
平均候選／碼 = 詞條數 / 唯一碼數
```

執行方式：

```bash
python3 collision_stats.py \
  --schema jyutping_nc.schema.yaml \
  --dict /usr/share/rime-data/jyutping.dict.yaml \
  --dict jyutping_nc.dict.yaml
```

程式會把詞庫與本機覆蓋詞條合併去重，再按「單字、全部詞條、多字詞條」三個範圍輸出全拼與雙拼的碰撞率。

### 單字

| 方案 | 詞條數 | 唯一碼數 | 平均候選／碼 | 重碼率 |
| --- | ---: | ---: | ---: | ---: |
| 粵拼全拼 | 24,381 | 700 | 34.83 | 97.13% |
| 本方案雙拼 | 24,381 | 413 | 59.03 | 98.31% |

單字層面，雙拼比全拼多約 1.18 個百分點的重碼率，但這正是雙拼以 2 鍵換取少量候選增加的正常代價。

### 全部詞條

| 方案 | 詞條數 | 唯一碼數 | 平均候選／碼 | 重碼率 |
| --- | ---: | ---: | ---: | ---: |
| 粵拼全拼 | 28,116 | 4,395 | 6.40 | 84.37% |
| 本方案雙拼 | 28,116 | 4,089 | 6.88 | 85.46% |

加入詞組後，雙拼與全拼的差距縮小至約 1.09 個百分點。

### 多字詞條

| 方案 | 詞條數 | 唯一碼數 | 平均候選／碼 | 重碼率 |
| --- | ---: | ---: | ---: | ---: |
| 粵拼全拼 | 3,735 | 3,695 | 1.01 | 1.07% |
| 本方案雙拼 | 3,735 | 3,676 | 1.02 | 1.58% |

只統計兩個音節或以上的詞條時，雙拼重碼率只有約 **1.58%**，與全拼的 **1.07%** 非常接近。這說明實際輸入時依靠詞組聯想和整句引擎，粵語雙拼不會比粵拼全拼或內地雙拼有明顯劣勢。

> 統計中，單字有 56 條、全部詞條有 71 條尚未分配雙拼碼，均為現有 `jyutping` 詞庫中的罕用讀音。

## 附錄：LSHK 聲母／韻母字數分佈

以下資料來源為 `jyut6ping3.chars.dict.yaml`，版本 `2026.08.10`，來源 `CanCLID/rime-cantonese-upstream`。字數為去重字頭數，詞條數為原始詞條行數；多音字會分別計入所屬聲母／韻母。

### 聲母分佈

| 聲母 | 字數（去重） | 詞條數 |
| --- | ---: | ---: |
| `b` | 1,238 | 1,455 |
| `p` | 931 | 1,079 |
| `m` | 1,341 | 1,610 |
| `f` | 1,314 | 1,465 |
| `d` | 1,432 | 1,635 |
| `t` | 1,285 | 1,439 |
| `n` | 659 | 807 |
| `l` | 2,097 | 2,502 |
| `g` | 2,161 | 2,425 |
| `k` | 1,126 | 1,212 |
| `ng` | 594 | 636 |
| `h` | 2,030 | 2,346 |
| `gw` | 560 | 584 |
| `kw` | 293 | 318 |
| `w` | 1,278 | 1,459 |
| `z` | 3,030 | 3,516 |
| `c` | 2,508 | 2,803 |
| `s` | 2,549 | 2,855 |
| `j` | 3,179 | 3,546 |
| 零聲母 | 516 | 639 |

### 韻母分佈

| 韻母 | 字數（去重） | 詞條數 |
| --- | ---: | ---: |
| `i` | 1,198 | 1,323 |
| `ip` | 368 | 414 |
| `it` | 494 | 550 |
| `ik` | 780 | 866 |
| `im` | 524 | 614 |
| `in` | 1,036 | 1,188 |
| `ing` | 1,217 | 1,389 |
| `iu` | 850 | 1,034 |
| `yu` | 578 | 667 |
| `yut` | 295 | 347 |
| `yun` | 854 | 984 |
| `u` | 474 | 513 |
| `up` | 0 | 0 |
| `ut` | 133 | 153 |
| `uk` | 792 | 873 |
| `um` | 0 | 0 |
| `un` | 315 | 366 |
| `ung` | 1,184 | 1,369 |
| `ui` | 337 | 388 |
| `e` | 232 | 272 |
| `ep` | 3 | 5 |
| `et` | 5 | 5 |
| `ek` | 87 | 90 |
| `em` | 3 | 3 |
| `en` | 0 | 0 |
| `eng` | 81 | 89 |
| `ei` | 1,105 | 1,248 |
| `eu` | 5 | 5 |
| `eot` | 149 | 160 |
| `eon` | 493 | 556 |
| `eoi` | 1,056 | 1,218 |
| `oe` | 28 | 33 |
| `oet` | 2 | 4 |
| `oek` | 210 | 243 |
| `oeng` | 569 | 645 |
| `o` | 713 | 844 |
| `ot` | 42 | 50 |
| `ok` | 580 | 670 |
| `on` | 155 | 202 |
| `ong` | 971 | 1,172 |
| `oi` | 403 | 456 |
| `ou` | 1,149 | 1,253 |
| `a` | 8 | 8 |
| `ap` | 272 | 331 |
| `at` | 630 | 694 |
| `ak` | 198 | 207 |
| `am` | 660 | 783 |
| `an` | 1,273 | 1,496 |
| `ang` | 447 | 498 |
| `ai` | 1,464 | 1,637 |
| `au` | 1,392 | 1,591 |
| `aa` | 707 | 858 |
| `aap` | 366 | 408 |
| `aat` | 282 | 311 |
| `aak` | 342 | 375 |
| `aam` | 469 | 550 |
| `aan` | 778 | 884 |
| `aang` | 212 | 234 |
| `aai` | 566 | 628 |
| `aau` | 425 | 497 |
| `m` | 4 | 6 |
| `ng` | 65 | 74 |

### 交叉統計術語

除了單一維度的聲母、韻母統計，本倉庫亦提供「聲母 × 韻母」交叉統計。交叉表以聲母做欄、韻母做行，每格表示某個聲母與某個韻母組合的數據。

| 名詞 | 意思 |
| --- | --- |
| `詞條數` | 原始字表逐行計數。同一個漢字如果有幾個讀音，會計算為幾條詞條。 |
| `字數（去重）` | 在同一個「聲母 × 韻母」格內，相同漢字只計一次。多音字在不同格仍然會各自計數。 |
| `百分比` | 將每格數值按所選基準轉換為百分比，方便比較「佔某個聲母」或「佔某個韻母」的分佈。 |

例如「行」可以讀 `hang4`、`hong4`、`haang4` 等多個音：

- `詞條數`會按讀音計算為多條；
- `字數（去重）`在每個聲韻格各自只計 1，但跨格總計仍然會重複；
- 因此交叉表總計不等於漢字總數，而是「聲韻配搭人次」。

### HTML 數據檢視

以下互動式 HTML 可直接在瀏覽器開啟，方便檢查每個聲母與韻母的交叉分佈：

- [字數（去重）交叉統計](<https://swithinchan.github.io/rime-cantonese-shuangpin/LSHK_聲母x韻母_交叉統計_字數（去重）.html>)
- [詞條數交叉統計](<https://swithinchan.github.io/rime-cantonese-shuangpin/LSHK_聲母x韻母_交叉統計_詞條數.html>)
- [百分比交叉統計](<https://swithinchan.github.io/rime-cantonese-shuangpin/LSHK_聲母x韻母_交叉統計_百分比.html>)

統計首頁：<https://swithinchan.github.io/rime-cantonese-shuangpin/>

## 檔案說明

| 檔案 | 用途 |
| --- | --- |
| `jyutping_nc.schema.yaml` | 本方案的 Rime schema，定義雙拼轉換規則 |
| `jyutping_nc.dict.yaml` | 本地覆蓋詞條，並導入 `jyutping` 詞庫 |
| `collision_stats.py` | 重現碰撞率計算，供社群檢驗與改進 |
| `default.custom.yaml` | 啟用 `jyutping_nc` schema |
| `build_script.sh` | 建置 Rime 資料並重啟 Fcitx5 |
| `test_rime.py` | 呼叫 librime 做候選字／候選詞回歸測試 |
| `jyut6ping3.*` | 相關粵拼詞庫、schema 與統計資料 |
| `loengfan.*` | 粵語兩分方案，與本雙拼方案不同 |

## 參考資料

- 香港語言學學會粵語拼音方案：<https://lshk.org/jyutping-scheme/>
- Rime 中州韻：<https://rime.im>
- rime-cantonese：<https://github.com/rime/rime-cantonese>
- 統計資料來源：<https://github.com/CanCLID/rime-cantonese-upstream>

## 致謝

本方案得以建立，有賴以下公開成果：

- 感謝香港語言學學會公布粵語拼音方案：<https://lshk.org/jyutping-scheme/>。
- 感謝前人在粵語拼音輸入法上的努力：《實用粵語拼音輸入法》，鄧思穎、童哲生著，香港：語言科技，1999 年。
- 感謝 MISTER-CHAN 在先行者方案上的嘗試：<https://github.com/MISTER-CHAN/rime-sg1pb3>。
- 感謝「粵拼輸入法 App」作者張兵先生的指導：<https://jyutping.app/>。
- 感謝香港中文大學「粵語審音配詞字庫」免費公開資料：<https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/>。
- 感謝 Rime 中州韻及 rime-cantonese 社群提供輸入法引擎與詞庫基礎。

## 開發聲明

本中文輸入法在開發、測試與文檔整理過程中，曾使用 AI 輔助生成。所使用的模型或工具包括 Gemini 與 DeepSeek；其中 DeepSeek 於 Open Interpreter harness 中執行。
