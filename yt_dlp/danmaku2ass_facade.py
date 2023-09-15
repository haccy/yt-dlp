
import io
from xml.etree import ElementTree
from .danmaku2ass import Danmaku2ASS
from collections.abc import Callable


def convert_niconico_to_ass(packets: list[dict[str, dict[str, str | int]]],
                            width: int,
                            height: int,
                            write_debug: Callable[[str], None]) -> str:

    packets_ele = ElementTree.Element("packets")

    for aPacket in packets:
        chat_obj = aPacket.get("chat")
        if not chat_obj:
            continue
        chat_obj_strvalue = {k: str(v)
                             for (k, v) in chat_obj.items()
                             if k != "content"}
        chat_ele = ElementTree.SubElement(packets_ele,
                                          "chat",
                                          attrib=chat_obj_strvalue)
        chat_ele.text = chat_obj.get("content")

    packets_xml = ElementTree.tostring(packets_ele, encoding="unicode")
    write_debug(f"{packets_xml=}")

    with io.StringIO(initial_value=packets_xml) as instr, io.StringIO() as outstr:
        Danmaku2ASS(input_files=(instr,),
                    input_format='Niconico',
                    output_file=outstr,
                    stage_width=width,
                    stage_height=height)
        return outstr.getvalue()


if __name__ == '__main__':
    pass
