import pandas as pd
import os
import requests
from io import StringIO
import csv

# base_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(base_dir, '../DE Dataset/lead_log.csv')
# lead_log = pd.read_csv(file_path)
# # print(lead_log)
lead_log        = 'https://drive.usercontent.google.com/u/0/uc?id=1YoLPpXwe9P7m3nCV3Qv6Q5RQXxkyYcaJ&export=download'
paid_trx        = 'https://drive.usercontent.google.com/u/0/uc?id=15MKY5_QAWUzvh2hFcOly-lc7rorwC9Qj&export=download'
ref_reward      = 'https://drive.usercontent.google.com/u/0/uc?id=1c8SU_jDovGv9qTdMSMKlw3dBiZ2iv0UQ&export=download'
user_logs       = 'https://drive.usercontent.google.com/u/0/uc?id=1iDqk1XqGLC25LbG87SJVeBvtyFwFn9Pg&export=download'
user_ref_logs   = 'https://drive.usercontent.google.com/u/0/uc?id=1x8c1Vho7VvAxYNaihuuxc29qDEuH9tIX&export=download'
user_ref_stat   = 'https://drive.usercontent.google.com/u/0/uc?id=1fpiUzC62RBS4IKlGUj6dEpVPEqzbHYhW&export=download'
user_ref        = 'https://drive.usercontent.google.com/u/0/uc?id=1KNCa0HSetAmDxulbtZkifMSdYbm7mhZi&export=download'

# Get current datetime
now = pd.Timestamp.now().strftime('%Y-%m-%d')


class Models :

    def __init__(self) :
        pass

    def extract_data(self, url) :
        
        data_url = requests.get(url)
        data_csv = StringIO(data_url.text)
        df = pd.read_csv(data_csv)
        
        return df
    
    def read_all_file(self) :
        pass
    

    def join_table(self) :

        valid_user_ref = self.extract_data(user_ref)
        valid_user_ref_logs = self.extract_data(user_ref_logs).drop_duplicates(subset='user_referral_id')

        valid_user_logs = self.extract_data(user_logs).loc[self.extract_data(user_logs)['is_deleted'] == False]
        valid_user_logs = valid_user_logs.drop_duplicates(subset='user_id')

        valid_paid_trx = self.extract_data(paid_trx)

        valid_ref_reward = self.extract_data(ref_reward)

        valid_user_ref_stat = self.extract_data(user_ref_stat)

        valid_lead_log = self.extract_data(lead_log)
        valid_lead_log = valid_lead_log.drop_duplicates(subset='lead_id')

        table_1 = pd.merge(valid_user_ref, valid_user_ref_logs, left_on=['referral_id'], right_on=['user_referral_id'], how='left')
        table_1 = table_1.rename(columns={'created_at': 'reward_granted_at'})

        table_2 = pd.merge(table_1, valid_user_logs, left_on=['referrer_id'], right_on=['user_id'], how='left')
        table_2 = table_2.drop(columns=['id_x', 'id_y', 'is_deleted'])
        table_2 = table_2.rename(columns={
            'name': 'referrer_name',
            'phone_number': 'referrer_phone_number',
            'homeclub': 'referrer_homeclub',
            'timezone_homeclub': 'referrertimezone_homeclub',
            'membership_expired_date': 'referrer_membership_expired_date'
            })
        
        table_3 = pd.merge(table_2, valid_paid_trx, on=['transaction_id'], how='left')

        table_4 = pd.merge(table_3, valid_ref_reward, left_on=['referral_reward_id'], right_on=['id'], how='left')
        table_4 = table_4.rename(columns={'created_at':'ref_rewards_created_at'})

        table_5 = pd.merge(table_4, valid_user_ref_stat, left_on=['user_referral_status_id'], right_on=['id'], how='left')
        table_5 = table_5.rename(columns={'created_at':'user_referral__statuses_created_at'})
        
        table_6_lead = table_5.loc[table_5['referral_source'] == 'Lead']
        table_6_lead = pd.merge(table_6_lead, valid_lead_log, left_on=['referee_id'], right_on=['lead_id'], how='left')
        table_6_lead = table_6_lead.drop(['current_status', 'timezone_location', 'preferred_location', 'created_at', 'lead_id', 'id'], axis=1)

        table_6_non_lead = table_5.loc[table_5['referral_source'] != 'Lead']
        table_6_non_lead.loc[table_6_non_lead .referral_source == 'Draft Transaction', 'source_category'] = 'Offline'
        table_6_non_lead.loc[table_6_non_lead .referral_source == 'User Sign Up', 'source_category'] = 'Online'

        table_7 = pd.concat([table_6_lead, table_6_non_lead], ignore_index=True)
        

        return table_7

    def get_final_table(self):

        final_table = self.join_table()

        final_table = final_table[[
                            'referral_id'
                            , 'referral_source'
                            , 'source_category'
                            , 'referral_at'
                            , 'referrer_id'
                            , 'referrer_name'
                            , 'referrer_phone_number'
                            , 'referrer_homeclub'
                            , 'referrer_membership_expired_date'
                            , 'referee_id'
                            , 'referee_name'
                            , 'referee_phone'
                            , 'description'
                            , 'reward_value'
                            , 'transaction_id'
                            , 'transaction_status'
                            , 'transaction_at'
                            , 'transaction_location'
                            , 'transaction_type'
                            , 'updated_at'
                            , 'reward_granted_at'
                            , 'is_reward_granted'
                            , 'ref_rewards_created_at'
                            , 'user_referral__statuses_created_at'
                            ]]

        final_table['referral_details_id'] = [f'{i:05}' for i in range(1, len(final_table) + 1)]
        final_table['is_business_logic_valid'] = ''
        final_table = final_table.rename(columns={
            'source_category' : 'referral_source_category'
            , 'description' : 'referral_status'
            , 'reward_value' : 'num_reward_days'
        })   

        final_table['num_reward_days'] = final_table['num_reward_days'].str.replace(' days', '', regex=False)
        final_table['num_reward_days'] = pd.to_numeric(final_table['num_reward_days'], errors='coerce')

        final_table['is_reward_granted'] = final_table['is_reward_granted'].fillna(False)
        final_table['is_reward_granted'] = final_table['is_reward_granted'].astype('bool')

        final_table['transaction_at'] = pd.to_datetime(final_table['transaction_at'])
        final_table['transaction_at'] = final_table['transaction_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        final_table['transaction_at'] = pd.to_datetime(final_table['transaction_at'], format='%Y-%m-%d %H:%M:%S')


        final_table['referral_at'] = pd.to_datetime(final_table['referral_at'])
        final_table['referral_at'] = final_table['referral_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        final_table['referral_at'] = pd.to_datetime(final_table['referral_at'], format='%Y-%m-%d %H:%M:%S')

        final_table['user_referral__statuses_created_at'] = pd.to_datetime(final_table['user_referral__statuses_created_at'])
        final_table['user_referral__statuses_created_at'] = final_table['user_referral__statuses_created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        final_table['user_referral__statuses_created_at'] = pd.to_datetime(final_table['user_referral__statuses_created_at'], format='%Y-%m-%d %H:%M:%S')

        final_table['ref_rewards_created_at'] = pd.to_datetime(final_table['ref_rewards_created_at'])
        final_table['ref_rewards_created_at'] = final_table['ref_rewards_created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        final_table['ref_rewards_created_at'] = pd.to_datetime(final_table['ref_rewards_created_at'], format='%Y-%m-%d %H:%M:%S')

        final_table['referrer_membership_expired_date'] = pd.to_datetime(final_table['referrer_membership_expired_date'])

        cols = ['referral_details_id'] + [col for col in final_table.columns if col != 'referral_details_id']
        final_table = final_table[cols]

        def fill_na_based_on_dtype(series):
            if series.dtype == 'float64' or series.dtype == 'int64':
                return series.fillna(0)
            elif series.dtype == 'object':
                return series.fillna('')
            elif series.dtype == 'string':
                return series.fillna('')
            elif pd.api.types.is_datetime64_any_dtype(series):
                return series.fillna(pd.NaT)
            else:
                return series

        final_table = final_table.apply(fill_na_based_on_dtype)

        return final_table
    
    def get_validation_referral(self) :

        final_table = self.get_final_table()
        final_table['is_business_logic_valid'] = False
        final_table['is_business_logic_valid'] = final_table['is_business_logic_valid'].astype(bool)
        final_table.loc[
                (final_table['num_reward_days'] > 0) 
                & (final_table['referral_status'] == 'Berhasil') 
                & (final_table['transaction_id'].notna().any()) 
                & (final_table['transaction_status'] == 'PAID') 
                & (final_table['transaction_type'] == 'NEW') 
                & (final_table['transaction_at'] >= final_table['referral_at']) 
                & (final_table['transaction_at'].dt.month == final_table['referral_at'].dt.month)
                & (final_table['referrer_membership_expired_date'] >= pd.Timestamp(now))
                & (final_table['is_reward_granted'] == True)
                , 'is_business_logic_valid'] = True


        final_table.loc[
                        (final_table['referral_status'].isin(['Menunggu', 'Tidak Berhasil']))
                        & (final_table['num_reward_days'] == 0) 
                        , 'is_business_logic_valid'] = True

        final_table.loc[
                        (final_table['num_reward_days'] > 0) 
                        & (final_table['referral_status'] != 'Berhasil')
                        , 'is_business_logic_valid'] = False

        final_table.loc[
                        (final_table['num_reward_days'] > 0) 
                        & (final_table['transaction_id'].isnull())
                        , 'is_business_logic_valid'] = False

        final_table.loc[
                        (final_table['num_reward_days'] == 0) 
                        & (final_table['transaction_id'].notna().any())
                        & (final_table['transaction_status'] == 'PAID')
                        & (final_table['transaction_at'] > final_table['referral_at']) 
                        , 'is_business_logic_valid'] = False


        final_table.loc[
                        (final_table['referral_status'] == 'Berhasil')
                        & (final_table['num_reward_days'] == 0)
                        , 'is_business_logic_valid'] = False

        final_table.loc[
                        (final_table['transaction_at'] < final_table['referral_at']) 
                        , 'is_business_logic_valid'] = False

        #adding logic
        final_table.loc[
                        (final_table['ref_rewards_created_at'] >= final_table['user_referral__statuses_created_at']) 
                        , 'is_business_logic_valid'] = False


        final_table.rename(columns={
            'source_category' : 'referral_source_category',
            'desctiption' : 'referral_status',
            'reward_value' : 'num_reward_days'
        })
        final_table[['referral_details_id'
                            , 'referral_id'
                            , 'referral_source'
                            , 'referral_source_category'
                            , 'referral_at'
                            , 'referrer_id'
                            , 'referrer_name'
                            , 'referrer_phone_number'
                            , 'referrer_homeclub'   
                            , 'referee_id'
                            , 'referee_name'
                            , 'referee_phone'
                            , 'referral_status'
                            , 'num_reward_days'
                            , 'transaction_id'
                            , 'transaction_status'
                            , 'transaction_at'
                            , 'transaction_location'
                            , 'transaction_type'
                            , 'updated_at'
                            , 'reward_granted_at'
                            ,'is_business_logic_valid']]
        # a = final_table.is_business_logic_valid.value_counts()
        # print(a)
        final_table

        return final_table




