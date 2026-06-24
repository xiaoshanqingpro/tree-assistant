#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""树木学助手 v1.5.1 — 交互优化：移除底部模拟考试/复习错题，题型筛选移入侧边栏，错题自动切换"""
import json, os, re, sys

# 脚本所在目录即项目根目录
base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "questions.json"), "r", encoding="utf-8") as f:
    questions = json.load(f)

page_table = [
    ("苏铁科",28,28,1),("银杏科",29,29,1),("南洋杉科",30,30,1),
    ("松科",31,55,25),("杉科",56,61,6),("柏科",62,68,7),
    ("罗汉松科",69,72,4),("三尖杉科",73,73,1),("红豆杉科",74,79,6),
    ("木兰科",80,106,27),("樟科",107,134,28),("蔷薇科",135,166,32),
    ("苏木科",167,182,16),("含羞草科",183,192,10),("蝶形花科",193,252,60),
    ("金缕梅科",253,264,12),("杨柳科",265,283,19),("壳斗科",284,313,30),
    ("胡桃科",314,320,7),("木麻黄科",321,321,1),("榆科",322,330,9),
    ("桑科",331,363,33),("梧桐科",364,373,10),("大戟科",374,388,15),
    ("山茶科",389,425,37),("桃金娘科",426,438,13),("红树科",439,483,45),
    ("芸香科",484,497,14),("楝科",498,505,8),("无患子科",506,512,7),
    ("漆树科",513,533,21),("木犀科",534,546,13),("茜草科",547,559,13),
    ("马鞭草科",560,582,23),("棕榈科",583,583,1),("竹亚科",584,609,26),
]

QJSON = json.dumps(questions, ensure_ascii=False)
PAGE_JSON = json.dumps(page_table, ensure_ascii=False)

retrieval_keys = [
    {"title":"裸子植物15种检索表","species":"苏铁、银杏、油杉、金钱松、马尾松、湿地松、杉木、柳杉、水杉、侧柏、福建柏、圆柏、罗汉松、竹柏、南方红豆杉",
     "key":"1. 茎常不分枝；叶大型羽状深裂……1.苏铁\n1. 茎有分枝；叶小型非羽状深裂\n  2. 叶扇形；叶脉二叉分枝……2.银杏\n  2. 叶非扇形\n    3. 雌球花发育成球果\n      4. 珠鳞与苞鳞离生\n        5. 叶条形种鳞扁平\n          6. 无短枝叶排成二列……3.油杉\n          6. 具短枝……4.金钱松\n        5. 叶针形种鳞盾状\n          7. 2针一束细软……5.马尾松\n          7. 3针一束粗硬……6.湿地松\n      4. 珠鳞与苞鳞合生/半合生\n        8. 螺旋状互生\n          9. 叶条状披针形……7.杉木\n          9. 叶锥形……8.柳杉\n        8. 交互对生叶条形……9.水杉\n    3. 种子包于肉质假种皮\n      10. 花粉有气囊假种皮全包\n        11. 叶条形螺旋状……10.罗汉松\n        11. 叶椭圆形近对生……11.竹柏\n      10. 花粉无气囊……12.南方红豆杉"},
    {"title":"木兰科-金缕梅科15种检索表","species":"白兰、鹅掌楸、樟树、山鸡椒、枇杷、月季、梅、凤凰木、紫荆、台湾相思、银合欢、红豆树、刺桐、枫香、檵木",
     "key":"1. 花被不分化为花萼和花冠\n  2. 花单生聚合果\n    3. 花腋生聚合蓇葖果……1.白兰花\n    3. 花顶生聚合翅果……2.鹅掌楸\n  2. 花排成花序核果/浆果\n    4. 圆锥花序两性花……3.樟树\n    4. 伞形花序单性花……4.山鸡椒\n1. 花被分化为花萼和花冠\n  5. 非蒴果\n    6. 非荚果\n      7. 梨果合心皮雌蕊子房下位……5.枇杷\n      7. 聚合瘦果/核果离心皮/单雌蕊\n        8. 聚合瘦果离心皮……6.月季\n        8. 核果单雌蕊……7.梅\n    6. 荚果\n      9. 整齐花镊合状头状花序\n        10. 花金黄色……8.台湾相思\n        10. 花银白色……9.银合欢\n      9. 不整齐花覆瓦状非头状\n        11. 非蝶形花冠\n          12. 伞房状总状……10.凤凰木\n          12. 花簇生……11.紫荆\n        11. 蝶形花冠\n          13. 圆锥花序雄蕊分离……12.红豆树\n          13. 总状花序单体雄蕊……13.刺桐\n  5. 蒴果\n    14. 单性花单被花头状……14.枫香\n    14. 两性花双被花短穗状……15.檵木"},
    {"title":"杨柳科-桃金娘科15种检索表","species":"垂柳、板栗、石栎、枫杨、木麻黄、榕树、构树、油桐、木油桐、茶、油茶、木荷、桉树、桃金娘、白千层",
     "key":"1. 复叶→一回奇数羽状复叶……1.枫杨\n1. 单叶\n  2. 柔荑花序\n    3. 雄花序柔荑状\n      4. 壳斗针刺状……2.板栗\n      4. 壳斗鳞片/瘤状……3.石栎\n    3. 蒴果种子有白毛……4.垂柳\n  2. 非柔荑花序\n    5. 蒴果\n      6. 子房上位有乳汁……5.油桐\n      6. 子房下位/半下位\n        7. 帽状体……6.桉树\n        7. 蒴果多种开裂……7.木荷\n    5. 非蒴果\n      8. 聚花果/隐花果有乳汁……8.榕树\n      8. 核果/浆果\n        9. 子房下位有帽状体……9.白千层\n        9. 子房上位核果含芳香油……10.茶"},
    {"title":"红树科-竹亚科15种检索表","species":"柑橘、龙眼、荔枝、盐肤木、桂花、女贞、水团花、柚木、棕榈、蒲葵、鱼尾葵、毛竹、孝顺竹、箭竹、苦竹",
     "key":"1. 双子叶\n  2. 复叶\n    3. 单身复叶……1.柑橘\n    3. 羽状复叶……2.龙眼\n  2. 单叶\n    4. 叶对生\n      5. 合瓣花冠\n        6. 子房上位蒴果/浆果……3.女贞\n        6. 子房上位核果/蒴果……4.桂花\n      5. 离瓣花冠有托叶……5.水团花\n    4. 叶互生/基生\n      7. 掌状分裂……6.棕榈\n      7. 羽状全裂鱼尾状……7.鱼尾葵\n1. 单子叶(竹亚科)\n  9. 合轴丛生……8.孝顺竹\n  9. 单轴散生……9.毛竹"},
]
KEY_JSON = json.dumps(retrieval_keys, ensure_ascii=False)

print(f"Questions: {len(questions)}, Page table: {len(page_table)} families")

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no,viewport-fit=cover,maximum-scale=1.0">
<meta name="theme-color" content="#3d7a54">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="树木学冲刺">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="manifest" href="manifest.json">
<title>树木学 v1.5.1</title>
<style>
:root{--g9:#1a3c2a;--g8:#2d5a3f;--g7:#3d7a54;--g6:#4a9a67;--g5:#5cb878;--g0:#edf7f0;--gold:#c8963e;--w:#fff;--t:#2c3e2d;--tl:#5a6b5c;--red:#c0392b;--r:16px;--rs:10px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif;background:linear-gradient(160deg,#e8f0e9,#d4e8d9 30%,#c8e0cf 60%,#e8f0e9);color:var(--t);line-height:1.55;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none}
.app{display:flex;flex-direction:column;height:100dvh;max-width:520px;margin:0 auto;overflow:hidden}

.topbar{display:flex;align-items:center;justify-content:space-between;padding:7px 12px;background:var(--g7);color:white;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,.15);z-index:10}
.topbar .title{font-size:15px;font-weight:700;display:flex;align-items:center;gap:4px}
.topbar .ver{font-size:9px;opacity:.55;font-weight:400;margin-left:4px}
.menu-btn{width:36px;height:36px;border:none;border-radius:50%;background:rgba(255,255,255,.2);color:white;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center}

.tabs{display:flex;flex-shrink:0;background:var(--w);border-bottom:2px solid #eee}
.tab{flex:1;padding:10px 6px;border:none;background:none;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;text-align:center;transition:all .2s;color:var(--tl);position:relative}
.tab.on{color:var(--g7)}.tab.on::after{content:'';position:absolute;bottom:-2px;left:10%;right:10%;height:3px;background:var(--g7);border-radius:2px}

.stats-row{display:flex;gap:4px;padding:6px 10px;flex-shrink:0;justify-content:center;background:rgba(255,255,255,.4)}
.stats-row .st{background:var(--w);border-radius:16px;padding:4px 12px;font-size:11px;font-weight:600;box-shadow:0 1px 4px rgba(0,0,0,.05);display:flex;align-items:center;gap:3px}
.stats-row .st b{font-size:14px}.st.ok b{color:var(--g6)}.st.rv b{color:#c62828}.st.cn b{color:var(--g7)}

.card-area{flex:1;display:flex;flex-direction:column;padding:8px 10px;overflow-y:auto;-webkit-overflow-scrolling:touch;min-height:0}
.card-area::-webkit-scrollbar{display:none}

.flashcard{flex:0 1 auto;align-self:stretch;display:flex;flex-direction:column;position:relative;min-height:200px;max-height:72vh;border-radius:var(--r);overflow:hidden;transition:box-shadow .2s,border-color .2s;margin:auto 0}
.flashcard.correct{border:3px solid #4caf50;box-shadow:0 0 28px rgba(76,175,80,.45)}
.flashcard.wrong{border:3px solid #ef5350;box-shadow:0 0 28px rgba(239,83,80,.45)}

.card-face{flex:1;border-radius:var(--r);padding:16px 14px;display:flex;flex-direction:column;overflow-y:auto;-webkit-overflow-scrolling:touch;border:3px solid transparent;max-height:70vh}
.card-face::-webkit-scrollbar{display:none}.card-face.hidden{display:none!important}
.front{background:linear-gradient(160deg,#fefefd,#faf8f2 50%,#f7f3e8);border-color:#e8dfcc;cursor:pointer}
.back{background:linear-gradient(160deg,#f8faf7,#eef5ef 50%,#e3efe4);border-color:#c8dcc8;cursor:pointer}

.feedback-ring{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;pointer-events:none;opacity:0;z-index:5;transition:opacity .12s}
.feedback-ring.good{background:rgba(76,175,80,.88);color:white}.feedback-ring.show{opacity:1}.feedback-ring.bad{background:rgba(239,83,80,.88);color:white}

.qtype-badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:600;margin-bottom:3px;align-self:flex-start}
.bt-noun{background:#e8f5e9;color:#2e7d32}.bt-fill{background:#e3f2fd;color:#1565c0}.bt-choice{background:#fff3e0;color:#e65100}.bt-judge{background:#fce4ec;color:#c62828}.bt-qa{background:#f3e5f5;color:#6a1b9a}
.ch-badge{font-size:10px;color:var(--tl);margin-bottom:6px}
.qtext{font-size:16px;font-weight:600;line-height:1.55;margin:4px 0;flex-shrink:0}
.opts{margin-top:8px;display:flex;flex-direction:column;gap:6px;flex-shrink:0}
.opt-btn{padding:10px 14px;border-radius:10px;border:2px solid #e0e0e0;font-size:13px;cursor:pointer;background:white;text-align:left;font-family:inherit;line-height:1.4;color:var(--t);transition:all .15s;display:flex;align-items:flex-start;gap:8px}
.opt-btn:active{transform:scale(.97)}
.opt-btn .ol{font-weight:700;flex-shrink:0;width:20px;height:20px;border-radius:50%;border:2px solid #ccc;display:flex;align-items:center;justify-content:center;font-size:10px;transition:all .15s}
.opt-btn.sel{border-color:var(--g6);background:#f0faf3}.opt-btn.sel .ol{border-color:var(--g6);background:var(--g6);color:white}
.opt-btn.rc{border-color:#4caf50!important;background:#e8f5e9!important}.opt-btn.rc .ol{border-color:#4caf50!important;background:#4caf50!important;color:white!important}
.opt-btn.rw{border-color:#ef5350!important;background:#fce4ec!important}.opt-btn.rw .ol{border-color:#ef5350!important;background:#ef5350!important;color:white!important}
.opt-btn.rn{border-color:#ddd!important;background:#f5f5f5!important;opacity:.4!important}
.opt-btn.disabled{pointer-events:none}

.hint{font-size:11px;color:var(--g6);font-weight:500;text-align:center;margin-top:auto;padding-top:6px;animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,to{opacity:.4}50%{opacity:1}}

.a-label{font-size:11px;font-weight:700;color:var(--g7);border-bottom:2px solid var(--g3);padding-bottom:5px;margin-bottom:8px;flex-shrink:0}
.a-text{font-size:14px;line-height:1.7;color:var(--t);flex:1;min-height:0;overflow-y:auto}.a-text strong{color:var(--g8)}
.a-page{display:block;margin-top:8px;padding:8px 12px;background:var(--g0);border-radius:8px;font-size:12px;color:var(--g7);font-weight:600}
.a-hint{font-size:10px;color:var(--tl);text-align:center;margin-top:auto;padding-top:8px;font-style:italic;flex-shrink:0}

.qa-area{display:flex;flex-direction:column;gap:8px;margin-top:10px;flex-shrink:0}
.qa-ta{width:100%;min-height:90px;padding:10px 12px;border:2px solid #ddd;border-radius:10px;font-size:13px;font-family:inherit;line-height:1.6;resize:vertical;color:var(--t);background:var(--w)}
.qa-ta:focus{outline:none;border-color:var(--g6);box-shadow:0 0 0 3px rgba(74,154,103,.15)}
.qa-sub{padding:8px 16px;border:none;border-radius:20px;background:var(--g6);color:white;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;align-self:flex-end}
.qa-sc{display:none;padding:10px;border-radius:8px;margin-top:6px;font-size:12px;line-height:1.6}
.qa-sc.show{display:block}.qa-hit{color:#2e7d32;font-weight:600}.qa-miss{color:#c62828;font-weight:600}
.qa-bar-outer{height:6px;background:#eee;border-radius:3px;margin:6px 0;overflow:hidden}.qa-bar-inner{height:100%;border-radius:3px;transition:width .5s}
.fill-blanks{display:flex;flex-direction:column;gap:8px;margin-top:8px;flex-shrink:0}
.fill-row{display:flex;align-items:center;gap:8px}
.fill-num{font-size:12px;font-weight:700;color:var(--g7);min-width:24px}
.fill-inp{flex:1;padding:8px 12px;border:2px solid #ddd;border-radius:8px;font-size:13px;font-family:inherit;background:var(--w);color:var(--t)}
.fill-inp:focus{outline:none;border-color:var(--g6)}
.fill-inp.ok{border-color:#4caf50!important;background:#e8f5e9!important}
.fill-inp.bad{border-color:#ef5350!important;background:#fce4ec!important}
.fill-check{padding:8px 16px;border:none;border-radius:20px;background:var(--g6);color:white;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;align-self:flex-end;margin-top:6px}
.fill-score{display:none;padding:8px;border-radius:8px;margin-top:6px;font-size:12px;line-height:1.6}
.fill-score.show{display:block}

.actions{display:flex;gap:7px;padding:8px 10px;flex-shrink:0;justify-content:center;background:rgba(255,255,255,.5);flex-wrap:wrap}
.btn{padding:10px 16px;border:none;border-radius:22px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;white-space:nowrap;display:flex;align-items:center;gap:4px;box-shadow:0 2px 8px rgba(0,0,0,.08);transition:all .15s}
.btn:active{transform:scale(.93)}.btn:disabled{opacity:.35;pointer-events:none}
.btn-ok{background:linear-gradient(135deg,#4caf50,#43a047);color:white;flex:1}
.btn-no{background:linear-gradient(135deg,#ef5350,#e53935);color:white;flex:1}
.btn-next{background:var(--w);color:var(--tl);border:1.5px solid #ddd}
.btn-rand{background:linear-gradient(135deg,var(--gold),#b8862d);color:white}

/* drawer */
.overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.4);z-index:99;opacity:0;pointer-events:none;transition:opacity .3s}
.overlay.open{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;bottom:0;width:86vw;max-width:360px;background:var(--w);z-index:100;transform:translateX(100%);transition:transform .35s cubic-bezier(.4,0,0,1);display:flex;flex-direction:column;box-shadow:-4px 0 32px rgba(0,0,0,.2)}
.drawer.open{transform:translateX(0)}
.drawer-head{background:linear-gradient(135deg,var(--g8),var(--g6));color:white;padding:24px 18px 16px;flex-shrink:0;display:flex;align-items:center;justify-content:space-between}
.drawer-head h3{font-size:16px}
.drawer-close{width:34px;height:34px;border:none;border-radius:50%;background:rgba(255,255,255,.2);color:white;font-size:18px;cursor:pointer}
.drawer-body{flex:1;overflow-y:auto;padding:0 12px 16px;-webkit-overflow-scrolling:touch}

/* Drawer sections & nav buttons */
.dr-section{margin-top:8px}
.dr-section-title{padding:8px 12px;background:var(--g0);border-radius:8px;font-size:12px;font-weight:600;color:var(--g7);cursor:pointer;display:flex;align-items:center;justify-content:space-between;user-select:none}
.dr-section-title .arrow{transition:transform .3s;font-size:10px}
.dr-section-title.open .arrow{transform:rotate(90deg)}
.dr-section-body{display:none;padding-top:6px}
.dr-section-body.open{display:block}

.dr-nav-btn{display:block;width:100%;padding:8px 12px;border:none;border-radius:8px;background:white;font-size:12px;text-align:left;cursor:pointer;font-family:inherit;margin-bottom:3px;font-weight:500;color:var(--t);box-shadow:0 1px 3px rgba(0,0,0,.06);transition:all .15s}
.dr-nav-btn:active{background:var(--g0);transform:scale(.98)}
.dr-nav-btn.active{border-left:3px solid var(--g6);background:var(--g0);color:var(--g7)}
.dr-nav-btn .icon{margin-right:6px}
.dr-nav-btn.warn{color:#c62828;font-weight:600}

/* Filter chips inside drawer */
.dr-chips{display:flex;flex-wrap:wrap;gap:4px;padding:4px 0}
.dr-chip{padding:3px 10px;border-radius:12px;border:1.5px solid #ddd;font-size:10px;cursor:pointer;background:white;font-weight:500;font-family:inherit}
.dr-chip.on{background:var(--g6);color:white;border-color:var(--g6)}

.dr-stats{display:flex;gap:6px;padding:6px 0}
.dr-st{flex:1;text-align:center;padding:8px 6px;border-radius:var(--rs);background:var(--g0)}
.dr-st .num{font-size:18px;font-weight:700}.dr-st .lbl{font-size:10px;color:var(--tl)}
.dr-st.ok .num{color:#2e7d32}.dr-st.no .num{color:#c62828}.dr-st.td .num{color:var(--t)}
.dr-progress{padding:0 0 8px}.dr-progress .bar-outer{height:5px;background:#ddd;border-radius:3px;overflow:hidden}
.dr-progress .bar-inner{height:100%;background:linear-gradient(90deg,var(--g5),var(--g6));border-radius:3px;transition:width .5s}

.q-nav-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:4px}
.q-nav-btn{padding:6px 8px;border-radius:6px;border:1.5px solid #ddd;font-size:10px;cursor:pointer;background:white;text-align:left;font-family:inherit;line-height:1.3;display:flex;align-items:center;gap:4px}
.q-nav-btn .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;background:#ddd}
.q-nav-btn .dot.ok{background:#4caf50}.q-nav-btn .dot.no{background:#ef5350}.q-nav-btn .dot.cur{background:var(--g6);box-shadow:0 0 0 3px rgba(74,154,103,.3)}
.q-nav-btn.current{border-color:var(--g6);background:var(--g0)}

/* viewer */
.vwr-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:#000;z-index:300;display:none;flex-direction:column}
.vwr-overlay.open{display:flex}
.vwr-head{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;color:white;flex-shrink:0}
.vwr-close{width:36px;height:36px;border:none;border-radius:50%;background:rgba(255,255,255,.2);color:white;font-size:20px;cursor:pointer}
.vwr-body{flex:1;overflow-y:auto;padding:16px;color:white;-webkit-overflow-scrolling:touch}

.page-tbl{width:100%;border-collapse:collapse;font-size:11px;margin-top:8px}
.page-tbl td,.page-tbl th{padding:5px 6px;text-align:center;border-bottom:1px solid rgba(255,255,255,.15)}
.page-tbl th{background:rgba(255,255,255,.1);color:white;font-weight:600;position:sticky;top:0}

.fab{position:fixed;bottom:24px;right:16px;width:52px;height:52px;border:none;border-radius:50%;background:linear-gradient(135deg,var(--g7),var(--g6));color:white;font-size:22px;cursor:pointer;z-index:50;box-shadow:0 4px 20px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;transition:all .2s}
.fab:active{transform:scale(.9)}
@media(max-width:480px){
  .card-face{padding:12px 10px}.qtext{font-size:14px}.opt-btn{font-size:12px;padding:8px 10px}.a-text{font-size:13px}.btn{padding:9px 12px;font-size:11px}
  .stats-row{padding:4px 6px;gap:3px}.stats-row .st{padding:3px 8px;font-size:10px}.stats-row .st b{font-size:12px}
  .topbar{padding:5px 10px}.topbar .title{font-size:13px}
}
</style>
</head>
<body>
<div class="app">

<div class="topbar">
  <div class="title">树木学·期末冲刺<span class="ver">v1.5.1</span></div>
  <button class="menu-btn" onclick="openDrawer()">&#9776;</button>
</div>

<div class="stats-row" id="statsRow">
  <div class="st"><b id="stRemain">-</b>剩余</div>
  <div class="st cn"><b id="stCorrect">0</b>正确</div>
  <div class="st ok"><b id="stAcc">-</b>正确率</div>
  <div class="st rv"><b id="stReview">0</b>需复习</div>
</div>

<div class="card-area" id="cardArea">
  <div class="flashcard" id="flashcard">
    <div class="card-face front" id="frontFace" onclick="onFrontTap(event)">
      <span class="qtype-badge" id="qtBadge"></span>
      <span class="ch-badge" id="chBadge"></span>
      <div class="qtext" id="qtext"></div>
      <div class="opts" id="optsBox"></div>
      <div class="hint" id="hintLine">点击卡片 / 按空格 查看答案</div>
      <div class="qa-area" id="qaArea" style="display:none">
        <textarea class="qa-ta" id="qaTA" placeholder="在此输入你的答案..."></textarea>
        <button class="qa-sub" onclick="submitQA(event)">提交作答</button>
        <div class="qa-sc" id="qaSc"></div>
      </div>
      <div class="fill-blanks" id="fillBlanks" style="display:none"></div>
      <button class="fill-check" id="fillCheck" style="display:none" onclick="checkFills(event)">提交填空</button>
      <div class="fill-score" id="fillScore"></div>
    </div>
    <div class="card-face back hidden" id="backFace" onclick="onBackTap(event)">
      <div class="a-label">参考答案</div>
      <div class="a-text" id="aText"></div>
      <span class="a-page" id="aPage" style="display:none"></span>
      <div class="a-hint">点击卡片 / 按空格 返回</div>
    </div>
    <div class="feedback-ring" id="fbRing"></div>
  </div>
</div>

<div class="actions" id="actionsBar">
  <button class="btn btn-ok" id="btnOk" disabled>答对了</button>
  <button class="btn btn-no" id="btnNo" disabled>需复习</button>
  <button class="btn btn-next" id="btnNext">下一题</button>
  <button class="btn btn-rand" id="btnRand">随机</button>
</div>


<button class="fab" onclick="openDrawer()">&#9776;</button>
</div><!-- /app -->

<div class="overlay" id="overlay" onclick="closeDrawer()"></div>
<div class="drawer" id="drawer">
  <div class="drawer-head"><h3>学习导航</h3><button class="drawer-close" onclick="closeDrawer()">&times;</button></div>
  <div class="drawer-body">

    <div class="dr-stats">
      <div class="dr-st ok"><div class="num" id="dsOk">0</div><div class="lbl">已掌握</div></div>
      <div class="dr-st no"><div class="num" id="dsNo">0</div><div class="lbl">需复习</div></div>
      <div class="dr-st td"><div class="num" id="dsTodo">0</div><div class="lbl">未作答</div></div>
    </div>
    <div class="dr-progress"><span style="font-size:10px;color:var(--tl)">进度 <b id="dsPct">0%</b></span>
      <div class="bar-outer"><div class="bar-inner" id="dsBar" style="width:0%"></div></div>
    </div>

    <!-- Quick actions -->
    <button class="dr-nav-btn" id="drExam"><span class="icon">&#128220;</span> 模拟考试（随机组卷）</button>
    <button class="dr-nav-btn warn" id="drReviewWrong" style="display:none"><span class="icon">&#128260;</span> 只练错题</button>
    <button class="dr-nav-btn" id="drShuffle"><span class="icon">&#127922;</span> 随机全部（重置进度）</button>

    <!-- 题型导航 -->
    <div class="dr-section" id="drSecType">
      <div class="dr-section-title open" onclick="drToggle('drSecType')">题型导航 <span class="arrow">&#9660;</span></div>
      <div class="dr-section-body open" id="drSecTypeBody">
        <div class="dr-chips" id="drTypeChips"></div>
      </div>
    </div>

    <!-- 章节导航 -->
    <div class="dr-section" id="drSecChap">
      <div class="dr-section-title" onclick="drToggle('drSecChap')">章节导航 <span class="arrow">&#9654;</span></div>
      <div class="dr-section-body" id="drSecChapBody">
        <div class="q-nav-grid" id="dsChapters"></div>
      </div>
    </div>

    <!-- 题库（默认收起） -->
    <div class="dr-section" id="drSecBank">
      <div class="dr-section-title" onclick="drToggle('drSecBank')">全部题目 <span style="font-size:10px;color:var(--tl);font-weight:400" id="drBankCnt"></span> <span class="arrow">&#9654;</span></div>
      <div class="dr-section-body" id="drSecBankBody">
        <div class="q-nav-grid" id="dsAllQ"></div>
      </div>
    </div>

    <!-- 工具 -->
    <div class="dr-section" id="drSecTools">
      <div class="dr-section-title" onclick="drToggle('drSecTools')">工具 <span class="arrow">&#9654;</span></div>
      <div class="dr-section-body" id="drSecToolsBody">
        <button class="dr-nav-btn" id="drPageTable"><span class="icon">&#128214;</span> 课本页码对照表 (36科)</button>
        <button class="dr-nav-btn" id="drKeys"><span class="icon">&#128221;</span> 检索表练习</button>
        <button class="dr-nav-btn" id="drReset"><span class="icon">&#128260;</span> 重置进度</button>
      </div>
    </div>
  </div>
</div>

<div class="vwr-overlay" id="vwrOverlay">
  <div class="vwr-head"><span id="vwrTitle"></span><button class="vwr-close" onclick="closeViewer()">&times;</button></div>
  <div class="vwr-body" id="vwrBody"></div>
</div>

<script>
var QDATA = ''' + QJSON + r''';
var KEY_DATA = ''' + KEY_JSON + r''';
var PAGE_DATA = ''' + PAGE_JSON + r''';

var qs=[],ci=0,flipped=false,hist={},streak=0,mode='all';
var TM={"名词解释":"bt-noun","填空题":"bt-fill","单选题":"bt-choice","判断题":"bt-judge","问答题":"bt-qa"};
var LM={"名词解释":"名","填空题":"填","单选题":"选","判断题":"判","问答题":"问"};
var TP=["名词解释","填空题","单选题","判断题","问答题"];
var aType="all",aCh="all";
var judging=false,chosen=null,timer=null;

// ====== PERSIST ======
function sh(){try{localStorage.setItem('dendrology_v13',JSON.stringify(hist));}catch(e){}}
function lh(){try{var h=localStorage.getItem('dendrology_v13');if(h){hist=JSON.parse(h);}}catch(e){}}
function ct(){if(timer){clearTimeout(timer);timer=null;}}

// ====== FILTERS ======
function buildQs(){
  if(mode==='wrong'){
    var ids=Object.keys(hist).filter(function(k){return hist[k]==='wrong';});
    if(!ids.length){mode='all';qs=QDATA.filter(function(q){return(aType==='all'||q.type===aType)&&(aCh==='all'||q.chapter===aCh);});}
    else{qs=QDATA.filter(function(q){return ids.indexOf(String(q.id))>=0&&(aType==='all'||q.type===aType)&&(aCh==='all'||q.chapter===aCh);});}
  }else{
    qs=QDATA.filter(function(q){return(aType==='all'||q.type===aType)&&(aCh==='all'||q.chapter===aCh);});
  }
  if(!qs.length)qs=QDATA.slice();ci=Math.min(ci,qs.length-1);if(ci<0)ci=0;
}

function setType(t){aType=t;if(t!=='all')aCh='all';buildQs();rc();renderAll();ud();}
function setCh(c){aCh=c;if(c!=='all')aType='all';buildQs();rc();renderAll();ud();}
function rc(){ct();chosen=null;judging=false;flipped=false;}

// ====== RENDER ======
function renderAll(){renderCard();updateStats();ub();}
function renderCard(){
  rc();var q=qs[ci];if(!q)return;
  document.getElementById('qtBadge').textContent=q.type;document.getElementById('qtBadge').className='qtype-badge '+TM[q.type];
  document.getElementById('chBadge').textContent=q.chapter+(mode==='wrong'?' [错题库]':'');
  document.getElementById('qtext').textContent=q.question;
  document.getElementById('aText').innerHTML=fmt(q.answer);
  var ap=document.getElementById('aPage');
  if(q.chapter){var pt=PAGE_DATA.find(function(p){return p[0]===q.chapter;});if(pt){ap.style.display='';ap.innerHTML='📖 课本 '+pt[1]+'-'+pt[2]+'页 ('+pt[3]+'页)';}else{ap.style.display='none';}}else{ap.style.display='none';}
  if(q.type==='判断题'){document.getElementById('optsBox').innerHTML='<button class="opt-btn" data-oi="0"><span class="ol">✓</span> 正确</button><button class="opt-btn" data-oi="1"><span class="ol">✗</span> 错误</button>';document.getElementById('optsBox').style.display='';document.getElementById('hintLine').textContent='点击判断，自动揭晓';}
  else if(q.options){var opts=q.options.split(/[A-D]\.\s*/).filter(Boolean);var oh='';opts.forEach(function(o,i){oh+='<button class="opt-btn" data-oi="'+i+'"><span class="ol">'+String.fromCharCode(65+i)+'</span>'+o.trim()+'</button>';});document.getElementById('optsBox').innerHTML=oh;document.getElementById('optsBox').style.display='';document.getElementById('hintLine').textContent='点击选项作答 / 点击卡片翻转';}
  else{document.getElementById('optsBox').innerHTML='';document.getElementById('optsBox').style.display='none';document.getElementById('hintLine').textContent='点击卡片 / 按空格 查看答案';document.getElementById('fillBlanks').style.display='none';document.getElementById('fillCheck').style.display='none';document.getElementById('fillScore').className='fill-score';if(q.type==='填空题'){var blanks=q.answer.split(';');var fb='';blanks.forEach(function(b,i){fb+='<div class=fill-row><span class=fill-num>'+(i+1)+'.</span><input class=fill-inp id=fillInp'+i+' placeholder=第'+(i+1)+'空></div>';});document.getElementById('fillBlanks').innerHTML=fb;document.getElementById('fillBlanks').style.display='';document.getElementById('fillCheck').style.display='';document.getElementById('hintLine').textContent='填写后点击提交填空核对答案';document.getElementById('optsBox').style.display='none';}else if(q.type==='问答题'){document.getElementById('qaArea').style.display='';document.getElementById('qaTA').value='';document.getElementById('qaSc').className='qa-sc';}else{document.getElementById('qaArea').style.display='none';}}
  document.getElementById('frontFace').classList.remove('hidden');document.getElementById('backFace').classList.add('hidden');
  document.getElementById('flashcard').className='flashcard';document.getElementById('fbRing').className='feedback-ring';
  document.getElementById('cardArea').scrollTop=0;ub();
}

function fmt(t){return t.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>');}
function ub(){
  var q=qs[ci];var isI=q&&(q.type==='单选题'||q.type==='判断题');var en=flipped&&!isI&&qs.length>0;
  var bok=document.getElementById('btnOk'),bno=document.getElementById('btnNo');
  if(bok){bok.disabled=!en;bok.style.display=isI?'none':'';}
  if(bno){bno.disabled=!en;bno.style.display=isI?'none':'';}
}

// ====== CARD TAP ======
function onFrontTap(e){e.stopPropagation();if(judging||timer)return;var t=e.target;if(t.tagName==='INPUT'||t.tagName==='TEXTAREA')return;var b=t.closest('button.opt-btn');if(b){if(chosen!==null)return;choiceSel(b);return;}doFlip();}
function onBackTap(e){e.stopPropagation();if(judging||timer)return;if(qs[ci]&&qs[ci].type==='判断题'&&chosen!==null){nextQ();return;}if(chosen!==null)return;doFlip();}
function choiceSel(btn){
  if(judging||chosen!==null)return;var idx=parseInt(btn.dataset.oi);chosen=idx;judging=true;
  var btns=document.querySelectorAll('.opt-btn');btns.forEach(function(b,i){b.classList.add('disabled');if(i===idx)b.classList.add('sel');else b.classList.add('rn');});
  timer=setTimeout(function(){
    document.getElementById('frontFace').classList.add('hidden');document.getElementById('backFace').classList.remove('hidden');document.getElementById('cardArea').scrollTop=0;flipped=true;
    var q=qs[ci],correctIdx;
    if(q.type==='判断题')correctIdx=q.answer.indexOf('✓')===0?0:1;
    else{var m=q.answer.match(/^([A-D])\./);correctIdx=m?m[1].charCodeAt(0)-65:-1;}
    var ok=(idx===correctIdx),fc=document.getElementById('flashcard'),ring=document.getElementById('fbRing');
    if(ok){fc.className='flashcard correct';ring.className='feedback-ring good show';ring.textContent='✓';hist[q.id]='correct';streak++;btns[idx].classList.add('rc');}
    else{fc.className='flashcard wrong';ring.className='feedback-ring bad show';ring.textContent='✗';hist[q.id]='wrong';streak=0;btns[idx].classList.add('rw');if(correctIdx>=0)btns[correctIdx].classList.add('rc');}
    sh();updateStats();ud();ub();
    timer=setTimeout(function(){ring.className='feedback-ring';fc.className='flashcard';judging=false;timer=null;},800);
  },400);
}
function doFlip(){
  if(!qs.length||judging||timer)return;var q=qs[ci];
  if((q.type==='单选题'||q.type==='判断题')&&chosen===null){flipped=!flipped;if(flipped){document.getElementById('frontFace').classList.add('hidden');document.getElementById('backFace').classList.remove('hidden');}else{document.getElementById('frontFace').classList.remove('hidden');document.getElementById('backFace').classList.add('hidden');}ub();return;}
  if(q.type!=='单选题'&&q.type!=='判断题'){flipped=!flipped;if(flipped){document.getElementById('frontFace').classList.add('hidden');document.getElementById('backFace').classList.remove('hidden');}else{document.getElementById('frontFace').classList.remove('hidden');document.getElementById('backFace').classList.add('hidden');}ub();}
}

// ====== MARK ======
function doMark(ok){
  if(!flipped||!qs.length||timer||judging)return;var q=qs[ci];if(q.type==='单选题'||q.type==='判断题')return;
  judging=true;ct();var fc=document.getElementById('flashcard'),ring=document.getElementById('fbRing');
  if(ok){ring.className='feedback-ring good show';ring.textContent='✓';fc.className='flashcard correct';hist[q.id]='correct';streak++;}
  else{ring.className='feedback-ring bad show';ring.textContent='✗';fc.className='flashcard wrong';hist[q.id]='wrong';streak=0;}
  sh();updateStats();ud();ub();
  timer=setTimeout(function(){ring.className='feedback-ring';fc.className='flashcard';judging=false;timer=null;nextQ();},500);
}
function updateStats(){
  var tot=qs.length,ans=qs.filter(function(q){return hist[q.id];}).length,ok=qs.filter(function(q){return hist[q.id]==='correct';}).length,no=QDATA.filter(function(q){return hist[q.id]==='wrong';}).length;
  document.getElementById('stRemain').textContent=tot-ans;document.getElementById('stCorrect').textContent=ok;document.getElementById('stAcc').textContent=ans>0?Math.round(ok/ans*100)+'%':'-';document.getElementById('stReview').textContent=no;
}

// ====== QA SCORING ======
function submitQA(e){e.stopPropagation();var q=qs[ci];if(!q||q.type!=='问答题')return;var t=document.getElementById('qaTA').value.trim();if(!t){alert('请先输入答案！');return;}scoreIt(t,q,'qaSc');}
function scoreIt(txt,q,sid){
  var kw=q.keywords||[];if(!kw.length)return;var hit=[],miss=[];kw.forEach(function(k){if(txt.indexOf(k)>=0)hit.push(k);else miss.push(k);});
  var pct=Math.round(hit.length/kw.length*100),cl=pct>=70?'#4caf50':pct>=40?'#ff9800':'#e74c3c';
  var el=document.getElementById(sid);el.innerHTML='<div style=font-weight:700>得分:<span style=color:'+cl+'>'+hit.length+'/'+kw.length+'('+pct+'%)</span></div>'+(hit.length?'<div style=margin-top:4px><span class=qa-hit>'+hit.join(' ✓ ')+'</span></div>':'')+(miss.length?'<div style=margin-top:4px><span class=qa-miss>'+miss.join(' ✗ ')+'</span></div>':'')+'<div class=qa-bar-outer><div class=qa-bar-inner style=width:'+pct+'%;background:'+cl+'></div></div><div style=font-size:11px;color:var(--tl);margin-top:4px>点击卡片/空格查看完整参考答案</div>';el.className='qa-sc show';
  var ok=pct>=60;if(!hist[q.id]){hist[q.id]=ok?'correct':'wrong';if(ok)streak++;else streak=0;sh();updateStats();ud();}
}


// ====== FILL-BLANK CHECKING ======
function checkFills(e){
  e.stopPropagation();
  var q=qs[ci];if(!q||q.type!=='填空题')return;
  var blanks=q.answer.split(';');var correct=0,total=blanks.length;
  blanks.forEach(function(ans,i){
    var inp=document.getElementById('fillInp'+i);if(!inp)return;
    var val=inp.value.trim().replace(/\s+/g,'');
    var exp=ans.trim().replace(/\s+/g,'');
    var terms=exp.split(/[、，,。\.]/).filter(function(t){return t.length>=2;});
    if(terms.length<1)terms=[exp];
    var hit=terms.some(function(t){return val.indexOf(t)>=0;});
    if(hit||val===exp||(exp.length>8&&val.length>=exp.length*0.5&&exp.indexOf(val)>=0)){
      inp.classList.add('ok');inp.classList.remove('bad');correct++;
    }else{inp.classList.add('bad');inp.classList.remove('ok');}
  });
  var pct=Math.round(correct/total*100),cl=pct>=70?'#4caf50':pct>=40?'#ff9800':'#e74c3c';
  var el=document.getElementById('fillScore');
  el.innerHTML='<div style=font-weight:700>填空得分:<span style=color:'+cl+'>'+correct+'/'+total+'('+pct+'%)</span></div><div class=qa-bar-outer><div class=qa-bar-inner style=width:'+pct+'%;background:'+cl+'></div></div><div style=font-size:11px;color:var(--tl);margin-top:4px>点击卡片/空格查看完整参考答案</div>';
  el.className='fill-score show';
  var ok=pct>=60;
  if(!hist[q.id]){hist[q.id]=ok?'correct':'wrong';if(ok)streak++;else streak=0;sh();updateStats();ud();}
}

// ====== NAV ======
function nextQ(){if(!qs.length)return;ci=(ci+1)%qs.length;rc();renderAll();}
function prevQ(){if(ci>0){ci--;rc();renderAll();}}
function randQ(){if(!qs.length)return;ci=Math.floor(Math.random()*qs.length);rc();renderAll();}
function jumpTo(i){ci=i;rc();renderAll();}

// ====== DRAWER ======
function openDrawer(){document.getElementById('overlay').classList.add('open');document.getElementById('drawer').classList.add('open');ud();}
function closeDrawer(){document.getElementById('overlay').classList.remove('open');document.getElementById('drawer').classList.remove('open');}
function drToggle(id){var b=document.getElementById(id+'Body'),t=document.querySelector('#'+id+' .dr-section-title');if(b.classList.contains('open')){b.classList.remove('open');t.classList.remove('open');}else{b.classList.add('open');t.classList.add('open');}}

function ud(){
  var tot=qs.length,ok=qs.filter(function(q){return hist[q.id]==='correct';}).length,no=qs.filter(function(q){return hist[q.id]==='wrong';}).length;
  document.getElementById('dsOk').textContent=ok;document.getElementById('dsNo').textContent=no;document.getElementById('dsTodo').textContent=tot-ok-no;
  var pct=tot>0?Math.round((ok+no)/tot*100):0;document.getElementById('dsPct').textContent=pct+'%';document.getElementById('dsBar').style.width=pct+'%';
  document.getElementById('drBankCnt').textContent='('+tot+'题)';
  var allWrong=QDATA.filter(function(q){return hist[q.id]==='wrong';}).length;
  var rwBtn=document.getElementById('drReviewWrong');
  if(allWrong>0){rwBtn.style.display='';rwBtn.innerHTML='<span class="icon">&#128260;</span> 只练错题 ('+allWrong+'题)';}else{rwBtn.style.display='none';}
  if(mode==='wrong')rwBtn.classList.add('active');else rwBtn.classList.remove('active');

  // Type chips
  var tc=document.getElementById('drTypeChips');
  tc.innerHTML='<button class="dr-chip'+(aType==='all'&&mode!=='wrong'?' on':'')+'" onclick="drSetType(\'all\');closeDrawer()">全部</button>';
  TP.forEach(function(t){
    var n=QDATA.filter(function(q){return q.type===t&&(mode!=='wrong'||hist[q.id]==='wrong');}).length;
    if(n>0)tc.innerHTML+='<button class="dr-chip'+(aType===t&&mode!=='wrong'?' on':'')+'" onclick="drSetType(\''+t+'\');closeDrawer()">'+t+'('+n+')</button>';
  });

  // Chapter nav
  var CH=[];
  QDATA.forEach(function(q){if(CH.indexOf(q.chapter)<0)CH.push(q.chapter);});
  var fm={"苏铁科":"总论-裸子植物","银杏科":"总论-裸子植物","南洋杉科":"总论-裸子植物","松科":"总论-裸子植物","杉科":"总论-裸子植物","柏科":"总论-裸子植物","罗汉松科":"总论-裸子植物","三尖杉科":"总论-裸子植物","红豆杉科":"总论-裸子植物","木兰科":"木兰科-金缕梅科","樟科":"木兰科-金缕梅科","蔷薇科":"木兰科-金缕梅科","苏木科":"木兰科-金缕梅科","含羞草科":"木兰科-金缕梅科","蝶形花科":"木兰科-金缕梅科","金缕梅科":"木兰科-金缕梅科","杨柳科":"杨柳科-桃金娘科","壳斗科":"杨柳科-桃金娘科","胡桃科":"杨柳科-桃金娘科","木麻黄科":"杨柳科-桃金娘科","榆科":"杨柳科-桃金娘科","桑科":"杨柳科-桃金娘科","梧桐科":"杨柳科-桃金娘科","大戟科":"杨柳科-桃金娘科","山茶科":"杨柳科-桃金娘科","桃金娘科":"杨柳科-桃金娘科","红树科":"红树科-竹亚科","芸香科":"红树科-竹亚科","楝科":"红树科-竹亚科","无患子科":"红树科-竹亚科","漆树科":"红树科-竹亚科","木犀科":"红树科-竹亚科","茜草科":"红树科-竹亚科","马鞭草科":"红树科-竹亚科","棕榈科":"红树科-竹亚科","竹亚科":"红树科-竹亚科"};
  var ch='';var seen={};var chapCnt={};
  QDATA.forEach(function(q){var bc=fm[q.chapter]||'';if(bc)chapCnt[bc]=(chapCnt[bc]||0)+1;});
  PAGE_DATA.forEach(function(p){
    var fn=p[0],bc=fm[fn]||'';
    if(!seen[bc]){seen[bc]=true;var cnt=chapCnt[bc]||0;ch+='<button class=\"q-nav-btn\" style=\"grid-column:1/-1;background:var(--g0);font-weight:700;font-size:11px\" onclick=\"drSetCh(\\''+bc+'\\');closeDrawer()\">'+bc+' ('+cnt+'题)</button>';}
    var n=QDATA.filter(function(q){return q.chapter===bc;}).length;
    ch+='<button class=\"q-nav-btn'+(aCh===bc?' current':'')+'\" onclick=\"drSetCh(\\''+bc+'\\');closeDrawer()\" title=\"课本p'+p[1]+'-'+p[2]+'\">'+fn+'</button>';
  });
  document.getElementById('dsChapters').innerHTML=ch||'<div style=\"font-size:10px;color:var(--tl)\">暂无</div>';

  // Question grid
  var qh='';qs.forEach(function(q,i){var cls='q-nav-btn';if(i===ci)cls+=' current';var dot='dot';if(hist[q.id]==='correct')dot+=' ok';if(hist[q.id]==='wrong')dot+=' no';if(i===ci)dot+=' cur';qh+='<button class="'+cls+'" data-qi="'+i+'"><span class="'+dot+'"></span>'+LM[q.type]+(i+1)+' '+q.question.substring(0,10)+'</button>';});
  document.getElementById('dsAllQ').innerHTML=qh||'<div style="font-size:10px;color:var(--tl)">暂无</div>';
}

function drSetType(t){
  mode='all';aType=t;aCh='all';buildQs();rc();renderAll();ud();
}
function drSetCh(c){
  mode='all';aCh=c;aType='all';buildQs();rc();renderAll();ud();
}
function startWrongMode(){
  var ids=Object.keys(hist).filter(function(k){return hist[k]==='wrong';});
  if(!ids.length){alert('暂无错题！');return;}
  mode='wrong';aType='all';aCh='all';buildQs();ci=0;rc();renderAll();ud();
}

// ====== EXAM MODE ======
var examQ=[],examIdx=0,examHist={},eJudging=false,eChosen=null,eTimer=null;
var EX={names:5,fills:10,choices:10,judges:10,qas:5};

function startExam(){
  if(!confirm('开始模拟考试？\n题型:名词解释5+填空10+单选10+判断10+问答5=40题\n（与真实考试题型一致）'))return;
  closeDrawer();
  document.getElementById('actionsBar').style.display='none';
  var pool={};TP.forEach(function(t){pool[t]=[];});QDATA.forEach(function(q){if(pool[q.type])pool[q.type].push(q);});
  function pick(arr,n){var a=arr.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a.slice(0,n);}
  examQ=[];examQ=examQ.concat(pick(pool['名词解释']||[],EX.names)).concat(pick(pool['填空题']||[],EX.fills)).concat(pick(pool['单选题']||[],EX.choices)).concat(pick(pool['判断题']||[],EX.judges)).concat(pick(pool['问答题']||[],EX.qas));
  examIdx=0;examHist={};eJudging=false;eChosen=null;
  document.getElementById('flashcard').innerHTML='<div class="card-face front" id="eFront" onclick="eTap(event)"><span class="qtype-badge" id="eBadge"></span><span class="ch-badge" id="eCh"></span><div style="font-size:11px;color:var(--tl);margin-bottom:8px" id="eProg"></div><div class="qtext" id="eQ"></div><div class="opts" id="eOpts"></div><div class="hint" id="eHint">点击卡片/空格 查看答案</div></div><div class="card-face back hidden" id="eBack" onclick="eTap(event)"><div class="a-label">参考答案</div><div class="a-text" id="eA"></div><div class="a-hint">点击卡片/空格 返回，点答对/需复习继续</div></div><div class="feedback-ring" id="eRing"></div>';
  document.getElementById('actionsBar').style.display='flex';
  document.getElementById('actionsBar').innerHTML='<button class="btn btn-ok" id="eOk" disabled>答对了</button><button class="btn btn-no" id="eNo" disabled>需复习</button><button class="btn btn-next" id="eNext">下一题</button><button class="btn" onclick="submitExam()" style="background:linear-gradient(135deg,#c0392b,#e74c3c);color:white">交卷</button>';
  document.getElementById('eOk').onclick=function(){eMark(true);};document.getElementById('eNo').onclick=function(){eMark(false);};document.getElementById('eNext').onclick=function(){eNextQ();};
  eRender();eStats();
}
function eRender(){
  var q=examQ[examIdx];if(!q)return;eJudging=false;document.getElementById('eBadge').textContent=q.type;document.getElementById('eBadge').className='qtype-badge '+TM[q.type];document.getElementById('eCh').textContent=q.chapter;document.getElementById('eQ').textContent=q.question;document.getElementById('eA').innerHTML=fmt(q.answer);document.getElementById('eProg').textContent='第'+(examIdx+1)+'/'+examQ.length+'题  '+q.type;
  if(q.type==='判断题'){document.getElementById('eOpts').innerHTML='<button class="opt-btn" data-oi="0"><span class="ol">✓</span> 正确</button><button class="opt-btn" data-oi="1"><span class="ol">✗</span> 错误</button>';document.getElementById('eOpts').style.display='';document.getElementById('eHint').textContent='点击判断';}
  else if(q.options){var opts=q.options.split(/[A-D]\.\s*/).filter(Boolean);var oh='';opts.forEach(function(o,i){oh+='<button class="opt-btn" data-oi="'+i+'"><span class="ol">'+String.fromCharCode(65+i)+'</span>'+o.trim()+'</button>';});document.getElementById('eOpts').innerHTML=oh;document.getElementById('eOpts').style.display='';document.getElementById('eHint').textContent='点击选项作答';}
  else{document.getElementById('eOpts').innerHTML='';document.getElementById('eOpts').style.display='none';document.getElementById('eHint').textContent='点击卡片/空格查看答案';}
  document.getElementById('eFront').classList.remove('hidden');document.getElementById('eBack').classList.add('hidden');document.getElementById('cardArea').scrollTop=0;eUb();
}
function eTap(e){e.stopPropagation();var b=e.target.closest('button.opt-btn');if(b){eChoice(b);return;}var q=examQ[examIdx];if(!q.options&&q.type!=='判断题'){if(document.getElementById('eBack').classList.contains('hidden')){document.getElementById('eFront').classList.add('hidden');document.getElementById('eBack').classList.remove('hidden');}else{document.getElementById('eFront').classList.remove('hidden');document.getElementById('eBack').classList.add('hidden');}eUb();}}
function eChoice(btn){
  if(eJudging)return;eJudging=true;var idx=parseInt(btn.dataset.oi);
  var btns=document.querySelectorAll('#flashcard .opt-btn');btns.forEach(function(b,i){b.classList.add('disabled');if(i===idx)b.classList.add('sel');else b.classList.add('rn');});
  eTimer=setTimeout(function(){
    document.getElementById('eFront').classList.add('hidden');document.getElementById('eBack').classList.remove('hidden');document.getElementById('cardArea').scrollTop=0;
    var q=examQ[examIdx],correctIdx;
    if(q.type==='判断题')correctIdx=q.answer.indexOf('✓')===0?0:1;
    else{var m=q.answer.match(/^([A-D])\./);correctIdx=m?m[1].charCodeAt(0)-65:-1;}
    var ok=(idx===correctIdx);
    if(ok){examHist[examIdx]='correct';document.getElementById('flashcard').className='flashcard correct';btns[idx].classList.add('rc');}else{examHist[examIdx]='wrong';document.getElementById('flashcard').className='flashcard wrong';btns[idx].classList.add('rw');if(correctIdx>=0)btns[correctIdx].classList.add('rc');}
    eStats();eUb();setTimeout(function(){document.getElementById('flashcard').className='flashcard';eJudging=false;},600);
  },400);
}
function eMark(ok){var q=examQ[examIdx];if(q.options||q.type==='判断题')return;if(document.getElementById('eBack').classList.contains('hidden'))return;examHist[examIdx]=ok?'correct':'wrong';eStats();eNextQ();}
function eNextQ(){if(examIdx<examQ.length-1){examIdx++;eRender();eStats();}else{submitExam();}}
function eUb(){var q=examQ[examIdx],isI=q&&(q.options||q.type==='判断题'),vis=!document.getElementById('eBack').classList.contains('hidden');document.getElementById('eOk').disabled=!(vis&&!isI);document.getElementById('eNo').disabled=!(vis&&!isI);document.getElementById('eOk').style.display=isI?'none':'';document.getElementById('eNo').style.display=isI?'none':'';}
function eStats(){var tot=examQ.length,ans=Object.keys(examHist).length,ok=Object.values(examHist).filter(function(v){return v==='correct';}).length;document.getElementById('stRemain').textContent=tot-ans;document.getElementById('stCorrect').textContent=ok;document.getElementById('stAcc').textContent=ans>0?Math.round(ok/ans*100)+'%':'-';}

function submitExam(){
  var tot=examQ.length,ans=Object.keys(examHist).length,ok=Object.values(examHist).filter(function(v){return v==='correct';}).length,score=Math.round(ok/tot*100);if(isNaN(score))score=0;
  alert('考试结束!\n得分:'+score+'分('+ok+'/'+tot+')');
  mode='all';aType='all';aCh='all';buildQs();rc();renderAll();ud();
  document.getElementById('actionsBar').innerHTML='<button class="btn btn-ok" id="btnOk" disabled>答对了</button><button class="btn btn-no" id="btnNo" disabled>需复习</button><button class="btn btn-next" id="btnNext">下一题</button><button class="btn btn-rand" id="btnRand">随机</button>';
  document.getElementById('actionsBar').style.display='';
  setupMainBtns();
}

// ====== VIEWER ======
function showPageTable(){
  var h='<h3 style="font-size:16px;margin-bottom:12px">36科 - 课本页码对照表</h3><p style="font-size:12px;opacity:.7;margin-bottom:12px">《树木学(南方本)》祁承经、汤庚国 | 上册p28-320 | 下册p321-609</p>';
  h+='<table class="page-tbl"><tr><th>#</th><th>科名</th><th>起始页</th><th>结束页</th><th>页数</th></tr>';
  PAGE_DATA.forEach(function(p,i){h+='<tr><td>'+(i+1)+'</td><td>'+p[0]+'</td><td>'+p[1]+'</td><td>'+p[2]+'</td><td>'+p[3]+'</td></tr>';});
  h+='</table><p style="font-size:10px;opacity:.5;margin-top:12px;text-align:center">共36科 582页</p>';
  document.getElementById('vwrTitle').textContent='课本页码对照表';document.getElementById('vwrBody').innerHTML=h;document.getElementById('vwrOverlay').classList.add('open');
}
function showKeys(){
  var h='<h3 style="font-size:16px;margin-bottom:8px">编制检索表练习</h3><p style="font-size:11px;opacity:.7;margin-bottom:14px">考试分值:10分 | 10个物种 | 定距格式 | 建议优先裸子/被子、双子叶/单子叶、科特征编排</p>';
  KEY_DATA.forEach(function(k,i){h+='<div style="background:rgba(255,255,255,.08);border-radius:8px;padding:12px;margin-bottom:10px"><h4 style="font-size:13px;margin-bottom:4px">'+(i+1)+'. '+k.title+'</h4><p style="font-size:10px;opacity:.7;margin-bottom:6px">物种:'+k.species+'</p><pre style="font-size:10px;line-height:1.6;white-space:pre-wrap">'+k.key+'</pre></div>';});
  document.getElementById('vwrTitle').textContent='检索表练习';document.getElementById('vwrBody').innerHTML=h;document.getElementById('vwrOverlay').classList.add('open');
}
function closeViewer(){document.getElementById('vwrOverlay').classList.remove('open');}

// ====== SETUP ======
function setupMainBtns(){
  document.getElementById('btnOk').onclick=function(){doMark(true);};
  document.getElementById('btnNo').onclick=function(){doMark(false);};
  document.getElementById('btnNext').onclick=function(){nextQ();};
  document.getElementById('btnRand').onclick=function(){randQ();};
}
function setupDrawer(){
  document.getElementById('drExam').onclick=function(){startExam();};
  document.getElementById('drReviewWrong').onclick=function(){startWrongMode();closeDrawer();};
  document.getElementById('drShuffle').onclick=function(){mode='all';aType='all';aCh='all';buildQs();for(var i=qs.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=qs[i];qs[i]=qs[j];qs[j]=t;}ci=0;hist={};streak=0;sh();rc();renderAll();closeDrawer();};
  document.getElementById('drPageTable').onclick=function(){showPageTable();};
  document.getElementById('drKeys').onclick=function(){showKeys();};
  document.getElementById('drReset').onclick=function(){if(confirm('确定重置所有学习进度？')){hist={};streak=0;mode='all';aType='all';aCh='all';buildQs();ci=0;sh();rc();renderAll();ud();closeDrawer();}};
  document.getElementById('drawer').addEventListener('click',function(e){
    var b=e.target.closest('button[data-qi]');if(b){jumpTo(parseInt(b.dataset.qi));closeDrawer();}
  });
}

// ====== INIT ======
function setupKB(){
  document.addEventListener('keydown',function(e){
    if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA')return;
    switch(e.code){
      case 'Space':e.preventDefault();if(!judging&&!timer)doFlip();break;
      case 'ArrowRight':e.preventDefault();nextQ();break;
      case 'ArrowLeft':e.preventDefault();prevQ();break;
      case 'Digit1':case 'KeyA':if(flipped&&!judging){e.preventDefault();doMark(true);}break;
      case 'Digit2':case 'KeyD':if(flipped&&!judging){e.preventDefault();doMark(false);}break;
      case 'KeyR':if(!e.ctrlKey){e.preventDefault();randQ();}break;
    }
  });
}
function setupSwipe(){
  var sx=0,sy=0;
  document.getElementById('cardArea').addEventListener('touchstart',function(e){sx=e.touches[0].clientX;sy=e.touches[0].clientY;},{passive:true});
  document.getElementById('cardArea').addEventListener('touchend',function(e){
    if(judging||timer)return;var dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
    if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)){if(dx<0)nextQ();else prevQ();}
  });
}

function init(){
  lh();mode='all';aType='all';aCh='all';buildQs();setupMainBtns();setupDrawer();renderAll();ud();setupKB();setupSwipe();
}
init();
</script>
</body>
</html>'''

# Write
for p in [os.path.join(base, "www", "index.html"),
          os.path.join(base, "index.html")]:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{os.path.getsize(p):>8,} bytes  {p}")

print("构建完成！浏览器打开 index.html 即可使用。")
