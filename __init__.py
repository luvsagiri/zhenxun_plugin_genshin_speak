import requests
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.internal.params import ArgStr
from nonebot.params import RegexMatched, EventPlainText
from nonebot.typing import T_State

__zx_plugin_name__ = "原神说"
__plugin_usage__ = """
usage：
    使用https://www.bilibili.com/video/BV1rB4y157fd的api进行原神角色语音合成
    由于使用api,不保证此插件长期可用,也不知调用限制,有时还会服务器过载
    请勿用于商业用途
    [角色名]说[内容]
    [角色名]快速说[内容]
    [角色名]慢慢说[内容]
    角色列表:
    派蒙, 凯亚, 安柏, 丽莎, 琴,
    香菱, 枫原万叶, 迪卢克, 温迪, 可莉,
    早柚, 托马, 芭芭拉, 优菈, 云堇,
    钟离, 魈, 凝光, 雷电将军, 北斗,
    甘雨, 七七, 刻晴, 神里绫华, 戴因斯雷布,
    雷泽, 神里绫人, 罗莎莉亚, 阿贝多, 八重神子,
    宵宫, 荒泷一斗, 九条裟罗, 夜兰, 珊瑚宫心海,
    五郎, 散兵, 女士, 达达利亚, 莫娜,
    班尼特, 申鹤, 行秋, 烟绯, 久岐忍,
    辛焱, 砂糖, 胡桃, 重云, 菲谢尔
    诺艾尔, 迪奥娜, 鹿野院平藏]
    (xiao好像写不出来)
""".strip()
__plugin_des__ = "原神角色语音合成"
__plugin_cmd__ = ["原神说"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
    "cost_gold": 0,
}
__plugin_type__ = "来点语音吧~"
__plugin_version__ = 0.1
__plugin_author__ = "luvsagiri"
__plugin_cd_limit__ = {
    "cd": 10,
    "rst": "冷静点，别冲了！"
}
__plugin_block_limit__ = {
    "rst": "你正在冲！"
}

URL = "http://233366.proxy.nscc-gz.cn:8888/"
genshinspeak = on_regex(
    "(派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|戴因斯雷布|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|散兵|女士|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏)(快速|慢慢|慢速)?说",
    priority=5, block=True)


@genshinspeak.handle()
async def _(state: T_State, cmd: str = RegexMatched(), arg: str = EventPlainText()):
    if arg.strip().strip(cmd):
        state["arg"] = arg.strip().strip(cmd)


@genshinspeak.got("arg", prompt="要说点什么？")
async def _(cmd: str = RegexMatched(), arg: str = ArgStr("arg")):
    text = arg.strip(cmd)
    if len(text) == 0:
        await genshinspeak.finish("请携带要说的内容")
    length = '1.2'
    if cmd[-3:-1] == "快速":
        length = '0.6'
        speaker = cmd[:-3]
    elif cmd[-2:] in ["慢速", "慢慢"]:
        length = '2'
        speaker = cmd[:-3]
    else:
        speaker = cmd[:-1]
    url = URL + "?speaker=" + speaker + "&text=" + text + "&length=" + length
    record_resp = requests.get(url=url)
    if record_resp.status_code != 200:
        await genshinspeak.finish(f"api访问出错啦,错误码{record_resp.status_code}\n详细信息:\n{record_resp.text}")
    record_byte = record_resp.content
    await genshinspeak.finish(MessageSegment.record(record_byte))
