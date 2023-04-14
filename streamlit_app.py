import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def create_fundraising_graphic(goal, raised):
    percent_raised = (raised / goal) * 100
    percent_remaining = 100 - percent_raised

    fig, ax = plt.subplots(figsize=(10, 2))
    ax.barh([0], [percent_raised], color='blue', label='Raised')
    ax.barh([0], [percent_remaining], left=[percent_raised], color='lightblue', label='Remaining')

    ax.set_xlim(0, 100)

    ax.set_title('Fundraising Progress', fontsize=16)
    plt.xlabel(f'Our Goal: ${goal}', fontsize=14)
    plt.ylabel('')

    ax.get_yaxis().set_visible(False)

    ax.text(percent_raised / 2, 0, f'${raised} Raised ({percent_raised:.0f}%)', ha='center', va='center', fontsize=12, color='white')
    ax.text(percent_raised + (percent_remaining / 2), 0, f'${goal-raised} Remaining ({percent_remaining:.0f}%)', ha='center', va='center', fontsize=12, color='black')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.legend()

    return fig

st.set_page_config(page_title='Fundraising Progress Graphic', layout='wide')

st.title('Fundraising Progress Graphic')

goal = st.number_input('Enter your fundraising goal:', value=10000, step=100)
raised = st.number_input('Enter the amount raised so far:', value=5000, step=100)

if st.button('Generate Graphic'):
    fig = create_fundraising_graphic(goal, raised)
    st.pyplot(fig)

    # Save the graphic as a PNG
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Convert the PNG to base64 and create a download link
    b64 = base64.b64encode(buf.getvalue()).decode()
    link = f'<a href="data:image/png;base64,{b64}" download="fundraising_progress.png">Download Graphic as PNG</a>'
    st.markdown(link, unsafe_allow_html=True)
