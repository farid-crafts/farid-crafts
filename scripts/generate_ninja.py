from PIL import Image, ImageDraw, ImageFont
import math, os, random

W, H, FRAMES, DURATION, S = 720, 180, 28, 65, 4
C = {
    "bg0": (4, 8, 19), "bg2": (13, 30, 58), "sil": (11, 24, 45),
    "sil2": (21, 39, 68), "line": (34, 74, 120), "cyan": (53, 169, 255),
    "ice": (210, 236, 255), "white": (240, 249, 255), "hair": (15, 23, 42),
    "hair2": (27, 43, 69), "silver": (174, 199, 230), "skin": (218, 169, 151),
    "skin2": (240, 198, 174), "eye": (25, 158, 255), "eye2": (110, 215, 255),
    "cloth": (9, 14, 26), "cloth2": (20, 31, 50), "cloth3": (36, 52, 76),
    "steel": (87, 127, 170), "ground": (5, 11, 23), "glow": (23, 119, 210)
}

def get_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except OSError:
        return ImageFont.load_default()
SMALL, TINY = get_font(8), get_font(7)

def background():
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        base = tuple(int(C["bg0"][i] * (1-t) + C["bg2"][i] * t) for i in range(3))
        for x in range(W):
            moon_glow = max(0, 1-math.sqrt(((x-590)/310)**2 + ((y-60)/150)**2))*17
            horizon = max(0, 1-abs(y-126)/70)*max(0, 1-abs(x-385)/560)*7
            px[x,y] = tuple(min(255,int(v+moon_glow+horizon)) for v in base)
    d = ImageDraw.Draw(im)
    # Stepped pixel moon and layered night clouds
    for box,col in [
        ((586,27,626,65),(131,181,238)), ((594,21,622,69),(179,216,251)),
        ((601,25,632,61),(221,240,255)), ((613,31,632,54),(240,249,255)),
        ((586,34,594,45),(221,240,255)), ((601,21,613,26),(221,240,255)),
        ((614,62,626,68),(155,198,243))
    ]: d.rectangle(box, fill=col)
    for x,y,w,h,col in [
        (500,25,42,7,C["sil2"]),(523,18,40,7,C["sil2"]),(545,29,47,6,C["sil2"]),
        (535,41,36,5,C["line"]),(640,33,48,6,C["sil2"]),(650,24,35,5,C["sil2"]),
        (454,52,40,5,C["sil"]),(480,45,36,5,C["sil"]),
        (30,50,42,6,C["sil2"]),(55,42,37,6,C["sil2"]),(80,55,48,6,C["sil2"]),(115,48,42,5,C["sil"])
    ]: d.rectangle((x,y,x+w,y+h), fill=col)
    # Temple and torii silhouettes
    d.polygon([(22,88),(50,72),(77,88),(69,92),(30,92)], fill=(11,24,45))
    d.rectangle((30,89,69,93), fill=(11,24,45))
    d.rectangle((37,91,41,140), fill=(6,13,28)); d.rectangle((90,95,95,140), fill=(7,15,31))
    d.polygon([(601,104),(639,82),(676,104),(669,109),(608,109)], fill=(8,19,38))
    d.rectangle((611,105,666,111), fill=(8,19,38))
    d.rectangle((619,109,626,146), fill=(7,15,31)); d.rectangle((652,109,659,146), fill=(7,15,31))
    d.rectangle((626,123,652,127), fill=(9,23,43)); d.rectangle((629,136,648,140), fill=(9,23,43))
    for x,y in [(632,117),(644,117),(632,130),(644,130),(51,103),(58,103),(51,115),(58,115)]:
        d.rectangle((x,y,x+2,y+4), fill=(38,96,152))
    for box in [(0,126,38,150),(42,132,70,150),(84,123,114,151),(630,126,664,150),(672,120,708,150),(685,132,719,151)]:
        d.rectangle(box, fill=(7,15,30))
    d.rectangle((0,148,W,151), fill=(25,101,170)); d.rectangle((0,151,W,153), fill=(71,185,255))
    d.rectangle((0,154,W,H), fill=C["ground"]); d.line((0,155,W,155), fill=(12,34,62), width=2)
    rng = random.Random(19)
    for _ in range(44):
        x,y = rng.randint(0,W-1),rng.randint(9,105)
        if 570<x<640 and 15<y<70: continue
        d.rectangle((x,y,x+rng.choice([1,2]),y+1), fill=rng.choice([C["line"],C["sil2"],C["cyan"]]))
    d.text((14,10),"RIIDDEV  //  SHINOBI RUN",font=SMALL,fill=(132,183,235))
    d.text((706,10),"SPEED MODE / ONLINE",font=TINY,fill=(78,131,192),anchor="ra")
    return im

BG = background()
rng = random.Random(2026)
STREAKS = [(rng.randrange(-100,W+100),rng.randrange(48,148),rng.randrange(12,58),rng.choice([3,4,5,7,9]),rng.choice([C["line"],C["glow"],C["cyan"]]),rng.choice([1,1,2])) for _ in range(46)]
DUST = [(rng.randrange(W),rng.randrange(120,165),rng.choice([C["cyan"],C["ice"],C["steel"])) for _ in range(20)]

def runner(frame):
    # A hand-built pixel ninja with side-swept silver hair, blue eye, wind scarf and alternating sprint legs.
    layer = Image.new("RGBA",(112,144),(0,0,0,0)); d=ImageDraw.Draw(layer); s=S
    phase=frame%4
    def box(x0,y0,x1,y1,col):
        d.rectangle((x0*s,y0*s,(x1+0)*s-1,(y1+0)*s-1),fill=col)
    def poly(points,col): d.polygon([(x*s,y*s) for x,y in points],fill=col)
    def line(points,col,width=1): d.line([(x*s,y*s) for x,y in points],fill=col,width=width*s,joint="curve")
    # Scarf/cape whip backwards in the wind
    tail=[0,2,1,-1][phase]
    poly([(12,16),(8,17),(4,15),(0,17),(4,19),(8,20),(2,22),(7,23),(13,21),(15,18)],C["cloth"])
    poly([(11,17),(7,18),(3,17),(7,20),(3,21),(8,21),(14,19)],C["cloth3"])
    poly([(10,18+tail),(6,19+tail),(2,18+tail)],C["cyan"])
    # Two distinct stride poses; boots and knees are kept blocky and readable
    if phase in (0,1):
        poly([(11,26),(15,26),(15,29),(12,31),(8,32),(5,31),(8,28)],C["cloth2"])
        poly([(7,30),(10,31),(7,34),(2,34),(2,32),(5,32)],C["cloth"])
        box(2,33,8,35,C["cloth"]); box(2,33,6,34,C["cloth3"])
        poly([(15,26),(19,26),(20,29),(23,30),(24,32),(20,33),(17,31),(14,29)],C["cloth2"])
        poly([(20,31),(24,31),(26,33),(26,35),(20,35),(18,34)],C["cloth"])
        box(21,33,26,34,C["steel"])
    else:
        poly([(11,26),(15,26),(16,29),(19,31),(18,33),(14,32),(10,30),(8,28)],C["cloth2"])
        poly([(15,30),(19,31),(22,33),(22,35),(16,35),(13,33)],C["cloth"])
        box(17,33,22,34,C["steel"])
        poly([(10,26),(13,26),(12,29),(9,31),(7,33),(3,33),(3,31),(6,29)],C["cloth2"])
        poly([(4,31),(8,31),(7,33),(8,34),(3,35),(0,34),(1,32)],C["cloth"])
        box(1,33,7,34,C["steel"])
    # Leaning torso, cape facets, strap and small blue buckle
    poly([(10,17),(18,17),(22,21),(21,27),(18,29),(13,28),(8,27),(7,22)],C["cloth"])
    poly([(10,18),(18,18),(20,21),(18,25),(14,26),(10,24),(8,21)],C["cloth2"])
    poly([(9,19),(12,19),(11,24),(8,26),(6,24),(7,21)],C["cloth"])
    poly([(18,18),(22,19),(25,21),(24,24),(21,25),(19,22)],C["cloth2"])
    box(13,20,17,25,C["cloth"]); box(14,22,16,23,C["steel"]); box(14,22,15,23,C["cyan"])
    line([(8,19),(4,27)],C["steel"]); line([(7,19),(3,26)],C["ice"])
    # Sprinting arm pump alternates with the legs
    if phase in (0,1):
        poly([(18,19),(21,19),(24,21),(25,23),(23,25),(20,23),(18,22)],C["cloth2"])
        box(23,22,26,25,C["cloth"]); box(24,23,26,24,C["steel"])
        poly([(10,20),(8,20),(6,22),(5,24),(7,25),(10,23)],C["cloth2"]); box(4,23,7,26,C["cloth"])
    else:
        poly([(18,19),(21,19),(22,21),(20,23),(17,22)],C["cloth2"]); box(16,21,19,24,C["cloth"])
        poly([(10,20),(7,20),(5,21),(3,23),(5,25),(8,23),(11,22)],C["cloth2"])
        box(3,22,6,25,C["cloth"]); box(3,23,5,24,C["steel"])
    # Head turned toward the running direction
    poly([(7,5),(9,2),(14,1),(18,2),(21,5),(23,8),(22,12),(19,15),(15,17),(10,16),(7,13),(6,9)],C["hair"])
    box(9,7,21,15,C["skin"]); box(10,9,20,14,C["skin2"]); box(8,9,10,12,C["skin"])
    # Big windswept fringe and silver forelock
    poly([(5,8),(6,4),(10,1),(16,1),(20,3),(23,6),(23,9),(20,8),(18,10),(16,7),(13,10),(11,8),(9,12),(7,13)],C["hair"])
    poly([(16,2),(19,3),(22,6),(23,9),(21,8),(19,6),(17,7)],C["silver"])
    poly([(18,4),(20,5),(22,8),(21,11),(19,9)],C["white"])
    poly([(7,7),(10,4),(14,3),(13,6),(10,8),(9,11),(7,12)],C["hair2"])
    box(10,11,13,12,C["hair"])
    # One prominent electric-blue eye for a side-facing sprint
    box(16,11,19,12,C["hair"]); box(16,12,19,13,C["eye"]); box(17,12,18,13,C["eye2"])
    box(13,13,15,14,C["hair"])
    # Face mask / scarf, rim light and shoulder pixel
    poly([(8,13),(11,14),(18,14),(21,13),(20,16),(17,18),(11,17),(8,16)],C["cloth"])
    box(10,14,19,15,C["cloth2"]); box(11,15,17,16,C["cloth"]); box(9,16,18,17,C["cloth3"])
    box(8,17,12,18,C["cyan"]); box(12,17,16,18,C["cloth2"]); box(10,19,12,20,C["steel"])
    # Tiny sparks trailing behind, animated with the sprint cycle
    for dx,dy in [(-5,16),(-8,20),(-5,24),(-3,28)]:
        xx=(dx+(frame%3))*s; yy=dy*s
        d.rectangle((xx,yy,xx+5,yy+2),fill=C["cyan"] if frame%2 else C["steel"])
    return layer.rotate(7,resample=Image.Resampling.NEAREST,expand=False,center=(56,72))

def make_frame(frame):
    im=BG.copy(); d=ImageDraw.Draw(im)
    # Speed lines and pixel streaks race backward at multiple parallax speeds.
    for i,(x,y,length,speed,col,thick) in enumerate(STREAKS):
        xx=(x-frame*speed)%(W+length)-length; yy=y+((frame+i)%3-1)
        d.rectangle((xx,yy,xx+length,yy+thick-1),fill=col)
    for i in range(19):
        x=(i*47-frame*13)%(W+55)-24; y=158+(i%3)*5; ln=11+(i%4)*5
        d.rectangle((x,y,x+ln,y+1),fill=(19,54,88))
    for i,(x,y,col) in enumerate(DUST):
        xx=(x-frame*(2+i%4))%W; yy=y-(5 if (frame+i)%5==0 else 0)
        if frame%3: d.rectangle((xx,yy,xx+2,yy+2),fill=col)
    d.ellipse((270,145,432,159),fill=(7,35,65)); d.ellipse((294,148,411,156),fill=(15,67,111))
    # Blue afterimage trail gives the runner a sense of acceleration.
    for j,alpha_col in [(1,(16,47,83)),(2,(12,31,59))]:
        x0=294-j*15-(frame%3)*2
        d.polygon([(x0+44,69),(x0+72,73),(x0+59,78),(x0+29,77)],fill=alpha_col)
        d.rectangle((x0+8,100+j*4,x0+38,102+j*4),fill=alpha_col)
    im.paste(runner(frame),(294,8),runner(frame))
    d=ImageDraw.Draw(im)
    d.text((14,25),"RUN LOOP / ACTIVE",font=TINY,fill=(73,128,189))
    d.rectangle((W-58,23,W-14,26),fill=(16,35,60))
    d.rectangle((W-58,23,W-18+(frame%7)*3,26),fill=(58,168,255))
    return im

frames=[make_frame(i) for i in range(FRAMES)]
palette_source=Image.new("RGB",(W,H*FRAMES))
for i,frame in enumerate(frames): palette_source.paste(frame,(0,i*H))
palette=palette_source.quantize(colors=128,method=Image.Quantize.MEDIANCUT)
p_frames=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
os.makedirs("assets",exist_ok=True)
p_frames[0].save("assets/ninja-pixel-patrol.gif",save_all=True,append_images=p_frames[1:],duration=DURATION,loop=0,optimize=True,disposal=2)
print("Generated assets/ninja-pixel-patrol.gif:",os.path.getsize("assets/ninja-pixel-patrol.gif"),"bytes")
