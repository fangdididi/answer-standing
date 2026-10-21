[English](README.md) | **简体中文**

# Answer Standing（AI 回答站位）

**查清 AI 助手到底怎么介绍你的产品，用数字说话，并在源头修正错误回答。**

当有人问 ChatGPT、Claude、Gemini、Perplexity、Copilot、DeepSeek、豆包或 Kimi“做 X 用什么工具最好”时，回答里会点名几个产品，再顺带说几条事实。Answer Standing 是一个 AI 智能体技能，用来测量：你的产品（或公司、项目、你自己的名字）在不在这些回答里，说的内容是不是真的，错误说法从哪里来，以及你的修正到底有没有带来变化。

它把 AI 当作证人：同样的问题问好几遍，原样记录每一条回答，把每条陈述与核实过的事实比对，把错误追溯到具体网页和平台资料，修正这些源头，再用同一套规程和诚实的统计检验复测。

## 为什么需要它

- **一张截图不算测量。** 回答会随运行次数、模式、语言和地区变化。本技能重复采样，用带 95% 区间的比率报告。
- **被提到还不够。** 被提到却说错价格，或者被安上同名者的负面新闻，可能比不被提到更糟。每条说法都要判定。
- **你改不了回答，只能改它的来源。** 每条错误说法都落到一个具体网址上的具体修正，以及一个复查日期。
- **不自我安慰。** 内置的对比会告诉你，变化是真实的、可能的，还是只是噪声。

## 功能

- 事实底表：带截至日期、公开网址、同名者和已失效事实
- 四类问题题库（品类题、对比题、直问题、问题题），核心题固定不改
- 固定采样规程：新对话、记录模式、每题 3 次以上、回答原文存档
- 逐条阅读回答：是否提及、排第几、态度（推荐/中性/提醒避开）、声量份额
- 六种说法判定：正确、过时、错误、编造、混淆、无法核对
- 来源追溯阶梯：从回答引用的链接一直查到“模型记忆”
- 源头优先的修正计划，带诚信底线（不刷评价、不匿名发帖）
- `standing.py` 辅助脚本（Python 3，无依赖）：`init`、`tally`、`claims`、`compare`
- 一页纸站位报告模板

## 安装

技能就是包含 `SKILL.md`（英文）和 `SKILL.zh-CN.md`（中文）的整个文件夹。请复制完整文件夹，让 `scripts/` 和 `templates/` 一起带上。

**Claude Code**

```bash
git clone https://github.com/fangdididi/answer-standing.git ~/.claude/skills/answer-standing
```

**Codex / 读取 `~/.agents/skills` 的智能体**

```bash
git clone https://github.com/fangdididi/answer-standing.git ~/.agents/skills/answer-standing
```

**Cursor**（项目的技能目录）

```bash
git clone https://github.com/fangdididi/answer-standing.git .cursor/skills/answer-standing
```

**其他智能体**：把 `SKILL.zh-CN.md` 或 `SKILL.md` 的内容粘贴进它的指令里，或者直接让它从本仓库地址安装这个技能。

## 使用

在对话里这样说即可：

- “查一下 ChatGPT 和 Perplexity 是怎么介绍我们的 App 的，网址 acme.example。”
- “AI 老说我们没有免费版，帮我查清原因并修好。”
- “我们一个月前改了价格页，AI 的回答变了吗？”
- “AI 推荐了哪个竞品而不是我们？为什么？”

智能体最多问三个问题，建好工作目录 `standing/`，然后按十个步骤走完。你也可以直接运行脚本：

```bash
python3 scripts/standing.py init standing/
python3 scripts/standing.py tally standing/answers.csv --brand "Acme"
python3 scripts/standing.py claims standing/claims.csv
python3 scripts/standing.py compare standing/answers-before.csv standing/answers-after.csv
```

## 输出示例

```text
answers read: 72   brand mentioned: 22   rate  30.6%  (95% range  21.1% -  42.0%)
by family
  category      3/18   16.7%
  comparison    1/18    5.6%
  direct       18/18  100.0%
  problem       0/18    0.0%  <- never mentioned

claims: 7   correct=2, stale=3, invented=1, conflated=1
wrong claims by fact (fix these first)
  platforms   2x  sources: own FAQ page /faq; comparison article 2025

before: 22/72  30.6%
after : 26/72  36.1%
z = +0.71  ->  no detectable change
```

上面的意思是：被点名问到时 AI 认识这个产品，但在品类题和问题题里几乎不会主动推荐；前后两批的提及率差异还在正常波动范围内，不能说已经变好。

完整示例见 [`examples/example-en.md`](examples/example-en.md)（一个产品）和 [`examples/example-zh.md`](examples/example-zh.md)（一位作者）。所有示例数据均为虚构。

## 文件结构

```text
answer-standing/
├── SKILL.md               # 技能说明（英文）
├── SKILL.zh-CN.md         # 技能说明（中文）
├── README.md
├── README.zh-CN.md
├── LICENSE
├── scripts/
│   └── standing.py        # init / tally / claims / compare
├── templates/
│   ├── truth-sheet.yaml   # 事实底表
│   ├── questions.csv      # 问题题库
│   ├── answers.csv        # 回答记录
│   └── claims.csv         # 说法判定
└── examples/
    ├── example-en.md
    ├── example-zh.md
    ├── answers-before.csv
    ├── answers-after.csv
    └── claims-before.csv
```

## 原则

- 只用核实过的事实；不知道就写不知道。
- 不承诺结果；结果连同不确定性一起报告。
- 不做操纵：不刷评价、不水军、不批量生产同质内容。

## 许可证

MIT © fangdididi
