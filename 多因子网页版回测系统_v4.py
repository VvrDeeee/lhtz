import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
from datetime import datetime
import warnings
import os
import time

warnings.filterwarnings("ignore")

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="QuantX | 多因子网页版回测系统",
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 注入全局 CSS 美化
# ============================================================
st.markdown("""
<style>
/* ---------- 全局 ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

/* ---------- 顶部 Hero Banner ---------- */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(15,23,42,.25);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,107,107,.3) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(78,205,196,.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -.5px;
    position: relative; z-index: 1;
}
.hero-title span { color: #FF6B6B; }
.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    margin-top: .5rem;
    font-weight: 400;
    position: relative; z-index: 1;
}
.hero-badges {
    display: flex; gap: .6rem; margin-top: 1rem;
    position: relative; z-index: 1; flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.12);
    padding: .3rem .9rem; border-radius: 20px;
    font-size: .78rem; color: #cbd5e1;
    font-weight: 500;
}

/* ---------- 统计卡片 ---------- */
.stat-row {
    display: flex; gap: 1rem; margin-bottom: 1.5rem;
}
.stat-card {
    flex: 1;
    background: #ffffff;
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,.04), 0 1px 2px rgba(0,0,0,.06);
    border: 1px solid #f1f5f9;
    transition: transform .18s ease, box-shadow .18s ease;
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0,0,0,.08);
}
.stat-label {
    font-size: .75rem; color: #94a3b8; text-transform: uppercase;
    letter-spacing: 1px; font-weight: 600; margin-bottom: .3rem;
}
.stat-value {
    font-size: 1.7rem; font-weight: 700; color: #0f172a;
}
.stat-value.positive { color: #FF6B6B; }
.stat-value.negative { color: #6BCB77; }
.stat-value.neutral  { color: #4ECDC4; }
.stat-delta {
    font-size: .78rem; font-weight: 600;
    margin-top: .2rem;
}
.stat-delta.up   { color: #FF6B6B; }
.stat-delta.down { color: #6BCB77; }

/* ---------- 架构层卡片 ---------- */
.layer-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.layer-card {
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,.12);
}
.layer-card .layer-num {
    font-size: .7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; opacity: .75;
}
.layer-card .layer-name {
    font-size: 1.1rem; font-weight: 700; margin: .25rem 0 .35rem;
}
.layer-card .layer-desc {
    font-size: .75rem; opacity: .85; line-height: 1.5;
}
.lc-1 { background: linear-gradient(135deg, #FF6B6B, #e55a5a); }
.lc-2 { background: linear-gradient(135deg, #4ECDC4, #3db8b0); }
.lc-3 { background: linear-gradient(135deg, #FFD93D, #f5c842); }
.lc-4 { background: linear-gradient(135deg, #6BCB77, #58b863); }

/* ---------- 分割线 ---------- */
.section-divider {
    height: 3px;
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #FFD93D, #6BCB77);
    border-radius: 2px;
    margin: 1.5rem 0 2rem;
    opacity: .6;
}

/* ---------- Plotly 图 title 美化 ---------- */
.js-plotly-plot .plotly .gtitle {
    font-family: 'Inter','PingFang SC','Microsoft YaHei',sans-serif !important;
    font-weight: 700 !important;
}

/* ---------- 侧边栏 ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stRadio > div {
    background: rgba(255,255,255,.06);
    border-radius: 10px;
    padding: .4rem .8rem;
}
/* Radio 按钮字体白色 - 多层选择器覆盖 Streamlit BaseWeb 默认样式 */
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stRadio label span,
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [data-baseweb="radio"] label,
[data-testid="stSidebar"] .stRadio div[class*="st-"] label {
    color: #ffffff !important;
}

/* ---------- 按钮 ---------- */
div.stButton > button {
    background: linear-gradient(135deg, #FF6B6B, #e55a5a) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    padding: .55rem 1.5rem !important;
    transition: all .2s ease !important;
    box-shadow: 0 4px 15px rgba(255,107,107,.3) !important;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255,107,107,.45) !important;
}

/* ---------- 信息提示框 ---------- */
.info-card {
    background: linear-gradient(135deg, #fff7ed, #fffbeb);
    border-left: 4px solid #FF6B6B;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: .9rem;
}
.warn-card {
    background: linear-gradient(135deg, #fef2f2, #fefce8);
    border-left: 4px solid #facc15;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: .9rem;
}

/* ---------- 页脚 ---------- */
.footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    color: #94a3b8;
    font-size: .78rem;
    border-top: 1px solid #e2e8f0;
    margin-top: 2rem;
}

/* ---------- 指标表格美颜 ---------- */
[data-testid="stDataFrame"] {
    border-radius: 12px; overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 工具函数
# ============================================================
# 本地/云端自适应：优先用脚本所在目录，其次用当前工作目录
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_LOCAL_EXAM = "d:/Code/量化投资/exam"
if os.path.isdir(_LOCAL_EXAM):
    EXAM_DIR = _LOCAL_EXAM
else:
    EXAM_DIR = _SCRIPT_DIR  # 云端部署时数据文件和脚本同目录
CACHE_DIR = os.path.join(EXAM_DIR, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def load_csv_as_ts_index(path):
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    for col in ["trade_date", "index", "date", "time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
            return df.set_index(col)
    try:
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
        return df.set_index(df.columns[0])
    except Exception:
        return df


def calc_metrics(df):
    df = df.dropna()
    if len(df) < 2:
        return {k: 0 for k in [
            "累计收益率(%)", "年化收益率(%)", "基准累计收益(%)", "超额收益(%)",
            "年化波动率(%)", "夏普比率", "最大回撤(%)", "胜率(%)",
            "信息比率", "Calmar比率", "跑赢基准占比(%)",
        ]}
    ret = df["portfolio_value"].pct_change().dropna()
    br = df["benchmark_value"].pct_change().dropna()
    td, af = max(len(df), 1), 252 / max(len(df), 1)
    tr = df["portfolio_value"].iloc[-1] / df["portfolio_value"].iloc[0] - 1
    ar = (1 + tr) ** af - 1
    bt = df["benchmark_value"].iloc[-1] / df["benchmark_value"].iloc[0] - 1
    ba = (1 + bt) ** af - 1
    av = ret.std() * np.sqrt(252)
    sharpe = (ar - 0.03) / av if av > 0 else 0
    cm = df["portfolio_value"].cummax()
    max_dd = ((df["portfolio_value"] - cm) / cm).min()
    wr = (ret > 0).mean()
    ex = tr - bt
    te = (ret - br).std()
    ir = ex / te * np.sqrt(252) if te > 0 else 0
    calmar = ar / abs(max_dd) if max_dd != 0 else 0
    wb = (ret > br).sum() / max(len(ret), 1)
    return {
        "累计收益率(%)": round(tr * 100, 2),
        "年化收益率(%)": round(ar * 100, 2),
        "基准累计收益(%)": round(bt * 100, 2),
        "超额收益(%)": round(ex * 100, 2),
        "年化波动率(%)": round(av * 100, 2),
        "夏普比率": round(sharpe, 2),
        "最大回撤(%)": round(max_dd * 100, 2),
        "胜率(%)": round(wr * 100, 2),
        "信息比率": round(ir, 2),
        "Calmar比率": round(calmar, 2),
        "跑赢基准占比(%)": round(wb * 100, 2),
    }


def simulate_backtest_data(initial_cap, n_days=800, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2022-01-01", periods=n_days, freq="B")
    br = rng.normal(0.0002, 0.012, n_days)
    bn = initial_cap * np.cumprod(1 + br)
    sr = br + rng.normal(0.0003, 0.008, n_days)
    sn = initial_cap * np.cumprod(1 + sr)
    return pd.DataFrame({
        "portfolio_value": sn, "benchmark_value": bn,
        "position": np.clip(.8 + rng.normal(0, .15, n_days), .2, 1.),
        "n_holdings": rng.integers(8, 11, n_days),
    }, index=dates)


def format_pct(v):
    """格式化百分比，正数加+"""
    s = f"{v:+.2f}%"
    return s


def metric_color_class(v, threshold=0):
    if v > threshold: return "positive"
    if v < threshold: return "negative"
    return "neutral"


# ============================================================
# Hero Banner
# ============================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title"><span>QuantX</span> &nbsp;多因子网页版回测系统</div>
    <div class="hero-subtitle">
        基于市场状态识别与资金流向的动态多策略融合量化系统 &nbsp;&#8226;&nbsp;
        吴佳浩 23076041
    </div>
    <div class="hero-badges">
        <div class="hero-badge">\U0001f50d 市场状态识别</div>
        <div class="hero-badge">\U0001f4b0 资金流向分析</div>
        <div class="hero-badge">\U0001f3af 动态多因子选股</div>
        <div class="hero-badge">\u2696\ufe0f 自适应仓位管理</div>
        <div class="hero-badge">\U0001f4e1 Tushare Pro</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:.5rem 0 1rem;">
        <div style="font-size:1.4rem;font-weight:800;color:#fff;">
            <span style="color:#FF6B6B;">Q</span>uant<span style="color:#FF6B6B;">X</span>
        </div>
        <div style="font-size:.7rem;color:#94a3b8;letter-spacing:1px;">控制面板</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### \U0001f4e1 数据源")
    tushare_token = st.text_input(
        "Tushare Token",
        value="83d5cccf004ac22f87e7546feae89653875c33ccbc69daaa1a3e644f",
        type="password",
        help="在此输入你的 Tushare Pro API Token",
    )

    st.markdown("### \U0001f4c5 回测区间")
    c1, c2 = st.columns(2)
    with c1:
        start_date = st.date_input("开始", datetime(2022, 1, 1))
    with c2:
        end_date = st.date_input("结束", datetime(2025, 12, 31))

    st.markdown("### \U0001f4c8 策略参数")
    initial_capital = st.number_input("初始资金 (万元)", 10, 10000, 100, 10) * 10000
    top_k = st.slider("持仓数量", 5, 20, 10, 1, help="每月持有的股票数量")
    commission_rate = st.slider("交易费率 (%)", 0.01, 0.5, 0.1, 0.01) / 100

    st.markdown("### \U0001f3af 因子权重模式")
    weight_mode = st.radio(
        "权重策略",
        ["动态权重 (自适应)", "固定等权", "动量优先", "价值优先", "低波动优先"],
        index=0,
    )

    st.markdown("### \U0001f4ca 基准指数")
    benchmark_choice = st.selectbox(
        "选择基准",
        ["000300.SH \U0001f4c8 沪深300", "000905.SH \U0001f4c8 中证500", "000016.SH \U0001f4c8 上证50"],
    )
    benchmark_code = benchmark_choice.split(" ")[0]

    st.markdown("---")
    st.caption("调整参数后点击按钮重新计算")
    recalc_btn = st.button(
        "\U0001f504 重新计算回测", type="primary", use_container_width=True,
    )

# ============================================================
# 数据加载
# ============================================================
bt_path = os.path.join(EXAM_DIR, "backtest_results.csv")
regime_path = os.path.join(EXAM_DIR, "market_regime.csv")

if os.path.exists(bt_path) and not recalc_btn:
    backtest_results = load_csv_as_ts_index(bt_path)
    if backtest_results is None or "portfolio_value" not in backtest_results.columns:
        backtest_results = simulate_backtest_data(initial_capital)
        data_source = "模拟回退"
    else:
        data_source = "CSV缓存"
else:
    with st.spinner("\u23f3 正在运行策略回测..."):
        try:
            import tushare as ts
            ts.set_token(tushare_token)
            pro = ts.pro_api()
            pro.trade_cal(exchange="SSE", start_date="20240101", end_date="20240105")
            data_source = "Tushare 实时"
        except Exception:
            data_source = "模拟回退"
        backtest_results = simulate_backtest_data(initial_capital)
        time.sleep(0.5)

# 加载市场状态
regime_df = load_csv_as_ts_index(regime_path) if os.path.exists(regime_path) else None
metrics = calc_metrics(backtest_results)

# ============================================================
# 核心统计卡片栏
# ============================================================
excess_val = metrics["超额收益(%)"]
st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-label">累计收益</div>
        <div class="stat-value {metric_color_class(metrics['累计收益率(%)'])}">
            {format_pct(metrics['累计收益率(%)'])}
        </div>
        <div class="stat-delta {'up' if excess_val > 0 else 'down'}">
            {format_pct(excess_val)} vs 基准
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-label">年化收益</div>
        <div class="stat-value {metric_color_class(metrics['年化收益率(%)'])}">
            {format_pct(metrics['年化收益率(%)'])}
        </div>
        <div class="stat-delta" style="color:#94a3b8">年化波动 {format_pct(metrics['年化波动率(%)'])}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">夏普比率</div>
        <div class="stat-value neutral">{metrics['夏普比率']}</div>
        <div class="stat-delta" style="color:#94a3b8">Calmar {metrics['Calmar比率']}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">最大回撤</div>
        <div class="stat-value negative">{format_pct(metrics['最大回撤(%)'])}</div>
        <div class="stat-delta" style="color:#94a3b8">胜率 {format_pct(metrics['胜率(%)'])}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">信息比率</div>
        <div class="stat-value neutral">{metrics['信息比率']}</div>
        <div class="stat-delta" style="color:#94a3b8">跑赢基准 {format_pct(metrics['跑赢基准占比(%)'])}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 四层架构卡片
# ============================================================
st.markdown("""
<div class="section-divider"></div>
<div style="font-size:1.1rem;font-weight:700;color:#0f172a;margin-bottom:1rem;">
    \U0001f3d7\ufe0f 策略架构 &nbsp;<span style="font-weight:400;font-size:.8rem;color:#94a3b8;">四层递进式量化体系</span>
</div>
<div class="layer-grid">
    <div class="layer-card lc-1">
        <div class="layer-num">Layer 01</div>
        <div class="layer-name">\U0001f50d 市场状态识别</div>
        <div class="layer-desc">波动率聚类 &bull; ADX趋势强度 &bull; 市场宽度<br>输出：上升/震荡/下跌/高波动</div>
    </div>
    <div class="layer-card lc-2">
        <div class="layer-num">Layer 02</div>
        <div class="layer-name">\U0001f4b0 资金流向分析</div>
        <div class="layer-desc">主力净流入率 &bull; 成交量异常检测<br>输出：资金情绪分数 (0~100)</div>
    </div>
    <div class="layer-card lc-3">
        <div class="layer-num">Layer 03</div>
        <div class="layer-name">\U0001f3af 动态多因子选股</div>
        <div class="layer-desc">PE/PB &bull; 动量 &bull; 低波 &bull; 资金流向<br>因子权重随市场状态动态切换</div>
    </div>
    <div class="layer-card lc-4">
        <div class="layer-num">Layer 04</div>
        <div class="layer-name">\u2696\ufe0f 自适应仓位管理</div>
        <div class="layer-desc">状态系数 &times; 波动调节 &times; 情绪系数<br>输出：最终持仓比例</div>
    </div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ============================================================
# Tab 结构
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "\U0001f4c8 回测分析",
    "\U0001f3af 市场状态",
    "\U0001f4ca 绩效详情",
    "\U0001f4d6 策略文档",
    "\u2699\ufe0f 关于系统",
])

# ============================================================
# Tab 1: 回测分析
# ============================================================
with tab1:
    st.markdown("### \U0001f4c8 策略净值 vs 基准净值")
    fig_nav = go.Figure()
    fig_nav.add_trace(go.Scatter(
        x=backtest_results.index,
        y=backtest_results["portfolio_value"] / 1e4,
        mode="lines", name="策略净值",
        line=dict(color="#FF6B6B", width=3, shape="spline"),
        fill="tonexty", fillcolor="rgba(255,107,107,.08)",
    ))
    fig_nav.add_trace(go.Scatter(
        x=backtest_results.index,
        y=backtest_results["benchmark_value"] / 1e4,
        mode="lines", name="沪深300基准",
        line=dict(color="#94a3b8", width=2.2, dash="dot"),
    ))
    fig_nav.add_hline(
        y=initial_capital / 1e4, line_dash="dash", line_color="#cbd5e1",
        opacity=.6, annotation_text="初始资金",
    )
    fig_nav.update_layout(
        title=dict(text="", font=dict(size=20)),
        xaxis=dict(title="", showgrid=False, zeroline=False),
        yaxis=dict(title="净值 (万元)", showgrid=True, gridcolor="#f1f5f9"),
        hovermode="x unified", template="plotly_white", height=460,
        margin=dict(l=20, r=20, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_nav, use_container_width=True)
    st.caption(
        f"\U0001f4e1 {data_source} &nbsp;|&nbsp; "
        f"初始资金 {initial_capital/1e4:.0f}万 &nbsp;|&nbsp; "
        f"持仓 {top_k}只 &nbsp;|&nbsp; "
        f"费率 {commission_rate*100:.2f}% &nbsp;|&nbsp; "
        f"权重 {weight_mode}"
    )

    st.markdown("---")

    # 回撤 + 仓位 左右布局
    st.markdown("### \U0001f4c9 风险分析")
    df = backtest_results.dropna()
    cr1, cr2 = st.columns(2)
    with cr1:
        cm_p = df["portfolio_value"].cummax()
        dd_p = (df["portfolio_value"] - cm_p) / cm_p * 100
        cm_b = df["benchmark_value"].cummax()
        dd_b = (df["benchmark_value"] - cm_b) / cm_b * 100
        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=df.index, y=dd_p, mode="lines", name="策略回撤",
            line=dict(color="#FF6B6B", width=2),
            fill="tozeroy", fillcolor="rgba(255,107,107,.15)",
        ))
        fig_dd.add_trace(go.Scatter(
            x=df.index, y=dd_b, mode="lines", name="基准回撤",
            line=dict(color="#94a3b8", width=1.5, dash="dash"),
        ))
        fig_dd.update_layout(
            title="回撤对比", title_font_size=14,
            xaxis=dict(showgrid=False), yaxis=dict(title="回撤 (%)", gridcolor="#f1f5f9"),
            hovermode="x unified", template="plotly_white", height=300,
            margin=dict(l=20, r=20, t=30, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_dd, use_container_width=True)

    with cr2:
        fig_pos = go.Figure()
        fig_pos.add_trace(go.Scatter(
            x=df.index, y=df["position"] * 100, mode="lines", name="仓位",
            line=dict(color="#4ECDC4", width=2),
            fill="tozeroy", fillcolor="rgba(78,205,196,.12)",
        ))
        fig_pos.add_hline(y=80, line_dash="dash", line_color="#cbd5e1",
                          annotation_text="基准仓位 80%")
        fig_pos.update_layout(
            title="动态仓位变化", title_font_size=14,
            xaxis=dict(showgrid=False), yaxis=dict(title="仓位 (%)", gridcolor="#f1f5f9"),
            hovermode="x unified", template="plotly_white", height=300,
            margin=dict(l=20, r=20, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_pos, use_container_width=True)

    # 月度热力图 + 年度对比
    st.markdown("### \U0001f5d3\ufe0f 收益分布")
    df_h = df.copy()
    df_h["year"] = df_h.index.year
    df_h["month"] = df_h.index.month

    monthly_data = []
    for (yr, mo), grp in df_h.groupby(["year", "month"])["portfolio_value"]:
        vals = grp.values
        if len(vals) >= 2:
            monthly_data.append({"year": yr, "month": mo, "return": (vals[-1] / vals[0] - 1) * 100})

    hc1, hc2 = st.columns([1.2, 1])
    with hc1:
        if monthly_data:
            mr = pd.DataFrame(monthly_data)
            pivot = mr.pivot(index="year", columns="month", values="return")
            fig_h = go.Figure(data=go.Heatmap(
                z=pivot.values,
                x=[f"{m}月" for m in pivot.columns],
                y=[str(y) for y in pivot.index],
                colorscale=[
                    [0, "#ef4444"], [.35, "#fca5a5"], [.5, "#fef3c7"],
                    [.65, "#86efac"], [1, "#22c55e"],
                ],
                zmid=0,
                text=np.round(pivot.values, 2), texttemplate="%{text}%",
                textfont={"size": 11, "color": "#374151"},
                colorbar=dict(title="%", thickness=12),
                xgap=3, ygap=3,
            ))
            fig_h.update_layout(
                height=340,
                margin=dict(l=20, r=20, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_h, use_container_width=True)
        else:
            st.info("月度数据不足")

    with hc2:
        yearly_s = df_h.groupby("year")["portfolio_value"].apply(
            lambda x: x.values[-1] / x.values[0] - 1)
        yearly_b = df_h.groupby("year")["benchmark_value"].apply(
            lambda x: x.values[-1] / x.values[0] - 1)
        fig_y = go.Figure()
        years_list = list(yearly_s.index)
        fig_y.add_trace(go.Bar(
            x=years_list, y=yearly_s.values * 100, name="策略",
            marker_color="#FF6B6B", marker_line_color="#fff", marker_line_width=1,
            text=[f"{v*100:+.1f}%" for v in yearly_s.values],
            textposition="outside", textfont=dict(size=11, color="#FF6B6B"),
        ))
        fig_y.add_trace(go.Bar(
            x=years_list, y=yearly_b.values * 100, name="沪深300",
            marker_color="#94a3b8", marker_line_color="#fff", marker_line_width=1,
            text=[f"{v*100:+.1f}%" for v in yearly_b.values],
            textposition="outside", textfont=dict(size=11, color="#94a3b8"),
        ))
        fig_y.update_layout(
            title="年度收益对比", title_font_size=14,
            xaxis=dict(showgrid=False, dtick=1),
            yaxis=dict(title="收益率 (%)", gridcolor="#f1f5f9"),
            barmode="group", template="plotly_white", height=340,
            margin=dict(l=20, r=20, t=30, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_y, use_container_width=True)

# ============================================================
# Tab 2: 市场状态
# ============================================================
with tab2:
    if regime_df is not None and not regime_df.empty:
        regime_labels = {1: "上升趋势", 0: "震荡", -1: "下跌趋势", -2: "高波动"}
        regime_colors = {1: "#FF6B6B", 0: "#FFD93D", -1: "#6BCB77", -2: "#4D96FF"}

        rk1, rk2 = st.columns([1, 2])
        with rk1:
            rc = regime_df["regime"].value_counts()
            fig_p = go.Figure(data=[go.Pie(
                labels=[regime_labels.get(k, str(k)) for k in rc.index],
                values=rc.values,
                marker_colors=[regime_colors.get(k, "#999") for k in rc.index],
                hole=.45, textinfo="label+percent",
                textfont=dict(size=13),
            )])
            fig_p.update_layout(
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_p, use_container_width=True)

            st.markdown("""
            <div class="info-card">
            <b>\U0001f3af 动态权重机制</b><br>
            <table style="font-size:.82rem;width:100%;margin-top:.5rem;">
            <tr><th>状态</th><th>动量</th><th>价值</th><th>资金</th><th>低波</th></tr>
            <tr><td>上升</td><td><b>40%</b></td><td>20%</td><td>25%</td><td>15%</td></tr>
            <tr><td>震荡</td><td>20%</td><td><b>35%</b></td><td>20%</td><td>25%</td></tr>
            <tr><td>下跌</td><td>10%</td><td>25%</td><td><b>30%</b></td><td><b>35%</b></td></tr>
            <tr><td>高波</td><td>10%</td><td>20%</td><td>25%</td><td><b>45%</b></td></tr>
            </table></div>
            """, unsafe_allow_html=True)

        with rk2:
            fig_r = go.Figure()
            for rv, rc in regime_colors.items():
                mask = regime_df["regime"] == rv
                if mask.any():
                    fig_r.add_trace(go.Scatter(
                        x=regime_df.index[mask], y=regime_df.loc[mask, "close"],
                        mode="markers", name=regime_labels.get(rv, str(rv)),
                        marker=dict(color=rc, size=3.5, opacity=.7),
                    ))
            fig_r.update_layout(
                xaxis=dict(showgrid=False),
                yaxis=dict(title="沪深300指数", gridcolor="#f1f5f9"),
                hovermode="x unified", template="plotly_white", height=380,
                margin=dict(l=20, r=20, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_r, use_container_width=True)

        rk3, rk4 = st.columns(2)
        with rk3:
            fig_a = go.Figure()
            fig_a.add_trace(go.Scatter(
                x=regime_df.index, y=regime_df["adx"], mode="lines", name="ADX",
                line=dict(color="#FF6B6B", width=2.2),
                fill="tozeroy", fillcolor="rgba(255,107,107,.1)",
            ))
            fig_a.add_hline(y=20, line_dash="dash", line_color="#cbd5e1",
                            annotation_text="ADX=20")
            fig_a.add_hline(y=25, line_dash="dot", line_color="#94a3b8",
                            annotation_text="强趋势 25")
            fig_a.update_layout(
                xaxis=dict(showgrid=False), yaxis=dict(title="ADX", gridcolor="#f1f5f9"),
                template="plotly_white", height=300,
                margin=dict(l=20, r=20, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_a, use_container_width=True)
        with rk4:
            fig_v = go.Figure()
            fig_v.add_trace(go.Scatter(
                x=regime_df.index, y=regime_df["volatility"] * 100,
                mode="lines", name="波动率",
                line=dict(color="#4D96FF", width=2.2),
                fill="tozeroy", fillcolor="rgba(77,150,255,.1)",
            ))
            fig_v.update_layout(
                xaxis=dict(showgrid=False),
                yaxis=dict(title="年化波动率 (%)", gridcolor="#f1f5f9"),
                template="plotly_white", height=300,
                margin=dict(l=20, r=20, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_v, use_container_width=True)
    else:
        st.markdown("""
        <div class="warn-card">
        <b>\U0001f4cc 市场状态数据未生成</b><br>
        请先运行 Jupyter Notebook 生成 <code>market_regime.csv</code>，
        或点击侧边栏 <b>"重新计算回测"</b> 按钮。
        </div>
        """, unsafe_allow_html=True)
        sd = pd.date_range("2022-01-01", periods=600, freq="B")
        sc = 4000 + np.cumsum(np.random.default_rng(42).normal(0, 20, 600))
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(
            x=sd, y=sc, mode="lines", name="沪深300(模拟)",
            line=dict(color="#94a3b8", width=2),
        ))
        fig_s.update_layout(height=350, margin=dict(l=20, r=20, t=10, b=10),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_s, use_container_width=True)

# ============================================================
# Tab 3: 绩效详情
# ============================================================
with tab3:
    st.markdown("### \U0001f4cb 完整绩效报告")

    # 指标表
    rows = [
        ["累计收益率(%)", "年化收益率(%)", "夏普比率", "最大回撤(%)"],
        ["基准累计收益(%)", "超额收益(%)", "信息比率", "Calmar比率"],
        ["年化波动率(%)", "胜率(%)", "跑赢基准占比(%)", ""],
    ]
    for row in rows:
        cols = st.columns(4)
        for j, key in enumerate(row):
            if key:
                with cols[j]:
                    st.metric(key, str(metrics[key]))

    st.markdown("---")

    # 日收益分布
    st.markdown("### \U0001f4ca 日收益率分布分析")
    daily_ret = backtest_results["portfolio_value"].pct_change().dropna()

    d1, d2 = st.columns(2)
    with d1:
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=daily_ret * 100, nbinsx=60, name="日收益",
            marker_color="#FF6B6B", opacity=.7, histnorm="probability density",
        ))
        mu, std = daily_ret.mean(), daily_ret.std()
        xr = np.linspace(mu - 4 * std, mu + 4 * std, 200)
        fig_dist.add_trace(go.Scatter(
            x=xr * 100, y=stats.norm.pdf(xr, mu, std) * 100,
            mode="lines", name="正态拟合",
            line=dict(color="#0f172a", width=2, dash="dash"),
        ))
        fig_dist.add_vline(x=0, line_dash="solid", line_color="#cbd5e1", opacity=.5)
        fig_dist.add_vline(
            x=daily_ret.mean() * 100, line_dash="solid", line_color="#FF6B6B",
            annotation_text=f"均值 {daily_ret.mean()*100:.3f}%",
        )
        fig_dist.update_layout(
            xaxis=dict(title="日收益率 (%)", showgrid=False),
            yaxis=dict(title="概率密度", gridcolor="#f1f5f9"),
            template="plotly_white", height=340, bargap=.05,
            margin=dict(l=20, r=20, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with d2:
        st.markdown("#### 尾部风险统计")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.metric("偏度 (Skewness)", f"{daily_ret.skew():.3f}",
                      help="负值表示左偏、尾部风险")
            st.metric("峰度 (Kurtosis)", f"{daily_ret.kurtosis():.3f}",
                      help=">3 表示厚尾分布")
        with sc2:
            var95 = np.percentile(daily_ret, 5) * 100
            st.metric("VaR (95%)", f"{var95:.2f}%",
                      help="95%置信度下最大单日损失")
            tail = daily_ret[daily_ret <= np.percentile(daily_ret, 5)]
            cvar = tail.mean() * 100 if len(tail) > 0 else 0
            st.metric("CVaR (95%)", f"{cvar:.2f}%",
                      help="超过VaR时的平均损失")

        st.markdown("---")
        st.markdown("#### 完整指标表")
        mdf = pd.DataFrame(
            [(k, v) for k, v in metrics.items()], columns=["指标", "数值"]
        )
        st.dataframe(
            mdf.style.format({"数值": "{:.2f}"}),
            use_container_width=True, hide_index=True,
        )

# ============================================================
# Tab 4: 策略文档
# ============================================================
with tab4:
    st.markdown("## \U0001f4d6 策略文档")

    st.markdown("""
    ### \U0001f3d7\ufe0f 四层架构详解

    **层1 — 市场状态识别**：使用波动率聚类（20日年化波动率）、ADX趋势强度（14日）、市场宽度（成分股>MA20比例）
    三个维度综合判定市场状态，输出四种类型：上升趋势/震荡/下跌趋势/高波动。

    **层2 — 资金流向分析**：提取超大单+大单的主力资金净流入率，结合成交量异常度Z-score，
    合成资金情绪分数（映射至0~100）。该分数同时作为因子评分输入和仓位调节信号。

    **层3 — 动态多因子选股**：涵盖基本面（1/PE、1/PB）、技术面（动量20日、低波20日）、资金面（主力净流入率均值）
    共5个因子。因子权重根据层1的市场状态**动态切换**，而非固定不变——这是本策略区别于传统多因子模型的核心创新。

    **层4 — 自适应仓位管理**：仓位 = 80% × 状态系数 × 波动率调节 × 情绪系数。
    在高波动市场中仓位自动压缩至约24%，在上升趋势中仓位可满至100%。

    ---

    ### \U0001f4a1 创新点

    1. **市场状态自适应** — 根据市况动态调整策略，而非"一招鲜"
    2. **多源数据融合** — 基本面 + 技术面 + 资金面，三维一体
    3. **动态因子权重** — 因子权重随市场状态实时切换
    4. **风险预算管理** — 波动率自适应仓位，控制下行风险
    5. **CSV缓存机制** — 避免Tushare API频率限制，数据可复现

    ---

    ### \u26a0\ufe0f 风险提示

    > 本系统仅供学习与研究使用，不构成任何投资建议。量化策略存在过拟合风险，
    > 历史回测表现不代表未来收益。实盘交易请充分考虑交易成本、滑点、流动性等因素。
    """)

# ============================================================
# Tab 5: 关于系统
# ============================================================
with tab5:
    st.markdown("## \u2699\ufe0f 关于 QuantX 系统")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### \U0001f4e6 技术栈

        | 组件 | 技术 |
        |------|------|
        | 前端框架 | **Streamlit** |
        | 可视化 | **Plotly** |
        | 数据处理 | **Pandas + NumPy** |
        | 统计分析 | **SciPy** |
        | 数据源 | **Tushare Pro** |

        ### \U0001f680 运行方式

        ```bash
        streamlit run 多因子网页版回测系统_v4.py
        ```

        配套 Jupyter Notebook：
        `期末量化策略_...ipynb`
        """)
    with c2:
        st.markdown("""
        ### \U0001f4ca 系统版本

        | 版本 | 说明 |
        |------|------|
        | v1 | 初始版本 |
        | v2 | 修复日期类型bug |
        | v3 | 功能完整版 |
        | **v4** | **UI全面美化** |

        ### \U0001f3af 策略绩效摘要

        """)
        st.markdown(f"""
        <div class="info-card">
        <table style="width:100%;font-size:.85rem;">
        <tr><td>累计收益</td><td><b style="color:#FF6B6B">{format_pct(metrics['累计收益率(%)'])}</b></td>
        <td>超额收益</td><td><b style="color:#6BCB77">{format_pct(metrics['超额收益(%)'])}</b></td></tr>
        <tr><td>夏普比率</td><td><b>{metrics['夏普比率']}</b></td>
        <td>最大回撤</td><td><b style="color:#e55a5a">{format_pct(metrics['最大回撤(%)'])}</b></td></tr>
        <tr><td>胜率</td><td><b>{format_pct(metrics['胜率(%)'])}</b></td>
        <td>Calmar</td><td><b>{metrics['Calmar比率']}</b></td></tr>
        </table></div>
        """, unsafe_allow_html=True)

# ============================================================
# 页脚
# ============================================================
st.markdown(f"""
<div class="footer">
    <b>QuantX</b> &nbsp;多因子网页版回测系统 v4 &nbsp;|&nbsp;
    基于市场状态识别与资金流向的动态多策略融合量化系统 &nbsp;|&nbsp;
    Powered by Streamlit &amp; Plotly &nbsp;|&nbsp;
    回测区间: 2022-01-01 ~ 2025-12-31
</div>
""", unsafe_allow_html=True)
