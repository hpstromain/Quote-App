import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 28

st.set_page_config(page_title="RCP Quote Assistant", layout="centered")

st.title("📋 RCP Quote Assistant")
st.caption("Full prototype • Mobile optimized")

# ==================== PRICING DATA ====================
PRICING = {
    315: {
        '18': {'CL3': Decimal('28.74'), 'CL4': Decimal('29.79'), 'CL5': Decimal('29.84')},
        '24': {'CL3': Decimal('44.89'), 'CL4': Decimal('47.13'), 'CL5': Decimal('49.38')},
        '30': {'CL3': Decimal('63.79'), 'CL4': Decimal('66.98'), 'CL5': Decimal('70.17')},
        '36': {'CL3': Decimal('90.56'), 'CL4': Decimal('95.09'), 'CL5': Decimal('99.62')},
        '42': {'CL3': Decimal('110.25'), 'CL4': Decimal('115.76'), 'CL5': Decimal('121.28')},
        '48': {'CL3': Decimal('137.81'), 'CL4': Decimal('144.70'), 'CL5': Decimal('151.59')},
        '54': {'CL3': Decimal('189.00'), 'CL4': Decimal('198.45'), 'CL5': Decimal('207.90')},
        '60': {'CL3': Decimal('228.38'), 'CL4': Decimal('239.79'), 'CL5': Decimal('251.30')},
        '66': {'CL3': Decimal('271.69'), 'CL4': Decimal('285.27'), 'CL5': Decimal('298.86')},
        '72': {'CL3': Decimal('318.94'), 'CL4': Decimal('334.88'), 'CL5': Decimal('350.83')},
    },
    320: {
        '18': {'CL3': Decimal('29.20'), 'CL4': Decimal('30.25'), 'CL5': Decimal('30.30')},
        '24': {'CL3': Decimal('45.60'), 'CL4': Decimal('47.88'), 'CL5': Decimal('50.16')},
        '30': {'CL3': Decimal('64.80'), 'CL4': Decimal('68.04'), 'CL5': Decimal('71.28')},
        '36': {'CL3': Decimal('92.00'), 'CL4': Decimal('96.60'), 'CL5': Decimal('101.20')},
        '42': {'CL3': Decimal('112.00'), 'CL4': Decimal('117.60'), 'CL5': Decimal('123.20')},
        '48': {'CL3': Decimal('140.00'), 'CL4': Decimal('147.00'), 'CL5': Decimal('154.00')},
        '54': {'CL3': Decimal('192.00'), 'CL4': Decimal('201.60'), 'CL5': Decimal('211.20')},
        '60': {'CL3': Decimal('232.00'), 'CL4': Decimal('243.60'), 'CL5': Decimal('255.20')},
        '66': {'CL3': Decimal('276.00'), 'CL4': Decimal('289.80'), 'CL5': Decimal('303.60')},
        '72': {'CL3': Decimal('324.00'), 'CL4': Decimal('340.20'), 'CL5': Decimal('356.40')},
    }
}

FLARED_PRICES = {
    '15': Decimal('875'), '18': Decimal('1030'), '24': Decimal('1725
