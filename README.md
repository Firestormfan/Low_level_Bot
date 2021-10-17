# Low Level Bot
低レベルなFortniteのロビーボットです  
今作成中なので使うのは自己責任でお願いします
ちゃんとしたやつ使いたいならgomashio1596さんのFortnite-Lobbybot-V2とか使ってください

# HOW TO USE
1.install.batを起動します  
2.RUN.batを起動します  
3.enjoy

# config
## normal
| 設定名 | 内容 |
:---|:---
| prefix | コマンドの前に必要な文字列を指定します |
| outfit | 起動時のスキンを指定します(CID指定) |
| emote | 起動時のエモートを指定します(EID指定) |
| backpack | 起動時のバックパックを指定します(BID指定) |
| pickaxe | 起動時のつるはしを指定します(pickaxe_id指定) |
| banner | 起動時のバナーを指定します(banner_id指定) |
| color | 起動時のバナーの色を指定します |
| level | Botのレベルを指定します |
| owner | Botのオーナーを指定します(複数人指定可) |
| status | 起動時のステータスを指定します |
| blacklist | Botのブラックリストプレイヤーを指定します |
| platform | Botのプラットフォームを指定します(後述) |
| join_message | 参加時のメッセージを指定します |
| join_request | 参加リクエストを許可するかどうか |
## party_settings
| 設定名 | 内容 |
:---|:---
| privacy | Botのプライバシーを指定します(後述) |
| max_size | パーティーの最大サイズを指定します(1~16) |
| chat_enabled | チャットを有効化するかどうか |
| team_change | スクワッドフォーメーションを許可するかどうか |
## DEV
| 設定名 | 内容 |
:---|:---
| DEBUG | デバッグモードをオンにするかどうか |

# Commands
| コマンド名 | 内容 |
:---|:--- 
| partyinfo | パーティーID,パーティーリーダー,メンバー数を表示します。 |
| clear | エモートを停止します。 |
| outfit | スキンを変更します。 |
| emote | エモートを変更します。 |
| backpack | バックパックを変更します。 |
| pickaxe | つるはしを変更します。 |
| bp | バトルパスレベルを変更します。 |
| sitout | 欠場状態にします。 |
| ready | 準備OK状態にします。 |
| unready | 準備中にします。 |
| match | マッチ中に変更します。 |
| unmatch | マッチ状態を解除します。 |
| status | ステータスを変更します。 |
| chatban | 指定したユーザーをパーティーチャットから追い出します。 |
| togglepriv | プライバシーを切り替えます。 |
| hide | 指定したプレイヤーを非表示にします。 |
| show | 指定したプレイヤーを表示します。 |
| block | 指定したプレイヤーをブロックします。 |
| join | 指定したプレイヤーのパーティーに参加します。 |
| kick | 指定したプレイヤーをキックします。 |
| promote | 指定したプレイヤーにパーティーリーダーを譲渡します。 | 
| invite | 指定したプレイヤーを招待します。 |
| status | ステータスを変更します。 | 
| getkd | 指定したプラットフォーム(後述)でキルデス比を取得します。 (例 !getkd keyboard Tracebacker)
| open | パーティーをパブリックにします。 |
| close | パーティーをプライベートにします。 | 
| friendlist | フレンドリストを表示します。 | 
| togglepriv | プライバシーを切り替えます。 | 
| randomrecruit | スキンをランダムに選択された初期スキンに変更します。 |

# 使用可能なプライバシー
| プライバシー | 効果 |
:---|:--- 
| public | パブリック |
| private | プライベート |
| friends_allow_friends_of_friends | フレンドのフレンドを許可 |
| private_allow_friends_of_friends | フレンドのフレンドを許可(プライベート) |
| friends | フレンドのみ |

# 使用可能なプラットフォーム
| 名称 | 実際のプラットフォーム |
:---|:--- 
| WIN | Windows |
| MAC | MAC |
| PS4 | PS4 |
| PS5 | PS5 |
| XBO | XBox One |
| XBX | XBox Series X |
| SWT | Switch |
| IOS | IOS |
| AND | Android |

# getkdに使用できるプラットフォーム
- pad
- keyboard
- touch

# アップデート内容
- 一部バグを修正
- エラーを赤で表示するように
- 認証に失敗した際に再認証できるように
- プラットフォームの選択
- 新コマンド "randomrecruit" を追加

# 今後の予定
- ない

# よくわからない / バグがある
- [Twitter](https://twitter.com/brightnoahb) にDM送信してください
- [Discord](https://discord.gg/qkkARgd596)
