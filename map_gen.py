import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import statistics


def setup_map_raws(height=35, width=71):
    noise = PerlinNoise(octaves=7)
    xpix, ypix = height, width
    pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
    maps = []
    for x in range(width):
        maps.append([])
        for y in range(height):
            maps[x].append(".")
    return pic, maps


def print_map(ma):
    for x in range(len(ma)):
        for y in range(len(ma[x])):
            print(ma[x][y], end="")
        print()


def find_spawn(ma):
    for x in range(1, len(ma)):
        for y in range(1, len(ma[x])):
            bad = True
            if ma[x][y] == "." and \
                    ma[x - 1][y] == "." and \
                    ma[x + 1][y] == "." and \
                    ma[x][y - 1] == "." and \
                    ma[x][y + 1] == ".":
                bad = False
            if not bad:
                return x, y


def add_perlin(maps, pic, height=35, width=71):
    for x in range(len(pic)):
        for y in range(len(pic[x])):
            val = pic[x][y]
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                maps[x][y] = "W"
            elif val < -.3:
                maps[x][y] = "L"
            elif val > .2:
                maps[x][y] = "W"
            elif -.005 < val < .005:
                maps[x][y] = "B"
    px, py = find_spawn(maps)
    maps[px][py] = "P"
    return maps

def add_static_portion(ma,ma_height,ma_width):
    middle = """.........................
    .........................
    ..WWWWW..W.W.W.W..WWWWW..
    ..W.......LLLLL.......W..
    ..........LLLLL..........
    ..........LLGLL..........
    ..........LLLLL..........
    ..W.......LLLLL.......W..
    ..WWWWW..W.W.W.W..WWWWW..
    .........................
    ........................."""
    data = middle.split("\n")
    data = [e.strip() for e in data]
    y_start = int(ma_width/2)-int(len(data)/2)
    y_end = int(ma_width/2)+int(len(data)/2)

    x_start = int(ma_height / 2) - int(len(data[0]) / 2)
    x_end = int(ma_height / 2) + int(len(data[0]) / 2)
    maps = []
    for y in range(len(ma)):
        maps.append([])
        for x in range(0,len(ma[0])):
            if x_start <= x <= x_end and y_start <= y <= y_end:
                newx = x - x_start

                newy = y - y_start
                try:
                    maps[y].append(data[newy][newx])
                except:
                    print(newy, newx)

            else:
                maps[y].append(ma[y][x])
    # print_map(maps)
    return maps


def export_to_text(ma, save_file="dynamic.txt"):
    fout = open(save_file, "w")
    for x in range(len(ma)):
        for y in range(len(ma[x])):
            fout.write(ma[x][y].strip())
        fout.write("\n")
    fout.close()

def generate_map_from_text(filename="dynamic.txt"):
    fin = open(filename,"r")
    data = []
    while True:
        line = fin.readline()
        if line != "":
            data.append(line.strip())
        else:
            break
    return data

def generate_and_save_dynamic_map(height=35, width=71, file_name="dynamic.txt"):
    pic, maps = setup_map_raws(height, width)
    map = add_perlin(maps, pic, height, width)
    map = add_static_portion(map,height,width)
    export_to_text(map, file_name)


if __name__ == "__main__":
    # pic, maps = setup_map_raws()
    # map = add_perlin(maps, pic)
    # print_map(map)
    map = generate_map_from_text()

    add_static_portion(map,ma_height=35,ma_width=71)

