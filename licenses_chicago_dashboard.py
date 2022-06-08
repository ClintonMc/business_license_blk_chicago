import streamlit as st
import pandas as pd

st.title('Business Licenses in Black Chicago')

@st.cache
def load_data(url):
    df = pd.read_csv(url)
    return df

URL = st.secrets["public_gsheets_url"]
chi_license_df = load_data(URL)

blk_comms = ['AUSTIN','WEST GARFIELD','EAST GARFIELD','NORTH LAWNDALE','DOUGLAS','OAKLAND','FULLER PARK','GRAND BOULEVARD',\
             'KENWOOD','WASHINGTON HEIGHTS','WOODLAWN','SOUTH SHORE','CHATHAM','AVALON PARK','SOUTH CHICAGO','BURNSIDE','CALUMET HEIGHTS',\
             'ROSELAND','PULLMAN','SOUTH DEERING','WEST PULLMAN','RIVERDALE','WEST ENGLEWOOD','ENGLEWOOD','GREATER GRAND CROSSING',\
             'AUBURN GRESHAM','WASHINGTON PARK','MORGAN PARK']

black_license_df = chi_license_df[chi_license_df['community'].isin(blk_comms)]
non_black_license_df = chi_license_df[~chi_license_df['community'].isin(blk_comms)]

if non_black_license_df.shape[0] <= black_license_df.shape[0]:
    ratio = round(black_license_df.shape[0] / non_black_license_df.shape[0],2)
    st.subheader(f'Since 2002, majority-Black communities in Chicago have received {ratio} times more business\
            licenses than non-Black communities.')
else:
    ratio = round(non_black_license_df.shape[0] / black_license_df.shape[0],0).astype(int)
    st.subheader(f'Since 2002, majority-Black communities in Chicago have received {ratio} times fewer business\
            licenses than non-Black communities. If you have any thoughts or feelings about this, consider\
            sharing them with the City by following this [link](https://webapps1.chicago.gov/eforms/contactUsForm).')

community = st.selectbox(
    'Please select a neighborhood',
    black_license_df.community.unique()
)
activity_df = black_license_df[black_license_df['community']==community].business_activity.value_counts().head()
activity = activity_df.rename("Number of Licenses")
st.subheader(f'Top 5 Business Activities in {community}')
st.table(activity)

owners_df = black_license_df[black_license_df['community']==community].owner_name.value_counts().head()
owners = owners_df.rename("Number of Licenses")
st.subheader(f'Top 5 Business Owners in {community}')
st.table(owners)

community_df = pd.DataFrame(black_license_df[black_license_df['community']==community])
community_df['date_issued'] = pd.to_datetime(community_df['date_issued'])
community_df = community_df.set_index('date_issued').resample('MS').count()
st.subheader(f'Licenses Issued to {community} between {pd.Timestamp(community_df.index.min()).strftime("%d-%m-%Y")}\
     and {pd.Timestamp(community_df.index.max()).strftime("%d-%m-%Y")}')
st.line_chart(data=community_df['id'])
