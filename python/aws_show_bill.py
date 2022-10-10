#!/usr/bin/env python3

import datetime
import boto3


def get_monthly_service_cost(boto_cw_client, start_datetime, end_datetime, service=None):
    kwargs = {
        'TimePeriod': {'Start': start_datetime.strftime('%Y-%m-%d'), 'End': end_datetime.strftime('%Y-%m-%d')},
        'Granularity':'MONTHLY',
        'Metrics': ['UnblendedCost']
    }
    if service is not None:
        kwargs['Filter'] = {
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': [service]
            }
        }
    return boto_cw_client.get_cost_and_usage(**kwargs)


def time_cost_map(ce_cost_usage_resp):
    return {(period["TimePeriod"]["Start"], period["TimePeriod"]["End"]): float(period["Total"]["UnblendedCost"]["Amount"]) for period in ce_cost_usage_resp['ResultsByTime']}


if __name__ == '__main__':
    cost_ex = boto3.client('ce')
    now = datetime.datetime.now()
    six_months = datetime.timedelta(days=180)
    six_months_ago = now - six_months
    first_day_six_months_ago = six_months_ago - datetime.timedelta(days=(six_months_ago.day-1))
    total_cost_dict = time_cost_map(get_monthly_service_cost(cost_ex, first_day_six_months_ago, now))
    ec2_cost_dict = time_cost_map(get_monthly_service_cost(cost_ex, first_day_six_months_ago, now,
                                                           'Amazon Elastic Compute Cloud - Compute'))
    for start_date, end_date in sorted(total_cost_dict.keys(), key=lambda dates: dates[0]):
        if end_date == now.strftime('%Y-%m-%d'):
            duration = 'This month'
        else:
            duration = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%B')
        total_cost = total_cost_dict[(start_date, end_date)]
        ec2_cost = ec2_cost_dict[(start_date, end_date)]
        print(f'{duration:10}: ec2 - {ec2_cost:6.2f}, total - {total_cost:6.2f}')

