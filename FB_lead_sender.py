
from facebookads.adobjects.leadgenform import LeadgenForm
import datetime
import pandas as pd
import time
import numpy as np
global yday, today, filename_daily, credentials_path

form_ids = {'123456789' : 'my_lead_form'}

recipients = ['user@user.com']
credentials_path = "/home/user..."

yday = str(datetime.date.today() - datetime.timedelta(1))
today = str(datetime.date.today())

filename_daily = "/home/user..."

def initialize_facebook_api(credentials_path):
    cred = json.load(open(credentials_path))
    facebookads.FacebookAdsApi.init(cred['facebook']['app_id'], cred['facebook']['app_secret'],
                                    cred['facebook']['access_token'])

def get_leads_from_forms(form_ids):
    leads = []
    # This often fails for unknown reasons on FB side

    for i in (list(range(0, 5))):
        print("iteration number {} started".format(str(i)))
        try:
            for form_id in list(form_ids.keys()):
                form = LeadgenForm(form_id)
                for lead in form.get_leads():
                    data = lead.export_all_data()
                    data.update({'form_name' : form_ids[form_id]})
                    leads.append(data)
            return leads
        except:
            time.sleep(10)
            print("{} iteration failed \n".format(str(i)))
            pass

def parse_data(leads):
    big_df = pd.DataFrame()
    
    for l in leads:
        df = pd.DataFrame(l['field_data']).T.reset_index()
        df.columns = df.iloc[0]
        df.drop(0, inplace=True)
        df['FB_id'] = l['id']
        df['form_name'] = l['form_name']
        df['created'] = l['created_time'][:10]
        big_df = big_df.append(df)
        
    for col in big_df.columns:
        big_df[col] = big_df[col].apply(lambda x: x[0] if type(x) is list else x)
    big_df.reset_index(inplace=True, drop=True)
    big_df['email'] = big_df['email'].str.strip().str.lower()
    big_df.drop("name", axis=1, inplace=True)
    big_df.sort("created", ascending=False, inplace=True)

    return big_df


def save_yesterdays_leads(df, files, brand):
    yesterday_leads = df[df['created'] == yday]
    if yesterday_leads.empty is True:
        print("No yesterday leads found for {}".format(brand))
        return False
    else:
        yesterday_leads.to_excel(files[0], index=False)
        return True

def send_leads(recipients, files, brand):
    for recipient in recipients:
            send_email(toaddr=recipient, subject='{} FB leads for {}'.format(brand, yday),
               body="Hi, these are the leads from yesterday.".format(brand),
               attachment=True, file_paths=files)

def main(form_ids, recipients, files, fb_credentials, db_credentials, brand):
    try:
        initialize_facebook_api(fb_credentials)
        leads_raw = get_leads_from_forms(form_ids)
        if len(leads_raw) == 0:
            print("no all time leads found for {}, exiting".format(brand))
            return
        leads_clean = parse_data(leads_raw)
        if leads_clean.empty is True:
            print("lead parser returned an empty object, possible bug, exiting")
            return

        content = save_yesterdays_leads(leads_clean, files, brand)
        # only if there were leads yesterday
        if content:
            send_leads(recipients, files, brand)
    except Exception as e:
        print(e)
        send_email(toaddr='me@me.com', subject='FB lead sender FAILED for {}'.format(brand),
                   body="Debug the script")

if __name__ == '__main__':
    main(form_ids, recipients, [filename_daily], fb_credentials_path, "Brand Inc")
