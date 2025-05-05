import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

# Translation dictionaries - COMPLETE VERSION
translations = {
    "en": {
        "title": "💹 EUR/PLN Monitor Pro",
        "navigation": "Navigation",
        "nav_dashboard": "Dashboard",
        "nav_impact": "Impact Calculator",
        "nav_forecast": "Rate Forecast",
        "nav_events": "Historical Events",
        "change_language": "ZMIEŃ JĘZYK",
        "current_rate": "Current Exchange Rate",
        "refresh": "Refresh Data",
        "last_updated": "Last updated",
        "quick_conversion": "Quick Conversion",
        "historical_trend": "Historical Trend Analysis",
        "select_period": "Select time period",
        "period_7d": "7 days",
        "period_30d": "30 days",
        "period_90d": "90 days",
        "period_1y": "1 year",
        "period_5y": "5 years",
        "period_max": "Max available",
        "exchange_rate": "EUR/PLN Exchange Rate",
        "date": "Date",
        "key_metrics": "Key Metrics",
        "7d_change": "7-Day Change",
        "period_low": "Period Low",
        "period_high": "Period High",
        "from_low": "from low",
        "from_high": "from high",
        "insufficient_data": "Insufficient data for quantitative analysis",
        "impact_title": "💰 Exchange Rate Impact Calculator",
        "impact_description": "Understand how exchange rate fluctuations affect different scenarios",
        "polish_scenario": "Polish Scenario (PLN → EUR)",
        "polish_example": "Typical situation: Student receiving 3000 PLN salary",
        "italian_scenario": "Italian Scenario (EUR → PLN)",
        "italian_example": "Typical situation: Tourist with 1000 EUR budget",
        "monthly_income": "Monthly income (PLN)",
        "available_amount": "Available amount (EUR)",
        "current_conversion": "Current conversion:",
        "if_increases": "If rate increases 10% (weaker PLN):",
        "if_decreases": "If rate decreases 10% (stronger PLN):",
        "difference": "Difference:",
        "key_takeaways": "Key Takeaways:",
        "takeaway1": "- When PLN weakens (rate increases), Polish people get fewer EUR for their PLN",
        "takeaway2": "- When PLN strengthens (rate decreases), Italian tourists get fewer PLN for their EUR",
        "takeaway3": "- The opposite effect benefits each group respectively",
        "forecast_title": "📈 Rate Forecast",
        "forecast_instructions": "How to Use This Forecast",
        "forecast_description": "This tool projects future EUR/PLN exchange rates based on historical trends using linear regression:",
        "forecast_note": "Note: This is a mathematical projection, not financial advice. Past performance doesn't guarantee future results.",
        "forecast_period": "Forecast period (days):",
        "forecast_help": "Select how many days into the future to project",
        "rate_forecast": "EUR/PLN Rate Forecast",
        "next": "Next",
        "days": "days",
        "type": "Type",
        "current_trend": "Current Daily Trend",
        "increasing": "Increasing",
        "decreasing": "Decreasing",
        "per_day": "per day",
        "events_title": "📅 Historical Events Impact",
        "events_description": "Explore how major economic and political events affected the EUR/PLN exchange rate.",
        "select_event": "Select an event:",
        "exchange_rate_during": "EUR/PLN during",
        "starting_rate": "Starting Rate",
        "ending_rate": "Ending Rate",
        "change": "change",
        "eu_accession": "Poland EU Accession (2004)",
        "financial_crisis": "2008 Financial Crisis",
        "debt_crisis": "EU Debt Crisis",
        "elections_2015": "Polish Elections 2015",
        "elections_2019": "Polish Elections 2019",
        "covid_pandemic": "COVID-19 Pandemic",
        "russia_war": "Russia-Ukraine War",
        "about_app": "About This App:",
        "feature1": "- Real-time EUR/PLN exchange rate monitoring",
        "feature2": "- Historical trend analysis",
        "feature3": "- Rate forecasting tools",
        "feature4": "- Event impact studies",
        "created_by": "Created by",
        "data_source": "Data source: Yahoo Finance",
        "toggle_language_help": "Click to switch between English and Polish",
        "go_to": "Go to:"
    },
    "pl": {
        "title": "💹 Monitor EUR/PLN Pro",
        "navigation": "Nawigacja",
        "nav_dashboard": "Panel główny",
        "nav_impact": "Kalkulator wpływu",
        "nav_forecast": "Prognoza kursu",
        "nav_events": "Wydarzenia historyczne",
        "change_language": "CHANGE LANGUAGE",
        "current_rate": "Aktualny kurs wymiany",
        "refresh": "Odśwież dane",
        "last_updated": "Ostatnia aktualizacja",
        "quick_conversion": "Szybka konwersja",
        "historical_trend": "Analiza trendu historycznego",
        "select_period": "Wybierz okres",
        "period_7d": "7 dni",
        "period_30d": "30 dni",
        "period_90d": "90 dni",
        "period_1y": "1 rok",
        "period_5y": "5 lat",
        "period_max": "Maksymalny dostępny",
        "exchange_rate": "Kurs wymiany EUR/PLN",
        "date": "Data",
        "key_metrics": "Kluczowe wskaźniki",
        "7d_change": "Zmiana 7-dniowa",
        "period_low": "Minimum w okresie",
        "period_high": "Maksimum w okresie",
        "from_low": "od minimum",
        "from_high": "od maksimum",
        "insufficient_data": "Niewystarczające dane do analizy ilościowej",
        "impact_title": "💰 Kalkulator wpływu kursu wymiany",
        "impact_description": "Zrozumienie wpływu wahań kursu wymiany na różne scenariusze",
        "polish_scenario": "Scenariusz polski (PLN → EUR)",
        "polish_example": "Typowa sytuacja: Student otrzymujący 3000 PLN wynagrodzenia",
        "italian_scenario": "Scenariusz włoski (EUR → PLN)",
        "italian_example": "Typowa sytuacja: Turysta z budżetem 1000 EUR",
        "monthly_income": "Miesięczne wynagrodzenie (PLN)",
        "available_amount": "Dostępna kwota (EUR)",
        "current_conversion": "Aktualna konwersja:",
        "if_increases": "Jeśli kurs wzrośnie o 10% (słabszy PLN):",
        "if_decreases": "Jeśli kurs spadnie o 10% (silniejszy PLN):",
        "difference": "Różnica:",
        "key_takeaways": "Kluczowe wnioski:",
        "takeaway1": "- Gdy PLN słabnie (kurs rośnie), Polacy otrzymują mniej EUR za swoje PLN",
        "takeaway2": "- Gdy PLN wzmacnia się (kurs spada), włoscy turyści otrzymują mniej PLN za swoje EUR",
        "takeaway3": "- Odwrotny efekt przynosi korzyści każdej z grup odpowiednio",
        "forecast_title": "📈 Prognoza kursu",
        "forecast_instructions": "Instrukcja korzystania z prognozy",
        "forecast_description": "To narzędzie prognozuje przyszłe kursy wymiany EUR/PLN na podstawie trendów historycznych przy użyciu regresji liniowej:",
        "forecast_note": "Uwaga: To jest projekcja matematyczna, a nie porada finansowa. Wyniki historyczne nie gwarantują przyszłych rezultatów.",
        "forecast_period": "Okres prognozy (dni):",
        "forecast_help": "Wybierz liczbę dni do prognozy",
        "rate_forecast": "Prognoza kursu EUR/PLN",
        "next": "Następne",
        "days": "dni",
        "type": "Typ",
        "current_trend": "Aktualny trend dzienny",
        "increasing": "Wzrostowy",
        "decreasing": "Spadkowy",
        "per_day": "dziennie",
        "events_title": "📅 Wpływ wydarzeń historycznych",
        "events_description": "Zbadaj, jak ważne wydarzenia ekonomiczne i polityczne wpłynęły na kurs EUR/PLN.",
        "select_event": "Wybierz wydarzenie:",
        "exchange_rate_during": "Kurs EUR/PLN podczas",
        "starting_rate": "Kurs początkowy",
        "ending_rate": "Kurs końcowy",
        "change": "zmiana",
        "eu_accession": "Akcesja Polski do UE (2004)",
        "financial_crisis": "Kryzys finansowy 2008",
        "debt_crisis": "Kryzys zadłużenia w UE",
        "elections_2015": "Wybory w Polsce 2015",
        "elections_2019": "Wybory w Polsce 2019",
        "covid_pandemic": "Pandemia COVID-19",
        "russia_war": "Wojna Rosja-Ukraina",
        "about_app": "O aplikacji:",
        "feature1": "- Monitorowanie kursu EUR/PLN w czasie rzeczywistym",
        "feature2": "- Analiza trendów historycznych",
        "feature3": "- Narzędzia prognozowania kursu",
        "feature4": "- Badania wpływu wydarzeń",
        "created_by": "Autor",
        "data_source": "Źródło danych: Yahoo Finance",
        "toggle_language_help": "Kliknij, aby przełączyć między językiem angielskim a polskim",
        "go_to": "Idź do:"
    }
}

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

def toggle_language():
    if st.session_state.language == 'en':
        st.session_state.language = 'pl'
    else:
        st.session_state.language = 'en'

def t(key):
    return translations[st.session_state.language].get(key, f"[{key}]")

# Page configuration
st.set_page_config(
    page_title=t("title"),
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <p style="font-size: 12px; text-align: center;">
        Created by: <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a><br>
        <span style="color: red;">
            Please use the light theme, otherwise with the dark theme some parts might not be displayed correctly<br>
            Proszę używać jasnego motywu, ponieważ w przypadku ciemnego motywu niektóre elementy mogą nie być wyświetlane poprawnie
        </span>
    </p>
""", unsafe_allow_html=True)

# Custom CSS for professional styling
st.markdown("""
<style>
/* ===== CORE VARIABLES ===== */
:root {
    /* Light Theme (originale) */
    --light-primary: #1abc9c;
    --light-secondary: #3498db;
    --light-background: #FFFFFF;
    --light-text: #111111;
    --light-card: #FFFFFF;
    --light-border: #E1E3EB;
    --light-sidebar: #2c3e50;
    
    /* Dark Theme (modificato) */
    --dark-primary: #4BFFFC;
    --dark-background: #000000;
    --dark-text: #FFFFFF;
    --dark-card: #1A2639;
    --dark-border: #2A3A4D;
    --dark-sidebar: #1A2639;
    
    /* Default Light Theme */
    --primary: var(--light-primary);
    --secondary: var(--light-secondary);
    --background: var(--light-background);
    --text: var(--light-text);
    --card: var(--light-card);
    --border: var(--light-border);
    --sidebar: var(--light-sidebar);
}

/* ===== DARK THEME OVERRIDE ===== */
@media (prefers-color-scheme: dark) {
    :root {
        --primary: var(--dark-primary);
        --secondary: var(--dark-secondary);
        --background: var(--dark-background);
        --text: var(--dark-text);
        --card: var(--dark-card);
        --border: var(--dark-border);
        --sidebar: var(--dark-sidebar);
    }
}

/* ===== BASE STYLES ===== */
* {
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.6;
}

body {
    background-color: var(--background);
    color: var(--text);
}

/* ===== TYPOGRAPHY ===== */
h1 {
    font-size: 2.2em;
    font-weight: 700;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5em;
}

h2, h3, h4 {
    color: var(--text);
}

/* ===== SIDEBAR ===== */
.stSidebar {
    background: var(--sidebar) !important;
}

.stSidebar .sidebar-content {
    color: white !important;
}

.stSidebar label {
    color: white !important;
    font-weight: 600;
}

/* ===== CARDS & CONTAINERS ===== */
.metric-container {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    color: var(--text);
}

.plot-container, 
div[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1em;
}

/* ===== METRICS ===== */
.metric-value {
    font-size: 1.8em;
    font-weight: bold;
    font-family: monospace;
    color: var(--text);
}

.metric-label {
    font-size: 0.95em;
    color: var(--text);
    opacity: 0.8;
}

/* ===== HEATMAP INTERPRETATION BOX ===== */
.interpretation-box {
    background: var(--card) !important;
    border-left: 4px solid var(--primary) !important;
    padding: 1.25rem;
    margin: 1.5rem 0;
    border-radius: 0 8px 8px 0;
    color: white !important;
}

.interpretation-box,
.interpretation-box p,
.interpretation-box li,
.interpretation-box ul {
    color: white !important;
}

/* ===== TABLES ===== */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ===== DARK THEME ENHANCEMENTS ===== */
@media (prefers-color-scheme: dark) {
    /* Miglioramenti aggiuntivi per dark theme */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select {
        background-color: #121826 !important;
        color: white !important;
        border-color: var(--border) !important;
    }
    
    .stSlider .st-c7 {
        background-color: var(--primary) !important;
    }
    
    /* Heatmap text */
    .heatmap-annotation {
        fill: white !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Function to get current rate
def get_current_rate():
    try:
        eur_pln = yf.Ticker("EURPLN=X")
        data = eur_pln.history(period='1d')
        return data['Close'].iloc[-1]
    except Exception as e:
        st.error(f"{t('data_error')}: {e}")
        return 4.25  # Fallback value

# Function to get historical data
def get_historical_data(start_date, end_date=None):
    if end_date is None:
        end_date = datetime.now()
    
    try:
        eur_pln = yf.Ticker("EURPLN=X")
        df = eur_pln.history(start=start_date, end=end_date)
        df = df.reset_index()
        df = df[['Date', 'Close']].rename(columns={'Close': 'EUR/PLN'})
        return df
    except Exception as e:
        st.error(f"{t('historical_error')}: {e}")
        days = (end_date - start_date).days
        date_range = pd.date_range(start=start_date, periods=days)
        mock_rates = [4.2 + 0.1 * (i/10 + 0.5 * (i % 3)) for i in range(days)]
        return pd.DataFrame({'Date': date_range, 'EUR/PLN': mock_rates})

def forecast_exchange_rate(df, days_to_forecast=30):
    try:
        # Prepare data for modeling
        df['Days'] = (df['Date'] - df['Date'].min()).dt.days
        X = df['Days'].values.reshape(-1, 1)
        y = df['EUR/PLN'].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Create future dates
        last_date = df['Date'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, days_to_forecast+1)]
        future_days = [(date - df['Date'].min()).days for date in future_dates]
        
        # Predict future rates
        future_rates = model.predict(np.array(future_days).reshape(-1, 1))
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'EUR/PLN': future_rates,
            'Type': 'Forecast' if st.session_state.language == 'en' else 'Prognoza'
        })
        
        # Prepare historical data for plotting
        history_df = df.copy()
        history_df['Type'] = 'Historical' if st.session_state.language == 'en' else 'Historyczne'
        
        return pd.concat([history_df, forecast_df]), model.coef_[0]
    except Exception as e:
        st.error(f"{t('forecast_error')}: {e}")
        return None, 0

# Impact Calculator Page
def impact_page():
    st.title(t("impact_title"))
    
    current_rate = get_current_rate()
    
    st.markdown(f"### {t('impact_description')}")
    
    st.markdown(f"**{t('current_rate')}:** {current_rate:.4f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {t('polish_scenario')}")
        st.markdown(f"**{t('polish_example')}**")
        
        pln_amount = st.number_input(t("monthly_income"), 
                                   min_value=0, value=3000, step=100,
                                   key="pln_income")
        
        st.markdown("<div class='impact-box'>", unsafe_allow_html=True)
        st.markdown(f"**{t('current_conversion')}**")
        st.write(f"{pln_amount} PLN → {pln_amount / current_rate:.2f} EUR")
        
        st.markdown(f"**{t('if_increases')}**")
        st.write(f"{pln_amount} PLN → {pln_amount / (current_rate * 1.1):.2f} EUR")
        st.write(f"{t('difference')}: {(pln_amount / (current_rate * 1.1)) - (pln_amount / current_rate):.2f} EUR")
        
        st.markdown(f"**{t('if_decreases')}**")
        st.write(f"{pln_amount} PLN → {pln_amount / (current_rate * 0.9):.2f} EUR")
        st.write(f"{t('difference')}: {(pln_amount / (current_rate * 0.9)) - (pln_amount / current_rate):.2f} EUR")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {t('italian_scenario')}")
        st.markdown(f"**{t('italian_example')}**")
        
        eur_amount = st.number_input(t("available_amount"), 
                                   min_value=0, value=1000, step=100,
                                   key="eur_amount")
        
        st.markdown("<div class='impact-box'>", unsafe_allow_html=True)
        st.markdown(f"**{t('current_conversion')}**")
        st.write(f"{eur_amount} EUR → {eur_amount * current_rate:.2f} PLN")
        
        st.markdown(f"**{t('if_increases')}**")
        st.write(f"{eur_amount} EUR → {eur_amount * (current_rate * 1.1):.2f} PLN")
        st.write(f"{t('difference')}: {eur_amount * (current_rate * 1.1) - (eur_amount * current_rate):.2f} PLN")
        
        st.markdown(f"**{t('if_decreases')}**")
        st.write(f"{eur_amount} EUR → {eur_amount * (current_rate * 0.9):.2f} PLN")
        st.write(f"{t('difference')}: {eur_amount * (current_rate * 0.9) - (eur_amount * current_rate):.2f} PLN")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(f"**{t('key_takeaways')}**")
    st.markdown(t("takeaway1"))
    st.markdown(t("takeaway2"))
    st.markdown(t("takeaway3"))

# Main Dashboard Page
def dashboard_page():
    st.title(t("title"))
    
    # Current rate section
    current_rate = get_current_rate()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label=t("current_rate"), value=f"{current_rate:.4f}", 
                delta="0.00% " + ("from yesterday" if st.session_state.language == 'en' else "od wczoraj"))
        st.caption(f"{t('last_updated')}: {datetime.now().strftime('%H:%M:%S')}")

    with col2:
        st.markdown(f"### {t('quick_conversion')}")
        mini_col1, mini_col2 = st.columns(2)
        with mini_col1:
            pln = st.number_input("PLN → EUR", min_value=0.0, value=100.0, step=10.0)
            st.write(f"→ {pln / current_rate:.2f} €")
        with mini_col2:
            eur = st.number_input("EUR → PLN", min_value=0.0, value=100.0, step=10.0)
            st.write(f"→ {eur * current_rate:.2f} zł")
    
    st.markdown("---")
    
    # Historical chart section
    st.header(t("historical_trend"))
    
    period = st.radio(
        t("select_period"),
        [t("period_7d"), t("period_30d"), t("period_90d"), t("period_1y"), t("period_5y"), t("period_max")],
        horizontal=True,
        key="period_selector"
    )

    # Create mapping for actual days based on current language
    period_map = {
        t("period_7d"): 7,
        t("period_30d"): 30,
        t("period_90d"): 90,
        t("period_1y"): 365,
        t("period_5y"): 365*5,
        t("period_max"): 365*20
    }

    start_date = datetime.now() - timedelta(days=period_map[period])
    df = get_historical_data(start_date)

    if len(df) > 7:
        df['MA_7'] = df['EUR/PLN'].rolling(window=7).mean()

    fig = px.line(
        df, 
        x='Date', 
        y='EUR/PLN',
        title=f"{t('exchange_rate')} - {t('last')} {period}",
        labels={'EUR/PLN': t('exchange_rate'), 'Date': t('date')},
        template='plotly_white'
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title=t('date'),
        yaxis_title=t('exchange_rate'),
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.5)',
        font=dict(family="Helvetica Neue, Arial, sans-serif")
    )

    fig.update_traces(
        line=dict(width=2.5, color='#3498db'),
        hovertemplate="%{y:.4f} PLN<extra></extra>"
    )

    if 'MA_7' in df:
        fig.add_scatter(
            x=df['Date'], 
            y=df['MA_7'], 
            name='7-Day Moving Avg' if st.session_state.language == 'en' else 'Średnia 7-dniowa',
            line=dict(color='#e74c3c', width=2, dash='dot')
        )

    st.plotly_chart(fig, use_container_width=True)
    
    # Key metrics
    st.subheader(t("key_metrics"))
    
    if len(df) > 1:
        col1, col2, col3 = st.columns(3)
        with col1:
            period_days = min(7, len(df)-1)
            delta = (df['EUR/PLN'].iloc[-1] - df['EUR/PLN'].iloc[-period_days]) / df['EUR/PLN'].iloc[-period_days] * 100
            st.metric(t("7d_change"), f"{df['EUR/PLN'].iloc[-1]:.4f}", 
                     f"{delta:.2f}%", delta_color="inverse")

        with col2:
            min_rate = df['EUR/PLN'].min()
            st.metric(t("period_low"), f"{min_rate:.4f}", 
                     f"{(df['EUR/PLN'].iloc[-1] - min_rate):.4f} {t('from_low')}")

        with col3:
            max_rate = df['EUR/PLN'].max()
            st.metric(t("period_high"), f"{max_rate:.4f}", 
                     f"{(max_rate - df['EUR/PLN'].iloc[-1]):.4f} {t('from_high')}")
    else:
        st.warning(t("insufficient_data"))

# Forecast Page
def forecast_page():
    st.title(t("forecast_title"))
    
    st.markdown(f"### {t('forecast_instructions')}")
    st.markdown(t("forecast_description"))
    st.markdown(f"*{t('forecast_note')}*")
    
    # Get data for the forecast
    df = get_historical_data(datetime.now() - timedelta(days=90))
    
    forecast_days = st.slider(t("forecast_period"), 7, 90, 30, 
                             help=t("forecast_help"))
    
    forecast_df, trend_coef = forecast_exchange_rate(df, forecast_days)

    if forecast_df is not None:
        fig_forecast = px.line(
            forecast_df,
            x='Date',
            y='EUR/PLN',
            color='Type',
            title=f"{t('rate_forecast')} - {t('next')} {forecast_days} {t('days')}",
            height=500,
            color_discrete_map={
                "Historical": "#3498db",
                "Forecast": "#e74c3c"
            },
            labels={'EUR/PLN': t('exchange_rate'), 'Date': t('date'), 'Type': t('type')}
        )
        fig_forecast.update_layout(
            hovermode="x unified",
            margin=dict(l=20, r=20, t=60, b=20),
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Helvetica Neue, Arial, sans-serif")
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        trend_direction = t('increasing') if trend_coef > 0 else t('decreasing')
        st.metric(t("current_trend"), 
                 trend_direction, 
                 f"{abs(trend_coef):.6f} PLN {t('per_day')}")

# Historical Events Page
def events_page():
    st.title(t("events_title"))
    
    st.markdown(t("events_description"))
    
    major_events = {
        t("eu_accession"): (datetime(2003, 1, 1), datetime(2005, 12, 31)),
        t("financial_crisis"): (datetime(2007, 6, 1), datetime(2009, 12, 31)),
        t("debt_crisis"): (datetime(2010, 1, 1), datetime(2012, 12, 31)),
        t("elections_2015"): (datetime(2015, 1, 1), datetime(2016, 6, 30)),
        t("elections_2019"): (datetime(2019, 1, 1), datetime(2020, 6, 30)),
        t("covid_pandemic"): (datetime(2020, 1, 1), datetime(2021, 12, 31)),
        t("russia_war"): (datetime(2022, 2, 1), datetime(2022, 12, 31))
    }
    
    selected_event = st.selectbox(t("select_event"), list(major_events.keys()))
    
    start_date, end_date = major_events[selected_event]
    event_df = get_historical_data(start_date, end_date)
    
    if not event_df.empty:
        fig_event = px.line(
            event_df,
            x='Date',
            y='EUR/PLN',
            title=f"{t('exchange_rate_during')} {selected_event}",
            height=500
        )
        fig_event.update_layout(
            hovermode="x unified",
            margin=dict(l=20, r=20, t=60, b=20),
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Helvetica Neue, Arial, sans-serif")
        )
        fig_event.update_traces(line=dict(width=2.5, color='#3498db'))
        st.plotly_chart(fig_event, use_container_width=True)
        
        # Calculate event impact
        start_rate = event_df.iloc[0]['EUR/PLN']
        end_rate = event_df.iloc[-1]['EUR/PLN']
        change = ((end_rate - start_rate) / start_rate) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(t("starting_rate"), f"{start_rate:.4f}")
        with col2:
            st.metric(t("ending_rate"), f"{end_rate:.4f}", 
                     f"{change:.1f}% {t('change')}", delta_color="inverse")

# Sidebar navigation
st.sidebar.title(t("navigation"))
st.sidebar.button(t("change_language"), on_click=toggle_language, 
                  key="language_button", help=t("toggle_language_help"),
                  type="primary")

page = st.sidebar.radio(t("go_to"), 
                        [t("nav_dashboard"), t("nav_impact"), t("nav_forecast"), t("nav_events")],
                        index=0)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{t('about_app')}**")
st.sidebar.markdown(t("feature1"))
st.sidebar.markdown(t("feature2"))
st.sidebar.markdown(t("feature3"))
st.sidebar.markdown(t("feature4"))

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='text-align: center; font-size:14px;'>
    {t('created_by')} <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank" style='color: red;'>Luca Girlando</a><br>
</div>
""", unsafe_allow_html=True)

# Add missing error translations
translations["en"].update({
    "data_error": "Data retrieval error",
    "historical_error": "Historical data error"
})
translations["pl"].update({
    "data_error": "Błąd pobierania danych",
    "historical_error": "Błąd danych historycznych"
})

translations["en"]["forecast_error"] = "Forecast error"
translations["pl"]["forecast_error"] = "Błąd prognozy"

# Page routing
if page == t("nav_dashboard"):
    dashboard_page()
elif page == t("nav_impact"):
    impact_page()
elif page == t("nav_forecast"):
    forecast_page()
elif page == t("nav_events"):
    events_page()
