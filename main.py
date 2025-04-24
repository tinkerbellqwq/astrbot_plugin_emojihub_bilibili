from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from typing import Dict, List, Optional, Union

import base64
import random



class EmojiHubBili:
    def __init__(self, config: dict):
        self.config = config
        self.last_command_by_channel = {}
        self.groups = {}

    async def send_image(self, event: AstrMessageEvent, image_url: str):
        """发送图片"""
        yield event.image_result(image_url)

    async def determine_image_path(self, txt_path: str) -> dict:
        """从txt文件中随机获取图片URL"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"读取文件错误：{e}")
            return {'imageUrl': None}

        if not urls:
            logger.error(f"错误！无有效URL可用：{txt_path}")
            return {'imageUrl': None}

        # 随机选择一个URL
        image_url = random.choice(urls).strip()

        # 处理URL前缀
        if image_url.startswith('https:https://'):
            image_url = image_url.replace('https:', '')
        elif not image_url.startswith(('http://', 'https://')):
            image_url = f"https://i0.hdslb.com/bfs/{image_url}"

        logger.info(f"使用文件 {txt_path} 发送URL为 {image_url}")
        return {'imageUrl': image_url}

    def list_all_commands(self) -> str:
        """列出所有表情包命令"""
        commands = [emoji['command'] for emoji in self.config.get('MoreEmojiHubList', [])]
        return '\n'.join(commands)

    def get_random_emoji_command(self) -> Optional[str]:
        """获取随机表情包命令"""
        commands = [emoji['command'] for emoji in self.config.get('MoreEmojiHubList', [])]
        return random.choice(commands) if commands else None

    async def _get_image_as_base64(self, image_path: str) -> str:
        """将图片转换为base64"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f'Error converting image to base64: {e}')
            return None

@register("emojihub-bili", "YourName", "一个表情包插件", "1.0.0")
class EmojiHubBiliPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.emoji_hub = None

    async def initialize(self):
        """初始化插件"""
        try:
            config = {
                "repeatCommandDifferentiation": "userId",
                "MoreEmojiHubList": [
                    {"command": "0721", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/0721.txt"},
                    {"command": "2233", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/2233娘小剧场.txt"},
                    {"command": "acomu414", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/acomu414.txt"},
                    {"command": "ba", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/ba.txt"},
                    {"command": "capoo", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/capoo.txt"},
                    {"command": "chiikawa", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/chiikawa.txt"},
                    {"command": "doro", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/doro.txt"},
                    {"command": "downvote", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/Downvote.txt"},
                    {"command": "eveonecat", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/eveonecat.txt"},
                    {"command": "fufu", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/fufu.txt"},
                    {"command": "gbc", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/GirlsBandCry.txt"},
                    {"command": "kemomimi", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/kemomimi酱表情包.txt"},
                    {"command": "koimeme", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/koimeme.txt"},
                    {"command": "mygo", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/mygo.txt"},
                    {"command": "seseren", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/seseren.txt"},
                    {"command": "亚托莉", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/亚托莉表情包.txt"},
                    {"command": "初音未来", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/初音未来Q.txt"},
                    {"command": "卡拉彼丘", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/卡拉彼丘.txt"},
                    {"command": "孤独摇滚", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/孤独摇滚.txt"},
                    {"command": "宇佐紀", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/宇佐紀.txt"},
                    {"command": "小黑子", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/小黑子.txt"},
                    {"command": "心海", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/心海.txt"},
                    {"command": "柴郡", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/柴郡.txt"},
                    {"command": "永雏小菲", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/永雏小菲.txt"},
                    {"command": "流萤", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/流萤.txt"},
                    {"command": "滑稽", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/滑稽.txt"},
                    {"command": "狗妈", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/狗妈.txt"},
                    {"command": "玛丽猫", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/玛丽猫.txt"},
                    {"command": "瑟莉亚", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/瑟莉亚.txt"},
                    {"command": "甘城猫猫", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/甘城猫猫.txt"},
                    {"command": "男娘武器库", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/男娘武器库.txt"},
                    {"command": "疾旋鼬", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/疾旋鼬.txt"},
                    {"command": "白圣女", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/白圣女.txt"},
                    {"command": "白圣女黑白", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/白圣女黑白.txt"},
                    {"command": "绪山真寻", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/绪山真寻.txt"},
                    {"command": "藤田琴音", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/藤田琴音.txt"},
                    {"command": "蜜汁工坊", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/蜜汁工坊.txt"},
                    {"command": "败犬女主", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/败犬女主.txt"},
                    {"command": "赛马娘", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/赛马娘.txt"},
                    {"command": "阿夸", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/阿夸.txt"},
                    {"command": "阿尼亚", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/阿尼亚.txt"},
                    {"command": "鹿乃子", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/鹿乃子.txt"},
                    {"command": "龙图", "sourceUrl": "data/plugins/astrbot_plugin_emojihub_bilibili/txts/龙图.txt"}
                ]
            }
            self.emoji_hub = EmojiHubBili(config)
            logger.info("表情包插件初始化成功")
        except Exception as e:
            logger.error(f"表情包插件初始化失败: {e}")
            raise

    @filter.command("emojihub")
    async def emojihub(self, event: AstrMessageEvent):
        """显示所有可用的表情包命令"""
        try:
            commands = self.emoji_hub.list_all_commands()
            yield event.plain_result(f"可用的表情包指令：\n{commands}")
        except Exception as e:
            logger.error(f"显示表情包命令列表失败: {e}")
            yield event.plain_result("获取表情包命令列表失败，请稍后重试")

    @filter.command("onemore", alias={"再来一张", "再来一张表情包"})
    async def onemore(self, event: AstrMessageEvent):
        """发送上次使用的表情包"""
        try:
            last_command = self.emoji_hub.last_command_by_channel.get(event.get_session_id())
            if last_command:
                # 执行上次使用的命令
                for emoji in self.emoji_hub.config.get('MoreEmojiHubList', []):
                    if emoji['command'] == last_command:
                        image_result = await self.emoji_hub.determine_image_path(emoji['sourceUrl'])
                        if image_result['imageUrl']:
                            async for result in self.emoji_hub.send_image(event, image_result['imageUrl']):
                                yield result
                            return
                yield event.plain_result("找不到上次使用的表情包，请重新发送一个表情包")
            else:
                yield event.plain_result("没有找到上一个命令，请先执行一个命令！")
        except Exception as e:
            logger.error(f"发送上次表情包失败: {e}")
            yield event.plain_result("发送表情包失败，请稍后重试")

    @filter.command("random", alias={"随机表情包"})
    async def random(self, event: AstrMessageEvent):
        """随机发送一个表情包"""
        try:
            random_command = self.emoji_hub.get_random_emoji_command()
            if random_command:
                for emoji in self.emoji_hub.config.get('MoreEmojiHubList', []):
                    if emoji['command'] == random_command:
                        image_result = await self.emoji_hub.determine_image_path(emoji['sourceUrl'])
                        if image_result['imageUrl']:
                            async for result in self.emoji_hub.send_image(event, image_result['imageUrl']):
                                yield result
                            return
                yield event.plain_result("随机表情包获取失败，请稍后重试")
            else:
                yield event.plain_result("没有任何表情包配置，请检查插件配置项！")
        except Exception as e:
            logger.error(f"发送随机表情包失败: {e}")
            yield event.plain_result("发送表情包失败，请稍后重试")

    async def terminate(self):
        """插件销毁方法"""
        try:
            self.emoji_hub = None
            logger.info("表情包插件已销毁")
        except Exception as e:
            logger.error(f"表情包插件销毁失败: {e}")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):
        """处理所有消息"""
        try:
            message = event.get_message_str().strip()
            # 如果消息以/开头，去掉/后再处理
            if message.startswith('/'):
                command = message[1:]
            else:
                command = message
            
            # 检查是否是有效的命令
            for emoji in self.emoji_hub.config.get('MoreEmojiHubList', []):
                if emoji['command'] == command:
                    # 记录当前命令
                    self.emoji_hub.last_command_by_channel[event.get_session_id()] = command
                    
                    # 获取并发送图片
                    image_result = await self.emoji_hub.determine_image_path(emoji['sourceUrl'])
                    if image_result['imageUrl']:
                        async for result in self.emoji_hub.send_image(event, image_result['imageUrl']):
                            yield result
                        return
                    else:
                        yield event.plain_result("获取图片失败，请稍后重试")
                        return
        except Exception as e:
            logger.error(f"处理消息失败: {e}")
