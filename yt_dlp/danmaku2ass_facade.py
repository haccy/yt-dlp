from __future__ import annotations
import io
from xml.etree import ElementTree

from .danmaku2ass import Danmaku2ASS
from .YoutubeDL import YoutubeDL


def convert_niconico_to_ass(packet: list[dict[str, dict[str, str | int]]],
                            width: int,
                            height: int,
                            downloader: YoutubeDL) -> str:

    packet_ele = ElementTree.Element('packet')

    for packet_content in packet:
        chat_obj_strvalue = {
            k: str(v) for (k, v) in packet_content.items() if k not in ('body', 'commands')
        }
        chat_obj_strvalue['mail'] = ' '.join(packet_content.get('commands', {}))
        chat_obj_strvalue['vpos'] = str(int(int(chat_obj_strvalue.get('vposMs')) / 10))
        chat_obj_strvalue['date'] = '-99'

        chat_ele = ElementTree.SubElement(packet_ele, 'chat', attrib=chat_obj_strvalue)
        chat_ele.text = packet_content.get('body')

    packet_xml = ElementTree.tostring(packet_ele, encoding='unicode')
    downloader.write_debug(f'{packet_xml=}')

    with io.StringIO(initial_value=packet_xml) as instr, io.StringIO() as outstr:
        Danmaku2ASS(input_files=(instr,),
                    input_format='Niconico',
                    output_file=outstr,
                    stage_width=width,
                    stage_height=height)
        return outstr.getvalue()


if __name__ == '__main__':
    pass
