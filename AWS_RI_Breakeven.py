from datetime import datetime, timedelta

'''
The point at which a reserved instance (RI) purchase breaks even is the point at
which the remaining cost on the RI contract is less than or equal to the amount already
saved over on demand pricing. That is, when the customer has saved more than what is
left to pay.

The remaining cost on an RI contract is the remaining hourly commitment, plus the remaining
up-front commitment amortized at the hourly level. (Depending on the purchase option,
either of these may be zero.) AWS provides a combined "effective hourly" rate in their
pricing documentation which does this calculation for us.
'''

def breakeven(od_hourly, ri_hourly, ant_purch_date):
    ri_yearly = ri_hourly*8760 # AWS doesn't account for leap years

    ant_purch_datetime = datetime(int(ant_purch_date[:4]), int(ant_purch_date[5:7]), int(ant_purch_date[8:]))

    # Empty counter for hours since purchase
    hours = 0
    # Pre-loading "delta" - to be used as delta between "remaining cost" and "savings so far"
    delta = 1

    # When delta < 0, then "remaining cost" < "savings so far"
    while delta > 0:
        savings = (od_hourly*hours)-(ri_hourly*hours)
        remaining = ri_yearly-(ri_hourly*hours)
        delta = remaining-savings
        hours += 1

    # Add resulting hours to purchase date to find breakeven date
    breakeven_date = ant_purch_datetime + timedelta(hours=hours)

    return breakeven_date

if __name__ == '__main__':
    print('You will be asked to input some pricing information. For reference, see these links.')
    print('EC2: https://aws.amazon.com/ec2/pricing/reserved-instances/pricing/')
    print('RDS: https://aws.amazon.com/rds/pricing/')
    print('ElastiCache: https://aws.amazon.com/elasticache/pricing/')
    
    od_hourly = float(input('\nInput the ON DEMAND HOURLY rate as float: '))*0.9 # Reflects 10% EDP discount
    ri_hourly = float(input('Input the RESERVED EFFECTIVE HOURLY rate as float: '))
    ant_purch_date = input('Input the ANTICIPATED PURCHASE DATE in yyyy-mm-dd format: ')
    
    breakeven_date = breakeven(od_hourly, ri_hourly, ant_purch_date)
    
    print(f'\nYour purchase will breakeven on {breakeven_date.year}-{breakeven_date.month}-{breakeven_date.day}')
