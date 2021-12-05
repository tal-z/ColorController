import matplotlib.pyplot as plt
from ColorController.conversions import invert_rgb, rgb_to_hex


def place_title_linebreak(title):
    title = title.split(" ")
    new_title = ""
    line = ""
    for word in title:
        if len(line) + len(word) < 12:
            line += word + " "
            new_title += word + " "
        else:
            new_title += "\n " + word + " "
            line = ""
    return new_title


def set_title_fontsize(title):
    fontsize = 40
    title_len = len(title)
    if title_len > 15:
        fontsize = 50 - title_len
    return fontsize


def show_named_color(color_object, rotatelabels=False, labelfontsize=12, *args, **kwargs):
    if color_object.name.lower() == 'grey':
        rotatelabels = True
        labelfontsize = 4
    data = [1 for code in color_object.hex_code]
    explode = [.05 for d in data]
    plt.pie(data,
            explode=explode,
            labels=color_object.hex_code,
            rotatelabels=rotatelabels,
            textprops={'fontsize': labelfontsize},
            colors=color_object.hex_code,
            )
    plt.title(place_title_linebreak(color_object.name.upper()), fontsize=set_title_fontsize(color_object.name))
    plt.tight_layout()
    plt.show()


def show_coded_color(color_object, *args, **kwargs):
    fig, ax = plt.subplots()
    data = [1 for name in color_object.name] * 2
    list_spacer = [" " for name in color_object.name]
    hex_str = "#" + color_object.hex_code.lstrip('#')
    ax.pie(data,
           colors=[hex_str for name in color_object.name],
           wedgeprops={'linewidth': 3, 'ec': 'black'}
           )
    ax.pie(data,
           labels=[place_title_linebreak(n.replace("_", " ")).upper() for n in color_object.name] + list_spacer,
           textprops={'fontsize': 15},
           rotatelabels=False,
           startangle=90,
           colors=[hex_str for name in color_object.name + list_spacer],
           wedgeprops={'linewidth': 1, 'ec': hex_str}
           )
    plt.title(color_object.hex_code.upper(), fontsize=40)
    r, g, b = color_object.rgb
    text_r, text_g, text_b = invert_rgb(r, g, b)
    if all(abs(ch1-ch2) < 75 for (ch1, ch2) in zip((text_r, text_g, text_b), (r, g, b))):
        text_color = '#000000'
    else:
        text_color = rgb_to_hex(text_r, text_g, text_b)
    ax.text(x=-.65, y=-.15, s=f'Hex Code: {color_object.hex_code}\n'
                              f'RGB: {color_object.rgb}\n'
                              f'HSV: {color_object.hsv}', color=text_color)
    plt.tight_layout()
    plt.show()
