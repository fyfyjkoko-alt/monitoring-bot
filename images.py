
# Made By @MR_ARMAN_08

#  Join - @TEAM_X_OG

# This Is Licenced Under MT

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO

def create_player_id_card(user, bot_username="Testmods10_Bot"):
    """
    Ultra Premium Gaming ID Card - Professional Edition
    """
    # ═══════════════════════
    # CONFIG
    # ═══════════════════════
    WIDTH, HEIGHT = 800, 1100
    
    BG_COLOR = (15, 15, 25)
    CARD_BG = (25, 25, 40)
    ACCENT_BLUE = (64, 224, 208)
    ACCENT_PURPLE = (138, 43, 226)
    ACCENT_PINK = (255, 105, 180)
    GOLD = (255, 215, 0)
    WHITE = (245, 245, 255)
    GRAY = (150, 150, 170)
    
    FONT_PATH = "fonts/Roboto-Bold.ttf"
    
    try:
        font_title = ImageFont.truetype(FONT_PATH, 48)
        font_name = ImageFont.truetype(FONT_PATH, 42)
        font_med = ImageFont.truetype(FONT_PATH, 28)
        font_small = ImageFont.truetype(FONT_PATH, 22)
        font_tiny = ImageFont.truetype(FONT_PATH, 18)
    except:
        font_title = font_name = font_med = font_small = font_tiny = ImageFont.load_default()

    # ════════════════════════
    # CREATE BASE
    # ════════════════════════
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    for y in range(HEIGHT):
        alpha = int(20 * (1 - y / HEIGHT))
        r = BG_COLOR[0] + alpha
        g = BG_COLOR[1] + alpha
        b = BG_COLOR[2] + int(alpha * 1.5)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # ════════════════════════
    # MAIN CARD CONTAINER
    # ════════════════════════
    margin = 40
    card_top = 30
    card_height = HEIGHT - 60
    
    shadow_offset = 8
    draw.rounded_rectangle(
        [(margin + shadow_offset, card_top + shadow_offset), 
         (WIDTH - margin + shadow_offset, card_top + card_height + shadow_offset)],
        radius=25, fill=(0, 0, 0, 100)
    )
    
    draw.rounded_rectangle(
        [(margin, card_top), (WIDTH - margin, card_top + card_height)],
        radius=25, fill=CARD_BG
    )
    
    draw.rounded_rectangle(
        [(margin, card_top), (WIDTH - margin, card_top + card_height)],
        radius=25, outline=ACCENT_BLUE, width=3
    )

    # ════════════════════════
    # TOP HEADER SECTION
    # ════════════════════════
    header_height = 140
    
    for i in range(header_height):
        ratio = i / header_height
        color_val = int(40 * (1 - ratio))
        draw.line([(margin, card_top + i), (WIDTH - margin, card_top + i)], 
                 fill=(color_val, color_val, color_val + 20))
    
    draw.text((WIDTH // 2, card_top + 50), "ELITE PLAYER", 
              font=font_title, anchor="mm", fill=ACCENT_BLUE)
    draw.text((WIDTH // 2, card_top + 100), "IDENTITY CARD", 
              font=font_med, anchor="mm", fill=GRAY)
    
    line_y = card_top + header_height - 20
    draw.line([(margin + 60, line_y), (WIDTH - margin - 60, line_y)], 
             fill=ACCENT_PURPLE, width=2)

    # ════════════════════════
    # AVATAR SECTION WITH PROPER FALLBACK
    # ════════════════════════
    avatar_size = 280
    avatar_y = card_top + header_height + 40
    
    avatar_loaded = False
    try:
        if hasattr(user, 'photo_url') and user.photo_url:
            response = requests.get(user.photo_url, timeout=5)
            if response.status_code == 200:
                avatar = Image.open(BytesIO(response.content)).convert("RGBA")
                avatar_loaded = True
    except:
        pass
    
    if not avatar_loaded:
        avatar = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
        draw_av = ImageDraw.Draw(avatar)
        
        for y in range(avatar_size):
            ratio = y / avatar_size
            r = int(ACCENT_PURPLE[0] * ratio + ACCENT_BLUE[0] * (1 - ratio))
            g = int(ACCENT_PURPLE[1] * ratio + ACCENT_BLUE[1] * (1 - ratio))
            b = int(ACCENT_PURPLE[2] * ratio + ACCENT_BLUE[2] * (1 - ratio))
            draw_av.line([(0, y), (avatar_size, y)], fill=(r, g, b))
        
        initial = user.first_name[0].upper() if user.first_name else "?"
        try:
            initial_font = ImageFont.truetype(FONT_PATH, 140)
        except:
            initial_font = font_title
        
        draw_av.text((avatar_size // 2, avatar_size // 2), initial, 
                    font=initial_font, anchor="mm", fill=WHITE)
    
    avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
    
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    
    output_avatar = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    output_avatar.paste(avatar, (0, 0))
    output_avatar.putalpha(mask)
    
    paste_x = (WIDTH - avatar_size) // 2
    
    ring_colors = [ACCENT_PINK, ACCENT_PURPLE, ACCENT_BLUE]
    for i, color in enumerate(ring_colors):
        offset = (i + 1) * 15
        ring_size = avatar_size + offset * 2
        ring_pos = (paste_x - offset, avatar_y - offset)
        draw.ellipse(
            [ring_pos[0], ring_pos[1], 
             ring_pos[0] + ring_size, ring_pos[1] + ring_size],
            outline=color, width=4
        )
    
    img.paste(output_avatar, (paste_x, avatar_y), output_avatar)

    # ════════════════════════
    # USER INFO SECTION
    # ════════════════════════
    info_y = avatar_y + avatar_size + 60
    
    display_name = user.username if user.username else user.first_name
    if user.username:
        display_name = f"@{display_name}"
    
    name_bbox = draw.textbbox((WIDTH // 2, info_y), display_name, 
                             font=font_name, anchor="mm")
    padding = 25
    draw.rounded_rectangle(
        [name_bbox[0] - padding, name_bbox[1] - padding,
         name_bbox[2] + padding, name_bbox[3] + padding],
        radius=15, fill=(45, 45, 70)
    )
    
    draw.text((WIDTH // 2, info_y), display_name, 
              font=font_name, anchor="mm", fill=GOLD)

    # ══════════════════
    # INFO BOX
    # ══════════════════
    box_y = info_y + 80
    box_height = 200
    
    draw.rounded_rectangle(
        [(margin + 80, box_y), (WIDTH - margin - 80, box_y + box_height)],
        radius=20, fill=(35, 35, 55), outline=ACCENT_BLUE, width=2
    )
    
    draw.text((WIDTH // 2, box_y + 40), "GAMING PLATFORM", 
              font=font_tiny, anchor="mm", fill=GRAY)
    draw.text((WIDTH // 2, box_y + 70), f"🎮 {bot_username}", 
              font=font_med, anchor="mm", fill=ACCENT_BLUE)
    
    draw.text((WIDTH // 2, box_y + 115), "PLAYER ID", 
              font=font_tiny, anchor="mm", fill=GRAY)
    draw.text((WIDTH // 2, box_y + 145), f"#{user.id}", 
              font=font_med, anchor="mm", fill=WHITE)

    # ════════
    # BADGES SECTION
    # ════════
    badge_y = box_y + box_height + 50
    badge_size = 100
    spacing = 180
    
    badges = [
        {"icon": "⚡", "label": "ACTIVE", "color": ACCENT_BLUE},
        {"icon": "👑", "label": "VIP", "color": GOLD},
        {"icon": "✓", "label": "VERIFIED", "color": (50, 205, 50)}
    ]
    
    start_x = WIDTH // 2 - (len(badges) - 1) * spacing // 2
    
    for i, badge in enumerate(badges):
        x = start_x + i * spacing
        
        draw.ellipse(
            [x - badge_size // 2, badge_y, 
             x + badge_size // 2, badge_y + badge_size],
            fill=(50, 50, 70), outline=badge["color"], width=4
        )
        
        draw.text((x, badge_y + badge_size // 2), badge["icon"], 
                 font=font_name, anchor="mm", fill=badge["color"])
        
        draw.text((x, badge_y + badge_size + 25), badge["label"], 
                 font=font_tiny, anchor="mm", fill=GRAY)

    # ══════ ════════════
    # FOOTER
    # ═══════════════════
    footer_y = HEIGHT - 70
    
    draw.line([(margin + 60, footer_y - 20), (WIDTH - margin - 60, footer_y - 20)], 
             fill=ACCENT_PURPLE, width=2)
    
    draw.text((WIDTH // 2, footer_y + 10), "━━━━ ⚡ POWERED BY AI ⚡ ━━━━", 
              font=font_small, anchor="mm", fill=GRAY)

    # ════════════════
    # SAVE
    # ════════════════
    bio = BytesIO()
    img.save(bio, format="PNG", quality=95)
    bio.name = "player_card.png"
    bio.seek(0)
    return bio
