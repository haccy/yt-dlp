
import io
from typing import Union
from xml.etree import ElementTree
from .danmaku2ass import Danmaku2ASS


def convert_niconico_to_ass(packets: list[dict[str, dict[str, Union[int, str]]]],
                            width: int,
                            height: int) -> str:

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
    print(f"{packets_xml=}")

    with io.StringIO(initial_value=packets_xml) as instr, io.StringIO() as outstr:
        Danmaku2ASS(input_files=(instr,),
                    input_format='Niconico',
                    output_file=outstr,
                    stage_width=width,
                    stage_height=height)
        return outstr.getvalue()


if __name__ == '__main__':
    ret = convert_niconico_to_ass([{
        "chat": {
            "thread": "1419089061",
            "no": 13546,
            "vpos": 196891,
            "date": 1692448657,
            "date_usec": 817157,
            "anonymity": 1,
            "score": -120,
            "user_id": "nvc:_oQHxX-bhSKVliBz6TL7q2FbP-I",
            "mail": "184",
            "content": "\u307e\u3058\u304b\u3088\u30de\u30f3\u30a8\u30f3\u6700\u4f4e\u3060\u306a\uff01"
        }
    }], 640, 360)
    print(f"{ret=!s}")
