import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["figure.max_open_warning"] = 0
import matplotlib.patches as mpatches
import numpy as np
import streamlit as st

st.set_page_config(page_title="응급상황 대응 매뉴얼", layout="wide")

# ============================================================================
# 4컷 픽토그램: 지브리풍(따뜻한 파스텔 배경 + 언덕/구름) 분위기로 표현
# ============================================================================

PANEL_COLORS = ["#c97b4a", "#5f8f7a", "#4f7fa3", "#b45a5a"]  # 지브리풍 톤다운 파스텔 팔레트
PANEL_BG = "#faf3e6"     # 따뜻한 종이 배경색
PANEL_HILL = "#cfe0c4"   # 부드러운 언덕색
PANEL_CLOUD = "#ffffff"  # 구름색


def draw_panel_background(ax):
    """지브리풍 분위기를 내기 위한 배경(따뜻한 배경 + 언덕 + 구름)"""
    ax.add_patch(mpatches.FancyBboxPatch((-2.3, -2.3), 4.6, 4.6, boxstyle="round,pad=0,rounding_size=0.6",
                                          linewidth=0, facecolor=PANEL_BG, zorder=0))
    ax.add_patch(plt.Circle((0, -2.7), 2.5, color=PANEL_HILL, alpha=0.7, zorder=1))
    for cx, cy, r in [(-1.5, 1.7, 0.5), (-1.05, 1.9, 0.4), (-1.85, 1.6, 0.32)]:
        ax.add_patch(plt.Circle((cx, cy), r, color=PANEL_CLOUD, alpha=0.75, zorder=1))


def glyph_call(ax, color):
    box = mpatches.FancyBboxPatch((-0.7, -1.4), 1.4, 2.8, boxstyle="round,pad=0.05,rounding_size=0.3",
                                   linewidth=0, facecolor=color)
    ax.add_patch(box)
    ax.add_patch(plt.Circle((0, -1.0), 0.15, color="white"))
    for r in (1.3, 1.9):
        ax.add_patch(mpatches.Arc((-0.7, 0), r * 2, r * 2, angle=0, theta1=300, theta2=60, color=color, lw=3))


def glyph_check(ax, color):
    ax.text(0, 0, "?", fontsize=60, ha="center", va="center", color=color, fontweight="bold")


def glyph_compress(ax, color):
    ax.add_patch(plt.Rectangle((-1, 0.3), 2, 0.6, color=color))
    ax.annotate("", xy=(0, -1.3), xytext=(0, 0.2), arrowprops=dict(arrowstyle="-|>", color=color, lw=4))
    ax.annotate("", xy=(-0.9, -1.1), xytext=(-0.9, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=3))
    ax.annotate("", xy=(0.9, -1.1), xytext=(0.9, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=3))


def glyph_aed(ax, color):
    t = np.linspace(0, 2 * np.pi, 100)
    x = 16 * np.sin(t) ** 3 / 16
    y = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) / 16
    ax.fill(x * 1.3, y * 1.3, color=color)


def glyph_heimlich(ax, color):
    ax.annotate("", xy=(0, 1.7), xytext=(0, -1.7), arrowprops=dict(arrowstyle="-|>", color=color, lw=6))
    ax.add_patch(plt.Circle((0, -1.7), 0.35, color=color))


def glyph_water(ax, color):
    x = np.linspace(-1.6, 1.6, 100)
    for i, dy in enumerate([0.7, 0, -0.7]):
        y = 0.3 * np.sin(3 * x + i) + dy
        ax.plot(x, y, color=color, lw=4)


def glyph_bandage(ax, color):
    ax.add_patch(plt.Rectangle((-1.2, -0.35), 2.4, 0.7, color=color))
    ax.add_patch(plt.Rectangle((-0.35, -1.2), 0.7, 2.4, color=color))


def glyph_elevate(ax, color):
    ax.annotate("", xy=(0, 1.7), xytext=(0, -1.7), arrowprops=dict(arrowstyle="-|>", color=color, lw=6))


def glyph_shade(ax, color):
    ax.add_patch(plt.Polygon([(-1.2, 0.6), (1.2, 0.6), (0, 1.9)], closed=True, color=color))
    ax.plot([0, 0], [0.6, -1.5], lw=6, color=color)


def glyph_cutpower(ax, color):
    ax.add_patch(plt.Rectangle((-1, -1.6), 2, 3.2, fill=False, lw=4, edgecolor=color))
    ax.plot([0, 0.7], [-0.3, 1.1], lw=5, color=color)
    ax.add_patch(plt.Circle((0, -0.3), 0.12, color=color))


def glyph_insulate(ax, color):
    ax.plot([-1.7, 1.7], [0.6, -0.6], lw=3, color=color)
    ax.plot([0, 1.3], [0, 1.5], lw=5, color=color)


def glyph_crouch(ax, color):
    ax.add_patch(plt.Circle((-0.8, 0.7), 0.4, fill=False, lw=4, edgecolor=color))
    ax.plot([-0.8, 0.8], [0.3, -0.3], lw=5, color=color)
    ax.plot([0.8, 1.5], [-0.3, -0.1], lw=5, color=color)
    for i in range(3):
        xs = np.linspace(-1.6, 1.6, 30)
        ys = 0.15 * np.sin(6 * xs + i) + 1.6 + i * 0.4
        ax.plot(xs, ys, color=color, lw=2, alpha=0.6)


def glyph_exitdoor(ax, color):
    ax.add_patch(plt.Rectangle((-1.3, -1.6), 1.6, 3.2, fill=False, lw=4, edgecolor=color))
    ax.annotate("", xy=(1.9, 0), xytext=(0.3, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=5))


def glyph_caution(ax, color):
    ax.add_patch(plt.Polygon([(-1.5, -1.2), (1.5, -1.2), (0, 1.6)], closed=True, fill=False, lw=5, edgecolor=color))
    ax.text(0, -0.3, "!", fontsize=40, ha="center", va="center", color=color, fontweight="bold")


def glyph_fire(ax, color):
    verts = [(-0.6, -1.5), (-0.9, 0.2), (-0.2, 0.4), (-0.4, 1.0), (0.3, 0.6), (0.2, 1.7), (0.9, 0.3), (0.5, -0.3), (0.7, -1.5)]
    ax.add_patch(plt.Polygon(verts, closed=True, color=color))


def glyph_shelter(ax, color):
    ax.add_patch(plt.Rectangle((-1.7, 0.4), 3.4, 0.5, color=color))
    ax.plot([-1.4, -1.4], [0.4, -1.6], lw=5, color=color)
    ax.plot([1.4, 1.4], [0.4, -1.6], lw=5, color=color)


def glyph_openspace(ax, color):
    ax.plot([-1.8, 1.8], [-1.2, -1.2], lw=4, color=color)
    ax.add_patch(plt.Circle((0, -0.3), 0.35, fill=False, lw=4, edgecolor=color))
    ax.plot([0, 0], [-0.65, -1.2], lw=4, color=color)
    ax.annotate("", xy=(1.6, -0.3), xytext=(0.5, -0.3), arrowprops=dict(arrowstyle="-|>", color=color, lw=3))


def glyph_throwring(ax, color):
    ax.add_patch(plt.Circle((0, 0), 1.4, fill=False, lw=6, edgecolor=color))
    ax.add_patch(plt.Circle((0, 0), 0.7, fill=False, lw=6, edgecolor=color))


def glyph_recovery(ax, color):
    ax.add_patch(plt.Circle((-1.2, -0.6), 0.5, fill=False, lw=4, edgecolor=color))
    ax.plot([-0.7, 1.3], [-0.6, -0.6], lw=5, color=color)
    ax.plot([1.3, 1.6], [-0.6, -0.05], lw=4, color=color)


def glyph_press(ax, color):
    ax.add_patch(plt.Rectangle((-1.1, -0.4), 2.2, 0.8, color=color))
    ax.annotate("", xy=(0, 0.2), xytext=(0, 1.4), arrowprops=dict(arrowstyle="-|>", color=color, lw=4))


def glyph_alert(ax, color):
    ax.add_patch(mpatches.FancyBboxPatch((-1.6, -0.2), 3.2, 1.6, boxstyle="round,pad=0.1",
                                          fill=False, lw=4, edgecolor=color))
    ax.plot([-0.4, -0.8], [-0.2, -1.3], lw=4, color=color)
    ax.text(0, 0.6, "!", fontsize=36, ha="center", va="center", color=color, fontweight="bold")


GLYPHS = {
    "call": glyph_call, "check": glyph_check, "compress": glyph_compress, "aed": glyph_aed,
    "heimlich": glyph_heimlich, "water": glyph_water, "bandage": glyph_bandage, "elevate": glyph_elevate,
    "shade": glyph_shade, "cutpower": glyph_cutpower, "insulate": glyph_insulate, "crouch": glyph_crouch,
    "exitdoor": glyph_exitdoor, "caution": glyph_caution, "fire": glyph_fire, "shelter": glyph_shelter,
    "openspace": glyph_openspace, "throwring": glyph_throwring, "recovery": glyph_recovery, "press": glyph_press,
    "alert": glyph_alert,
}

PICTO = {
    "심정지 (심폐소생술)": [("check", "반응·호흡 확인"), ("call", "119 신고"), ("compress", "가슴압박 30회"), ("aed", "AED 사용")],
    "기도 폐쇄 (하임리히법)": [("check", "기침 유도"), ("heimlich", "하임리히법 시행"), ("call", "119 신고"), ("compress", "의식소실 시 CPR")],
    "화상": [("water", "찬물로 냉각"), ("caution", "물집 유지"), ("bandage", "거즈로 덮기"), ("call", "심하면 119")],
    "출혈": [("press", "직접 압박"), ("elevate", "부위 높이기"), ("bandage", "붕대로 고정"), ("call", "지속되면 119")],
    "열사병 / 온열질환": [("shade", "그늘로 이동"), ("water", "체온 낮추기"), ("check", "의식 확인"), ("call", "119 신고")],
    "감전 사고": [("cutpower", "전원 차단"), ("insulate", "절연물로 분리"), ("check", "반응 확인"), ("compress", "필요시 CPR")],
    "화재": [("fire", "화재 알리기"), ("crouch", "낮은 자세로 이동"), ("exitdoor", "대피 · 재진입 금지"), ("call", "119 신고")],
    "지진": [("shelter", "탁자 아래 대피"), ("cutpower", "가스·전기 차단"), ("exitdoor", "출구 확보"), ("openspace", "넓은 공간 이동")],
    "물놀이 안전사고 (익수)": [("throwring", "구조장비로 구조"), ("check", "반응 확인"), ("compress", "필요시 CPR"), ("recovery", "회복자세 유지")],
}

ILLUSTRATION_DIR = "illustrations"  # 이 폴더에 icon_key.png(예: call.png)를 넣으면 그림 대신 사용됩니다


def get_custom_illustration_path(icon_key):
    path = os.path.join(ILLUSTRATION_DIR, f"{icon_key}.png")
    return path if os.path.exists(path) else None


@st.cache_data(show_spinner=False)
def build_icon_figure(icon_key, color):
    """지브리풍 배경(따뜻한 배경·언덕·구름) 위에 아이콘 도형을 그린 작은 figure를 반환합니다.
    (그림 안에 한글 텍스트를 넣지 않아, 폰트에 한글이 없는 환경에서도 깨지지 않습니다.)"""
    fig, ax = plt.subplots(figsize=(1.8, 1.8))
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    draw_panel_background(ax)
    GLYPHS[icon_key](ax, color)
    fig.patch.set_facecolor(PANEL_BG)
    fig.tight_layout(pad=0.3)
    return fig


def get_pictogram_items(situation_name):
    """(종류, 이미지경로 또는 figure, 캡션) 4개를 반환.
    illustrations/ 폴더에 지브리풍으로 직접 제작한 PNG가 있으면 그것을 우선 사용하고,
    없으면 코드로 그린 배경+아이콘 figure를 사용합니다."""
    items = []
    for idx, (icon_key, caption) in enumerate(PICTO[situation_name]):
        color = PANEL_COLORS[idx % len(PANEL_COLORS)]
        custom_path = get_custom_illustration_path(icon_key)
        if custom_path:
            items.append(("image", custom_path, caption))
        else:
            fig = build_icon_figure(icon_key, color)
            items.append(("figure", fig, caption))
    return items

SITUATIONS = {
    "심정지 (심폐소생술)": {
        "call_119": "즉시 119 신고, 주변에 자동심장충격기(AED)가 있는지 확인",
        "steps": [
            "환자의 어깨를 두드리며 반응이 있는지 확인합니다.",
            "반응이 없으면 즉시 119에 신고하고, 주변에 자동심장충격기(AED)를 요청합니다.",
            "환자를 단단하고 평평한 바닥에 눕히고, 가슴 중앙(양쪽 젖꼭지 사이)에 손바닥을 겹쳐 올립니다.",
            "팔을 곧게 편 상태로 분당 100~120회 속도, 5cm 깊이로 가슴을 압박합니다.",
            "가슴압박 30회 · 인공호흡 2회를 반복합니다. (인공호흡이 어려우면 가슴압박만 계속해도 됩니다)",
            "AED가 도착하면 전원을 켜고 음성 안내에 따라 패드를 부착합니다.",
            "119 구급대원이 도착할 때까지 멈추지 않고 반복합니다.",
        ],
        "cautions": [
            "가슴압박을 시작하기 전에 반드시 반응과 호흡을 확인합니다.",
            "압박 중간에 손이 가슴에서 떨어지지 않도록 합니다.",
        ],
    },
    "기도 폐쇄 (하임리히법)": {
        "call_119": "이물질이 계속 빠지지 않거나 의식을 잃으면 즉시 119 신고",
        "steps": [
            "환자가 기침을 할 수 있으면 스스로 기침해서 이물질을 뱉어내도록 격려합니다.",
            "숨을 쉬지 못하거나 기침을 못하면, 환자 뒤에서 두 발을 벌리고 섭니다.",
            "양손을 환자의 명치와 배꼽 사이 중앙에 놓고 주먹을 감싸 쥡니다.",
            "빠르게 위쪽으로 당기듯 밀어 올리기를 반복합니다.",
            "이물질이 나오거나 환자가 다시 말을 할 수 있을 때까지 반복합니다.",
            "환자가 의식을 잃으면 바닥에 눕히고 즉시 심폐소생술(가슴압박)을 시작합니다.",
        ],
        "cautions": [
            "주먹을 밀어 올릴 때 갈비뼈(가슴뼈)에 직접 닿지 않도록 주의합니다.",
            "영아의 경우 등을 두드리는 방법이 다르므로 성인과 같은 방법을 쓰지 않습니다.",
        ],
    },
    "화상": {
        "call_119": "화상 범위가 넓거나 얼굴·기도에 화상을 입었다면 즉시 119 신고",
        "steps": [
            "화상 부위를 흐르는 차가운 수돗물로 10~15분 정도 식혀줍니다.",
            "물집은 터뜨리지 않습니다.",
            "화상 부위에 옷 등이 달라붙어 있다면 억지로 떼어내지 않고 그대로 둡니다.",
            "깨끗한 거즈나 천으로 상처를 가볍게 덮어줍니다.",
            "통증이 심하거나 범위가 넓으면 병원으로 이송합니다.",
        ],
        "cautions": [
            "얼음을 직접 상처에 대지 않습니다.",
            "민간요법(된장, 소주 등)을 바르지 않습니다.",
        ],
    },
    "출혈": {
        "call_119": "출혈이 멎지 않거나 대량 출혈이면 즉시 119 신고",
        "steps": [
            "깨끗한 천이나 거즈로 상처 부위를 직접 누릅니다.",
            "가능하면 상처 부위를 심장보다 높게 올립니다.",
            "출혈이 계속되면 압박을 유지한 채 다른 천을 덧대어 계속 누릅니다.",
            "지혈이 되면 붕대로 압박 상태를 고정합니다.",
        ],
        "cautions": [
            "상처를 직접 들여다보려고 자주 떼어보지 않습니다.",
            "지혈대는 다른 방법으로 출혈이 멎지 않을 때 최후 수단으로만 사용합니다.",
        ],
    },
    "열사병 / 온열질환": {
        "call_119": "의식이 흐려지거나 체온이 매우 높으면 즉시 119 신고",
        "steps": [
            "환자를 즉시 그늘지고 시원한 곳으로 옮깁니다.",
            "옷을 느슨하게 풀어줍니다.",
            "찬물이나 물수건, 부채·선풍기 등을 이용해 체온을 빠르게 낮춥니다.",
            "의식이 있으면 시원한 물을 조금씩 마시게 합니다.",
            "신속히 병원으로 이송합니다.",
        ],
        "cautions": [
            "의식이 없는 환자에게 물이나 음식을 억지로 먹이지 않습니다.",
        ],
    },
    "감전 사고": {
        "call_119": "즉시 119 신고",
        "steps": [
            "전원을 차단할 수 있으면 먼저 전원(두꺼비집 등)을 차단합니다.",
            "전원 차단이 어렵다면 마른 나무막대 등 절연물로 환자를 전선에서 떼어냅니다.",
            "환자의 반응과 호흡을 확인합니다.",
            "호흡이 없으면 즉시 심폐소생술을 시작합니다.",
        ],
        "cautions": [
            "감전된 환자를 맨손으로 직접 만지지 않습니다.",
            "물기가 있는 곳에서는 절대 접근하지 않습니다.",
        ],
    },
    "화재": {
        "call_119": "즉시 119 신고 (대피가 최우선)",
        "steps": [
            "\"불이야\"라고 크게 외쳐 주변에 알립니다.",
            "젖은 수건 등으로 코와 입을 막고 낮은 자세로 이동합니다.",
            "연기가 많으면 배는 바닥에 대지 않고 팔과 무릎으로 기어서 이동합니다.",
            "문을 열기 전 문손잡이가 뜨거우면 다른 대피로를 찾습니다.",
            "밖으로 나온 뒤에는 다시 안으로 들어가지 않습니다.",
            "대피할 수 없다면 문틈을 젖은 천으로 막고 창가에서 구조를 기다립니다.",
        ],
        "cautions": [
            "엘리베이터는 절대 이용하지 않고 계단으로 대피합니다.",
        ],
    },
    "지진": {
        "call_119": "부상자가 있으면 즉시 119 신고",
        "steps": [
            "흔들리는 동안에는 튼튼한 탁자 아래로 들어가 몸을 보호하고 다리를 붙잡습니다.",
            "흔들림이 멈추면 가스와 전기를 차단합니다.",
            "출입문을 열어 출구를 확보합니다.",
            "밖으로 나갈 때는 계단을 이용하고, 떨어지는 물건에 유의하며 이동합니다.",
            "건물 밖에서는 담장, 간판 등에서 떨어진 넓은 공간으로 대피합니다.",
        ],
        "cautions": [
            "흔들리는 도중에는 무리하게 밖으로 뛰쳐나가지 않습니다.",
        ],
    },
    "물놀이 안전사고 (익수)": {
        "call_119": "즉시 119 신고",
        "steps": [
            "구조 장비(튜브, 줄 등)를 먼저 던져 구조하고, 직접 물에 들어가는 것은 최후의 수단으로만 합니다.",
            "환자를 물 밖으로 옮긴 뒤 반응과 호흡을 확인합니다.",
            "호흡이 없으면 즉시 심폐소생술을 시작합니다.",
            "숨을 쉬고 있으면 옆으로 눕혀 기도를 확보하고 체온 저하를 막기 위해 담요 등으로 덮어줍니다.",
        ],
        "cautions": [
            "구조자가 수영에 능숙하지 않다면 직접 뛰어들지 않습니다.",
        ],
    },
}

# ============================================================================
# 데이터: 장소별로 자주 발생하는 상황 + 장소별 추가 안전 수칙
# ============================================================================

LOCATIONS = {
    "가정": {
        "situations": ["화재", "심정지 (심폐소생술)", "화상", "감전 사고", "기도 폐쇄 (하임리히법)", "지진"],
        "tips": [
            "소화기와 화재경보기의 위치를 미리 파악해 둡니다.",
            "가스밸브와 전기차단기 위치를 가족 모두가 알아 둡니다.",
            "무거운 가구는 넘어지지 않도록 고정해 둡니다.",
        ],
    },
    "학교 / 사무실": {
        "situations": ["화재", "지진", "심정지 (심폐소생술)", "출혈"],
        "tips": [
            "비상구와 대피 경로를 미리 확인해 둡니다.",
            "건물 내 AED(자동심장충격기) 위치를 알아 둡니다.",
            "정기 대피 훈련에 적극적으로 참여합니다.",
        ],
    },
    "야외 / 등산": {
        "situations": ["열사병 / 온열질환", "출혈", "심정지 (심폐소생술)"],
        "tips": [
            "이동 경로와 하산 시간을 미리 가족·지인에게 알려 둡니다.",
            "충분한 물과 상비약을 챙깁니다.",
            "휴대전화 배터리를 충분히 충전해 둡니다.",
        ],
    },
    "차량 / 도로": {
        "situations": ["출혈", "심정지 (심폐소생술)", "화재"],
        "tips": [
            "사고 발생 시 비상등을 켜고 안전삼각대를 설치합니다.",
            "가능하면 차량을 갓길 등 안전한 곳으로 이동시킵니다.",
            "2차 사고 예방을 위해 도로 밖 안전한 곳으로 대피합니다.",
        ],
    },
    "해변 / 물놀이": {
        "situations": ["물놀이 안전사고 (익수)", "심정지 (심폐소생술)", "열사병 / 온열질환"],
        "tips": [
            "안전요원이 있는 구역에서만 물놀이를 합니다.",
            "튜브나 구명조끼 등 안전장비를 착용합니다.",
            "음주 후 물놀이는 하지 않습니다.",
        ],
    },
}


def render_situation(name):
    data = SITUATIONS[name]
    items = get_pictogram_items(name)

    col_pic, col_text = st.columns([1, 1.4])
    with col_pic:
        row1 = st.columns(2)
        row2 = st.columns(2)
        grid_cols = row1 + row2
        for i, item in enumerate(items):
            kind, payload, caption = item
            with grid_cols[i]:
                if kind == "image":
                    st.image(payload, use_container_width=True)
                else:
                    st.pyplot(payload, use_container_width=True)
                st.markdown(
                    f"<p style='text-align:center; font-weight:600; margin-top:-8px;'>{i + 1}. {caption}</p>",
                    unsafe_allow_html=True,
                )
    with col_text:
        st.error(f"119 신고: {data['call_119']}")
        st.markdown("**대응 순서**")
        for i, step in enumerate(data["steps"], start=1):
            st.write(f"{i}. {step}")
        if data["cautions"]:
            st.warning("주의사항\n\n" + "\n".join(f"- {c}" for c in data["cautions"]))


# ============================================================================
# 화면 구성
# ============================================================================

st.title("응급상황 대응 매뉴얼")
st.caption(
    "소방청·국민재난안전포털 자료를 바탕으로 정리한 일반인용 응급 대응 요령입니다. "
    "실제 응급 상황에서는 119의 안내를 최우선으로 따르세요."
)

tab_situation, tab_location = st.tabs(["상황별로 보기", "장소별로 보기"])

with tab_situation:
    situation = st.selectbox("상황을 선택하세요", list(SITUATIONS.keys()))
    render_situation(situation)

with tab_location:
    location = st.selectbox("장소를 선택하세요", list(LOCATIONS.keys()))
    loc_data = LOCATIONS[location]

    st.markdown("**이 장소에서 미리 알아두면 좋은 것**")
    for tip in loc_data["tips"]:
        st.write(f"- {tip}")

    st.markdown("---")
    st.markdown(f"**{location}에서 자주 발생하는 응급상황**")
    for situation_name in loc_data["situations"]:
        with st.expander(situation_name):
            render_situation(situation_name)
